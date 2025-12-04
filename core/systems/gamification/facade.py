from collections import deque
import time
from typing import Any, Dict

from .services.gamification_service import (
    ContentVarietyOptimizer,
    DynamicDifficultyAdjustment,
    FlowStateOptimizer,
    InterventionSystem,
    NeuroadaptiveEngagementSystem,
)
from .domain.gamification import ContentVarietyType, Progress
from .services.progress_service import ProgressService
from .services.reward_service import RewardService
from .services.achievement_service import AchievementService
from .repositories.memory_repository import (
    MemoryAchievementRepository,
    MemoryBadgeRepository,
    MemoryProgressRepository,
    MemoryRewardRepository,
)


class GamificationSystem:
    def __init__(self, player_id: str):
        self.player_id = player_id
        self.dda = DynamicDifficultyAdjustment()
        self.flow_optimizer = FlowStateOptimizer()
        self.reward_system = RewardService()
        self.engagement_system = NeuroadaptiveEngagementSystem()
        self.progress_repository = MemoryProgressRepository()
        self.progress_visualization = ProgressService()
        self.content_variety = ContentVarietyOptimizer()
        self.intervention_system = InterventionSystem()
        self.achievement_repository = MemoryAchievementRepository()
        self.achievement_service = AchievementService(self.achievement_repository)
        self.badge_repository = MemoryBadgeRepository()
        self.reward_repository = MemoryRewardRepository()

        progress = self.progress_repository.get(self.player_id)
        if not progress:
            progress = Progress(player_id=self.player_id, level=1, experience=0)
            self.progress_repository.update(progress)

    def initialize_system(self) -> Dict[str, Any]:
        return {
            "status": "initialized",
            "framework_version": "2025",
            "systems_active": [
                "dynamic_difficulty_adjustment",
                "flow_state_optimization",
                "reinforcement_learning_rewards",
                "neuroadaptive_engagement",
                "progress_visualization",
                "content_variety_optimization",
            ],
            "initial_difficulty": self.dda.current_difficulty,
            "target_performance": self.dda.target_performance,
        }

    def process_player_action(
        self,
        action_type: str,
        success: bool,
        time_taken: int,
        difficulty: float = None,
        metadata: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        metadata = metadata or {}
        progress = self.progress_repository.get(self.player_id)
        if difficulty is None:
            difficulty = self.dda.current_difficulty
        self.engagement_system.track_behavior(
            action_type,
            time.time(),
            {
                **metadata,
                "success": success,
                "time_taken": time_taken,
                "difficulty": difficulty,
            },
        )
        self.dda.performance.add_encounter(success, time_taken, 0.5)
        performance_score = self.dda.performance.calculate_score()
        encounters = self.dda.performance.recent_encounters
        should_adjust, adjustment_amount = self.dda.should_apply_micro_adjustment(
            encounters
        )
        if should_adjust:
            new_difficulty = self.dda.apply_statistical_smoothing(
                self.dda.calculate_difficulty_adjustment(performance_score)
                + adjustment_amount
            )
        else:
            new_difficulty = self.dda.current_difficulty
        reward_event = self.reward_system.process_action(
            action_type,
            difficulty,
            time_taken,
            0.5,  # skill_level
        )
        if reward_event:
            self.reward_repository.add(reward_event)
        session_data = {
            "recent_actions": encounters[-5:],
            "last_action_time": time.time(),
            "frustration_level": 1.0
            - (performance_score * 0.7),  # motivation_level
        }
        if self.flow_optimizer.detect_flow_disruption(session_data):
            new_difficulty = self.flow_optimizer.auto_rebalance(new_difficulty)
        if "content_type" in metadata:
            content_type = ContentVarietyType(metadata["content_type"])
            self.content_variety.update_content_exposure(content_type)
        engagement_metrics = self.engagement_system.calculate_engagement_metrics()
        (
            should_intervene,
            intervention_type,
        ) = self.engagement_system.should_trigger_intervention()
        intervention_result = None
        if should_intervene:
            intervention_result = self.intervention_system.trigger_intervention(
                intervention_type,
                {
                    "player_performance": performance_score,
                    "engagement_level": engagement_metrics.get(
                        "session_duration", 0.5
                    ),
                    "current_difficulty": new_difficulty,
                    "player_preferences": {
                        "preferred_content": content_type.value
                        if "content_type" in metadata
                        else "combat"
                    },
                },
            )
        return {
            "action_processed": True,
            "success": success,
            "performance_score": performance_score,
            "difficulty_adjusted": new_difficulty != self.dda.current_difficulty,
            "new_difficulty": new_difficulty,
            "reward_given": reward_event is not None,
            "reward_details": {
                "amount": reward_event.received_reward if reward_event else 0,
                "motivation_index": reward_event.motivation_index
                if reward_event
                else 0,
            }
            if reward_event
            else None,
            "flow_disruption_detected": self.flow_optimizer.detect_flow_disruption(
                session_data
            ),
            "engagement_score": engagement_metrics,
            "intervention_triggered": should_intervene,
            "intervention_result": intervention_result,
        }

    def get_player_analytics(self) -> Dict[str, Any]:
        progress = self.progress_repository.get(self.player_id)
        engagement_metrics = self.engagement_system.calculate_engagement_metrics()
        churn_risk = self.engagement_system.predict_churn_risk()
        content_analysis = self.content_variety.get_content_variety_analysis()
        reward_analysis = self.reward_system.analyze_player_response()
        level_exp = self.progress_visualization.calculate_experience_requirement(
            progress.level
        )
        level_progress = self.progress_visualization.calculate_level_progress(
            progress.experience, level_exp
        )
        return {
            "player_state": {
                "current_level": progress.level,
                "total_experience": progress.experience,
                "skill_level": 0.5,
                "motivation_level": 0.7,
                "session_duration": 0,
                "actions_this_session": 0,
            },
            "performance": {
                "success_rate": self.dda.performance.success_rate,
                "time_efficiency": self.dda.performance.time_efficiency,
                "resource_efficiency": self.dda.performance.resource_efficiency,
                "overall_score": self.dda.performance.overall_score,
                "current_difficulty": self.dda.current_difficulty,
                "difficulty_history": list(self.dda.adjustment_history)[-10:],
            },
            "engagement": {
                "overall_score": self.engagement_system.engagement_score.overall_score,
                "engagement_level": self.engagement_system.engagement_score.engagement_level,
                "individual_metrics": engagement_metrics,
                "churn_risk": churn_risk,
                "intervention_history": list(
                    self.engagement_system.intervention_history
                )[-5:],
            },
            "rewards": {
                "total_motivation_index": self.reward_system.total_motivation_index,
                "player_sensitivity": self.reward_system.player_sensitivity,
                "reward_schedule_adjustments": reward_analysis.get(
                    "adjustments_needed", []
                ),
                "recent_rewards": len(self.reward_system.reward_history),
            },
            "content": {
                "content_variety": content_analysis,
                "recommendations": self.content_variety.recommend_content().value,
            },
            "progress": {
                "level_progress": level_progress,
                "next_level_requirement": self.progress_visualization.calculate_experience_requirement(
                    progress.level + 1
                ),
                "mastery_advancement": self.progress_visualization.calculate_mastery_advancement(
                    1
                ),
            },
        }

    def update_player_skill(self, new_skill_level: float) -> None:
        target_difficulty = self.flow_optimizer.calculate_optimal_difficulty(
            new_skill_level
        )
        self.dda.current_difficulty = target_difficulty

    def add_experience(self, exp_amount: int) -> Dict[str, Any]:
        progress = self.progress_repository.get(self.player_id)
        old_level = progress.level
        progress.experience += exp_amount
        required_exp = self.progress_visualization.calculate_experience_requirement(
            old_level
        )
        level_ups = 0
        while progress.experience >= required_exp:
            progress.experience -= required_exp
            level_ups += 1
            progress.level += 1
            required_exp = self.progress_visualization.calculate_experience_requirement(
                progress.level
            )
        self.progress_repository.update(progress)
        return {
            "experience_added": exp_amount,
            "old_level": old_level,
            "new_level": progress.level,
            "levels_gained": level_ups,
            "total_experience": progress.experience,
            "next_level_requirement": required_exp,
        }

    def get_system_statistics(self) -> Dict[str, Any]:
        return {
            "total_sessions_processed": len(
                self.engagement_system.intervention_history
            ),
            "total_rewards_distributed": len(
                self.reward_system.reward_history
            ),
            "average_motivation_index": self.reward_system.total_motivation_index
            / max(1, len(self.reward_system.reward_history)),
            "difficulty_adjustments": len(self.dda.adjustment_history),
            "current_player_count": 1,
            "system_uptime": 0,
            "active_interventions": len(
                [
                    i
                    for i in self.engagement_system.intervention_history
                    if time.time() - i.get("timestamp", 0) < 300
                ]
            ),
        }


_gamification_system = None


def get_gamification_system(player_id: str = "player1") -> GamificationSystem:
    global _gamification_system
    if _gamification_system is None:
        _gamification_system = GamificationSystem(player_id)
    return _gamification_system


def create_gamification_system(player_id: str = "player1") -> GamificationSystem:
    return GamificationSystem(player_id)
