from collections import deque
import math
import random
import statistics
import time
from typing import Any, Dict, List, Optional, Tuple

from ..domain.gamification import (
    ContentVarietyType,
    InterventionType,
    PerformanceMetrics,
    FlowStateMetrics,
    EngagementScore,
    ChurnRiskAnalysis,
)


class DynamicDifficultyAdjustment:
    def __init__(self):
        self.base_difficulty = 0.5
        self.current_difficulty = 0.5
        self.target_performance = 0.75
        self.adjustment_history = deque(maxlen=100)
        self.performance = PerformanceMetrics()

    def calculate_difficulty_adjustment(self, measured_performance: float) -> float:
        if measured_performance <= 0:
            measured_performance = 0.1
        adjustment_factor = 0.7 + 0.3 * (
            self.target_performance / measured_performance
        )
        new_difficulty = self.base_difficulty * adjustment_factor
        max_adjustment = self.base_difficulty * 0.15
        new_difficulty = max(0.1, min(0.9, new_difficulty))
        new_difficulty = max(
            self.base_difficulty - max_adjustment,
            min(self.base_difficulty + max_adjustment, new_difficulty),
        )
        return new_difficulty

    def apply_statistical_smoothing(
        self, new_difficulty: float, smoothing_factor: float = 0.7
    ) -> float:
        smoothed_difficulty = (
            new_difficulty * smoothing_factor
            + self.current_difficulty * (1 - smoothing_factor)
        )
        self.adjustment_history.append(
            {
                "old_difficulty": self.current_difficulty,
                "new_difficulty": smoothed_difficulty,
                "percent_change": abs(smoothed_difficulty - self.current_difficulty)
                / max(0.1, self.current_difficulty),
                "timestamp": time.time(),
            }
        )
        self.current_difficulty = smoothed_difficulty
        return smoothed_difficulty

    def generate_encounter_difficulty(
        self, player_skill: float, sigma: float = 0.15
    ) -> float:
        u1 = random.random()
        u2 = random.random()
        z0 = (-2 * math.log(u1)) ** 0.5 * math.cos(2 * math.pi * u2)
        difficulty = player_skill + (z0 * sigma)
        return max(0.1, min(0.9, difficulty))

    def should_apply_micro_adjustment(
        self, recent_encounters: List[Dict[str, Any]]
    ) -> Tuple[bool, float]:
        if len(recent_encounters) < 2:
            return False, 0.0
        success_pattern = [e["success"] for e in recent_encounters]
        recent_success_rate = sum(success_pattern) / len(success_pattern)
        if recent_success_rate >= 0.9:
            return True, 0.02
        elif recent_success_rate <= 0.3:
            return True, -0.02
        current_streak = 0
        max_streak = 0
        for success in success_pattern:
            if success:
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                current_streak = 0
        if max_streak >= 4:
            return True, 0.03
        elif current_streak >= 3:
            return True, -0.03
        return False, 0.0


class FlowStateOptimizer:
    def __init__(self):
        self.metrics = FlowStateMetrics()
        self.disruption_monitoring = True
        self.last_rebalance_time = 0.0

    def calculate_optimal_difficulty(self, player_skill: float) -> float:
        target_ratio = (0.9 + 1.2) / 2
        return player_skill / target_ratio

    def detect_flow_disruption(self, session_data: Dict[str, Any]) -> bool:
        indicators = {
            "rapid_failure_sequence": self._check_rapid_failures(session_data),
            "extended_inactivity": self._check_inactivity(session_data),
            "erratic_behavior": self._check_erratic_behavior(session_data),
            "frustration_signals": self._check_frustration(session_data),
        }
        disruption_count = sum(indicators.values())
        return disruption_count >= 2

    def _check_rapid_failures(self, session_data: Dict[str, Any]) -> bool:
        recent_actions = session_data.get("recent_actions", [])
        if len(recent_actions) < 5:
            return False
        failures = sum(
            1 for action in recent_actions[-5:] if not action.get("success", True)
        )
        return failures >= 4

    def _check_inactivity(self, session_data: Dict[str, Any]) -> bool:
        last_action_time = session_data.get("last_action_time", time.time())
        inactive_time = time.time() - last_action_time
        return inactive_time > 120

    def _check_erratic_behavior(self, session_data: Dict[str, Any]) -> bool:
        action_times = session_data.get("action_times", [])
        if len(action_times) < 3:
            return False
        time_diffs = [
            action_times[i] - action_times[i - 1] for i in range(1, len(action_times))
        ]
        if not time_diffs:
            return False
        variance = statistics.variance(time_diffs)
        return variance > 100

    def _check_frustration(self, session_data: Dict[str, Any]) -> bool:
        frustration_level = session_data.get("frustration_level", 0.0)
        return frustration_level > 0.7

    def auto_rebalance(self, current_difficulty: float) -> float:
        rebalance_time = time.time()
        if rebalance_time - self.last_rebalance_time < 30:
            return current_difficulty
        if self.metrics.challenge_skill_ratio < 0.9:
            adjustment = -0.05
        elif self.metrics.challenge_skill_ratio > 1.2:
            adjustment = 0.05
        else:
            adjustment = 0.0
        self.last_rebalance_time = rebalance_time
        return max(0.1, min(0.9, current_difficulty + adjustment))


class NeuroadaptiveEngagementSystem:
    def __init__(self):
        self.engagement_score = EngagementScore()
        self.churn_analysis = ChurnRiskAnalysis()
        self.intervention_history = deque(maxlen=50)
        self.behavioral_data = deque(maxlen=1000)

    def track_behavior(
        self, action_type: str, timestamp: float, metadata: Dict[str, Any]
    ) -> None:
        behavior_entry = {
            "action_type": action_type,
            "timestamp": timestamp,
            "metadata": metadata,
        }
        self.behavioral_data.append(behavior_entry)

    def calculate_engagement_metrics(self) -> Dict[str, float]:
        recent_data = [
            b for b in self.behavioral_data if time.time() - b["timestamp"] < 3600
        ]
        if not recent_data:
            return {
                metric: 0.5
                for metric in [
                    "session_duration",
                    "action_frequency",
                    "success_rate",
                    "exploration_rate",
                    "social_interaction",
                    "achievement_progress",
                ]
            }
        session_duration = min(
            1.0, (time.time() - recent_data[0]["timestamp"]) / 7200
        )
        time_span = max(
            1, (recent_data[-1]["timestamp"] - recent_data[0]["timestamp"]) / 60
        )
        action_frequency = min(1.0, len(recent_data) / (time_span * 30))
        success_actions = [
            b for b in recent_data if b["metadata"].get("success", False)
        ]
        success_rate = (
            len(success_actions) / len(recent_data) if recent_data else 0.5
        )
        action_types = set(b["action_type"] for b in recent_data)
        exploration_rate = min(1.0, len(action_types) / 6)
        social_actions = [
            b for b in recent_data if "social" in b["action_type"].lower()
        ]
        social_interaction = min(
            1.0, len(social_actions) / max(1, len(recent_data) * 0.2)
        )
        achievement_actions = [
            b for b in recent_data if "achievement" in b["action_type"].lower()
        ]
        achievement_progress = min(
            1.0, len(achievement_actions) / max(1, len(recent_data) * 0.1)
        )
        metrics = {
            "session_duration": session_duration,
            "action_frequency": action_frequency,
            "success_rate": success_rate,
            "exploration_rate": exploration_rate,
            "social_interaction": social_interaction,
            "achievement_progress": achievement_progress,
        }
        self.engagement_score.calculate_score(metrics)
        return metrics

    def predict_churn_risk(self) -> Dict[str, Any]:
        recent_data = [
            b for b in self.behavioral_data if time.time() - b["timestamp"] < 86400
        ]
        if len(recent_data) < 10:
            return {
                "risk_level": "low",
                "churn_probability": 0.1,
                "confidence": 0.5,
            }
        markers = {
            "decreasing_session_length": self._calculate_session_trend(
                recent_data
            ),
            "reduced_social_interaction": self._calculate_social_trend(
                recent_data
            ),
            "achievement_stagnation": self._calculate_achievement_trend(
                recent_data
            ),
            "increasing_failure_rate": self._calculate_failure_trend(recent_data),
            "login_frequency_decline": self._calculate_login_trend(recent_data),
            "negative_sentiment_indicators": self._calculate_sentiment_trend(
                recent_data
            ),
        }
        churn_prob = self.churn_analysis.calculate_risk(markers)
        return {
            "risk_level": self.churn_analysis.risk_level,
            "churn_probability": churn_prob,
            "confidence": self.churn_analysis.model_confidence,
            "behavioral_markers": markers,
        }

    def should_trigger_intervention(
        self,
    ) -> Tuple[bool, Optional[InterventionType]]:
        engagement_score = self.engagement_score.overall_score
        session_duration = self.engagement_score.individual_metrics.get(
            "session_duration", 0
        )
        if engagement_score < 0.6 and session_duration > 3:
            if engagement_score < 0.3:
                intervention = InterventionType.REWARD_BONUS
            elif engagement_score < 0.5:
                intervention = InterventionType.CONTENT_RECOMMENDATION
            else:
                intervention = InterventionType.ACHIEVEMENT_MILESTONE
            return True, intervention
        return False, None

    def _calculate_session_trend(self, data: List[Dict[str, Any]]) -> float:
        return random.uniform(0.1, 0.9)

    def _calculate_social_trend(self, data: List[Dict[str, Any]]) -> float:
        social_actions = [
            b for b in data if "social" in b["action_type"].lower()
        ]
        if len(social_actions) == 0:
            return 0.5
        recent_social = [
            b for b in social_actions if time.time() - b["timestamp"] < 3600
        ]
        return 0.5 if len(recent_social) > 0 else 0.8

    def _calculate_achievement_trend(self, data: List[Dict[str, Any]]) -> float:
        achievement_actions = [
            b for b in data if "achievement" in b["action_type"].lower()
        ]
        return 0.3 if len(achievement_actions) > 0 else 0.7

    def _calculate_failure_trend(self, data: List[Dict[str, Any]]) -> float:
        recent_failures = [
            b for b in data[-20:] if not b["metadata"].get("success", True)
        ]
        return min(1.0, len(recent_failures) / max(1, len(data[-20:])))

    def _calculate_login_trend(self, data: List[Dict[str, Any]]) -> float:
        if len(data) < 2:
            return 0.5
        time_span = data[-1]["timestamp"] - data[0]["timestamp"]
        avg_gap = time_span / len(data)
        return min(1.0, avg_gap / 3600)

    def _calculate_sentiment_trend(self, data: List[Dict[str, Any]]) -> float:
        frustration_indicators = [
            b for b in data if b["metadata"].get("frustration", 0) > 0.6
        ]
        return min(
            1.0, len(frustration_indicators) / max(1, len(data) * 0.1)
        )


class ContentVarietyOptimizer:
    def __init__(self):
        self.content_exposure = {ct.value: 0.0 for ct in ContentVarietyType}
        self.exploration_epsilon = 0.1
        self.wundt_optimal_range = (0.8, 1.0)

    def calculate_content_novelty(
        self, content_type: ContentVarietyType
    ) -> float:
        recent_exposure = self.content_exposure[content_type.value]
        standardized_novelty = (recent_exposure - 0.5) / 0.5
        wundt_value = math.exp(-(standardized_novelty**2))
        return wundt_value * 2.0

    def should_exploit_or_explore(self) -> bool:
        return random.random() < self.exploration_epsilon

    def recommend_content(self) -> ContentVarietyType:
        if self.should_exploit_or_explore():
            content_novelties = {
                ct: self.calculate_content_novelty(ct)
                for ct in ContentVarietyType
            }
            return max(content_novelties, key=content_novelties.get)
        else:
            optimal_content = []
            for ct in ContentVarietyType:
                novelty = self.calculate_content_novelty(ct)
                if (
                    self.wundt_optimal_range[0]
                    <= novelty
                    <= self.wundt_optimal_range[1]
                ):
                    optimal_content.append(ct)
            return (
                random.choice(optimal_content)
                if optimal_content
                else random.choice(list(ContentVarietyType))
            )

    def update_content_exposure(
        self, content_type: ContentVarietyType, exposure_amount: float = 0.1
    ) -> None:
        current = self.content_exposure[content_type.value]
        self.content_exposure[content_type.value] = min(
            1.0, current + exposure_amount
        )
        for ct in ContentVarietyType:
            if ct != content_type:
                self.content_exposure[ct.value] = max(
                    0.0, self.content_exposure[ct.value] - 0.01
                )

    def get_content_variety_analysis(self) -> Dict[str, Any]:
        novelty_scores = {
            ct.value: self.calculate_content_novelty(ct)
            for ct in ContentVarietyType
        }
        under_stimulated = [
            ct for ct, score in novelty_scores.items() if score < 0.3
        ]
        optimally_stimulated = [
            ct for ct, score in novelty_scores.items() if 0.3 <= score <= 0.8
        ]
        over_stimulated = [
            ct for ct, score in novelty_scores.items() if score > 0.8
        ]
        return {
            "content_novelty_scores": novelty_scores,
            "under_stimulated_content": under_stimulated,
            "optimally_stimulated_content": optimally_stimulated,
            "over_stimulated_content": over_stimulated,
            "variety_balance": len(optimally_stimulated)
            / len(ContentVarietyType),
        }


class InterventionSystem:
    def __init__(self):
        self.intervention_history = deque(maxlen=100)
        self.available_interventions = list(InterventionType)

    def trigger_intervention(
        self, intervention_type: InterventionType, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        intervention_data = {
            "type": intervention_type,
            "timestamp": time.time(),
            "context": context,
            "effectiveness": 0.0,
            "outcome": None,
        }
        if intervention_type == InterventionType.DYNAMIC_DIFFICULTY:
            intervention_data["outcome"] = self._apply_difficulty_adjustment(
                context
            )
        elif intervention_type == InterventionType.CONTENT_RECOMMENDATION:
            intervention_data["outcome"] = self._recommend_content(context)
        elif intervention_type == InterventionType.REWARD_BONUS:
            intervention_data["outcome"] = self._provide_bonus_reward(context)
        elif intervention_type == InterventionType.ACHIEVEMENT_MILESTONE:
            intervention_data["outcome"] = self._unlock_milestone(context)
        else:
            intervention_data["outcome"] = self._apply_generic_intervention(
                intervention_type, context
            )
        self.intervention_history.append(intervention_data)
        return intervention_data

    def _apply_difficulty_adjustment(
        self, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        current_difficulty = context.get("current_difficulty", 0.5)
        player_performance = context.get("player_performance", 0.5)
        if player_performance < 0.3:
            new_difficulty = max(0.1, current_difficulty - 0.2)
        elif player_performance > 0.8:
            new_difficulty = min(0.9, current_difficulty + 0.1)
        else:
            new_difficulty = current_difficulty
        return {
            "difficulty_adjusted": True,
            "old_difficulty": current_difficulty,
            "new_difficulty": new_difficulty,
            "adjustment_reason": "performance_based",
        }

    def _recommend_content(self, context: Dict[str, Any]) -> Dict[str, Any]:
        player_preferences = context.get("player_preferences", {})
        current_engagement = context.get("engagement_level", 0.5)
        if current_engagement < 0.3:
            recommended_content = "high_reward_quest"
        elif current_engagement < 0.6:
            recommended_content = "balanced_challenge"
        else:
            recommended_content = "mastery_opportunity"
        return {
            "content_recommended": True,
            "recommended_type": recommended_content,
            "reason": "engagement_based",
        }

    def _provide_bonus_reward(self, context: Dict[str, Any]) -> Dict[str, Any]:
        bonus_amount = random.randint(50, 200)
        return {
            "bonus_rewarded": True,
            "bonus_amount": bonus_amount,
            "reward_type": "motivation_bonus",
        }

    def _unlock_milestone(self, context: Dict[str, Any]) -> Dict[str, Any]:
        player_progress = context.get("player_progress", {})
        return {
            "milestone_unlocked": True,
            "milestone_type": "progress_milestone",
            "progress_percentage": player_progress.get("percentage", 0),
        }

    def _apply_generic_intervention(
        self, intervention_type: InterventionType, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        return {
            "intervention_applied": True,
            "type": intervention_type.value,
            "context_processed": bool(context),
        }
