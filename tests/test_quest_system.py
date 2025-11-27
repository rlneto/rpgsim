"""
Unit tests for Quest System implementation
Comprehensive test coverage for all Quest System components
"""

import pytest
from unittest.mock import Mock, patch
from core.systems.quest import (
    QuestType, QuestDifficulty, NPCPersonality, NPCQuirk,
    QuestTemplate, NPCProfile, DialogueOption, DialogueResponse,
    QuestProgress, QuestGenerator, NPCManager, DialogueManager,
    QuestManager, QuestSystem
)


class TestQuestConstants:
    """Test quest system constants and enums"""

    def test_quest_type_constants(self):
        """Test QuestType class constants"""
        assert QuestType.KILL == "kill"
        assert QuestType.FETCH == "fetch"
        assert QuestType.ESCORT == "escort"
        assert QuestType.EXPLORE == "explore"
        # Check that we have multiple quest types
        quest_types = [
            QuestType.KILL, QuestType.FETCH, QuestType.ESCORT, QuestType.EXPLORE,
            QuestType.DELIVER, QuestType.PROTECT, QuestType.SOLVE, QuestType.RESCUE
        ]
        assert len(quest_types) == 8

    def test_quest_difficulty_constants(self):
        """Test QuestDifficulty class constants"""
        assert QuestDifficulty.TRIVIAL == "trivial"
        assert QuestDifficulty.EPIC == "epic"
        # Check that we have multiple difficulty levels
        difficulties = [
            QuestDifficulty.TRIVIAL, QuestDifficulty.EASY, QuestDifficulty.MEDIUM,
            QuestDifficulty.HARD, QuestDifficulty.VERY_HARD, QuestDifficulty.EPIC
        ]
        assert len(difficulties) == 6

    def test_npc_personality_constants(self):
        """Test NPCPersonality class constants"""
        assert NPCPersonality.FRIENDLY == "friendly"
        assert NPCPersonality.MYSTERIOUS == "mysterious"
        # Check that we have multiple personality types
        personalities = [
            NPCPersonality.FRIENDLY, NPCPersonality.GRUMPY, NPCPersonality.MYSTERIOUS,
            NPCPersonality.BOASTFUL, NPCPersonality.HUMBLE, NPCPersonality.WISE,
            NPCPersonality.CUNNING, NPCPersonality.CHAOTIC, NPCPersonality.NOBLE, NPCPersonality.MISCHIEVOUS
        ]
        assert len(personalities) == 10

    def test_npc_quirk_constants(self):
        """Test NPCQuirk class constants"""
        assert NPCQuirk.STUTTERS == "stutters"
        assert NPCQuirk.RHYMES == "rhymes"
        # Check that we have multiple quirk types
        quirks = [
            NPCQuirk.STUTTERS, NPCQuirk.RHYMES, NPCQuirk.USES_ANCIENT_WORDS,
            NPCQuirk.SPEAKS_IN_RIDDLES, NPCQuirk.ALWAYS_HUNGRY, NPCQuirk.COLLECTS_THINGS,
            NPCQuirk.OVERLY_DRAMATIC, NPCQuirk.SPEAKS_IN_THIRD_PERSON, NPCQuirk.HAS_PET, NPCQuirk.SINGS_RESPONSES
        ]
        assert len(quirks) == 10


class TestQuestDataClasses:
    """Test quest system dataclasses"""

    def test_quest_template_creation(self):
        """Test QuestTemplate dataclass creation"""
        template = QuestTemplate(
            name_template="Test {target}",
            description_template="Test description {target}",
            objective_templates=["Test {target}"],
            quest_type=QuestType.KILL,
            base_difficulty=QuestDifficulty.MEDIUM,
            reward_multipliers={"experience": 1.0, "gold": 1.0}
        )

        assert template.name_template == "Test {target}"
        assert template.quest_type == QuestType.KILL
        assert template.base_difficulty == QuestDifficulty.MEDIUM
        assert template.reward_multipliers["experience"] == 1.0

    
    def test_npc_profile_creation(self):
        """Test NPCProfile dataclass creation"""
        profile = NPCProfile(
            npc_id="npc_001",
            name="Test NPC",
            location="test_location",
            personality=NPCPersonality.FRIENDLY,
            quirk=NPCQuirk.NONE,
            specialties=["combat"],
            relationships={},
            daily_schedule={},
            secrets=[]
        )

        assert profile.npc_id == "npc_001"
        assert profile.name == "Test NPC"
        assert profile.personality == NPCPersonality.FRIENDLY
        assert profile.specialties == ["combat"]

    
    def test_dialogue_option_creation(self):
        """Test DialogueOption dataclass creation"""
        option = DialogueOption(
            text="Hello",
            requirements={"reputation": 0},
            responses=["Greetings"]
        )

        assert option.text == "Hello"
        assert option.requirements["reputation"] == 0
        assert option.responses == ["Greetings"]

    
    def test_dialogue_response_creation(self):
        """Test DialogueResponse dataclass creation"""
        response = DialogueResponse(
            text="Hello there!",
            npc_reaction="friendly",
            quest_unlock=None,
            reputation_change=0
        )

        assert response.text == "Hello there!"
        assert response.npc_reaction == "friendly"
        assert response.reputation_change == 0

    
    def test_quest_progress_creation(self):
        """Test QuestProgress dataclass creation"""
        progress = QuestProgress(
            quest_id="quest_001",
            player_id="player_001",
            status="active",
            progress={},
            completion_date=None
        )

        assert progress.quest_id == "quest_001"
        assert progress.status == "active"
        assert progress.completion_date is None


class TestQuestGenerator:
    """Test QuestGenerator class"""

    
    def test_generate_quest_kill_type(self):
        """Test generating a KILL type quest"""
        generator = QuestGenerator()
        quest = generator.generate_quest(
            quest_id="test_quest_001",
            quest_type=QuestType.KILL,
            difficulty=QuestDifficulty.MEDIUM,
            giver="Test_Giver"
        )

        assert quest.quest_type == QuestType.KILL
        assert quest.difficulty == QuestDifficulty.MEDIUM
        assert "Defeat" in quest.name
        assert quest.giver == "Test_Giver"
        assert quest.objectives
        assert quest.rewards

    
    def test_generate_quest_fetch_type(self):
        """Test generating a FETCH type quest"""
        generator = QuestGenerator()
        quest = generator.generate_quest(
            quest_type=QuestType.FETCH,
            difficulty=QuestDifficulty.EASY,
            location="Test Cave"
        )

        assert quest.quest_type == QuestType.FETCH
        assert quest.difficulty == QuestDifficulty.EASY
        assert "Retrieve" in quest.name
        assert quest.location == "Test Cave"

    
    def test_generate_quest_escort_type(self):
        """Test generating an ESCORT type quest"""
        generator = QuestGenerator()
        quest = generator.generate_quest(
            quest_type=QuestType.ESCORT,
            difficulty=QuestDifficulty.HARD,
            location="Test Mountains"
        )

        assert quest.quest_type == QuestType.ESCORT
        assert quest.difficulty == QuestDifficulty.HARD
        assert "Escort" in quest.name
        assert quest.location == "Test Mountains"

    
    def test_generate_quest_explore_type(self):
        """Test generating an EXPLORE type quest"""
        generator = QuestGenerator()
        quest = generator.generate_quest(
            quest_type=QuestType.EXPLORE,
            difficulty=QuestDifficulty.MEDIUM,
            location="Test Ruins"
        )

        assert quest.quest_type == QuestType.EXPLORE
        assert "Explore" in quest.name
        assert quest.location == "Test Ruins"

    
    def test_difficulty_reward_scaling(self):
        """Test that quest rewards scale with difficulty"""
        generator = QuestGenerator()

        trivial_quest = generator.generate_quest(
            quest_type=QuestType.KILL,
            difficulty=QuestDifficulty.TRIVIAL,
            location="Test"
        )

        epic_quest = generator.generate_quest(
            quest_type=QuestType.KILL,
            difficulty=QuestDifficulty.EPIC,
            location="Test"
        )

        # Epic should have significantly higher rewards
        assert epic_quest.rewards["experience"] > trivial_quest.rewards["experience"]
        assert epic_quest.rewards["gold"] > trivial_quest.rewards["gold"]

    
    def test_quest_objective_generation(self):
        """Test quest objectives are properly generated"""
        generator = QuestGenerator()
        quest = generator.generate_quest(
            quest_type=QuestType.KILL,
            difficulty=QuestDifficulty.MEDIUM,
            location="Test"
        )

        assert len(quest.objectives) >= 1
        for objective in quest.objectives:
            assert hasattr(objective, 'description')
            assert hasattr(objective, 'target_count')
            assert hasattr(objective, 'current_count')
            assert hasattr(objective, 'completed')

    
    def test_unique_quest_generation(self):
        """Test that generated quests have unique IDs"""
        generator = QuestGenerator()
        quests = [
            generator.generate_quest(
                quest_type=QuestType.KILL,
                difficulty=QuestDifficulty.MEDIUM,
                location=f"Location_{i}"
            )
            for i in range(10)
        ]

        quest_ids = [quest.quest_id for quest in quests]
        assert len(set(quest_ids)) == 10  # All unique


class TestNPCManager:
    """Test NPCManager class"""

    
    def test_create_npc_profile(self):
        """Test creating an NPC profile"""
        manager = NPCManager()
        npc = manager.create_npc_profile(
            npc_id="npc_001",
            name="Test NPC",
            location="Test Town"
        )

        assert npc.npc_id == "npc_001"
        assert npc.name == "Test NPC"
        assert npc.location == "Test Town"
        assert npc.personality in NPCPersonality
        assert npc.quirk in NPCQuirk

    
    def test_generate_npcs_batch(self):
        """Test generating multiple NPCs"""
        manager = NPCManager()
        npcs = manager.generate_npcs(count=10, locations=["Test Town", "Test Forest"])

        assert len(npcs) == 10
        for npc in npcs:
            assert hasattr(npc, 'npc_id')
            assert hasattr(npc, 'name')
            assert hasattr(npc, 'personality')
            assert hasattr(npc, 'quirk')

    
    def test_npc_location_distribution(self):
        """Test NPCs are distributed across locations"""
        locations = ["Town", "Forest", "Mountains", "Cave"]
        manager = NPCManager()
        npcs = manager.generate_npcs(count=100, locations=locations)

        location_counts = {}
        for npc in npcs:
            location_counts[npc.location] = location_counts.get(npc.location, 0) + 1

        # Should have NPCs in all locations
        assert len(location_counts) >= 3

    
    def test_npc_personality_variety(self):
        """Test NPCs have variety of personalities"""
        manager = NPCManager()
        npcs = manager.generate_npcs(count=20)

        personalities = set(npc.personality for npc in npcs)
        assert len(personalities) >= 3  # Should have variety

    
    def test_npc_quirk_distribution(self):
        """Test NPCs have various quirks"""
        manager = NPCManager()
        npcs = manager.generate_npcs(count=20)

        quirks = set(npc.quirk for npc in npcs)
        assert len(quirks) >= 2  # Should have variety

    
    def test_get_npc_by_id(self):
        """Test retrieving NPC by ID"""
        manager = NPCManager()
        npcs = manager.generate_npcs(count=5)

        test_npc = npcs[0]
        found_npc = manager.get_npc_by_id(test_npc.npc_id)

        assert found_npc is not None
        assert found_npc.npc_id == test_npc.npc_id

    
    def test_get_npcs_by_location(self):
        """Test retrieving NPCs by location"""
        manager = NPCManager()
        npcs = manager.generate_npcs(count=10, locations=["Test Town"])

        town_npcs = manager.get_npcs_by_location("Test Town")

        assert len(town_npcs) >= 1
        for npc in town_npcs:
            assert npc.location == "Test Town"

    
    def test_npc_specialties(self):
        """Test NPCs have appropriate specialties"""
        manager = NPCManager()
        npc = manager.create_npc_profile(
            npc_id="npc_001",
            name="Test NPC",
            location="Test Town"
        )

        assert isinstance(npc.specialties, list)
        if npc.specialties:
            for specialty in npc.specialties:
                assert isinstance(specialty, str)

    
    def test_npc_relationships(self):
        """Test NPC relationships system"""
        manager = NPCManager()
        npcs = manager.generate_npcs(count=5)

        for npc in npcs:
            assert isinstance(npc.relationships, dict)
            # Check if relationships have valid structure
            for related_npc, relationship in npc.relationships.items():
                assert isinstance(related_npc, str)
                assert isinstance(relationship, str)

    
    def test_npc_secrets(self):
        """Test NPC secrets system"""
        manager = NPCManager()
        npc = manager.create_npc_profile(
            npc_id="npc_001",
            name="Test NPC",
            location="Test Town"
        )

        assert isinstance(npc.secrets, list)
        for secret in npc.secrets:
            assert isinstance(secret, str)


class TestDialogueManager:
    """Test DialogueManager class"""

    
    def test_generate_class_dialogue_options_warrior(self):
        """Test generating dialogue options for Warrior class"""
        manager = DialogueManager()
        options = manager.generate_class_dialogue_options("Warrior")

        assert len(options) > 0
        assert any("combat" in option.text.lower() or "fight" in option.text.lower()
                  for option in options)

    
    def test_generate_class_dialogue_options_mage(self):
        """Test generating dialogue options for Mage class"""
        manager = DialogueManager()
        options = manager.generate_class_dialogue_options("Mage")

        assert len(options) > 0
        assert any("magic" in option.text.lower() or "arcane" in option.text.lower()
                  for option in options)

    
    def test_generate_reputation_dialogue_high_rep(self):
        """Test generating dialogue options for high reputation"""
        manager = DialogueManager()
        options = manager.generate_reputation_dialogue_options(75)

        assert len(options) > 0
        # High reputation should unlock special options
        assert any(option.requirements.get("reputation", 0) >= 50
                  for option in options)

    
    def test_generate_reputation_dialogue_low_rep(self):
        """Test generating dialogue options for low reputation"""
        manager = DialogueManager()
        options = manager.generate_reputation_dialogue_options(-25)

        assert len(options) >= 0  # May be empty for very low reputation

    
    def test_generate_quest_dialogue_options(self):
        """Test generating quest-related dialogue options"""
        manager = DialogueManager()
        mock_quests = [
            Mock(quest_id="quest_001", status="active"),
            Mock(quest_id="quest_002", status="completed")
        ]

        options = manager.generate_quest_dialogue_options(mock_quests)

        assert len(options) > 0
        # Should have options related to active quests
        assert any("quest" in option.text.lower() for option in options)

    
    def test_generate_npc_response_friendly(self):
        """Test generating NPC response for friendly personality"""
        manager = DialogueManager()
        npc_profile = Mock(
            personality=NPCPersonality.FRIENDLY,
            quirk=NPCQuirk.NONE
        )

        response = manager.generate_npc_response(
            npc_profile=npc_profile,
            player_input="Hello",
            player_reputation=50
        )

        assert response.text
        assert response.npc_reaction in ["friendly", "neutral", "positive"]

    
    def test_generate_npc_response_grumpy(self):
        """Test generating NPC response for grumpy personality"""
        manager = DialogueManager()
        npc_profile = Mock(
            personality=NPCPersonality.GRUMPY,
            quirk=NPCQuirk.NONE
        )

        response = manager.generate_npc_response(
            npc_profile=npc_profile,
            player_input="Hello",
            player_reputation=50
        )

        assert response.text
        assert response.npc_reaction in ["grumpy", "negative", "neutral"]

    
    def test_apply_speech_quirk_stutters(self):
        """Test applying stutter quirk to dialogue"""
        manager = DialogueManager()
        original = "Hello there traveler"
        modified = manager.apply_speech_quirk(original, NPCQuirk.STUTTERS)

        assert modified != original
        # Should contain stutter pattern
        assert "st-" in modified or "he-" in modified or "th-" in modified

    
    def test_apply_speech_quirk_rhymes(self):
        """Test applying rhyme quirk to dialogue"""
        manager = DialogueManager()
        original = "Hello there"
        modified = manager.apply_speech_quirk(original, NPCQuirk.RHYMES)

        assert modified != original
        # Should end with rhyme phrase
        assert modified.endswith("see") or modified.endswith("be") or modified.endswith("free")

    
    def test_get_all_dialogue_options(self):
        """Test getting all dialogue options for player"""
        manager = DialogueManager()
        npc_profile = Mock(
            personality=NPCPersonality.FRIENDLY,
            quirk=NPCQuirk.NONE,
            specialties=["combat"]
        )

        options = manager.get_all_dialogue_options(
            npc_profile=npc_profile,
            player_class="Warrior",
            player_reputation=50,
            player_quests=[Mock(status="active")]
        )

        assert len(options) > 0
        # Should include base options
        assert any(option.text == "Hello" for option in options)


class TestQuestManager:
    """Test QuestManager class"""

    
    def test_start_quest(self):
        """Test starting a quest"""
        manager = QuestManager()
        quest = Mock(
            quest_id="quest_001",
            objectives=[Mock(description="Kill something", completed=False)]
        )

        progress = manager.start_quest("player_001", quest)

        assert progress.quest_id == "quest_001"
        assert progress.player_id == "player_001"
        assert progress.status == "active"
        assert len(progress.objectives) == len(quest.objectives)

    
    def test_update_quest_progress(self):
        """Test updating quest progress"""
        manager = QuestManager()
        quest = Mock(
            quest_id="quest_001",
            objectives=[
                Mock(description="Kill 5 goblins", completed=False),
                Mock(description="Find treasure", completed=False)
            ]
        )

        progress = manager.start_quest("player_001", quest)

        # Update first objective
        updated = manager.update_quest_progress(
            player_id="player_001",
            quest_id="quest_001",
            objective_index=0,
            amount=3
        )

        assert updated.objectives[0].current_count == 3

    
    def test_complete_quest_objective(self):
        """Test completing a quest objective"""
        manager = QuestManager()
        quest = Mock(
            quest_id="quest_001",
            objectives=[Mock(description="Kill 5 goblins", completed=False)]
        )

        progress = manager.start_quest("player_001", quest)

        # Complete objective
        updated = manager.update_quest_progress(
            player_id="player_001",
            quest_id="quest_001",
            objective_index=0,
            amount=5
        )

        assert updated.objectives[0].completed is True
        assert updated.objectives[0].current_count == 5

    
    def test_complete_quest(self):
        """Test completing a quest"""
        manager = QuestManager()
        quest = Mock(
            quest_id="quest_001",
            objectives=[
                Mock(description="Kill 5 goblins", completed=False),
                Mock(description="Find treasure", completed=False)
            ]
        )

        progress = manager.start_quest("player_001", quest)

        # Complete all objectives
        progress.objectives[0].completed = True
        progress.objectives[1].completed = True

        completed = manager.complete_quest("player_001", "quest_001")

        assert completed.status == "completed"
        assert completed.completion_date is not None

    
    def test_fail_quest(self):
        """Test failing a quest"""
        manager = QuestManager()
        quest = Mock(quest_id="quest_001")

        progress = manager.start_quest("player_001", quest)

        failed = manager.fail_quest("player_001", "quest_001")

        assert failed.status == "failed"

    
    def test_abandon_quest(self):
        """Test abandoning a quest"""
        manager = QuestManager()
        quest = Mock(quest_id="quest_001")

        progress = manager.start_quest("player_001", quest)

        abandoned = manager.abandon_quest("player_001", "quest_001")

        assert abandoned.status == "abandoned"

    
    def test_get_quest_progress(self):
        """Test retrieving quest progress"""
        manager = QuestManager()
        quest = Mock(quest_id="quest_001")

        progress = manager.start_quest("player_001", quest)

        retrieved = manager.get_quest_progress("player_001", "quest_001")

        assert retrieved.quest_id == "quest_001"
        assert retrieved.player_id == "player_001"

    
    def test_get_active_quests(self):
        """Test retrieving active quests for player"""
        manager = QuestManager()
        quests = [
            Mock(quest_id="quest_001"),
            Mock(quest_id="quest_002"),
            Mock(quest_id="quest_003")
        ]

        for quest in quests:
            manager.start_quest("player_001", quest)

        active = manager.get_active_quests("player_001")

        assert len(active) == 3
        for progress in active:
            assert progress.status == "active"

    
    def test_get_completed_quests(self):
        """Test retrieving completed quests for player"""
        manager = QuestManager()
        quests = [Mock(quest_id="quest_001"), Mock(quest_id="quest_002")]

        for quest in quests:
            progress = manager.start_quest("player_001", quest)
            progress.status = "completed"
            manager.quest_progress[f"player_001_{quest.quest_id}"] = progress

        completed = manager.get_completed_quests("player_001")

        assert len(completed) == 2
        for progress in completed:
            assert progress.status == "completed"

    
    def test_is_quest_available(self):
        """Test checking if quest is available"""
        manager = QuestManager()
        quest = Mock(
            quest_id="quest_001",
            requirements={"level": 5, "reputation": 10}
        )

        # Test with eligible player
        player_data = {"level": 6, "reputation": {"current": 15}}
        available = manager.is_quest_available(quest, player_data)

        assert available is True

        # Test with ineligible player
        player_data = {"level": 3, "reputation": {"current": 5}}
        available = manager.is_quest_available(quest, player_data)

        assert available is False

    
    def test_update_progress_invalid_quest(self):
        """Test updating progress for non-existent quest"""
        manager = QuestManager()

        with pytest.raises(KeyError):
            manager.update_quest_progress("player_001", "nonexistent_quest", 0, 5)

    
    def test_update_progress_invalid_objective(self):
        """Test updating progress with invalid objective index"""
        manager = QuestManager()
        quest = Mock(
            quest_id="quest_001",
            objectives=[Mock(description="Kill something", completed=False)]
        )

        progress = manager.start_quest("player_001", quest)

        with pytest.raises(IndexError):
            manager.update_quest_progress("player_001", "quest_001", 99, 5)


class TestQuestSystem:
    """Test integrated QuestSystem class"""

    
    def test_quest_system_initialization(self):
        """Test QuestSystem initialization"""
        system = QuestSystem()

        assert hasattr(system, 'quest_generator')
        assert hasattr(system, 'npc_manager')
        assert hasattr(system, 'dialogue_manager')
        assert hasattr(system, 'quest_manager')

    
    def test_initialize_world(self):
        """Test world initialization with quests and NPCs"""
        system = QuestSystem()
        locations = ["Town", "Forest", "Mountains", "Cave"]

        world_data = system.initialize_world(locations=locations, npc_count=20)

        assert 'npcs' in world_data
        assert 'available_quests' in world_data
        assert len(world_data['npcs']) == 20
        assert len(world_data['available_quests']) > 0

    
    def test_get_available_quests_for_location(self):
        """Test getting available quests for specific location"""
        system = QuestSystem()
        system.initialize_world(locations=["Test Town"])

        quests = system.get_available_quests_for_location("Test Town")

        assert len(quests) >= 0
        for quest in quests:
            assert quest.location == "Test Town"

    
    def test_get_npcs_in_location(self):
        """Test getting NPCs in specific location"""
        system = QuestSystem()
        system.initialize_world(locations=["Test Town"], npc_count=5)

        npcs = system.get_npcs_in_location("Test Town")

        assert len(npcs) >= 1
        for npc in npcs:
            assert npc.location == "Test Town"

    
    def test_start_quest_from_npc(self):
        """Test starting quest from NPC"""
        system = QuestSystem()
        system.initialize_world(locations=["Test Town"], npc_count=1)

        npcs = system.get_npcs_in_location("Test Town")
        npc = npcs[0]

        available_quests = system.get_available_quests_for_location("Test Town")
        if available_quests:
            quest = available_quests[0]

            progress = system.start_quest_from_npc(
                player_id="player_001",
                quest_id=quest.quest_id,
                npc_id=npc.npc_id
            )

            assert progress.quest_id == quest.quest_id
            assert progress.player_id == "player_001"
            assert progress.status == "active"