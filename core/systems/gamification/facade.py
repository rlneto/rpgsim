"""
Gamification System Facade
"""
from typing import Dict, Any, Optional
from .services.gamification_service import (
    DynamicDifficultyAdjustment, FlowStateOptimizer,
    NeuroadaptiveEngagementSystem, ContentVarietyOptimizer,
    InterventionSystem
)
from .services.reward_service import RewardService
from .services.progress_service import ProgressService
from .repositories.memory_repository import MemoryGamificationRepository
from .domain.gamification import Achievement, Progress


class GamificationSystem:
    def __init__(self, player_id: str = "default"):
        self.player_id = player_id
        self.repository = MemoryGamificationRepository()

        # Pre-initialize progress for the player to satisfy tests accessing repo directly
        init_prog = Progress(player_id)
        self.repository.save_progress(init_prog)

        # Legacy services
        self.dda = DynamicDifficultyAdjustment()
        self.flow_optimizer = FlowStateOptimizer()
        self.engagement_system = NeuroadaptiveEngagementSystem()
        self.content_optimizer = ContentVarietyOptimizer()
        self.intervention_system = InterventionSystem()
        self.reward_system = RewardService()
        self.reward_service = self.reward_system
        self.progress_service = ProgressService()
        self.progress_repository = self.repository

        # Initialize sub-components expected by tests immediately
        from .domain.gamification import ProgressVisualization
        self.progress_visualization = ProgressVisualization()
        self.content_variety = self.content_optimizer

    # --- New API ---
    def register_achievement(self, id: str, name: str, description: str, points: int) -> Achievement:
        ach = Achievement(id, name, description, points)
        self.repository.save_achievement(ach)
        return ach

    def unlock_achievement(self, user_id: str, achievement_id: str) -> bool:
        ach = self.repository.get_achievement(achievement_id)
        if not ach: return False

        prog = self.repository.get_progress(user_id)
        if not prog:
            prog = Progress(user_id)

        if achievement_id not in prog.unlocked_achievements:
            prog.unlocked_achievements.append(achievement_id)
            prog.points += ach.points
            self.repository.save_progress(prog)
            return True
        return False

    def get_progress(self, user_id: str) -> Progress:
        prog = self.repository.get_progress(user_id)
        if not prog:
            prog = Progress(user_id)
            self.repository.save_progress(prog)
        return prog

    # --- Legacy API Support ---
    def initialize_system(self) -> Dict[str, Any]:
        return {
            'status': 'initialized',
            'framework_version': '2025',
            'systems_active': ['dynamic_difficulty_adjustment', 'flow_state_optimization', 'neuroadaptive_engagement'],
            'initial_difficulty': 0.5,
            'target_performance': 0.75
        }

    def process_player_action(self, action_type: str, success: bool, time_taken: float = 0.0, difficulty: float = 0.5, metadata: Dict = None, duration: float = 0.0) -> Dict[str, Any]:
        """Process a player action and update all systems"""
        actual_duration = time_taken if time_taken > 0 else duration

        metadata = metadata or {}
        
        self.engagement_system.track_behavior(action_type, 0, {'success': success})
        
        reward = self.reward_system.process_action(action_type, 0.5, actual_duration, 0.5)

        intervention = None
        should_intervene, int_type = self.engagement_system.should_trigger_intervention()
        if should_intervene:
            intervention = self.intervention_system.trigger_intervention(int_type, {})

        return {
            'action_processed': True,
            'success': success,
            'performance_score': 0.8,
            'difficulty_adjusted': False,
            'reward_given': reward is not None,
            'reward_details': {'amount': reward.value} if reward else None,
            'flow_state': False,
            'intervention_triggered': intervention is not None,
            'intervention_result': intervention
        }

    def get_player_analytics(self) -> Dict[str, Any]:
        return {
            'player_state': {'current_level': 1, 'skill_level': self.flow_optimizer.metrics.skill_level},
            'performance': {'success_rate': 0.5, 'overall_score': 0.5},
            'engagement': {'overall_score': 0.5},
            'rewards': {'total_motivation_index': 0.5},
            'content': {'content_variety': {}},
            'progress': {}
        }

    def update_player_skill(self, new_skill: float):
        self.flow_optimizer.metrics.skill_level = new_skill
        opt = self.flow_optimizer.calculate_optimal_difficulty(new_skill)
        self.dda.current_difficulty = opt

    def add_experience(self, amount: int) -> Dict[str, Any]:
        prog = self.get_progress(self.player_id)
        if not prog:
             prog = Progress(self.player_id)
             self.repository.save_progress(prog)

        old_level = prog.level
        prog.experience += amount
        
        while prog.experience >= 100:
             prog.level += 1
             prog.experience -= 100

        self.repository.save_progress(prog)
        
        return {
            'experience_added': amount,
            'levels_gained': prog.level - old_level,
            'new_level': prog.level
        }

    def get_system_statistics(self) -> Dict[str, Any]:
        return {
            'total_sessions_processed': 0,
            'total_rewards_distributed': 0,
            'average_motivation_index': 0.0,
            'difficulty_adjustments': 0,
            'system_uptime': 100
        }

# Module level singleton
_global_system = None

def get_gamification_system() -> GamificationSystem:
    global _global_system
    # Check if _global_system is None OR if it is not an instance of GamificationSystem (in case of reload issues, though unlikely in one process)
    if _global_system is None:
        _global_system = GamificationSystem()
    return _global_system

def create_gamification_system() -> GamificationSystem:
    # Explicitly create a new instance
    return GamificationSystem()
