"""
Unit tests for quest system implementation
Uses pytest with hypothesis for edge and boundary testing
"""

import pytest
from hypothesis import given, strategies as st
from unittest.mock import MagicMock
from game.quest import Quest, QuestGiver, QuestManager
from tests.conftest import (
    create_test_player, mock_player, mock_quest, mock_npc,
    st_difficulty, st_item_quality
)


class TestQuest:
    """Test quest functionality"""
    
    @pytest.mark.unit
    def test_quest_creation_with_valid_data(self):
        """Test that quests are created correctly with valid data"""
        quest_data = {
            'id': 'quest_test',
            'name': 'Test Quest: The Missing Artifact',
            'type': 'fetch',
            'difficulty': 'medium',
            'description': 'Find the missing artifact and return it safely',
            'giver': 'npc_test',
            'rewards': {
                'experience': 500,
                'gold': 200,
                'items': ['item_test']
            },
            'objectives': [
                {'description': 'Find the artifact', 'completed': False},
                {'description': 'Return to quest giver', 'completed': False}
            ],
            'location': 'city_1'
        }
        
        quest = Quest(**quest_data)
        
        assert quest.id == 'quest_test'
        assert quest.name == 'Test Quest: The Missing Artifact'
        assert quest.type == 'fetch'
        assert quest.difficulty == 'medium'
        assert quest.giver == 'npc_test'
        assert quest.rewards == quest_data['rewards']
        assert len(quest.objectives) == 2
    
    @pytest.mark.unit
    def test_quest_objective_completion(self, mock_quest):
        """Test that quest objectives can be marked as completed"""
        # Initially no objectives should be completed
        completed_count = sum(1 for obj in mock_quest.objectives if obj['completed'])
        assert completed_count == 0
        
        # Complete first objective
        mock_quest.complete_objective('Find the artifact')
        
        completed_count = sum(1 for obj in mock_quest.objectives if obj['completed'])
        assert completed_count == 1
        
        # Complete second objective
        mock_quest.complete_objective('Return to quest giver')
        
        completed_count = sum(1 for obj in mock_quest.objectives if obj['completed'])
        assert completed_count == 2
    
    @pytest.mark.unit
    def test_quest_completion_check(self, mock_quest):
        """Test that quest completion is detected correctly"""
        # Initially quest should not be completed
        assert not mock_quest.is_completed()
        
        # Complete one objective
        mock_quest.complete_objective('Find the artifact')
        assert not mock_quest.is_completed()
        
        # Complete all objectives
        mock_quest.complete_objective('Return to quest giver')
        assert mock_quest.is_completed()
    
    @pytest.mark.unit
    def test_quest_rewards_scaling(self, mock_quest):
        """Test that quest rewards scale with difficulty"""
        # Test different difficulty levels
        difficulties = ['trivial', 'easy', 'medium', 'hard', 'very hard', 'epic']
        quest_rewards = {}
        
        for difficulty in difficulties:
            quest = Quest(
                id=f'quest_{difficulty}',
                name=f'Test Quest {difficulty}',
                type='fetch',
                difficulty=difficulty,
                description='Test quest',
                giver='test_npc',
                rewards={},
                objectives=[{'description': 'Test objective', 'completed': False}],
                location='test_location'
            )
            
            quest_rewards[difficulty] = quest.get_scaled_rewards()
        
        # Higher difficulty should give better rewards
        assert quest_rewards['epic']['experience'] > quest_rewards['trivial']['experience']
        assert quest_rewards['epic']['gold'] > quest_rewards['trivial']['gold']
        assert len(quest_rewards['epic']['items']) >= len(quest_rewards['trivial']['items'])
    
    @pytest.mark.unit
    @given(st.text(min_size=1, max_size=50), st_difficulty)
    def test_quest_creation_with_various_difficulties(self, name, difficulty):
        """Test quest creation with various difficulty levels"""
        quest = Quest(
            id='test_quest',
            name=name,
            type='fetch',
            difficulty=difficulty,
            description='Test quest',
            giver='test_npc',
            rewards={'experience': 100, 'gold': 50},
            objectives=[{'description': 'Test objective', 'completed': False}],
            location='test_location'
        )
        
        assert quest.name == name
        assert quest.difficulty == difficulty
    
    @pytest.mark.unit
    def test_quest_types(self):
        """Test that different quest types exist"""
        quest_types = ['fetch', 'kill', 'escort', 'explore', 'deliver', 'protect', 'solve', 'rescue']
        
        for quest_type in quest_types:
            quest = Quest(
                id=f'quest_{quest_type}',
                name=f'Test {quest_type} quest',
                type=quest_type,
                difficulty='medium',
                description='Test quest',
                giver='test_npc',
                rewards={'experience': 100, 'gold': 50},
                objectives=[{'description': 'Test objective', 'completed': False}],
                location='test_location'
            )
            
            assert quest.type == quest_type
    
    @pytest.mark.unit
    @given(st.lists(st.text(min_size=1, max_size=50), min_size=1, max_size=5))
    def test_quest_objectives_with_various_counts(self, objectives):
        """Test quests with varying numbers of objectives"""
        quest_objectives = [
            {'description': desc, 'completed': False}
            for desc in objectives
        ]
        
        quest = Quest(
            id='test_quest',
            name='Test Quest',
            type='fetch',
            difficulty='medium',
            description='Test quest',
            giver='test_npc',
            rewards={'experience': 100, 'gold': 50},
            objectives=quest_objectives,
            location='test_location'
        )
        
        assert len(quest.objectives) == len(objectives)
    
    @pytest.mark.unit
    def test_quest_prerequisites(self):
        """Test quest prerequisites system"""
        main_quest = Quest(
            id='main_quest',
            name='Main Quest',
            type='fetch',
            difficulty='hard',
            description='Main quest',
            giver='king_npc',
            rewards={'experience': 1000, 'gold': 500},
            objectives=[{'description': 'Complete main objective', 'completed': False}],
            location='throne_room',
            prerequisites=['intro_quest']
        )
        
        # Quest should not be available without completing prerequisites
        player = create_test_player("Warrior", 5)
        player.quests['completed'] = []
        
        assert not main_quest.is_available(player)
        
        # Make quest available after completing prerequisite
        player.quests['completed'].append('intro_quest')
        
        assert main_quest.is_available(player)
    
    @pytest.mark.unit
    def test_quest_time_limits(self):
        """Test quest time limit functionality"""
        quest = Quest(
            id='timed_quest',
            name='Timed Quest',
            type='fetch',
            difficulty='medium',
            description='Timed quest',
            giver='test_npc',
            rewards={'experience': 100, 'gold': 50},
            objectives=[{'description': 'Complete in time', 'completed': False}],
            location='test_location',
            time_limit=24  # 24 hours
        )
        
        # Should have time remaining
        assert quest.time_remaining() > 0
        
        # Should expire after time limit
        quest.start_time = quest.start_time - 25 * 3600  # 25 hours ago
        assert quest.time_remaining() < 0
    
    @pytest.mark.unit
    @given(st.integers(min_value=-100, max_value=100))
    def test_quest_reputation_requirements(self, reputation):
        """Test quest reputation requirements"""
        quest = Quest(
            id='reputation_quest',
            name='Reputation Quest',
            type='fetch',
            difficulty='medium',
            description='Reputation quest',
            giver='test_npc',
            rewards={'experience': 100, 'gold': 50},
            objectives=[{'description': 'Complete objective', 'completed': False}],
            location='test_location',
            reputation_required=50
        )
        
        player = create_test_player("Warrior", 5)
        player.reputation = {'TestCity': reputation, 'World': 0}
        
        if reputation >= 50:
            assert quest.is_available(player)
        else:
            assert not quest.is_available(player)


class TestQuestGiver:
    """Test quest giver functionality"""
    
    @pytest.mark.unit
    def test_quest_giver_creation(self, mock_npc):
        """Test that quest givers are created correctly"""
        quest_giver = QuestGiver(mock_npc)
        
        assert quest_giver.id == mock_npc.id
        assert quest_giver.name == mock_npc.name
        assert quest_giver.location == mock_npc.location
        assert quest_giver.personality == mock_npc.personality
        assert quest_giver.quirks == mock_npc.quirks
    
    @pytest.mark.unit
    def test_quest_giver_offers_quests(self):
        """Test that quest givers can offer quests"""
        quest_data = {
            'id': 'quest_test',
            'name': 'Test Quest',
            'type': 'fetch',
            'difficulty': 'medium',
            'description': 'Test quest',
            'giver': 'npc_test',
            'rewards': {'experience': 100, 'gold': 50},
            'objectives': [{'description': 'Test objective', 'completed': False}],
            'location': 'test_location'
        }
        
        quest = Quest(**quest_data)
        quest_giver = QuestGiver(mock_npc)
        quest_giver.add_quest(quest)
        
        assert quest in quest_giver.available_quests
    
    @pytest.mark.unit
    def test_quest_giver_dialogue_generation(self):
        """Test that quest givers generate appropriate dialogue"""
        quest_giver = QuestGiver(mock_npc)
        
        dialogue = quest_giver.generate_dialogue('greeting')
        
        assert 'greeting' in dialogue.lower()
        assert len(dialogue) > 10  # Reasonable dialogue length
    
    @pytest.mark.unit
    def test_quest_giver_dialogue_by_personality(self):
        """Test that quest giver dialogue matches personality"""
        personality_types = ['friendly', 'grumpy', 'mysterious', 'boastful', 'humble']
        
        for personality in personality_types:
            npc_data = MagicMock()
            npc_data.id = f'npc_{personality}'
            npc_data.name = f'NPC {personality}'
            npc_data.location = 'test_location'
            npc_data.personality = personality
            npc_data.quirks = 'none'
            
            quest_giver = QuestGiver(npc_data)
            dialogue = quest_giver.generate_dialogue('quest_offer')
            
            assert len(dialogue) > 10
            
            # Friendly personality should have positive tone
            if personality == 'friendly':
                assert any(word in dialogue.lower() for word in ['help', 'please', 'thank', 'welcome'])
            
            # Grumpy personality should have negative tone
            elif personality == 'grumpy':
                assert any(word in dialogue.lower() for word in ['hurry', 'bother', 'busy'])
    
    @pytest.mark.unit
    def test_quest_giver_responses_to_reputation(self):
        """Test that quest givers respond to player reputation"""
        quest_giver = QuestGiver(mock_npc)
        
        # Test with low reputation
        player_low = create_test_player("Warrior", 5)
        player_low.reputation = {'TestCity': -20, 'World': -10}
        
        dialogue_low = quest_giver.generate_dialogue_by_reputation(player_low)
        
        # Test with high reputation
        player_high = create_test_player("Warrior", 5)
        player_high.reputation = {'TestCity': 80, 'World': 50}
        
        dialogue_high = quest_giver.generate_dialogue_by_reputation(player_high)
        
        # Dialogues should be different
        assert dialogue_low != dialogue_high
    
    @pytest.mark.unit
    def test_quest_giver_responses_to_class(self):
        """Test that quest givers respond to player class"""
        quest_giver = QuestGiver(mock_npc)
        
        class_types = ['Warrior', 'Mage', 'Rogue']
        dialogues = {}
        
        for class_type in class_types:
            player = create_test_player(class_type, 5)
            dialogue = quest_giver.generate_dialogue_by_class(player)
            dialogues[class_type] = dialogue
        
        # Different classes should get different dialogues
        assert dialogues['Warrior'] != dialogues['Mage']
        assert dialogues['Mage'] != dialogues['Rogue']
        assert dialogues['Warrior'] != dialogues['Rogue']
    
    @pytest.mark.unit
    def test_quest_giver_remembers_completed_quests(self):
        """Test that quest givers remember completed quests"""
        quest_giver = QuestGiver(mock_npc)
        
        quest_data = {
            'id': 'quest_test',
            'name': 'Test Quest',
            'type': 'fetch',
            'difficulty': 'medium',
            'description': 'Test quest',
            'giver': 'npc_test',
            'rewards': {'experience': 100, 'gold': 50},
            'objectives': [{'description': 'Test objective', 'completed': False}],
            'location': 'test_location'
        }
        
        quest = Quest(**quest_data)
        quest_giver.add_quest(quest)
        quest_giver.complete_quest('quest_test')
        
        # Quest should move from available to completed
        assert quest not in quest_giver.available_quests
        assert 'quest_test' in quest_giver.completed_quests


class TestQuestManager:
    """Test quest manager functionality"""
    
    @pytest.mark.unit
    def test_quest_manager_creation(self):
        """Test that quest manager is created correctly"""
        quest_manager = QuestManager()
        
        assert quest_manager.active_quests == []
        assert quest_manager.completed_quests == []
        assert quest_manager.available_quests == []
    
    @pytest.mark.unit
    def test_quest_manager_adds_quests(self):
        """Test that quest manager can add quests"""
        quest_manager = QuestManager()
        
        quest_data = {
            'id': 'quest_test',
            'name': 'Test Quest',
            'type': 'fetch',
            'difficulty': 'medium',
            'description': 'Test quest',
            'giver': 'npc_test',
            'rewards': {'experience': 100, 'gold': 50},
            'objectives': [{'description': 'Test objective', 'completed': False}],
            'location': 'test_location'
        }
        
        quest = Quest(**quest_data)
        quest_manager.add_quest(quest)
        
        assert quest in quest_manager.available_quests
    
    @pytest.mark.unit
    def test_quest_manager_start_quest(self):
        """Test that quest manager can start quests"""
        quest_manager = QuestManager()
        player = create_test_player("Warrior", 5)
        
        quest_data = {
            'id': 'quest_test',
            'name': 'Test Quest',
            'type': 'fetch',
            'difficulty': 'medium',
            'description': 'Test quest',
            'giver': 'npc_test',
            'rewards': {'experience': 100, 'gold': 50},
            'objectives': [{'description': 'Test objective', 'completed': False}],
            'location': 'test_location'
        }
        
        quest = Quest(**quest_data)
        quest_manager.add_quest(quest)
        
        result = quest_manager.start_quest('quest_test', player)
        
        assert result is True
        assert quest not in quest_manager.available_quests
        assert quest in quest_manager.active_quests
        assert 'quest_test' in player.quests['active']
    
    @pytest.mark.unit
    def test_quest_manager_complete_quest(self):
        """Test that quest manager can complete quests"""
        quest_manager = QuestManager()
        player = create_test_player("Warrior", 5)
        
        quest_data = {
            'id': 'quest_test',
            'name': 'Test Quest',
            'type': 'fetch',
            'difficulty': 'medium',
            'description': 'Test quest',
            'giver': 'npc_test',
            'rewards': {
                'experience': 500,
                'gold': 200,
                'items': ['item_test']
            },
            'objectives': [
                {'description': 'Objective 1', 'completed': True},
                {'description': 'Objective 2', 'completed': True}
            ],
            'location': 'test_location'
        }
        
        quest = Quest(**quest_data)
        quest_manager.active_quests = [quest]
        
        # Track initial stats
        initial_exp = player.experience
        initial_gold = player.gold
        initial_items = len(player.inventory)
        
        result = quest_manager.complete_quest('quest_test', player)
        
        assert result is True
        assert quest not in quest_manager.active_quests
        assert quest in quest_manager.completed_quests
        assert 'quest_test' in player.quests['completed']
        
        # Check rewards were applied
        assert player.experience == initial_exp + quest.rewards['experience']
        assert player.gold == initial_gold + quest.rewards['gold']
        assert len(player.inventory) >= initial_items + len(quest.rewards['items'])
    
    @pytest.mark.unit
    def test_quest_manager_filters_available_quests(self):
        """Test that quest manager filters available quests by player status"""
        quest_manager = QuestManager()
        player = create_test_player("Warrior", 5)
        
        # Add quests with different requirements
        quest_easy = Quest(
            id='quest_easy',
            name='Easy Quest',
            type='fetch',
            difficulty='easy',
            description='Easy quest',
            giver='npc_easy',
            rewards={'experience': 50, 'gold': 25},
            objectives=[{'description': 'Easy objective', 'completed': False}],
            location='test_location',
            level_required=1
        )
        
        quest_hard = Quest(
            id='quest_hard',
            name='Hard Quest',
            type='fetch',
            difficulty='hard',
            description='Hard quest',
            giver='npc_hard',
            rewards={'experience': 1000, 'gold': 500},
            objectives=[{'description': 'Hard objective', 'completed': False}],
            location='test_location',
            level_required=10
        )
        
        quest_rep = Quest(
            id='quest_rep',
            name='Reputation Quest',
            type='fetch',
            difficulty='medium',
            description='Reputation quest',
            giver='npc_rep',
            rewards={'experience': 200, 'gold': 100},
            objectives=[{'description': 'Reputation objective', 'completed': False}],
            location='test_location',
            reputation_required=50
        )
        
        quest_manager.add_quest(quest_easy)
        quest_manager.add_quest(quest_hard)
        quest_manager.add_quest(quest_rep)
        
        # Filter available quests
        available = quest_manager.get_available_quests(player)
        
        # Player is level 5 with low reputation
        assert quest_easy in available
        assert quest_hard not in available  # Level too low
        assert quest_rep not in available   # Reputation too low
    
    @pytest.mark.unit
    def test_quest_manager_tracking_by_type(self):
        """Test that quest manager can track quests by type"""
        quest_manager = QuestManager()
        
        quest_types = ['fetch', 'kill', 'escort', 'explore']
        
        for quest_type in quest_types:
            quest = Quest(
                id=f'quest_{quest_type}',
                name=f'{quest_type.title()} Quest',
                type=quest_type,
                difficulty='medium',
                description=f'{quest_type.title()} quest',
                giver='npc_test',
                rewards={'experience': 100, 'gold': 50},
                objectives=[{'description': f'{quest_type} objective', 'completed': False}],
                location='test_location'
            )
            quest_manager.add_quest(quest)
        
        # Get quests by type
        for quest_type in quest_types:
            quests_of_type = quest_manager.get_quests_by_type(quest_type)
            assert len(quests_of_type) == 1
            assert quests_of_type[0].type == quest_type
    
    @pytest.mark.unit
    def test_quest_manager_tracking_by_difficulty(self):
        """Test that quest manager can track quests by difficulty"""
        quest_manager = QuestManager()
        
        difficulties = ['easy', 'medium', 'hard']
        
        for difficulty in difficulties:
            quest = Quest(
                id=f'quest_{difficulty}',
                name=f'{difficulty.title()} Quest',
                type='fetch',
                difficulty=difficulty,
                description=f'{difficulty.title()} quest',
                giver='npc_test',
                rewards={'experience': 100, 'gold': 50},
                objectives=[{'description': f'{difficulty} objective', 'completed': False}],
                location='test_location'
            )
            quest_manager.add_quest(quest)
        
        # Get quests by difficulty
        for difficulty in difficulties:
            quests_of_difficulty = quest_manager.get_quests_by_difficulty(difficulty)
            assert len(quests_of_difficulty) == 1
            assert quests_of_difficulty[0].difficulty == difficulty
    
    @pytest.mark.unit
    @given(st.integers(min_value=1, max_value=100))
    def test_quest_manager_quest_count_limits(self, quest_count):
        """Test that quest manager handles various numbers of quests"""
        quest_manager = QuestManager()
        
        for i in range(quest_count):
            quest = Quest(
                id=f'quest_{i}',
                name=f'Quest {i}',
                type='fetch',
                difficulty='medium',
                description=f'Quest {i}',
                giver='npc_test',
                rewards={'experience': 100, 'gold': 50},
                objectives=[{'description': f'Objective {i}', 'completed': False}],
                location='test_location'
            )
            quest_manager.add_quest(quest)
        
        # Should handle all quests without issues
        assert len(quest_manager.available_quests) == quest_count
        
        # Should be able to filter and retrieve quests
        filtered = quest_manager.get_available_quests(create_test_player("Warrior", 10))
        assert len(filtered) <= quest_count


class TestQuestRewards:
    """Test quest reward system"""
    
    @pytest.mark.unit
    def test_quest_reward_distribution(self):
        """Test that quest rewards are distributed correctly"""
        player = create_test_player("Warrior", 5)
        
        # Track initial values
        initial_exp = player.experience
        initial_gold = player.gold
        initial_items = len(player.inventory)
        
        rewards = {
            'experience': 500,
            'gold': 200,
            'items': ['sword', 'shield', 'potion'],
            'special_reward': 'title_hero'
        }
        
        QuestManager.distribute_rewards(player, rewards)
        
        # Check rewards were applied
        assert player.experience == initial_exp + rewards['experience']
        assert player.gold == initial_gold + rewards['gold']
        assert len(player.inventory) == initial_items + len(rewards['items'])
        assert 'title_hero' in player.titles
    
    @pytest.mark.unit
    @given(st.integers(min_value=0, max_value=10000))
    def test_quest_experience_rewards(self, experience):
        """Test experience rewards with various values"""
        player = create_test_player("Warrior", 5)
        player.experience = 0
        
        rewards = {
            'experience': experience,
            'gold': 100,
            'items': []
        }
        
        QuestManager.distribute_rewards(player, rewards)
        
        assert player.experience == experience
    
    @pytest.mark.unit
    @given(st.integers(min_value=0, max_value=10000))
    def test_quest_gold_rewards(self, gold):
        """Test gold rewards with various values"""
        player = create_test_player("Warrior", 5)
        player.gold = 0
        
        rewards = {
            'experience': 100,
            'gold': gold,
            'items': []
        }
        
        QuestManager.distribute_rewards(player, rewards)
        
        assert player.gold == gold
    
    @pytest.mark.unit
    @given(st.lists(st.text(min_size=1, max_size=20), min_size=0, max_size=10))
    def test_quest_item_rewards(self, items):
        """Test item rewards with various quantities"""
        player = create_test_player("Warrior", 5)
        player.inventory = []
        
        rewards = {
            'experience': 100,
            'gold': 50,
            'items': items.copy()
        }
        
        QuestManager.distribute_rewards(player, rewards)
        
        assert len(player.inventory) == len(items)
        for item in items:
            assert item in player.inventory
    
    @pytest.mark.unit
    def test_quest_special_rewards(self):
        """Test special reward types"""
        player = create_test_player("Warrior", 5)
        player.titles = []
        player.abilities = ['Attack', 'Defend']
        
        rewards = {
            'experience': 100,
            'gold': 50,
            'items': [],
            'special_reward': 'title_dragon_slayer'
        }
        
        QuestManager.distribute_rewards(player, rewards)
        
        assert 'title_dragon_slayer' in player.titles
        
        # Test ability reward
        rewards['special_reward'] = 'ability_fire_blast'
        player.abilities = ['Attack', 'Defend']
        
        QuestManager.distribute_rewards(player, rewards)
        
        assert 'fire_blast' in [ability.lower() for ability in player.abilities]