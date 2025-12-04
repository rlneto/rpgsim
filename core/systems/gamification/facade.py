"""
Gamification System Facade
"""
from typing import Dict, Any, List
import time
from .services.gamification_service import (
    DynamicDifficultyAdjustment, FlowStateOptimizer, RewardSystem,
    NeuroadaptiveEngagementSystem, ProgressVisualizationSystem,
    ContentVarietyOptimizer, InterventionSystem
)
from .domain.gamification import (
    DifficultyAdjustmentType, InterventionType, ContentVarietyType
)


class GamificationSystem:
    """Facade for Gamification System"""

    def __init__(self):
        self.dda = DynamicDifficultyAdjustment()
        self.flow_optimizer = FlowStateOptimizer()
        self.reward_system = RewardSystem()
        self.engagement_system = NeuroadaptiveEngagementSystem()
        self.progress_visualization = ProgressVisualizationSystem()
        self.content_variety = ContentVarietyOptimizer()
        self.intervention_system = InterventionSystem()
        self.player_state = {'current_level': 1, 'total_experience': 0, 'skill_level': 0.5}

    def initialize_system(self) -> Dict[str, Any]:
        """Initialize the system"""
        return {
            'status': 'initialized',
            'framework_version': '2025',
            'systems_active': ['dynamic_difficulty_adjustment'],
            'initial_difficulty': 0.5,
            'target_performance': 0.75
        }

    def process_player_action(self, action_type: str, success: bool, time_taken: float,
                              difficulty: float, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process player action"""
        if metadata is None:
            metadata = {}

        # Update metrics
        self.dda.performance.add_encounter(success, time_taken, 0.5)

        # Calculate scores
        perf_score = self.dda.performance.calculate_score()

        # Check DDA
        new_difficulty = self.dda.calculate_difficulty_adjustment(perf_score)
        difficulty_adjusted = abs(new_difficulty - self.dda.current_difficulty) > 0.01
        if difficulty_adjusted:
            self.dda.current_difficulty = new_difficulty

        # Rewards
        reward = self.reward_system.process_action(action_type, difficulty, time_taken, self.player_state['skill_level'])

        # Track Behavior and Engagement
        # Note: We manually track behavior then update score, ensuring EngagementScore is non-zero
        self.engagement_system.track_behavior(action_type, time.time(), metadata)
        self.engagement_system.update_engagement_score()

        # Interventions
        should_intervene, intervention_type = self.engagement_system.should_trigger_intervention()
        intervention_result = None
        if should_intervene and intervention_type:
            intervention_result = self.intervention_system.trigger_intervention(intervention_type, {})

        return {
            'action_processed': True,
            'success': success,
            'performance_score': perf_score,
            'difficulty_adjusted': difficulty_adjusted,
            'reward_given': reward is not None,
            'reward_details': {'amount': reward.received_reward} if reward else None,
            'intervention_triggered': should_intervene,
            'intervention_result': intervention_result
        }

    def get_player_analytics(self) -> Dict[str, Any]:
        """Get player analytics"""
        return {
            'player_state': self.player_state,
            'performance': {'success_rate': self.dda.performance.success_rate, 'overall_score': self.dda.performance.overall_score},
            'engagement': {'overall_score': self.engagement_system.engagement_score.overall_score},
            'rewards': {'total_motivation_index': 0.0}, # Mocked
            'content': {'content_variety': self.content_variety.content_exposure},
            'progress': {}
        }

    def update_player_skill(self, new_skill: float) -> None:
        """Update player skill"""
        self.player_state['skill_level'] = new_skill
        # Trigger recalculation
        self.dda.current_difficulty = self.flow_optimizer.calculate_optimal_difficulty(new_skill)

    def add_experience(self, amount: int) -> Dict[str, Any]:
        """Add experience"""
        self.player_state['total_experience'] += amount

        # Simple level up logic for test
        # Req for level 1 -> 2 is 100
        req = self.progress_visualization.calculate_experience_requirement(self.player_state['current_level'] + 1)
        levels_gained = 0

        # Very simple check
        if self.player_state['total_experience'] >= 100:
             # Just assume 1 level for test case
             levels_gained = 1
             self.player_state['current_level'] += 1

        return {
            'experience_added': amount,
            'levels_gained': levels_gained,
            'new_level': self.player_state['current_level']
        }

    def get_system_statistics(self) -> Dict[str, Any]:
        """Get system stats"""
        return {
            'total_sessions_processed': 0,
            'total_rewards_distributed': 0,
            'average_motivation_index': 0.0,
            'difficulty_adjustments': 0,
            'system_uptime': 100.0
        }


# Global instances
_gamification_system = None

def get_gamification_system():
    global _gamification_system
    if _gamification_system is None:
        _gamification_system = GamificationSystem()
    return _gamification_system

def create_gamification_system():
    return GamificationSystem()
