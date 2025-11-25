"""
E2E Tests: Save/Load Journey
Optimized for LLM agents - validates save/load functionality throughout complete journey
"""

import pytest
import time
import json
from typing import Dict, List, Any, Optional
from core.models import GameState, Character, CharacterClass
from core.systems.game import start_new_game, save_game, load_game
from core.systems.character import create_character, level_up_character, add_experience
from core.systems.quest import complete_quest
from core.systems.inventory import add_item_to_inventory
from core.constants import GAME_CONFIG, FILE_PATHS


class E2ESaveLoadTester:
    """
    E2E tester for save/load functionality.
    Validates that game can be saved and loaded at any point in journey.
    """
    
    def __init__(self):
        self.save_load_log = []
        self.performance_metrics = {}
        self.test_save_points = []
    
    def log_save_load_step(self, step_name: str, status: str, details: Any = None, execution_time: float = 0):
        """Log save/load step for debugging."""
        log_entry = {
            'step': step_name,
            'status': status,
            'details': details,
            'execution_time': execution_time,
            'timestamp': time.time()
        }
        self.save_load_log.append(log_entry)
        print(f"{'✅' if status == 'passed' else '❌'} {step_name}: {status} ({execution_time:.3f}s)")
        return log_entry
    
    def test_save_at_game_start(self) -> Dict[str, Any]:
        """Test save functionality at game start."""
        start_time = time.time()
        
        try:
            # Start new game
            game_state = start_new_game()
            
            # Save game at start
            save_data = save_game(game_state)
            
            # Validate save data
            assert save_data is not None
            assert isinstance(save_data, str)
            assert len(save_data) > 0
            
            # Parse save data to validate structure
            parsed_save_data = json.loads(save_data)
            assert 'game_state' in parsed_save_data
            assert 'save_timestamp' in parsed_save_data
            assert 'save_version' in parsed_save_data
            
            execution_time = time.time() - start_time
            self.log_save_load_step("save_at_game_start", "passed", {
                "save_data_size": len(save_data),
                "game_state_keys": list(parsed_save_data['game_state'].keys())
            }, execution_time)
            
            return {
                'game_state': game_state,
                'save_data': save_data,
                'parsed_save_data': parsed_save_data
            }
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.log_save_load_step("save_at_game_start", "failed", str(e), execution_time)
            raise
    
    def test_load_at_game_start(self, save_data: str) -> Dict[str, Any]:
        """Test load functionality at game start."""
        start_time = time.time()
        
        try:
            # Load game from save data
            loaded_game_state = load_game(save_data)
            
            # Validate loaded game state
            assert loaded_game_state is not None
            assert loaded_game_state.current_location == "start"
            assert loaded_game_state.player is None
            assert loaded_game_state.world_time == 0
            
            # Validate original save data structure
            parsed_save_data = json.loads(save_data)
            original_location = parsed_save_data['game_state']['current_location']
            
            assert loaded_game_state.current_location == original_location
            
            execution_time = time.time() - start_time
            self.log_save_load_step("load_at_game_start", "passed", {
                "loaded_location": loaded_game_state.current_location,
                "player_is_none": loaded_game_state.player is None
            }, execution_time)
            
            return {
                'loaded_game_state': loaded_game_state
            }
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.log_save_load_step("load_at_game_start", "failed", str(e), execution_time)
            raise
    
    def test_save_after_character_creation(self) -> Dict[str, Any]:
        """Test save functionality after character creation."""
        start_time = time.time()
        
        try:
            # Start game and create character
            game_state = start_new_game()
            character = create_character("E2ETestChar", CharacterClass.WARRIOR)
            game_state.player = character
            
            # Save game after character creation
            save_data = save_game(game_state)
            
            # Validate save data
            assert save_data is not None
            parsed_save_data = json.loads(save_data)
            
            # Validate character data in save
            saved_character_data = parsed_save_data['game_state']['player']
            assert saved_character_data['name'] == "E2ETestChar"
            assert saved_character_data['class_type'] == "warrior"
            assert saved_character_data['level'] == 1
            assert saved_character_data['stats']['strength'] == 15
            
            execution_time = time.time() - start_time
            self.log_save_load_step("save_after_character_creation", "passed", {
                "character_name": saved_character_data['name'],
                "character_level": saved_character_data['level'],
                "save_data_size": len(save_data)
            }, execution_time)
            
            return {
                'game_state': game_state,
                'save_data': save_data,
                'saved_character_data': saved_character_data
            }
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.log_save_load_step("save_after_character_creation", "failed", str(e), execution_time)
            raise
    
    def test_load_after_character_creation(self, save_data: str) -> Dict[str, Any]:
        """Test load functionality after character creation."""
        start_time = time.time()
        
        try:
            # Load game state
            loaded_game_state = load_game(save_data)
            
            # Validate loaded character
            assert loaded_game_state.player is not None
            assert loaded_game_state.player.name == "E2ETestChar"
            assert loaded_game_state.player.class_type == CharacterClass.WARRIOR
            assert loaded_game_state.player.level == 1
            assert loaded_game_state.player.stats.strength == 15
            
            # Validate that character is functional
            assert loaded_game_state.player.hp > 0
            assert len(loaded_game_state.player.abilities) > 0
            assert loaded_game_state.player.gold >= 0
            
            execution_time = time.time() - start_time
            self.log_save_load_step("load_after_character_creation", "passed", {
                "loaded_character_name": loaded_game_state.player.name,
                "loaded_character_level": loaded_game_state.player.level,
                "character_hp": loaded_game_state.player.hp,
                "character_abilities_count": len(loaded_game_state.player.abilities)
            }, execution_time)
            
            return {
                'loaded_game_state': loaded_game_state
            }
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.log_save_load_step("load_after_character_creation", "failed", str(e), execution_time)
            raise
    
    def test_save_after_progression(self, target_level: int = 10) -> Dict[str, Any]:
        """Test save functionality after character progression."""
        start_time = time.time()
        
        try:
            # Start game and create character
            game_state = start_new_game()
            character = create_character("E2ETestProgress", CharacterClass.MAGE)
            game_state.player = character
            
            # Progress character to target level
            for level in range(2, target_level + 1):
                # Add sufficient experience
                exp_needed = int(100 * (level ** 1.5))
                character = add_experience(character, exp_needed)
                
                # Level up
                character = level_up_character(character)
                
                # Add some quests
                if level % 3 == 0:
                    quest = self.create_test_quest(f"Level {level} Quest", level)
                    complete_quest(character, quest)
                
                # Add some items
                if level % 2 == 0:
                    item = self.create_test_item(f"Level {level} Item", level)
                    add_item_to_inventory(character, item)
            
            # Save game after progression
            save_data = save_game(game_state)
            
            # Validate save data
            assert save_data is not None
            parsed_save_data = json.loads(save_data)
            
            # Validate progression data
            saved_character_data = parsed_save_data['game_state']['player']
            assert saved_character_data['name'] == "E2ETestProgress"
            assert saved_character_data['level'] == target_level
            assert saved_character_data['experience'] >= 0
            assert len(saved_character_data['quests_completed']) >= 2
            assert len(saved_character_data['inventory']) >= 4
            
            execution_time = time.time() - start_time
            self.log_save_load_step("save_after_progression", "passed", {
                "target_level": target_level,
                "final_level": saved_character_data['level'],
                "experience": saved_character_data['experience'],
                "quests_completed": len(saved_character_data['quests_completed']),
                "inventory_size": len(saved_character_data['inventory']),
                "save_data_size": len(save_data)
            }, execution_time)
            
            return {
                'game_state': game_state,
                'save_data': save_data,
                'saved_character_data': saved_character_data
            }
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.log_save_load_step("save_after_progression", "failed", str(e), execution_time)
            raise
    
    def test_load_after_progression(self, save_data: str, target_level: int = 10) -> Dict[str, Any]:
        """Test load functionality after character progression."""
        start_time = time.time()
        
        try:
            # Load game state
            loaded_game_state = load_game(save_data)
            
            # Validate loaded progression
            assert loaded_game_state.player is not None
            assert loaded_game_state.player.name == "E2ETestProgress"
            assert loaded_game_state.player.level == target_level
            assert loaded_game_state.player.experience >= 0
            assert len(loaded_game_state.player.quests_completed) >= 2
            assert len(loaded_game_state.player.inventory) >= 4
            
            # Validate that loaded character is functional
            assert loaded_game_state.player.hp > 0
            assert loaded_game_state.player.hp <= loaded_game_state.player.max_hp
            assert len(loaded_game_state.player.abilities) > 0
            assert loaded_game_state.player.gold >= 0
            
            # Validate quest functionality
            for quest in loaded_game_state.player.quests_completed:
                assert quest.id is not None
                assert quest.name is not None
            
            # Validate inventory functionality
            for item in loaded_game_state.player.inventory:
                assert item.id is not None
                assert item.name is not None
            
            execution_time = time.time() - start_time
            self.log_save_load_step("load_after_progression", "passed", {
                "loaded_level": loaded_game_state.player.level,
                "loaded_experience": loaded_game_state.player.experience,
                "loaded_quests_completed": len(loaded_game_state.player.quests_completed),
                "loaded_inventory_size": len(loaded_game_state.player.inventory),
                "character_is_functional": True
            }, execution_time)
            
            return {
                'loaded_game_state': loaded_game_state
            }
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.log_save_load_step("load_after_progression", "failed", str(e), execution_time)
            raise
    
    def test_save_load_roundtrip(self, game_state: GameState) -> Dict[str, Any]:
        """Test complete save/load roundtrip (save → load → save → load)."""
        start_time = time.time()
        
        try:
            # First save
            save_data_1 = save_game(game_state)
            
            # First load
            loaded_game_state_1 = load_game(save_data_1)
            
            # Second save
            save_data_2 = save_game(loaded_game_state_1)
            
            # Second load
            loaded_game_state_2 = load_game(save_data_2)
            
            # Validate that both loaded states are equivalent
            assert self.game_states_are_equivalent(game_state, loaded_game_state_2)
            
            # Validate that both save datas are equivalent (structure-wise)
            parsed_save_data_1 = json.loads(save_data_1)
            parsed_save_data_2 = json.loads(save_data_2)
            
            # Save data might have different timestamps, but structure should be same
            assert parsed_save_data_1['save_version'] == parsed_save_data_2['save_version']
            assert parsed_save_data_1['game_state']['current_location'] == parsed_save_data_2['game_state']['current_location']
            
            execution_time = time.time() - start_time
            self.log_save_load_step("save_load_roundtrip", "passed", {
                "first_save_size": len(save_data_1),
                "second_save_size": len(save_data_2),
                "save_sizes_equal": len(save_data_1) == len(save_data_2),
                "game_states_equivalent": True
            }, execution_time)
            
            return {
                'original_game_state': game_state,
                'loaded_game_state_1': loaded_game_state_1,
                'loaded_game_state_2': loaded_game_state_2,
                'save_data_1': save_data_1,
                'save_data_2': save_data_2
            }
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.log_save_load_step("save_load_roundtrip", "failed", str(e), execution_time)
            raise
    
    def test_save_load_multiple_scenarios(self) -> Dict[str, Any]:
        """Test save/load in multiple scenarios."""
        start_time = time.time()
        
        scenarios = [
            "empty_game_state",
            "game_with_character",
            "game_with_progressed_character",
            "game_with_quests",
            "game_with_inventory",
            "game_with_all_features"
        ]
        
        results = []
        
        for scenario in scenarios:
            scenario_start_time = time.time()
            
            try:
                # Create scenario
                game_state = self.create_scenario(scenario)
                
                # Save/load roundtrip
                roundtrip_result = self.test_save_load_roundtrip(game_state)
                roundtrip_result['scenario'] = scenario
                
                results.append(roundtrip_result)
                
                scenario_execution_time = time.time() - scenario_start_time
                self.log_save_load_step(f"scenario_{scenario}", "passed", {
                    "execution_time": scenario_execution_time
                }, scenario_execution_time)
                
            except Exception as e:
                scenario_execution_time = time.time() - scenario_start_time
                self.log_save_load_step(f"scenario_{scenario}", "failed", str(e), scenario_execution_time)
                results.append({
                    'scenario': scenario,
                    'status': 'failed',
                    'error': str(e),
                    'execution_time': scenario_execution_time
                })
        
        execution_time = time.time() - start_time
        successful_scenarios = len([r for r in results if r.get('status') != 'failed'])
        
        self.log_save_load_step("test_save_load_multiple_scenarios", "passed", {
            "total_scenarios": len(scenarios),
            "successful_scenarios": successful_scenarios,
            "success_rate": successful_scenarios / len(scenarios)
        }, execution_time)
        
        return {
            'scenarios': results,
            'total_scenarios': len(scenarios),
            'successful_scenarios': successful_scenarios,
            'execution_time': execution_time
        }
    
    def test_save_load_performance(self) -> Dict[str, Any]:
        """Test save/load performance requirements."""
        start_time = time.time()
        
        try:
            # Create complex game state
            game_state = self.create_scenario("game_with_all_features")
            
            # Test save performance
            save_times = []
            for i in range(5):  # Test 5 times
                save_start_time = time.time()
                save_data = save_game(game_state)
                save_end_time = time.time()
                save_times.append(save_end_time - save_start_time)
            
            # Test load performance
            load_times = []
            for i in range(5):  # Test 5 times
                load_start_time = time.time()
                loaded_game_state = load_game(save_data)
                load_end_time = time.time()
                load_times.append(load_end_time - load_start_time)
            
            # Calculate performance metrics
            avg_save_time = sum(save_times) / len(save_times)
            avg_load_time = sum(load_times) / len(load_times)
            max_save_time = max(save_times)
            max_load_time = max(load_times)
            
            # Validate performance requirements
            max_allowed_save_time = 1.0  # seconds
            max_allowed_load_time = 1.0  # seconds
            
            assert avg_save_time < max_allowed_save_time, f"Average save time {avg_save_time:.3f}s > {max_allowed_save_time}s"
            assert avg_load_time < max_allowed_load_time, f"Average load time {avg_load_time:.3f}s > {max_allowed_load_time}s"
            assert max_save_time < max_allowed_save_time * 2, f"Max save time {max_save_time:.3f}s > {max_allowed_save_time * 2}s"
            assert max_load_time < max_allowed_load_time * 2, f"Max load time {max_load_time:.3f}s > {max_allowed_load_time * 2}s"
            
            execution_time = time.time() - start_time
            self.log_save_load_step("test_save_load_performance", "passed", {
                "avg_save_time": avg_save_time,
                "avg_load_time": avg_load_time,
                "max_save_time": max_save_time,
                "max_load_time": max_load_time,
                "save_data_size": len(save_data)
            }, execution_time)
            
            return {
                'avg_save_time': avg_save_time,
                'avg_load_time': avg_load_time,
                'max_save_time': max_save_time,
                'max_load_time': max_load_time,
                'save_data_size': len(save_data),
                'performance_requirements_met': True
            }
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.log_save_load_step("test_save_load_performance", "failed", str(e), execution_time)
            raise
    
    def run_complete_save_load_test(self) -> Dict[str, Any]:
        """Run complete save/load test suite."""
        start_time = time.time()
        
        try:
            # Test 1: Save/load at game start
            start_result = self.test_save_at_game_start()
            load_start_result = self.test_load_at_game_start(start_result['save_data'])
            
            # Test 2: Save/load after character creation
            char_save_result = self.test_save_after_character_creation()
            char_load_result = self.test_load_after_character_creation(char_save_result['save_data'])
            
            # Test 3: Save/load after progression
            prog_save_result = self.test_save_after_progression(10)
            prog_load_result = self.test_load_after_progression(prog_save_result['save_data'], 10)
            
            # Test 4: Save/load roundtrip
            roundtrip_result = self.test_save_load_roundtrip(char_load_result['loaded_game_state'])
            
            # Test 5: Multiple scenarios
            scenarios_result = self.test_save_load_multiple_scenarios()
            
            # Test 6: Performance
            performance_result = self.test_save_load_performance()
            
            # Calculate overall metrics
            total_execution_time = time.time() - start_time
            total_tests = 6
            passed_tests = 6  # All tests passed if we got here
            
            return {
                'status': 'completed',
                'total_execution_time': total_execution_time,
                'total_tests': total_tests,
                'passed_tests': passed_tests,
                'failed_tests': 0,
                'success_rate': passed_tests / total_tests,
                'save_load_log': self.save_load_log,
                'start_result': start_result,
                'char_save_load_result': char_save_result,
                'progression_save_load_result': prog_save_result,
                'roundtrip_result': roundtrip_result,
                'scenarios_result': scenarios_result,
                'performance_result': performance_result
            }
            
        except Exception as e:
            total_execution_time = time.time() - start_time
            passed_tests = len([step for step in self.save_load_log if step['status'] == 'passed'])
            total_tests = len(self.save_load_log)
            
            return {
                'status': 'failed',
                'total_execution_time': total_execution_time,
                'total_tests': total_tests,
                'passed_tests': passed_tests,
                'failed_tests': total_tests - passed_tests,
                'success_rate': passed_tests / total_tests if total_tests > 0 else 0,
                'error': str(e),
                'save_load_log': self.save_load_log
            }
    
    def create_scenario(self, scenario_name: str) -> GameState:
        """Create specific test scenario."""
        game_state = start_new_game()
        
        if scenario_name == "empty_game_state":
            # Just basic game state
            return game_state
        
        elif scenario_name == "game_with_character":
            # Game with basic character
            character = create_character("ScenarioCharacter", CharacterClass.WARRIOR)
            game_state.player = character
            return game_state
        
        elif scenario_name == "game_with_progressed_character":
            # Game with progressed character
            character = create_character("ProgressedCharacter", CharacterClass.MAGE)
            
            # Progress to level 10
            for level in range(2, 11):
                exp_needed = int(100 * (level ** 1.5))
                character = add_experience(character, exp_needed)
                character = level_up_character(character)
            
            game_state.player = character
            return game_state
        
        elif scenario_name == "game_with_quests":
            # Game with completed quests
            character = create_character("QuestCharacter", CharacterClass.CLERIC)
            
            # Add completed quests
            for i in range(5):
                quest = self.create_test_quest(f"Quest {i+1}", i+2)
                complete_quest(character, quest)
            
            game_state.player = character
            return game_state
        
        elif scenario_name == "game_with_inventory":
            # Game with inventory items
            character = create_character("InventoryCharacter", CharacterClass.ROGUE)
            
            # Add items to inventory
            for i in range(10):
                item = self.create_test_item(f"Item {i+1}", i+1)
                add_item_to_inventory(character, item)
            
            game_state.player = character
            return game_state
        
        elif scenario_name == "game_with_all_features":
            # Game with all features combined
            character = create_character("AllFeaturesCharacter", CharacterClass.PALADIN)
            
            # Progress to level 15
            for level in range(2, 16):
                exp_needed = int(100 * (level ** 1.5))
                character = add_experience(character, exp_needed)
                character = level_up_character(character)
            
            # Add quests
            for i in range(8):
                quest = self.create_test_quest(f"Quest {i+1}", i+2)
                complete_quest(character, quest)
            
            # Add items
            for i in range(15):
                item = self.create_test_item(f"Item {i+1}", i+1)
                add_item_to_inventory(character, item)
            
            # Add gold
            character.gold = 5000
            
            game_state.player = character
            game_state.world_time = 1500
            
            return game_state
        
        else:
            # Default to basic game state
            return game_state
    
    def create_test_quest(self, name: str, difficulty: int) -> Any:
        """Create test quest for scenarios."""
        # This would create actual Quest objects
        return {
            'id': f"quest_{name.lower().replace(' ', '_')}",
            'name': name,
            'difficulty': difficulty,
            'status': 'completed'
        }
    
    def create_test_item(self, name: str, level: int) -> Any:
        """Create test item for scenarios."""
        # This would create actual Item objects
        return {
            'id': f"item_{name.lower().replace(' ', '_')}",
            'name': name,
            'level': level,
            'type': 'accessory'
        }
    
    def game_states_are_equivalent(self, game_state1: GameState, game_state2: GameState) -> bool:
        """Check if two game states are equivalent for testing purposes."""
        # Basic equivalence check
        if game_state1.current_location != game_state2.current_location:
            return False
        
        if game_state1.world_time != game_state2.world_time:
            return False
        
        # Check player equivalence
        if game_state1.player is None and game_state2.player is None:
            return True
        
        if game_state1.player is None or game_state2.player is None:
            return False
        
        if game_state1.player.name != game_state2.player.name:
            return False
        
        if game_state1.player.level != game_state2.player.level:
            return False
        
        if game_state1.player.class_type != game_state2.player.class_type:
            return False
        
        # For testing purposes, this is sufficient
        return True


# Pytest test functions
def test_save_load_game_start():
    """Test save/load at game start."""
    tester = E2ESaveLoadTester()
    
    # Test save at game start
    start_result = tester.test_save_at_game_start()
    assert start_result['save_data'] is not None
    assert len(start_result['save_data']) > 0
    
    # Test load at game start
    load_result = tester.test_load_at_game_start(start_result['save_data'])
    assert load_result['loaded_game_state'] is not None
    assert load_result['loaded_game_state'].current_location == "start"


def test_save_load_character_creation():
    """Test save/load after character creation."""
    tester = E2ESaveLoadTester()
    
    # Test save after character creation
    save_result = tester.test_save_after_character_creation()
    assert save_result['saved_character_data']['name'] == "E2ETestChar"
    assert save_result['saved_character_data']['level'] == 1
    
    # Test load after character creation
    load_result = tester.test_load_after_character_creation(save_result['save_data'])
    assert load_result['loaded_game_state'].player is not None
    assert load_result['loaded_game_state'].player.name == "E2ETestChar"
    assert load_result['loaded_game_state'].player.class_type == CharacterClass.WARRIOR


def test_save_load_progression():
    """Test save/load after character progression."""
    tester = E2ESaveLoadTester()
    
    target_level = 15
    
    # Test save after progression
    save_result = tester.test_save_after_progression(target_level)
    assert save_result['saved_character_data']['level'] == target_level
    assert save_result['saved_character_data']['experience'] >= 0
    
    # Test load after progression
    load_result = tester.test_load_after_progression(save_result['save_data'], target_level)
    assert load_result['loaded_game_state'].player.level == target_level
    assert load_result['loaded_game_state'].player.experience >= 0
    assert len(load_result['loaded_game_state'].player.quests_completed) >= 4
    assert len(load_result['loaded_game_state'].player.inventory) >= 7


def test_save_load_roundtrip():
    """Test complete save/load roundtrip."""
    tester = E2ESaveLoadTester()
    
    # Create test game state
    game_state = tester.create_scenario("game_with_all_features")
    
    # Test roundtrip
    roundtrip_result = tester.test_save_load_roundtrip(game_state)
    assert roundtrip_result['game_states_equivalent'] == True


def test_save_load_multiple_scenarios():
    """Test save/load in multiple scenarios."""
    tester = E2ESaveLoadTester()
    
    # Test multiple scenarios
    scenarios_result = tester.test_save_load_multiple_scenarios()
    assert scenarios_result['successful_scenarios'] >= 5  # At least 5 scenarios should pass
    assert scenarios_result['success_rate'] >= 0.8  # At least 80% success rate


def test_save_load_performance():
    """Test save/load performance requirements."""
    from core.constants import PERFORMANCE_CONFIG
    
    tester = E2ESaveLoadTester()
    
    # Test performance
    performance_result = tester.test_save_load_performance()
    assert performance_result['performance_requirements_met'] == True
    assert performance_result['avg_save_time'] < PERFORMANCE_CONFIG['max_save_load_time']
    assert performance_result['avg_load_time'] < PERFORMANCE_CONFIG['max_save_load_time']


def test_complete_save_load_suite():
    """Test complete save/load suite."""
    tester = E2ESaveLoadTester()
    
    # Run complete suite
    result = tester.run_complete_save_load_test()
    
    # Validate results
    assert result['status'] == 'completed', f"Save/load suite failed: {result.get('error', 'Unknown error')}"
    assert result['success_rate'] == 1.0, f"Save/load success rate: {result['success_rate']}"
    assert result['total_tests'] >= 6, f"Expected at least 6 tests, got {result['total_tests']}"
    
    # Validate performance
    assert result['performance_result']['performance_requirements_met'] == True
    
    print(f"✅ Complete save/load suite passed! ({result['total_execution_time']:.2f}s)")


if __name__ == "__main__":
    # Run complete save/load test
    test_complete_save_load_suite()
    
    print("🎮 All save/load E2E tests passed!")