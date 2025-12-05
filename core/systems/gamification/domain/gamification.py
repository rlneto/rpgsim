from typing import Dict, List, Optional, Any
from enum import Enum
import math
import random
from dataclasses import dataclass, field
import time

class FlowStateMetrics:
    def __init__(self):
        self.skill_level = 0.5
        self.challenge_level = 0.5
        self.anxiety_score = 0.0
        self.boredom_score = 0.0
        self.flow_score = 0.0
        self.in_flow_state = False
        self.challenge_skill_ratio = 1.0
        self.engagement_level = 0.5
        self.focus_metrics = {}
        self.emotional_indicators = {}
        self.flow_indicators = []

    def calculate_flow_score(self) -> float:
        ratio = self.challenge_skill_ratio
        if ratio <= 1.1 and ratio >= 0.9:
            return 1.0
        elif ratio < 0.9:
            return ratio / 0.9
        else:
            return max(0.0, 1.0 - (ratio - 1.1))

    def update_engagement(self, **kwargs):
        if 'actions_per_minute' in kwargs:
            self.focus_metrics['actions_per_minute'] = kwargs['actions_per_minute']
        if 'decision_accuracy' in kwargs:
            self.focus_metrics['decision_accuracy'] = kwargs['decision_accuracy']
        if 'error_rate' in kwargs:
            self.focus_metrics['error_rate'] = kwargs['error_rate']
        if 'enjoyment' in kwargs:
            self.emotional_indicators['enjoyment_level'] = kwargs['enjoyment']
        if 'frustration' in kwargs:
            self.emotional_indicators['frustration_level'] = kwargs['frustration']
        if 'motivation' in kwargs:
            self.emotional_indicators['motivation_level'] = kwargs['motivation']

class PerformanceMetrics:
    def __init__(self):
        self.success_rate = 0.0
        self.time_efficiency = 0.0
        self.resource_efficiency = 0.0
        self.overall_score = 0.0
        self.recent_encounters = []
        self.completion_time = 0.0
        self.damage_taken = 0.0
        self.resource_usage = 0.0
        self.actions_per_minute = 0.0

    def calculate_score(self) -> float:
        score = (self.success_rate * 0.4) + (self.time_efficiency * 0.3) + (self.resource_efficiency * 0.3)
        self.overall_score = score
        return score

    def add_encounter(self, success: bool, time_taken: float, resources_used: float):
        encounter = {
            'success': success,
            'time_taken': time_taken,
            'resources_used': resources_used
        }
        self.recent_encounters.append(encounter)
        if len(self.recent_encounters) > 10:
            self.recent_encounters = self.recent_encounters[-10:]

        success_count = sum(1 for e in self.recent_encounters if e['success'])
        self.success_rate = success_count / len(self.recent_encounters)

class DifficultyAdjustmentType(Enum):
    INCREASE = "increase"
    DECREASE = "decrease"
    MAINTAIN = "maintain"

class EngagementMetricType(Enum):
    SESSION_DURATION = "session_duration"
    ACTION_FREQUENCY = "action_frequency"
    SUCCESS_RATE = "success_rate"
    EXPLORATION_RATE = "exploration_rate"
    SOCIAL_INTERACTION = "social_interaction"
    ACHIEVEMENT_PROGRESS = "achievement_progress"

class RewardScheduleType(Enum):
    FIXED_RATIO = "fixed_ratio"
    VARIABLE_RATIO = "variable_ratio"
    FIXED_INTERVAL = "fixed_interval"
    VARIABLE_INTERVAL = "variable_interval"

class InterventionType(Enum):
    DYNAMIC_DIFFICULTY = "dynamic_difficulty"
    REWARD_BOOST = "reward_boost"
    CONTENT_VARIETY = "content_variety"
    TUTORIAL_HINT = "tutorial_hint"
    REST_SUGGESTION = "rest_suggestion"
    CHALLENGE_EVENT = "challenge_event"
    REWARD_BONUS = "reward_bonus"
    CONTENT_RECOMMENDATION = "content_recommendation"
    ACHIEVEMENT_MILESTONE = "achievement_milestone"
    SOCIAL_CONNECTION_PROMPT = "social_connection_prompt"

class ContentVarietyType(Enum):
    COMBAT = "combat"
    EXPLORATION = "exploration"
    PUZZLES = "puzzles"
    SOCIAL = "social"
    CRAFTING = "crafting"
    STORY = "story"

class MotivationPillar(Enum):
    MASTERY = "mastery"
    AUTONOMY = "autonomy"
    PURPOSE = "purpose"
    RELATEDNESS = "relatedness"

class ProgressVisualizationType(Enum):
    LINEAR_BAR = "linear_bar"
    RADIAL_CHART = "radial_chart"
    NODE_MAP = "node_map"
    CONSTELLATION = "constellation"
    LOGARITHMIC = "logarithmic"

class RewardEvent:
    def __init__(self, reward_type: str, value: Any, timestamp: float,
                 context: Dict[str, Any], prediction_error: float = 0.0,
                 novelty_factor: float = 0.0):
        self.type = reward_type
        self.value = value
        self.timestamp = timestamp
        self.context = context
        self.prediction_error = prediction_error
        self.novelty_factor = novelty_factor
        self.motivation_index = 0.0
        self.difficulty = 0.5
        self.time_investment = 0.0
        self.skill_required = 0.5
        self.received_reward = 0

class RewardSchedule:
    def __init__(self, schedule_type: RewardScheduleType, parameters: Dict[str, Any] = None):
        self.schedule_type = schedule_type
        self.type = schedule_type
        self.parameters = parameters or {}
        self.last_reward_time = 0.0
        self.action_count = 0
        self.variable_ratio_min = 5
        self.variable_ratio_max = 10
        self.adaptation_enabled = True

    def should_reward(self, count: int) -> bool:
        if self.schedule_type == RewardScheduleType.VARIABLE_RATIO:
            threshold = random.randint(self.variable_ratio_min, self.variable_ratio_max)
            return count >= threshold
        return False

    def calculate_rare_reward_probability(self, n_encounters: int) -> float:
        return 0.05 * (1.0 - math.exp(-n_encounters / 20.0))

class EngagementScore:
    def __init__(self):
        self.current_score = 0.5
        self.metrics = {}
        self.history = []
        self.individual_metrics = {}
        self.weights = {}
        self.overall_score = 0.0
        self.engagement_level = "medium"

    def calculate_score(self, metrics: Dict[str, float]) -> float:
        weights = {
            'session_duration': 0.25,
            'action_frequency': 0.20,
            'success_rate': 0.15,
            'exploration_rate': 0.15,
            'social_interaction': 0.10,
            'achievement_progress': 0.15
        }

        score = 0.0
        for metric, value in metrics.items():
            if metric in weights:
                score += value * weights[metric]

        self.current_score = score
        self.overall_score = score
        self.history.append(score)

        if score < 0.3:
            self.engagement_level = "low"
        elif score > 0.7:
            self.engagement_level = "high"
        else:
            self.engagement_level = "medium"

        return score

class ChurnRiskAnalysis:
    def __init__(self, risk_level: float = 0.0, factors: List[str] = None):
        self.risk_level = "low"
        self.factors = factors or []
        self.churn_probability = 0.0
        self.weighted_score = 0.0
        self.behavioral_markers = {}
        self.model_confidence = 0.85

    def calculate_risk(self, markers: Dict[str, float]) -> float:
        if not markers: return 0.0
        avg = sum(markers.values()) / len(markers)
        self.churn_probability = avg

        if avg < 0.3:
            self.risk_level = "low"
        elif avg > 0.7:
            self.risk_level = "high"
        else:
            self.risk_level = "medium"

        return avg

class ProgressVisualization:
    def __init__(self, viz_type: ProgressVisualizationType = ProgressVisualizationType.LOGARITHMIC, data: Dict[str, Any] = None):
        self.type = viz_type
        self.data = data
        self.level_progress = 0.0
        self.scaling_type = viz_type

    def apply_logarithmic_scaling(self, value: float) -> float:
        if value <= 0: return 0.0
        return math.log1p(value) / math.log(2)

    def calculate_scaled_progress(self, metrics: Dict[str, float]) -> Dict[str, float]:
        return {k: self.apply_logarithmic_scaling(v) for k, v in metrics.items()}

@dataclass
class Achievement:
    id: str
    name: str
    description: str
    points: int

@dataclass
class Progress:
    user_id: str
    player_id: str = field(init=False) # alias for user_id
    points: int = 0
    level: int = 1
    experience: int = 0
    unlocked_achievements: List[str] = field(default_factory=list)

    def __post_init__(self):
        self.player_id = self.user_id

@dataclass
class Badge:
    id: str
    name: str

@dataclass
class Reward:
    id: str
    type: str
    value: Any
    player_id: str
