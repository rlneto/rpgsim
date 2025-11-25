"""
E2E Tests: Complete User Journey
Optimized for LLM agents - validates full game experience from start to finish
"""

import pytest
import time
from typing import Dict, List, Any
from core.models import GameState, Character, CharacterClass, Location, Quest, Enemy, Item
from core.systems.game import start_new_game, save_game, load_game
from core.systems.character import create_character, level_up_character, add_experience
from core.systems.combat import resolve_combat
from core.systems.quest import complete_quest
from core.systems.inventory import add_item_to_inventory, equip_item
from core.systems.location import travel_to_location
from core.constants import DEFAULT_CHARACTER_STATS, DEFAULT_ABILITIES, GAME_CONFIG


class E2EJourneyTester:
    """
    E2E tester for complete user journey.
    Validates that player can start game, create character, play, and reach ending.
    """
    
    def __init__(self):
        self.journey_log = []
        self.performance_metrics = {}
        self.start_time = None
    
    def log_step(self, step_name: str, status: str, details: Any = None, execution_time: float = 0):
        """Log journey step for debugging."""
        log_entry = {
            'step': step_name,
            'status': status,
            'details': details,
            'execution_time': execution_time,
            'timestamp': time.time()
        }
        self.journey_log.append(log_entry)
        print(f"{'✅' if status == 'passed' else '❌'} {step_name}: {status} ({execution_time:.3f}s)")
        return log_entry
    
    def test_game_startup(self) -> GameState:
        """Test game startup - first step of user journey."""
        start_time = time.time()
        
        try:
            # Start new game
            game_state = start_new_game()
            
            # Validate game state
            assert game_state is not None
            assert game_state.current_location == "start"
            assert game_state.player is None  # Character not created yet
            assert game_state.world_time == 0
            assert len(game_state.quests_active) == 0
            assert len(game_state.quests_completed) == 0
            
            execution_time = time.time() - start_time
            self.log_step("game_startup", "passed", {"location": game_state.current_location}, execution_time)
            
            return game_state
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.log_step("game_startup", "failed", str(e), execution_time)
            raise
    
    def test_character_creation(self, game_state: GameState) -> GameState:
        """Test character creation - second step of user journey."""
        start_time = time.time()
        
        try:
            # Create warrior character (good for victory ending)
            character = create_character("E2EHero", CharacterClass.WARRIOR)
            
            # Validate character creation
            assert character.name == "E2EHero"
            assert character.class_type == CharacterClass.WARRIOR
            assert character.level == 1
            assert character.stats.strength == 15
            assert character.stats.dexterity == 10
            assert character.stats.intelligence == 8
            assert character.stats.wisdom == 10
            assert character.stats.charisma == 8
            assert character.stats.constitution == 14
            assert character.hp == 60
            assert character.max_hp == 60
            assert character.gold == 100
            assert len(character.abilities) == 5
            assert len(character.inventory) == 0
            
            # Add character to game state
            game_state.player = character
            
            execution_time = time.time() - start_time
            self.log_step("character_creation", "passed", {
                "name": character.name,
                "class": character.class_type.value,
                "level": character.level
            }, execution_time)
            
            return game_state
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.log_step("character_creation", "failed", str(e), execution_time)
            raise
    
    def test_initial_gameplay(self, game_state: GameState) -> GameState:
        """Test initial gameplay - first combat and quest."""
        start_time = time.time()
        
        try:
            character = game_state.player
            
            # Test first combat
            goblin = create_test_enemy("Goblin", 2)
            combat_result = resolve_combat(character, goblin)
            
            assert combat_result['winner'] == 'player'
            assert combat_result['player_hp'] > 0
            assert combat_result['enemy_hp'] <= 0
            
            # Apply combat results
            character.hp = combat_result['player_hp']
            character.gold += combat_result['reward_gold']
            
            # Test first quest
            quest = create_test_quest("Kill Goblins", 2)
            complete_quest(character, quest)
            
            assert quest.id in character.quests_completed
            
            execution_time = time.time() - start_time
            self.log_step("initial_gameplay", "passed", {
                "enemies_defeated": 1,
                "quests_completed": len(character.quests_completed),
                "gold": character.gold
            }, execution_time)
            
            return game_state
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.log_step("initial_gameplay", "failed", str(e), execution_time)
            raise
    
    def test_character_progression(self, game_state: GameState) -> GameState:
        """Test character progression to mid-game (level 1-25)."""
        start_time = time.time()
        
        try:
            character = game_state.player
            
            # Progress through levels 2-25
            for level in range(2, 26):
                # Add sufficient experience
                exp_needed = get_experience_for_level(level)
                character = add_experience(character, exp_needed)
                
                # Level up
                character = level_up_character(character)
                
                # Validate level up
                assert character.level == level
                
                # Complete some quests
                if level % 3 == 0:
                    quest = create_test_quest(f"Level {level} Quest", level)
                    complete_quest(character, quest)
                
                # Add items to inventory
                if level % 5 == 0:
                    item = create_test_item(f"Level {level} Item", level)
                    add_item_to_inventory(character, item)
            
            # Validate mid-game state
            assert character.level == 25
            assert character.gold >= 1000
            assert len(character.quests_completed) >= 8
            assert len(character.inventory) >= 4
            
            # Validate stats growth
            assert character.stats.strength >= 20  # Maxed
            assert character.stats.dexterity >= 15
            assert character.stats.constitution >= 20  # Maxed
            
            execution_time = time.time() - start_time
            self.log_step("character_progression", "passed", {
                "final_level": character.level,
                "gold": character.gold,
                "quests_completed": len(character.quests_completed),
                "inventory_size": len(character.inventory)
            }, execution_time)
            
            return game_state
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.log_step("character_progression", "failed", str(e), execution_time)
            raise
    
    def test_late_game(self, game_state: GameState) -> GameState:
        """Test late game progression (level 25-50)."""
        start_time = time.time()
        
        try:
            character = game_state.player
            
            # Progress through levels 26-50
            for level in range(26, 51):
                # Add sufficient experience
                exp_needed = get_experience_for_level(level)
                character = add_experience(character, exp_needed)
                
                # Level up
                character = level_up_character(character)
                
                # Validate level up
                assert character.level == level
                
                # Complete main quests
                if level % 2 == 0:
                    quest = create_main_quest(f"Main Quest {level}", level)
                    complete_quest(character, quest)
                
                # Add powerful items
                if level % 3 == 0:
                    item = create_powerful_item(f"Powerful Item {level}", level)
                    add_item_to_inventory(character, item)
                    # Equip if better
                    if should_equip_item(character, item):
                        equip_item(character, item)
            
            # Validate end-game state
            assert character.level == 50
            assert character.gold >= 10000
            assert len(character.quests_completed) >= 20
            assert len(character.inventory) >= 10
            
            execution_time = time.time() - start_time
            self.log_step("late_game", "passed", {
                "final_level": character.level,
                "gold": character.gold,
                "quests_completed": len(character.quests_completed),
                "inventory_size": len(character.inventory)
            }, execution_time)
            
            return game_state
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.log_step("late_game", "failed", str(e), execution_time)
            raise
    
    def test_final_boss_combat(self, game_state: GameState) -> GameState:
        """Test final boss combat - climax of user journey."""
        start_time = time.time()
        
        try:
            character = game_state.player
            
            # Create final boss
            final_boss = create_final_boss("Dark Lord", 50)
            
            # Test combat with final boss
            combat_result = resolve_combat(character, final_boss)
            
            # Validate victory
            assert combat_result['winner'] == 'player'
            assert combat_result['player_hp'] > 0
            assert combat_result['enemy_hp'] <= 0
            
            # Apply combat results
            character.hp = combat_result['player_hp']
            character.gold += combat_result['reward_gold']
            
            # Validate rewards
            assert combat_result['reward_xp'] >= 10000
            assert combat_result['reward_gold'] >= 5000
            assert len(combat_result['reward_items']) > 0
            
            execution_time = time.time() - start_time
            self.log_step("final_boss_combat", "passed", {
                "player_hp": combat_result['player_hp'],
                "max_hp": character.max_hp,
                "reward_xp": combat_result['reward_xp'],
                "reward_gold": combat_result['reward_gold'],
                "reward_items": len(combat_result['reward_items'])
            }, execution_time)
            
            return game_state
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.log_step("final_boss_combat", "failed", str(e), execution_time)
            raise
    
    def test_ending_achievement(self, game_state: GameState, ending_type: str = "warrior_victory") -> GameState:
        """Test ending achievement - conclusion of user journey."""
        start_time = time.time()
        
        try:
            character = game_state.player
            
            # Achieve ending based on character class and achievements
            ending = achieve_ending(character, ending_type)
            
            # Validate ending
            assert ending.type == ending_type
            assert ending.achievable == True
            assert ending.description is not None
            
            # Add ending to game state
            game_state.ending = ending
            
            execution_time = time.time() - start_time
            self.log_step("ending_achievement", "passed", {
                "ending_type": ending.type,
                "ending_description": ending.description,
                "final_character_level": character.level
            }, execution_time)
            
            return game_state
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.log_step("ending_achievement", "failed", str(e), execution_time)
            raise
    
    def test_save_load_journey(self, game_state: GameState) -> GameState:
        """Test save/load functionality throughout journey."""
        start_time = time.time()
        
        try:
            # Save game at final state
            save_data = save_game(game_state)
            
            # Load game in new state
            loaded_game_state = load_game(save_data)
            
            # Validate loaded game state
            assert loaded_game_state.player.name == game_state.player.name
            assert loaded_game_state.player.level == game_state.player.level
            assert loaded_game_state.player.gold == game_state.player.gold
            assert len(loaded_game_state.player.quests_completed) == len(game_state.player.quests_completed)
            assert len(loaded_game_state.player.inventory) == len(game_state.player.inventory)
            
            execution_time = time.time() - start_time
            self.log_step("save_load_journey", "passed", {
                "save_data_size": len(str(save_data)),
                "loaded_player_level": loaded_game_state.player.level,
                "save_load_success": True
            }, execution_time)
            
            return loaded_game_state
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.log_step("save_load_journey", "failed", str(e), execution_time)
            raise
    
    def run_complete_journey(self) -> Dict[str, Any]:
        """Run complete user journey from start to finish."""
        self.start_time = time.time()
        print("🎮 Starting Complete E2E User Journey...")
        
        try:
            # Step 1: Game startup
            game_state = self.test_game_startup()
            
            # Step 2: Character creation
            game_state = self.test_character_creation(game_state)
            
            # Step 3: Initial gameplay
            game_state = self.test_initial_gameplay(game_state)
            
            # Step 4: Character progression
            game_state = self.test_character_progression(game_state)
            
            # Step 5: Late game
            game_state = self.test_late_game(game_state)
            
            # Step 6: Final boss combat
            game_state = self.test_final_boss_combat(game_state)
            
            # Step 7: Ending achievement
            game_state = self.test_ending_achievement(game_state, "warrior_victory")
            
            # Step 8: Save/load journey
            game_state = self.test_save_load_journey(game_state)
            
            # Calculate metrics
            total_time = time.time() - self.start_time
            passed_steps = len([step for step in self.journey_log if step['status'] == 'passed'])
            total_steps = len(self.journey_log)
            
            return {
                'status': 'completed',
                'total_time': total_time,
                'total_steps': total_steps,
                'passed_steps': passed_steps,
                'failed_steps': 0,
                'success_rate': passed_steps / total_steps,
                'journey_log': self.journey_log,
                'final_game_state': game_state
            }
            
        except Exception as e:
            total_time = time.time() - self.start_time
            passed_steps = len([step for step in self.journey_log if step['status'] == 'passed'])
            total_steps = len(self.journey_log)
            
            return {
                'status': 'failed',
                'total_time': total_time,
                'total_steps': total_steps,
                'passed_steps': passed_steps,
                'failed_steps': total_steps - passed_steps,
                'success_rate': passed_steps / total_steps,
                'error': str(e),
                'journey_log': self.journey_log
            }


# Helper functions for E2E testing
def create_test_enemy(name: str, level: int) -> Enemy:
    """Create test enemy for E2E testing."""
    from core.models import EnemyType
    
    return Enemy(
        id=f"enemy_{name.lower()}",
        name=name,
        type=EnemyType.BEAST,
        level=level,
        hp=10 + (level * 5),
        max_hp=10 + (level * 5),
        attack_power=5 + (level * 2),
        defense=2 + level,
        abilities=["Attack", "Bite"],
        reward_xp=50 + (level * 10),
        reward_gold=25 + (level * 5),
        reward_items=[],
        boss=False
    )


def create_test_quest(name: str, difficulty: int) -> Quest:
    """Create test quest for E2E testing."""
    return Quest(
        id=f"quest_{name.lower().replace(' ', '_')}",
        name=name,
        description=f"Complete {name} task",
        type="side_quest",
        difficulty="easy" if difficulty < 10 else "medium",
        giver="Quest_Giver",
        location="Town",
        objectives=[{
            'description': f"Complete {name}",
            'completed': True
        }],
        rewards={
            'xp': 100 + (difficulty * 10),
            'gold': 50 + (difficulty * 5),
            'items': []
        },
        status="completed"
    )


def create_main_quest(name: str, level: int) -> Quest:
    """Create main quest for E2E testing."""
    return Quest(
        id=f"main_quest_{name.lower().replace(' ', '_')}",
        name=name,
        description=f"Complete main quest: {name}",
        type="main_quest",
        difficulty="hard" if level > 30 else "medium",
        giver="Main_Quest_Giver",
        location="Castle",
        objectives=[{
            'description': f"Complete main quest: {name}",
            'completed': True
        }],
        rewards={
            'xp': 500 + (level * 20),
            'gold': 250 + (level * 10),
            'items': [f"Main_Reward_{level}"]
        },
        status="completed"
    )


def create_test_item(name: str, level: int) -> Item:
    """Create test item for E2E testing."""
    from core.models import ItemType, ItemRarity
    
    return Item(
        id=f"item_{name.lower().replace(' ', '_')}",
        name=name,
        type=ItemType.ACCESSORY,
        rarity=ItemRarity.UNCOMMON if level < 20 else ItemRarity.RARE,
        value=50 + (level * 10),
        stats_mod={
            'strength': 1 if level % 2 == 0 else 0,
            'dexterity': 1 if level % 3 == 0 else 0
        },
        abilities=[],
        description=f"Test item for level {level}",
        equippable=True,
        consumable=False
    )


def create_powerful_item(name: str, level: int) -> Item:
    """Create powerful item for E2E testing."""
    from core.models import ItemType, ItemRarity
    
    return Item(
        id=f"powerful_item_{name.lower().replace(' ', '_')}",
        name=name,
        type=ItemType.WEAPON if level % 2 == 0 else ItemType.ARMOR,
        rarity=ItemRarity.LEGENDARY,
        value=1000 + (level * 50),
        stats_mod={
            'strength': 5 if level % 2 == 0 else 0,
            'dexterity': 3,
            'constitution': 2
        },
        abilities=["Power Strike"],
        description=f"Powerful item for level {level}",
        equippable=True,
        consumable=False
    )


def create_final_boss(name: str, level: int) -> Enemy:
    """Create final boss for E2E testing."""
    from core.models import EnemyType
    
    return Enemy(
        id="final_boss",
        name=name,
        type=EnemyType.DEMON,
        level=level,
        hp=1000,
        max_hp=1000,
        attack_power=100,
        defense=50,
        abilities=["Attack", "Dark Strike", "Ultimate Attack", "Summon Minions"],
        reward_xp=10000,
        reward_gold=5000,
        reward_items=["Legendary_Sword", "Boss_Armor"],
        boss=True
    )


def achieve_ending(character: Character, ending_type: str) -> Dict[str, Any]:
    """Achieve specific ending based on character and achievements."""
    
    # Define ending based on character class and achievements
    endings = {
        "warrior_victory": {
            "type": "warrior_victory",
            "description": "The mighty warrior has defeated the Dark Lord and saved the kingdom!",
            "achievable": True,
            "requirements": {
                "class": "warrior",
                "level": 50,
                "final_boss_defeated": True
            }
        },
        "ultimate_hero": {
            "type": "ultimate_hero",
            "description": "The ultimate hero has achieved all possible victories!",
            "achievable": True,
            "requirements": {
                "level": 50,
                "final_boss_defeated": True,
                "all_main_quests_completed": True
            }
        }
    }
    
    return endings.get(ending_type, {
        "type": "unknown",
        "description": "Unknown ending achieved.",
        "achievable": False
    })


def should_equip_item(character: Character, item: Item) -> bool:
    """Determine if character should equip item."""
    # Simple logic: equip if item has stats and character doesn't have better
    if item.stats_mod and item.equippable:
        return True
    return False


def get_experience_for_level(level: int) -> int:
    """Get experience needed for level."""
    import math
    return int(100 * math.pow(level, 1.5))


# Pytest test functions
def test_complete_user_journey():
    """Test complete user journey from start to finish."""
    tester = E2EJourneyTester()
    
    result = tester.run_complete_journey()
    
    # Validate journey completion
    assert result['status'] == 'completed', f"Journey failed: {result.get('error', 'Unknown error')}"
    assert result['success_rate'] == 1.0, f"Journey success rate: {result['success_rate']}"
    assert result['total_steps'] >= 8, f"Expected at least 8 steps, got {result['total_steps']}"
    
    # Validate final state
    game_state = result['final_game_state']
    assert game_state.player.level == 50
    assert game_state.player.gold >= 10000
    assert game_state.ending is not None
    assert game_state.ending.achievable == True
    
    print(f"✅ Complete user journey passed! ({result['total_time']:.2f}s)")


def test_performance_requirements():
    """Test that E2E journey meets performance requirements."""
    from core.constants import PERFORMANCE_CONFIG
    
    tester = E2EJourneyTester()
    
    # Record start time
    start_time = time.time()
    
    result = tester.run_complete_journey()
    
    # Record end time
    end_time = time.time()
    total_execution_time = end_time - start_time
    
    # Validate performance requirements
    max_total_time = PERFORMANCE_CONFIG['max_test_execution_time'] * 10  # Allow 10x longer for E2E
    assert total_execution_time < max_total_time, f"E2E journey took too long: {total_execution_time}s > {max_total_time}s"
    
    print(f"✅ Performance requirements met! ({total_execution_time:.2f}s < {max_total_time}s)")


def test_save_load_functionality():
    """Test save/load functionality works throughout the journey."""
    tester = E2EJourneyTester()
    
    # Run journey up to final state
    game_state = tester.test_game_startup()
    game_state = tester.test_character_creation(game_state)
    game_state = tester.test_character_progression(game_state)
    
    # Save at multiple points
    save_points = []
    for level in [10, 15, 20, 25]:
        # Level up to save point
        while game_state.player.level < level:
            exp_needed = get_experience_for_level(level)
            game_state.player = add_experience(game_state.player, exp_needed)
            game_state.player = level_up_character(game_state.player)
        
        # Save game
        save_data = save_game(game_state)
        save_points.append({
            'level': level,
            'save_data': save_data
        })
    
    # Validate each save point can be loaded
    for save_point in save_points:
        loaded_game_state = load_game(save_point['save_data'])
        assert loaded_game_state.player.level == save_point['level']
        assert loaded_game_state.player.name == game_state.player.name
    
    print(f"✅ Save/load functionality validated at {len(save_points)} save points!")


if __name__ == "__main__":
    # Run complete journey test
    test_complete_user_journey()
    test_performance_requirements()
    test_save_load_functionality()
    
    print("🎮 All E2E journey tests passed!")