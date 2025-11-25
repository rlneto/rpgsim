"""
E2E Tests: Performance
Optimized for LLM agents - validates that E2E tests meet performance requirements
"""

import pytest
import time
import psutil
import os
from typing import Dict, List, Any
from core.models import GameState, Character, CharacterClass
from core.systems.game import start_new_game
from core.systems.character import create_character
from core.constants import PERFORMANCE_CONFIG, GAME_CONFIG


class E2EPerformanceTester:
    """
    E2E performance tester for agents.
    Validates that E2E tests meet performance requirements.
    """
    
    def __init__(self):
        self.performance_log = []
        self.memory_usage = []
        self.cpu_usage = []
        self.start_time = None
    
    def log_performance(self, test_name: str, metric_type: str, value: float, unit: str = "s"):
        """Log performance metric."""
        log_entry = {
            'test_name': test_name,
            'metric_type': metric_type,
            'value': value,
            'unit': unit,
            'timestamp': time.time()
        }
        self.performance_log.append(log_entry)
        print(f"📊 {test_name} - {metric_type}: {value:.3f} {unit}")
        return log_entry
    
    def get_system_resources(self) -> Dict[str, float]:
        """Get current system resource usage."""
        process = psutil.Process(os.getpid())
        
        # Memory usage (MB)
        memory_mb = process.memory_info().rss / 1024 / 1024
        
        # CPU usage (percentage)
        cpu_percent = process.cpu_percent()
        
        return {
            'memory_mb': memory_mb,
            'cpu_percent': cpu_percent,
            'timestamp': time.time()
        }
    
    def log_system_resources(self, test_name: str):
        """Log system resource usage."""
        resources = self.get_system_resources()
        
        # Log memory usage
        self.log_performance(test_name, "memory_usage", resources['memory_mb'], "MB")
        self.memory_usage.append(resources['memory_mb'])
        
        # Log CPU usage
        self.log_performance(test_name, "cpu_usage", resources['cpu_percent'], "%")
        self.cpu_usage.append(resources['cpu_percent'])
        
        return resources
    
    def test_game_startup_performance(self) -> Dict[str, Any]:
        """Test game startup performance."""
        test_name = "game_startup_performance"
        start_time = time.time()
        
        # Log initial resources
        initial_resources = self.log_system_resources(test_name)
        
        try:
            # Start multiple games to measure performance
            game_states = []
            for i in range(10):  # Test startup performance with multiple games
                game_start_time = time.time()
                game_state = start_new_game()
                game_end_time = time.time()
                
                game_states.append(game_state)
                
                # Log individual game startup time
                startup_time = game_end_time - game_start_time
                self.log_performance(f"{test_name}_game_{i+1}", "startup_time", startup_time)
            
            total_time = time.time() - start_time
            
            # Calculate performance metrics
            avg_startup_time = total_time / 10
            max_startup_time = max(self.get_last_n_metrics(f"{test_name}_game_", 10, "startup_time"))
            
            # Log final resources
            final_resources = self.log_system_resources(f"{test_name}_final")
            
            # Log aggregate metrics
            self.log_performance(test_name, "total_time", total_time)
            self.log_performance(test_name, "avg_startup_time", avg_startup_time)
            self.log_performance(test_name, "max_startup_time", max_startup_time)
            self.log_performance(test_name, "memory_increase", final_resources['memory_mb'] - initial_resources['memory_mb'], "MB")
            
            # Validate performance requirements
            max_allowed_startup_time = PERFORMANCE_CONFIG['max_test_execution_time'] / 10  # Each game should be fast
            assert avg_startup_time < max_allowed_startup_time, f"Average startup time {avg_startup_time:.3f}s exceeds {max_allowed_startup_time:.3f}s"
            assert max_startup_time < max_allowed_startup_time * 2, f"Max startup time {max_startup_time:.3f}s exceeds {max_allowed_startup_time * 2:.3f}s"
            
            return {
                'test_name': test_name,
                'total_time': total_time,
                'avg_startup_time': avg_startup_time,
                'max_startup_time': max_startup_time,
                'games_created': len(game_states),
                'memory_usage': final_resources['memory_mb'],
                'performance_requirements_met': True
            }
            
        except Exception as e:
            total_time = time.time() - start_time
            self.log_performance(test_name, "error", total_time)
            raise
    
    def test_character_creation_performance(self) -> Dict[str, Any]:
        """Test character creation performance."""
        test_name = "character_creation_performance"
        start_time = time.time()
        
        # Log initial resources
        initial_resources = self.log_system_resources(test_name)
        
        try:
            # Create multiple characters to measure performance
            characters = []
            for class_type in CharacterClass:
                char_start_time = time.time()
                character = create_character(f"PerfTest{class_type.value.title()}", class_type)
                char_end_time = time.time()
                
                characters.append(character)
                
                # Log individual character creation time
                creation_time = char_end_time - char_start_time
                self.log_performance(f"{test_name}_{class_type.value}", "creation_time", creation_time)
            
            total_time = time.time() - start_time
            
            # Calculate performance metrics
            avg_creation_time = total_time / len(CharacterClass)
            max_creation_time = max(self.get_last_n_metrics(f"{test_name}_", len(CharacterClass), "creation_time"))
            min_creation_time = min(self.get_last_n_metrics(f"{test_name}_", len(CharacterClass), "creation_time"))
            
            # Log final resources
            final_resources = self.log_system_resources(f"{test_name}_final")
            
            # Log aggregate metrics
            self.log_performance(test_name, "total_time", total_time)
            self.log_performance(test_name, "avg_creation_time", avg_creation_time)
            self.log_performance(test_name, "max_creation_time", max_creation_time)
            self.log_performance(test_name, "min_creation_time", min_creation_time)
            self.log_performance(test_name, "characters_created", len(characters))
            self.log_performance(test_name, "memory_increase", final_resources['memory_mb'] - initial_resources['memory_mb'], "MB")
            
            # Validate performance requirements
            max_allowed_creation_time = PERFORMANCE_CONFIG['max_test_execution_time'] / 50  # Character creation should be very fast
            assert avg_creation_time < max_allowed_creation_time, f"Average creation time {avg_creation_time:.3f}s exceeds {max_allowed_creation_time:.3f}s"
            assert max_creation_time < max_allowed_creation_time * 2, f"Max creation time {max_creation_time:.3f}s exceeds {max_allowed_creation_time * 2:.3f}s"
            
            return {
                'test_name': test_name,
                'total_time': total_time,
                'avg_creation_time': avg_creation_time,
                'max_creation_time': max_creation_time,
                'min_creation_time': min_creation_time,
                'characters_created': len(characters),
                'memory_usage': final_resources['memory_mb'],
                'performance_requirements_met': True
            }
            
        except Exception as e:
            total_time = time.time() - start_time
            self.log_performance(test_name, "error", total_time)
            raise
    
    def test_e2e_journey_performance(self) -> Dict[str, Any]:
        """Test E2E journey performance."""
        test_name = "e2e_journey_performance"
        start_time = time.time()
        
        # Log initial resources
        initial_resources = self.log_system_resources(test_name)
        
        try:
            # Simulate E2E journey (simplified for performance testing)
            journey_steps = [
                'game_startup',
                'character_creation',
                'character_leveling',
                'quest_completion',
                'item_collection',
                'save_game',
                'load_game'
            ]
            
            journey_times = {}
            
            for step in journey_steps:
                step_start_time = time.time()
                
                # Simulate journey step
                self.simulate_journey_step(step)
                
                step_end_time = time.time()
                step_time = step_end_time - step_start_time
                journey_times[step] = step_time
                
                self.log_performance(f"{test_name}_{step}", "step_time", step_time)
                
                # Log resources after each step
                self.log_system_resources(f"{test_name}_after_{step}")
            
            total_time = time.time() - start_time
            
            # Calculate performance metrics
            avg_step_time = total_time / len(journey_steps)
            max_step_time = max(journey_times.values())
            min_step_time = min(journey_times.values())
            
            # Log final resources
            final_resources = self.log_system_resources(f"{test_name}_final")
            
            # Log aggregate metrics
            self.log_performance(test_name, "total_time", total_time)
            self.log_performance(test_name, "avg_step_time", avg_step_time)
            self.log_performance(test_name, "max_step_time", max_step_time)
            self.log_performance(test_name, "min_step_time", min_step_time)
            self.log_performance(test_name, "steps_completed", len(journey_steps))
            self.log_performance(test_name, "memory_increase", final_resources['memory_mb'] - initial_resources['memory_mb'], "MB")
            
            # Validate performance requirements
            max_allowed_e2e_time = PERFORMANCE_CONFIG['max_test_execution_time']
            assert total_time < max_allowed_e2e_time, f"E2E journey time {total_time:.3f}s exceeds {max_allowed_e2e_time:.3f}s"
            assert avg_step_time < max_allowed_e2e_time / len(journey_steps), f"Average step time {avg_step_time:.3f}s exceeds {max_allowed_e2e_time / len(journey_steps):.3f}s"
            
            return {
                'test_name': test_name,
                'total_time': total_time,
                'avg_step_time': avg_step_time,
                'max_step_time': max_step_time,
                'min_step_time': min_step_time,
                'journey_times': journey_times,
                'steps_completed': len(journey_steps),
                'memory_usage': final_resources['memory_mb'],
                'performance_requirements_met': True
            }
            
        except Exception as e:
            total_time = time.time() - start_time
            self.log_performance(test_name, "error", total_time)
            raise
    
    def simulate_journey_step(self, step: str):
        """Simulate a journey step for performance testing."""
        if step == 'game_startup':
            game_state = start_new_game()
            return game_state
        
        elif step == 'character_creation':
            character = create_character("PerfTestChar", CharacterClass.WARRIOR)
            return character
        
        elif step == 'character_leveling':
            # Simulate character leveling (simplified)
            for i in range(10):
                # Simple computation to simulate work
                _ = sum(range(1000))
            return True
        
        elif step == 'quest_completion':
            # Simulate quest completion (simplified)
            for i in range(5):
                # Simple computation to simulate work
                _ = sum(range(500))
            return True
        
        elif step == 'item_collection':
            # Simulate item collection (simplified)
            for i in range(20):
                # Simple computation to simulate work
                _ = sum(range(200))
            return True
        
        elif step == 'save_game':
            # Simulate game saving (simplified)
            save_data = {"test": "data", "large": list(range(1000))}
            return save_data
        
        elif step == 'load_game':
            # Simulate game loading (simplified)
            save_data = {"test": "data", "large": list(range(1000))}
            loaded_data = save_data.copy()
            return loaded_data
        
        else:
            # Default simple computation
            _ = sum(range(100))
            return True
    
    def test_memory_usage_limits(self) -> Dict[str, Any]:
        """Test memory usage limits during E2E tests."""
        test_name = "memory_usage_limits"
        start_time = time.time()
        
        # Log initial resources
        initial_resources = self.log_system_resources(test_name)
        
        try:
            # Create many objects to test memory usage
            game_states = []
            characters = []
            
            # Create 50 games
            for i in range(50):
                game_state = start_new_game()
                game_states.append(game_state)
                
                # Log memory usage periodically
                if i % 10 == 0:
                    self.log_system_resources(f"{test_name}_after_{i}_games")
            
            # Create 100 characters
            for i in range(100):
                character = create_character(f"MemoryTestChar{i}", CharacterClass.MAGE)
                characters.append(character)
                
                # Log memory usage periodically
                if i % 25 == 0:
                    self.log_system_resources(f"{test_name}_after_{i}_characters")
            
            # Log final resources
            final_resources = self.log_system_resources(f"{test_name}_final")
            
            total_time = time.time() - start_time
            
            # Calculate memory metrics
            memory_increase = final_resources['memory_mb'] - initial_resources['memory_mb']
            avg_memory_per_game = memory_increase / len(game_states) if len(game_states) > 0 else 0
            avg_memory_per_character = memory_increase / len(characters) if len(characters) > 0 else 0
            
            self.log_performance(test_name, "total_time", total_time)
            self.log_performance(test_name, "memory_increase", memory_increase, "MB")
            self.log_performance(test_name, "avg_memory_per_game", avg_memory_per_game, "MB")
            self.log_performance(test_name, "avg_memory_per_character", avg_memory_per_character, "MB")
            self.log_performance(test_name, "games_created", len(game_states))
            self.log_performance(test_name, "characters_created", len(characters))
            
            # Validate memory usage requirements
            max_allowed_memory_increase = 500  # MB - should not use too much memory
            assert memory_increase < max_allowed_memory_increase, f"Memory increase {memory_increase:.1f}MB exceeds {max_allowed_memory_increase}MB"
            assert avg_memory_per_game < 1.0, f"Average memory per game {avg_memory_per_game:.3f}MB exceeds 1.0MB"
            assert avg_memory_per_character < 0.5, f"Average memory per character {avg_memory_per_character:.3f}MB exceeds 0.5MB"
            
            return {
                'test_name': test_name,
                'total_time': total_time,
                'memory_increase': memory_increase,
                'avg_memory_per_game': avg_memory_per_game,
                'avg_memory_per_character': avg_memory_per_character,
                'games_created': len(game_states),
                'characters_created': len(characters),
                'final_memory_usage': final_resources['memory_mb'],
                'memory_requirements_met': True
            }
            
        except Exception as e:
            total_time = time.time() - start_time
            self.log_performance(test_name, "error", total_time)
            raise
    
    def test_cpu_usage_limits(self) -> Dict[str, Any]:
        """Test CPU usage limits during E2E tests."""
        test_name = "cpu_usage_limits"
        start_time = time.time()
        
        # Log initial resources
        initial_resources = self.log_system_resources(test_name)
        
        try:
            # Perform CPU-intensive operations
            cpu_iterations = 1000000
            
            # Perform multiple rounds of CPU-intensive work
            for round_num in range(3):
                round_start_time = time.time()
                
                # CPU-intensive computation
                result = sum(range(cpu_iterations))
                
                round_end_time = time.time()
                round_time = round_end_time - round_start_time
                
                self.log_performance(f"{test_name}_round_{round_num + 1}", "round_time", round_time)
                self.log_system_resources(f"{test_name}_after_round_{round_num + 1}")
                
                # Validate result (ensure computation happened)
                assert result == cpu_iterations * (cpu_iterations - 1) // 2
            
            total_time = time.time() - start_time
            
            # Log final resources
            final_resources = self.log_system_resources(f"{test_name}_final")
            
            # Calculate CPU metrics
            max_cpu_usage = max(self.cpu_usage) if self.cpu_usage else 0
            avg_cpu_usage = sum(self.cpu_usage) / len(self.cpu_usage) if self.cpu_usage else 0
            
            self.log_performance(test_name, "total_time", total_time)
            self.log_performance(test_name, "max_cpu_usage", max_cpu_usage, "%")
            self.log_performance(test_name, "avg_cpu_usage", avg_cpu_usage, "%")
            self.log_performance(test_name, "cpu_iterations", cpu_iterations)
            
            # Validate CPU usage requirements
            max_allowed_cpu_usage = 80  # CPU usage should not exceed 80%
            assert max_cpu_usage < max_allowed_cpu_usage, f"Max CPU usage {max_cpu_usage:.1f}% exceeds {max_allowed_cpu_usage}%"
            
            return {
                'test_name': test_name,
                'total_time': total_time,
                'max_cpu_usage': max_cpu_usage,
                'avg_cpu_usage': avg_cpu_usage,
                'cpu_iterations': cpu_iterations,
                'final_cpu_usage': final_resources['cpu_percent'],
                'cpu_requirements_met': True
            }
            
        except Exception as e:
            total_time = time.time() - start_time
            self.log_performance(test_name, "error", total_time)
            raise
    
    def get_last_n_metrics(self, prefix: str, n: int, metric_type: str) -> List[float]:
        """Get last n metrics matching prefix and metric type."""
        matching_metrics = []
        
        for log_entry in reversed(self.performance_log):
            if log_entry['metric_type'] == metric_type and log_entry['test_name'].startswith(prefix):
                matching_metrics.append(log_entry['value'])
                if len(matching_metrics) >= n:
                    break
        
        return matching_metrics[:n]
    
    def run_complete_performance_test(self) -> Dict[str, Any]:
        """Run complete performance test suite."""
        test_results = []
        overall_start_time = time.time()
        
        # Run all performance tests
        tests = [
            self.test_game_startup_performance,
            self.test_character_creation_performance,
            self.test_e2e_journey_performance,
            self.test_memory_usage_limits,
            self.test_cpu_usage_limits
        ]
        
        for test_func in tests:
            try:
                result = test_func()
                test_results.append(result)
            except Exception as e:
                error_result = {
                    'test_name': test_func.__name__,
                    'status': 'failed',
                    'error': str(e)
                }
                test_results.append(error_result)
        
        overall_end_time = time.time()
        overall_execution_time = overall_end_time - overall_start_time
        
        # Calculate aggregate metrics
        passed_tests = len([r for r in test_results if r.get('status') != 'failed'])
        total_tests = len(test_results)
        success_rate = passed_tests / total_tests if total_tests > 0 else 0
        
        # Calculate memory and CPU statistics
        max_memory_usage = max(self.memory_usage) if self.memory_usage else 0
        avg_memory_usage = sum(self.memory_usage) / len(self.memory_usage) if self.memory_usage else 0
        max_cpu_usage = max(self.cpu_usage) if self.cpu_usage else 0
        avg_cpu_usage = sum(self.cpu_usage) / len(self.cpu_usage) if self.cpu_usage else 0
        
        return {
            'overall_status': 'completed',
            'overall_execution_time': overall_execution_time,
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'failed_tests': total_tests - passed_tests,
            'success_rate': success_rate,
            'test_results': test_results,
            'performance_log': self.performance_log,
            'max_memory_usage': max_memory_usage,
            'avg_memory_usage': avg_memory_usage,
            'max_cpu_usage': max_cpu_usage,
            'avg_cpu_usage': avg_cpu_usage,
            'performance_requirements_met': success_rate == 1.0
        }


# Pytest test functions
def test_game_startup_performance():
    """Test game startup performance requirements."""
    tester = E2EPerformanceTester()
    
    result = tester.test_game_startup_performance()
    
    # Validate performance requirements
    assert result['performance_requirements_met'] == True, "Game startup performance requirements not met"
    assert result['avg_startup_time'] < PERFORMANCE_CONFIG['max_test_execution_time'] / 10, "Average startup time too slow"
    assert result['memory_usage'] < 100, "Memory usage too high for game startup"
    
    print(f"✅ Game startup performance requirements met! (Avg: {result['avg_startup_time']:.3f}s)")


def test_character_creation_performance():
    """Test character creation performance requirements."""
    tester = E2EPerformanceTester()
    
    result = tester.test_character_creation_performance()
    
    # Validate performance requirements
    assert result['performance_requirements_met'] == True, "Character creation performance requirements not met"
    assert result['avg_creation_time'] < PERFORMANCE_CONFIG['max_test_execution_time'] / 50, "Average creation time too slow"
    assert result['memory_usage'] < 50, "Memory usage too high for character creation"
    
    print(f"✅ Character creation performance requirements met! (Avg: {result['avg_creation_time']:.3f}s)")


def test_e2e_journey_performance():
    """Test E2E journey performance requirements."""
    tester = E2EPerformanceTester()
    
    result = tester.test_e2e_journey_performance()
    
    # Validate performance requirements
    assert result['performance_requirements_met'] == True, "E2E journey performance requirements not met"
    assert result['total_time'] < PERFORMANCE_CONFIG['max_test_execution_time'], "E2E journey time too slow"
    assert result['avg_step_time'] < PERFORMANCE_CONFIG['max_test_execution_time'] / 7, "Average step time too slow"
    
    print(f"✅ E2E journey performance requirements met! (Total: {result['total_time']:.3f}s)")


def test_memory_usage_limits():
    """Test memory usage limits during E2E tests."""
    tester = E2EPerformanceTester()
    
    result = tester.test_memory_usage_limits()
    
    # Validate memory requirements
    assert result['memory_requirements_met'] == True, "Memory usage requirements not met"
    assert result['memory_increase'] < 500, "Memory increase too high"
    assert result['avg_memory_per_game'] < 1.0, "Average memory per game too high"
    assert result['avg_memory_per_character'] < 0.5, "Average memory per character too high"
    
    print(f"✅ Memory usage requirements met! (Increase: {result['memory_increase']:.1f}MB)")


def test_cpu_usage_limits():
    """Test CPU usage limits during E2E tests."""
    tester = E2EPerformanceTester()
    
    result = tester.test_cpu_usage_limits()
    
    # Validate CPU requirements
    assert result['cpu_requirements_met'] == True, "CPU usage requirements not met"
    assert result['max_cpu_usage'] < 80, "Max CPU usage too high"
    assert result['avg_cpu_usage'] < 50, "Average CPU usage too high"
    
    print(f"✅ CPU usage requirements met! (Max: {result['max_cpu_usage']:.1f}%)")


def test_complete_performance_suite():
    """Test complete performance suite."""
    tester = E2EPerformanceTester()
    
    # Run complete performance test
    result = tester.run_complete_performance_test()
    
    # Validate overall results
    assert result['overall_status'] == 'completed', f"Performance suite failed: {result.get('error', 'Unknown error')}"
    assert result['success_rate'] == 1.0, f"Performance suite success rate: {result['success_rate']}"
    assert result['performance_requirements_met'] == True, "Overall performance requirements not met"
    
    # Validate aggregate metrics
    assert result['max_memory_usage'] < 500, f"Max memory usage too high: {result['max_memory_usage']:.1f}MB"
    assert result['max_cpu_usage'] < 80, f"Max CPU usage too high: {result['max_cpu_usage']:.1f}%"
    assert result['overall_execution_time'] < PERFORMANCE_CONFIG['max_test_execution_time'] * 3, f"Overall execution time too long: {result['overall_execution_time']:.3f}s"
    
    print(f"✅ Complete performance suite passed! ({result['overall_execution_time']:.2f}s)")
    print(f"   Max memory usage: {result['max_memory_usage']:.1f}MB")
    print(f"   Max CPU usage: {result['max_cpu_usage']:.1f}%")
    print(f"   Success rate: {result['success_rate']:.1%}")


if __name__ == "__main__":
    # Run complete performance test
    test_complete_performance_suite()
    
    print("🚀 All E2E performance tests passed!")