"""
Gamification system domain entities and value objects
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
import math
import time
import random


class DifficultyAdjustmentType(Enum):
    """Types of difficulty adjustment."""

    STATISTICAL_SMOOTHING = "statistical_smoothing"
    PERFORMANCE_BASED = "performance_based"
    FLOW_OPTIMIZED = "flow_optimized"
    MICRO_ADJUSTMENT = "micro_adjustment"
    INTERVENTION_TRIGGERED = "intervention_triggered"


class EngagementMetricType(Enum):
    """Types of engagement metrics."""

    SESSION_DURATION = "session_duration"
    ACTION_FREQUENCY = "action_frequency"
    SUCCESS_RATE = "success_rate"
    EXPLORATION_RATE = "exploration_rate"
    SOCIAL_INTERACTION = "social_interaction"
    ACHIEVEMENT_PROGRESS = "achievement_progress"
    FOCUS_LEVEL = "focus_level"
    CHALLENGE_PERCEPTION = "challenge_perception"


class RewardScheduleType(Enum):
    """Types of reward schedules."""

    VARIABLE_RATIO = "variable_ratio"
    FIXED_INTERVAL = "fixed_interval"
    VARIABLE_INTERVAL = "variable_interval"
    PROGRESSIVE_JACKPOT = "progressive_jackpot"
    PREDICTION_ERROR = "prediction_error"


class InterventionType(Enum):
    """Types of player interventions."""

    DYNAMIC_DIFFICULTY = "dynamic_difficulty"
    CONTENT_RECOMMENDATION = "content_recommendation"
    SOCIAL_CONNECTION_PROMPT = "social_connection_prompt"
    ACHIEVEMENT_MILESTONE = "achievement_milestone"
    REWARD_BONUS = "reward_bonus"
    STORY_PROGRESSION_HINT = "story_progression_hint"


class ContentVarietyType(Enum):
    """Content variety categories."""

    COMBAT = "combat"
    EXPLORATION = "exploration"
    PUZZLES = "puzzles"
    SOCIAL = "social"
    CRAFTING = "crafting"
    STORY = "story"


class MotivationPillar(Enum):
    """Self-Determination Theory pillars."""

    AUTONOMY = "autonomy"
    COMPETENCE = "competence"
    RELATEDNESS = "relatedness"


class ProgressVisualizationType(Enum):
    """Progress visualization types."""

    LOGARITHMIC = "logarithmic"
    LINEAR = "linear"
    DIMINISHING_RETURNS = "diminishing_returns"
    EXPONENTIAL = "exponential"


@dataclass
class Achievement:
    id: str
    name: str
    description: str
    unlocked: bool = False


@dataclass
class Badge:
    id: str
    name: str
    icon: str


@dataclass
class Progress:
    player_id: str
    level: int
    experience: int


@dataclass
class Reward:
    player_id: str
    item: str
    quantity: int


@dataclass
class PerformanceMetrics:
    """Player performance metrics for DDA."""

    success_rate: float = 0.0
    time_efficiency: float = 0.0
    resource_efficiency: float = 0.0
    overall_score: float = 0.0
    recent_encounters: List[Dict[str, Any]] = field(default_factory=list)

    def calculate_score(self) -> float:
        """Calculate weighted performance score."""
        self.overall_score = (
            self.success_rate * 0.4
            + self.time_efficiency * 0.3
            + self.resource_efficiency * 0.3
        )
        return max(0.0, min(1.0, self.overall_score))

    def add_encounter(
        self, success: bool, time_taken: int, resources_used: float
    ) -> None:
        """Add encounter data and update metrics."""
        encounter = {
            "success": success,
            "time_taken": time_taken,
            "resources_used": resources_used,
            "timestamp": time.time(),
        }
        self.recent_encounters.append(encounter)

        if len(self.recent_encounters) > 10:
            self.recent_encounters.pop(0)

        successes = sum(1 for e in self.recent_encounters if e["success"])
        self.success_rate = successes / len(self.recent_encounters)

        avg_time = sum(e["time_taken"] for e in self.recent_encounters) / len(
            self.recent_encounters
        )
        self.time_efficiency = max(
            0.0, 1.0 - (avg_time - 60) / 240
        )

        self.resource_efficiency = sum(
            1 - e["resources_used"] for e in self.recent_encounters
        ) / len(self.recent_encounters)


@dataclass
class FlowStateMetrics:
    """Flow state monitoring metrics."""

    challenge_skill_ratio: float = 1.0
    engagement_level: float = 0.5
    focus_metrics: Dict[str, float] = field(default_factory=dict)
    emotional_indicators: Dict[str, float] = field(default_factory=dict)
    flow_indicators: List[bool] = field(default_factory=list)
    last_adjustment: float = 0.0

    def calculate_flow_score(self) -> float:
        """Calculate flow state score using Chen equation."""
        if 0.9 <= self.challenge_skill_ratio <= 1.2:
            return 1.0
        elif self.challenge_skill_ratio < 0.9:
            return self.challenge_skill_ratio / 0.9
        else:
            return max(0.0, 1.0 - (self.challenge_skill_ratio - 1.2) / 2.0)

    def update_engagement(
        self,
        actions_per_minute: float,
        decision_accuracy: float,
        error_rate: float,
        enjoyment: float,
        frustration: float,
        motivation: float,
    ) -> None:
        """Update engagement metrics."""
        self.focus_metrics = {
            "actions_per_minute": actions_per_minute,
            "decision_accuracy": decision_accuracy,
            "error_rate": error_rate,
        }

        self.emotional_indicators = {
            "enjoyment_level": enjoyment,
            "frustration_level": frustration,
            "motivation_level": motivation,
        }

        self.engagement_level = (
            enjoyment * 0.3
            + motivation * 0.3
            + decision_accuracy * 0.2
            + actions_per_minute / 25 * 0.2
        )


@dataclass
class RewardEvent:
    """Individual reward event data."""

    id: int
    type: str
    difficulty: float
    time_investment: int
    skill_required: float
    expected_reward: int
    received_reward: int
    prediction_error: float
    motivation_index: float
    novelty_factor: float
    timestamp: float


@dataclass
class RewardSchedule:
    """Reinforcement learning reward schedule configuration."""

    schedule_type: RewardScheduleType
    variable_ratio_min: int = 5
    variable_ratio_max: int = 10
    rare_reward_base_prob: float = 0.05
    adaptation_enabled: bool = True

    def should_reward(self, actions_since_last_reward: int) -> bool:
        """Determine if reward should be given based on schedule."""
        if self.schedule_type == RewardScheduleType.VARIABLE_RATIO:
            vr_ratio = random.randint(self.variable_ratio_min, self.variable_ratio_max)
            return actions_since_last_reward >= vr_ratio
        return False

    def calculate_rare_reward_probability(self, encounters_since_last: int) -> float:
        """Calculate rare reward probability using P = 0.05 * (1 - e^(-n/20))."""
        n = encounters_since_last
        return self.rare_reward_base_prob * (1 - math.exp(-n / 20))


@dataclass
class EngagementScore:
    """Comprehensive engagement score calculation."""

    individual_metrics: Dict[str, float] = field(default_factory=dict)
    weights: Dict[str, float] = field(default_factory=dict)
    overall_score: float = 0.0
    engagement_level: str = "medium"
    last_update: float = field(default_factory=time.time)

    def calculate_score(
        self, metrics: Dict[str, float], weights: Optional[Dict[str, float]] = None
    ) -> float:
        """Calculate weighted engagement score."""
        default_weights = {
            "session_duration_weight": 0.25,
            "action_frequency_weight": 0.20,
            "success_rate_weight": 0.15,
            "exploration_rate_weight": 0.15,
            "social_interaction_weight": 0.10,
            "achievement_progress_weight": 0.15,
        }

        self.weights = weights or default_weights
        self.individual_metrics = metrics

        self.overall_score = 0.0
        for metric, value in metrics.items():
            weight_key = f"{metric}_weight"
            if weight_key in self.weights:
                self.overall_score += value * self.weights[weight_key]

        if self.overall_score > 0.7:
            self.engagement_level = "high"
        elif self.overall_score > 0.4:
            self.engagement_level = "medium"
        else:
            self.engagement_level = "low"

        self.last_update = time.time()
        return self.overall_score


@dataclass
class ChurnRiskAnalysis:
    """Player churn risk prediction."""

    behavioral_markers: Dict[str, float] = field(default_factory=dict)
    weighted_score: float = 0.0
    churn_probability: float = 0.0
    risk_level: str = "low"
    model_confidence: float = 0.85
    last_analysis: float = field(default_factory=time.time)

    def calculate_risk(self, markers: Dict[str, float]) -> float:
        """Calculate churn probability using behavioral markers."""
        self.behavioral_markers = markers

        marker_weights = {
            "decreasing_session_length": 0.25,
            "reduced_social_interaction": 0.20,
            "achievement_stagnation": 0.15,
            "increasing_failure_rate": 0.15,
            "login_frequency_decline": 0.15,
            "negative_sentiment_indicators": 0.10,
        }

        self.weighted_score = 0.0
        for marker, value in markers.items():
            if marker in marker_weights:
                self.weighted_score += value * marker_weights[marker]

        self.churn_probability = 1 / (1 + math.exp(-5 * (self.weighted_score - 0.5)))

        if self.churn_probability > 0.7:
            self.risk_level = "high"
        elif self.churn_probability > 0.3:
            self.risk_level = "medium"
        else:
            self.risk_level = "low"

        self.last_analysis = time.time()
        return self.churn_probability


@dataclass
class ProgressVisualization:
    """Progress visualization using Weber-Fechner law."""

    level_progress: float = 0.0
    skill_progress: float = 0.0
    achievement_progress: float = 0.0
    exploration_progress: float = 0.0
    overall_progress: float = 0.0
    scaling_type: ProgressVisualizationType = ProgressVisualizationType.LOGARITHMIC

    def apply_logarithmic_scaling(
        self, progress: float, k: float = 0.5, s0: float = 0.01
    ) -> float:
        """Apply Weber-Fechner logarithmic scaling: ΔP = k * ln(S/S₀)."""
        if progress <= 0:
            return 0.0

        current_state = max(progress, s0)
        scaled_value = k * math.log(current_state / s0)
        return min(1.0, max(0.0, scaled_value))

    def calculate_scaled_progress(
        self, raw_metrics: Dict[str, float]
    ) -> Dict[str, float]:
        """Calculate scaled progress metrics."""
        scaled = {}

        for metric, value in raw_metrics.items():
            if self.scaling_type == ProgressVisualizationType.LOGARITHMIC:
                scaled[metric] = self.apply_logarithmic_scaling(value)
            else:
                scaled[metric] = value

        return scaled
