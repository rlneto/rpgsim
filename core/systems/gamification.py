"""
Gamification System - Modern 2025 player engagement and motivation mechanics.

Implements Dynamic Difficulty Adjustment (DDA), flow state optimization,
reinforcement learning reward schedules, neuroadaptive engagement systems,
progress visualization with Weber-Fechner law, and advanced psychological
principles for optimal player experience.

Complexity: Very High
Dependencies: Character, Combat, Equipment, Quest, Progression, Dungeon Systems
"""

import random
import math
import time
from enum import Enum
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from collections import deque
import statistics


# Core Enums
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


# Core Data Classes
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
            self.success_rate * 0.4 +
            self.time_efficiency * 0.3 +
            self.resource_efficiency * 0.3
        )
        return max(0.0, min(1.0, self.overall_score))

    def add_encounter(self, success: bool, time_taken: int, resources_used: float) -> None:
        """Add encounter data and update metrics."""
        encounter = {
            'success': success,
            'time_taken': time_taken,
            'resources_used': resources_used,
            'timestamp': time.time()
        }
        self.recent_encounters.append(encounter)

        # Keep only last 10 encounters for performance calculation
        if len(self.recent_encounters) > 10:
            self.recent_encounters.pop(0)

        # Update metrics
        successes = sum(1 for e in self.recent_encounters if e['success'])
        self.success_rate = successes / len(self.recent_encounters)

        avg_time = sum(e['time_taken'] for e in self.recent_encounters) / len(
            self.recent_encounters
        )
        self.time_efficiency = max(0.0, 1.0 - (avg_time - 60) / 240)  # Normalize around 1-5 minutes

        self.resource_efficiency = sum(
            1 - e['resources_used'] for e in self.recent_encounters
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
        # Optimal range is 0.9 to 1.2
        if 0.9 <= self.challenge_skill_ratio <= 1.2:
            return 1.0
        elif self.challenge_skill_ratio < 0.9:
            return self.challenge_skill_ratio / 0.9
        else:  # > 1.2
            return max(0.0, 1.0 - (self.challenge_skill_ratio - 1.2) / 2.0)

    def update_engagement(self, actions_per_minute: float, decision_accuracy: float,
                         error_rate: float, enjoyment: float, frustration: float,
                         motivation: float) -> None:
        """Update engagement metrics."""
        self.focus_metrics = {
            'actions_per_minute': actions_per_minute,
            'decision_accuracy': decision_accuracy,
            'error_rate': error_rate
        }

        self.emotional_indicators = {
            'enjoyment_level': enjoyment,
            'frustration_level': frustration,
            'motivation_level': motivation
        }

        # Calculate overall engagement level
        self.engagement_level = (
            enjoyment * 0.3 +
            motivation * 0.3 +
            decision_accuracy * 0.2 +
            actions_per_minute / 25 * 0.2  # Normalize to 0-1
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

    def calculate_score(self, metrics: Dict[str, float],
                       weights: Optional[Dict[str, float]] = None) -> float:
        """Calculate weighted engagement score."""
        default_weights = {
            'session_duration_weight': 0.25,
            'action_frequency_weight': 0.20,
            'success_rate_weight': 0.15,
            'exploration_rate_weight': 0.15,
            'social_interaction_weight': 0.10,
            'achievement_progress_weight': 0.15
        }

        self.weights = weights or default_weights
        self.individual_metrics = metrics

        # Calculate weighted score
        self.overall_score = 0.0
        for metric, value in metrics.items():
            weight_key = f"{metric}_weight"
            if weight_key in self.weights:
                self.overall_score += value * self.weights[weight_key]

        # Determine engagement level
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
            'decreasing_session_length': 0.25,
            'reduced_social_interaction': 0.20,
            'achievement_stagnation': 0.15,
            'increasing_failure_rate': 0.15,
            'login_frequency_decline': 0.15,
            'negative_sentiment_indicators': 0.10
        }

        # Calculate weighted score
        self.weighted_score = 0.0
        for marker, value in markers.items():
            if marker in marker_weights:
                self.weighted_score += value * marker_weights[marker]

        # Apply sigmoid function for probability
        self.churn_probability = 1 / (1 + math.exp(-5 * (self.weighted_score - 0.5)))

        # Determine risk level
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

    def apply_logarithmic_scaling(self, progress: float, k: float = 0.5, s0: float = 0.01) -> float:
        """Apply Weber-Fechner logarithmic scaling: ΔP = k * ln(S/S₀)."""
        if progress <= 0:
            return 0.0

        S = max(progress, s0)  # Current state, avoid log(0)
        scaled_value = k * math.log(S / s0)
        return min(1.0, max(0.0, scaled_value))

    def calculate_scaled_progress(self, raw_metrics: Dict[str, float]) -> Dict[str, float]:
        """Calculate scaled progress metrics."""
        scaled = {}

        for metric, value in raw_metrics.items():
            if self.scaling_type == ProgressVisualizationType.LOGARITHMIC:
                scaled[metric] = self.apply_logarithmic_scaling(value)
            else:
                scaled[metric] = value  # No scaling for other types

        return scaled


# Core System Classes
class DynamicDifficultyAdjustment:
    """Manages dynamic difficulty adjustment based on player performance."""

    def __init__(self):
        self.base_difficulty = 0.5
        self.current_difficulty = 0.5
        self.target_performance = 0.75
        self.adjustment_history = deque(maxlen=100)
        self.performance = PerformanceMetrics()

    def calculate_difficulty_adjustment(self, measured_performance: float) -> float:
        """
        Apply DDA formula: New_Difficulty = Base_Difficulty * (0.7 + 0.3 * (Target_Performance / Measured_Performance))
        """
        if measured_performance <= 0:
            measured_performance = 0.1  # Avoid division by zero

        adjustment_factor = 0.7 + 0.3 * (self.target_performance / measured_performance)
        new_difficulty = self.base_difficulty * adjustment_factor

        # Clamp to valid range and ensure maximum 15% adjustment
        max_adjustment = self.base_difficulty * 0.15
        new_difficulty = max(0.1, min(0.9, new_difficulty))
        new_difficulty = max(
            self.base_difficulty - max_adjustment,
            min(self.base_difficulty + max_adjustment, new_difficulty)
        )

        return new_difficulty

    def apply_statistical_smoothing(self,
        new_difficulty: float,
        smoothing_factor: float = 0.7) -> float:
        """Apply statistical smoothing to avoid jarring difficulty spikes."""
        smoothed_difficulty = (
            new_difficulty * smoothing_factor +
            self.current_difficulty * (1 - smoothing_factor)
        )

        # Record adjustment
        self.adjustment_history.append({
            'old_difficulty': self.current_difficulty,
            'new_difficulty': smoothed_difficulty,
            'percent_change': abs(smoothed_difficulty - self.current_difficulty) / max(0.1,
        self.current_difficulty),
            'timestamp': time.time()
        })

        self.current_difficulty = smoothed_difficulty
        return smoothed_difficulty

    def generate_encounter_difficulty(self, player_skill: float, sigma: float = 0.15) -> float:
        """Generate encounter difficulty using Gaussian distribution centered on player skill."""
        # Box-Muller transform for Gaussian distribution
        u1 = random.random()
        u2 = random.random()
        z0 = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)

        difficulty = player_skill + (z0 * sigma)
        return max(0.1, min(0.9, difficulty))

    def should_apply_micro_adjustment(self, recent_encounters: List[Dict[str, Any]]) -> Tuple[bool,
        float]:
        """Determine if micro-adjustment is needed based on success patterns."""
        if len(recent_encounters) < 2:
            return False, 0.0

        success_pattern = [e['success'] for e in recent_encounters]
        recent_success_rate = sum(success_pattern) / len(success_pattern)

        # Pattern detection
        if recent_success_rate >= 0.9:  # Too easy
            return True, 0.02  # Small increase
        elif recent_success_rate <= 0.3:  # Too hard
            return True, -0.02  # Small decrease

        # Check for streaks
        current_streak = 0
        max_streak = 0
        for success in success_pattern:
            if success:
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                current_streak = 0

        if max_streak >= 4:  # Winning streak
            return True, 0.03
        elif current_streak >= 3:  # Losing streak (current)
            return True, -0.03

        return False, 0.0


class FlowStateOptimizer:
    """Manages flow state optimization using Chen flow equation and Gaussian distribution."""

    def __init__(self):
        self.metrics = FlowStateMetrics()
        self.disruption_monitoring = True
        self.last_rebalance_time = 0.0

    def calculate_optimal_difficulty(self, player_skill: float) -> float:
        """Calculate optimal difficulty to maintain flow state (ratio 0.9-1.2)."""
        # Target ratio in the middle of optimal range
        target_ratio = (0.9 + 1.2) / 2  # 1.05
        return player_skill / target_ratio

    def detect_flow_disruption(self, session_data: Dict[str, Any]) -> bool:
        """Detect flow disruption signs in real-time."""
        indicators = {
            'rapid_failure_sequence': self._check_rapid_failures(session_data),
            'extended_inactivity': self._check_inactivity(session_data),
            'erratic_behavior': self._check_erratic_behavior(session_data),
            'frustration_signals': self._check_frustration(session_data)
        }

        # Flow disruption detected if multiple indicators are true
        disruption_count = sum(indicators.values())
        return disruption_count >= 2

    def _check_rapid_failures(self, session_data: Dict[str, Any]) -> bool:
        """Check for rapid sequence of failures."""
        recent_actions = session_data.get('recent_actions', [])
        if len(recent_actions) < 5:
            return False

        # Check if 4 out of last 5 actions were failures
        failures = sum(1 for action in recent_actions[-5:] if not action.get('success', True))
        return failures >= 4

    def _check_inactivity(self, session_data: Dict[str, Any]) -> bool:
        """Check for extended inactivity."""
        last_action_time = session_data.get('last_action_time', time.time())
        inactive_time = time.time() - last_action_time
        return inactive_time > 120  # 2 minutes of inactivity

    def _check_erratic_behavior(self, session_data: Dict[str, Any]) -> bool:
        """Check for erratic behavior patterns."""
        # Simple heuristic: inconsistent timing between actions
        action_times = session_data.get('action_times', [])
        if len(action_times) < 3:
            return False

        # Calculate variance in action timing
        time_diffs = [action_times[i] - action_times[i-1] for i in range(1, len(action_times))]
        if not time_diffs:
            return False

        variance = statistics.variance(time_diffs)
        return variance > 100  # High variance indicates erratic behavior

    def _check_frustration(self, session_data: Dict[str, Any]) -> bool:
        """Check for frustration signals."""
        frustration_level = session_data.get('frustration_level', 0.0)
        return frustration_level > 0.7

    def auto_rebalance(self, current_difficulty: float) -> float:
        """Automatically rebalance difficulty when flow disruption is detected."""
        rebalance_time = time.time()

        # Limit rebalance frequency
        if rebalance_time - self.last_rebalance_time < 30:  # 30 seconds minimum
            return current_difficulty

        # Apply adjustment based on current metrics
        if self.metrics.challenge_skill_ratio < 0.9:  # Too hard
            adjustment = -0.05
        elif self.metrics.challenge_skill_ratio > 1.2:  # Too easy
            adjustment = 0.05
        else:
            adjustment = 0.0

        self.last_rebalance_time = rebalance_time
        return max(0.1, min(0.9, current_difficulty + adjustment))


class RewardSystem:
    """Manages reinforcement learning reward schedules and prediction error modeling."""

    def __init__(self):
        self.schedule = RewardSchedule(RewardScheduleType.VARIABLE_RATIO)
        self.reward_history = deque(maxlen=1000)
        self.actions_since_last_reward = 0
        self.encounters_since_last_rare = 0
        self.total_motivation_index = 0.0
        self.player_sensitivity = "medium"

    def process_action(self, action_type: str, difficulty: float, time_investment: int,
        skill_required: float) -> Optional[RewardEvent]:
        """Process a player action and determine if reward should be given."""
        self.actions_since_last_reward += 1
        self.encounters_since_last_rare += 1

        # Calculate expected reward
        base_reward = 50
        difficulty_multiplier = 1 + difficulty
        time_multiplier = min(2.0, time_investment / 120)
        skill_multiplier = 1 + skill_required

        expected_reward = int(base_reward * difficulty_multiplier * time_multiplier * skill_multiplier)

        # Apply variable ratio schedule
        should_reward = self.schedule.should_reward(self.actions_since_last_reward)

        # Check for rare reward
        rare_prob = self.schedule.calculate_rare_reward_probability(self.encounters_since_last_rare)
        is_rare_reward = random.random() < rare_prob

        if should_reward or is_rare_reward:
            # Apply prediction error modeling
            novelty_factor = random.uniform(0.8, 1.3)
            received_reward = int(expected_reward * novelty_factor)

            # Calculate prediction error and motivation index
            prediction_error = received_reward - expected_reward
            motivation_index = prediction_error * novelty_factor * 0.73  # Formula from BDD

            # Create reward event
            reward_event = RewardEvent(
                id=len(self.reward_history),
                type=action_type,
                difficulty=difficulty,
                time_investment=time_investment,
                skill_required=skill_required,
                expected_reward=expected_reward,
                received_reward=received_reward,
                prediction_error=prediction_error,
                motivation_index=motivation_index,
                novelty_factor=novelty_factor,
                timestamp=time.time()
            )

            self.reward_history.append(reward_event)
            self.total_motivation_index += motivation_index
            self.actions_since_last_reward = 0

            if is_rare_reward:
                self.encounters_since_last_rare = 0

            return reward_event

        # No reward, but still track expected reward for prediction error
        prediction_error = -expected_reward
        motivation_index = prediction_error * 0.9 * 0.73  # Standard novelty factor for no reward
        self.total_motivation_index += motivation_index

        return None

    def analyze_player_response(self) -> Dict[str, Any]:
        """Analyze player response patterns to adapt reward schedule."""
        if len(self.reward_history) < 5:
            return {'player_sensitivity': 'unknown', 'adjustments_needed': []}

        recent_rewards = list(self.reward_history)[-10:]  # Last 10 rewards

        # Calculate player responsiveness metrics
        avg_motivation = sum(r.motivation_index for r in recent_rewards) / len(recent_rewards)
        avg_reward_size = sum(r.received_reward for r in recent_rewards) / len(recent_rewards)

        # Determine player sensitivity
        if avg_motivation > 20:
            self.player_sensitivity = 'high'
        elif avg_motivation > 10:
            self.player_sensitivity = 'medium'
        else:
            self.player_sensitivity = 'low'

        # Generate adjustment recommendations
        adjustments = []
        if self.player_sensitivity == 'high':
            adjustments.append('increase_base_reward')
        elif self.player_sensitivity == 'low':
            adjustments.append('add_bonus_rewards')

        # Analyze reward frequency
        avg_time_between = self._calculate_avg_time_between_rewards(recent_rewards)
        if avg_time_between < 3:
            adjustments.append('decrease_vr_ratio')
        elif avg_time_between > 7:
            adjustments.append('increase_vr_ratio')

        return {
            'player_sensitivity': self.player_sensitivity,
            'avg_motivation': avg_motivation,
            'avg_reward_size': avg_reward_size,
            'adjustments_needed': adjustments
        }

    def _calculate_avg_time_between_rewards(self, rewards: List[RewardEvent]) -> float:
        """Calculate average time between rewards."""
        if len(rewards) < 2:
            return 5.0  # Default

        time_diffs = [rewards[i].timestamp - rewards[i-1].timestamp for i in range(1, len(rewards))]
        return sum(time_diffs) / len(time_diffs)


class NeuroadaptiveEngagementSystem:
    """Manages neuroadaptive engagement tracking and churn prediction."""

    def __init__(self):
        self.engagement_score = EngagementScore()
        self.churn_analysis = ChurnRiskAnalysis()
        self.intervention_history = deque(maxlen=50)
        self.behavioral_data = deque(maxlen=1000)

    def track_behavior(self, action_type: str, timestamp: float, metadata: Dict[str, Any]) -> None:
        """Track player behavior for analysis."""
        behavior_entry = {
            'action_type': action_type,
            'timestamp': timestamp,
            'metadata': metadata
        }
        self.behavioral_data.append(behavior_entry)

    def calculate_engagement_metrics(self) -> Dict[str, float]:
        """Calculate comprehensive engagement metrics."""
        # Calculate metrics from behavioral data
        recent_data = [b for b in self.behavioral_data if time.time() - b['timestamp'] < 3600]  # Last hour

        if not recent_data:
            return {metric: 0.5 for metric in ['session_duration', 'action_frequency',
        'success_rate',
                                              'exploration_rate', 'social_interaction',
        'achievement_progress']}

        # Session duration (normalized to 0-1, assuming max 2 hours is optimal)
        session_duration = min(1.0, (time.time() - recent_data[0]['timestamp']) / 7200)

        # Action frequency (actions per minute)
        time_span = max(1, (recent_data[-1]['timestamp'] - recent_data[0]['timestamp']) / 60)
        action_frequency = min(1.0, len(recent_data) / (time_span * 30))  # Normalize to 30 actions per minute

        # Success rate
        success_actions = [b for b in recent_data if b['metadata'].get('success', False)]
        success_rate = len(success_actions) / len(recent_data) if recent_data else 0.5

        # Exploration rate (variety of action types)
        action_types = set(b['action_type'] for b in recent_data)
        exploration_rate = min(1.0, len(action_types) / 6)  # Assume 6 main action types

        # Social interaction rate
        social_actions = [b for b in recent_data if 'social' in b['action_type'].lower()]
        social_interaction = min(1.0, len(social_actions) / max(1, len(recent_data) * 0.2))

        # Achievement progress
        achievement_actions = [b for b in recent_data if 'achievement' in b['action_type'].lower()]
        achievement_progress = min(1.0, len(achievement_actions) / max(1, len(recent_data) * 0.1))

        metrics = {
            'session_duration': session_duration,
            'action_frequency': action_frequency,
            'success_rate': success_rate,
            'exploration_rate': exploration_rate,
            'social_interaction': social_interaction,
            'achievement_progress': achievement_progress
        }

        # Update engagement score
        self.engagement_score.calculate_score(metrics)

        return metrics

    def predict_churn_risk(self) -> Dict[str, Any]:
        """Predict player churn risk using behavioral markers."""
        # Calculate behavioral markers from recent data
        recent_data = [b for b in self.behavioral_data if time.time() - b['timestamp'] < 86400]  # Last 24 hours

        if len(recent_data) < 10:
            return {'risk_level': 'low', 'churn_probability': 0.1, 'confidence': 0.5}

        # Calculate behavioral markers
        markers = {
            'decreasing_session_length': self._calculate_session_trend(recent_data),
            'reduced_social_interaction': self._calculate_social_trend(recent_data),
            'achievement_stagnation': self._calculate_achievement_trend(recent_data),
            'increasing_failure_rate': self._calculate_failure_trend(recent_data),
            'login_frequency_decline': self._calculate_login_trend(recent_data),
            'negative_sentiment_indicators': self._calculate_sentiment_trend(recent_data)
        }

        # Calculate churn probability
        churn_prob = self.churn_analysis.calculate_risk(markers)

        return {
            'risk_level': self.churn_analysis.risk_level,
            'churn_probability': churn_prob,
            'confidence': self.churn_analysis.model_confidence,
            'behavioral_markers': markers
        }

    def should_trigger_intervention(self) -> Tuple[bool, Optional[InterventionType]]:
        """Determine if intervention should be triggered based on engagement."""
        engagement_score = self.engagement_score.overall_score
        session_duration = self.engagement_score.individual_metrics.get('session_duration', 0)

        # Check if engagement is below threshold for more than 3 minutes
        if engagement_score < 0.6 and session_duration > 3:
            # Select appropriate intervention type
            if engagement_score < 0.3:
                intervention = InterventionType.REWARD_BONUS
            elif engagement_score < 0.5:
                intervention = InterventionType.CONTENT_RECOMMENDATION
            else:
                intervention = InterventionType.ACHIEVEMENT_MILESTONE

            return True, intervention

        return False, None

    def _calculate_session_trend(self, data: List[Dict[str, Any]]) -> float:
        """Calculate decreasing session length trend (0-1, higher is worse)."""
        # Simplified: check if recent sessions are shorter
        return random.uniform(0.1, 0.9)  # Placeholder implementation

    def _calculate_social_trend(self, data: List[Dict[str, Any]]) -> float:
        """Calculate reduced social interaction trend (0-1, higher is worse)."""
        social_actions = [b for b in data if 'social' in b['action_type'].lower()]
        if len(social_actions) == 0:
            return 0.5

        # Calculate if social interaction is decreasing
        recent_social = [b for b in social_actions if time.time() - b['timestamp'] < 3600]
        return 0.5 if len(recent_social) > 0 else 0.8

    def _calculate_achievement_trend(self, data: List[Dict[str, Any]]) -> float:
        """Calculate achievement stagnation (0-1, higher is worse)."""
        achievement_actions = [b for b in data if 'achievement' in b['action_type'].lower()]
        return 0.3 if len(achievement_actions) > 0 else 0.7

    def _calculate_failure_trend(self, data: List[Dict[str, Any]]) -> float:
        """Calculate increasing failure rate (0-1, higher is worse)."""
        recent_failures = [b for b in data[-20:] if not b['metadata'].get('success', True)]
        return min(1.0, len(recent_failures) / max(1, len(data[-20:])))

    def _calculate_login_trend(self, data: List[Dict[str, Any]]) -> float:
        """Calculate login frequency decline (0-1, higher is worse)."""
        # Simplified: check if actions are spread out over time
        if len(data) < 2:
            return 0.5

        time_span = data[-1]['timestamp'] - data[0]['timestamp']
        avg_gap = time_span / len(data)
        return min(1.0, avg_gap / 3600)  # Normalize to hourly gaps

    def _calculate_sentiment_trend(self, data: List[Dict[str, Any]]) -> float:
        """Calculate negative sentiment indicators (0-1, higher is worse)."""
        # Look for frustration indicators in metadata
        frustration_indicators = [b for b in data if b['metadata'].get('frustration', 0) > 0.6]
        return min(1.0, len(frustration_indicators) / max(1, len(data) * 0.1))


class ProgressVisualizationSystem:
    """Manages progress visualization using Weber-Fechner law and optimal cognitive load."""

    def __init__(self):
        self.visualization = ProgressVisualization()
        self.experience_multiplier = 1.12
        self.base_experience = 100

    def calculate_experience_requirement(self, level: int) -> int:
        """Calculate experience requirement for given level using 1.12x multiplier."""
        if level == 1:
            return self.base_experience
        return int(self.base_experience * (self.experience_multiplier ** (level - 1)))

    def calculate_level_progress(self, current_exp: int, level_exp: int) -> float:
        """Calculate level progress with logarithmic scaling."""
        raw_progress = current_exp / max(1, level_exp)
        return self.visualization.apply_logarithmic_scaling(raw_progress)

    def calculate_mastery_advancement(self, mastery_level: int) -> Dict[str, float]:
        """Calculate mastery advancement with diminishing returns."""
        # Effort increases exponentially
        effort_required = int(10 * (1.2 ** (mastery_level - 1)))

        # Visible advancement decreases but remains perceptible
        if mastery_level == 1:
            advancement = 1.0
        else:
            advancement = 1.0 / math.sqrt(mastery_level - 1)

        return {
            'effort_required': effort_required,
            'visible_advancement': min(1.0, max(0.1, advancement)),
            'total_effort_to_level': effort_required
        }

    def apply_logarithmic_scaling(self,
        raw_progress: float,
        k: float = 0.5,
        s0: float = 0.01) -> float:
        """Apply Weber-Fechner law: ΔP = k * ln(S/S₀)."""
        return self.visualization.apply_logarithmic_scaling(raw_progress)

    def calculate_constant_perceived_effort(self, progression_levels: List[float]) -> float:
        """Calculate variance in perceived effort across progression levels."""
        perceived_efforts = []
        k = 0.3  # Effort scaling constant
        S0 = 0.05  # Minimum progress

        for level in progression_levels:
            if level > S0:
                perceived_effort = k * math.log(level / S0)
            else:
                perceived_effort = 0.0
            perceived_efforts.append(perceived_effort)

        # Calculate variance ratio
        avg_effort = sum(perceived_efforts) / len(perceived_efforts)
        variance = sum((e - avg_effort) ** 2 for e in perceived_efforts) / len(perceived_efforts)
        std_dev = math.sqrt(variance)

        return std_dev / avg_effort if avg_effort > 0 else 0.0


class ContentVarietyOptimizer:
    """Manages content variety using Wundt curve and exploration-exploitation balance."""

    def __init__(self):
        self.content_exposure = {ct.value: 0.0 for ct in ContentVarietyType}
        self.exploration_epsilon = 0.1  # ε-greedy exploration rate
        self.wundt_optimal_range = (0.8, 1.0)

    def calculate_content_novelty(self, content_type: ContentVarietyType) -> float:
        """Calculate content novelty using Wundt curve: Y = e^(-X^2)."""
        recent_exposure = self.content_exposure[content_type.value]

        # Standardize novelty around 0.5
        standardized_novelty = (recent_exposure - 0.5) / 0.5

        # Apply Wundt curve
        wundt_value = math.exp(-(standardized_novelty ** 2))
        return wundt_value

    def should_exploit_or_explore(self) -> bool:
        """Determine whether to exploit known preferences or explore new content."""
        return random.random() < self.exploration_epsilon

    def recommend_content(self) -> ContentVarietyType:
        """Recommend content type using exploration-exploitation balance."""
        if self.should_exploit_or_explore():
            # Explore: choose content with highest novelty
            content_novelties = {
                ct: self.calculate_content_novelty(ct)
                for ct in ContentVarietyType
            }
            return max(content_novelties, key=content_novelties.get)
        else:
            # Exploit: choose content with optimal novelty (but not overexposed)
            optimal_content = []
            for ct in ContentVarietyType:
                novelty = self.calculate_content_novelty(ct)
                if self.wundt_optimal_range[0] <= novelty <= self.wundt_optimal_range[1]:
                    optimal_content.append(ct)

            return random.choice(optimal_content) if optimal_content else random.choice(list(ContentVarietyType))

    def update_content_exposure(self,
        content_type: ContentVarietyType,
        exposure_amount: float = 0.1) -> None:
        """Update content exposure tracking."""
        current = self.content_exposure[content_type.value]
        self.content_exposure[content_type.value] = min(1.0, current + exposure_amount)

        # Decay other content types slightly
        for ct in ContentVarietyType:
            if ct != content_type:
                self.content_exposure[ct.value] = max(0.0, self.content_exposure[ct.value] - 0.01)

    def get_content_variety_analysis(self) -> Dict[str, Any]:
        """Get analysis of content variety across all types."""
        novelty_scores = {
            ct.value: self.calculate_content_novelty(ct)
            for ct in ContentVarietyType
        }

        under_stimulated = [ct for ct, score in novelty_scores.items() if score < 0.3]
        optimally_stimulated = [ct for ct, score in novelty_scores.items() if 0.3 <= score <= 0.8]
        over_stimulated = [ct for ct, score in novelty_scores.items() if score > 0.8]

        return {
            'content_novelty_scores': novelty_scores,
            'under_stimulated_content': under_stimulated,
            'optimally_stimulated_content': optimally_stimulated,
            'over_stimulated_content': over_stimulated,
            'variety_balance': len(optimally_stimulated) / len(ContentVarietyType)
        }


class InterventionSystem:
    """Manages intervention mechanisms for player engagement."""

    def __init__(self):
        self.intervention_history = deque(maxlen=100)
        self.available_interventions = list(InterventionType)

    def trigger_intervention(self, intervention_type: InterventionType, context: Dict[str,
        Any]) -> Dict[str, Any]:
        """Trigger a specific intervention type."""
        intervention_data = {
            'type': intervention_type,
            'timestamp': time.time(),
            'context': context,
            'effectiveness': 0.0,
            'outcome': None
        }

        # Apply intervention effects based on type
        if intervention_type == InterventionType.DYNAMIC_DIFFICULTY:
            intervention_data['outcome'] = self._apply_difficulty_adjustment(context)
        elif intervention_type == InterventionType.CONTENT_RECOMMENDATION:
            intervention_data['outcome'] = self._recommend_content(context)
        elif intervention_type == InterventionType.REWARD_BONUS:
            intervention_data['outcome'] = self._provide_bonus_reward(context)
        elif intervention_type == InterventionType.ACHIEVEMENT_MILESTONE:
            intervention_data['outcome'] = self._unlock_milestone(context)
        else:
            intervention_data['outcome'] = self._apply_generic_intervention(intervention_type,
        context)

        self.intervention_history.append(intervention_data)
        return intervention_data

    def _apply_difficulty_adjustment(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Apply difficulty adjustment intervention."""
        current_difficulty = context.get('current_difficulty', 0.5)
        player_performance = context.get('player_performance', 0.5)

        # Adjust difficulty based on performance
        if player_performance < 0.3:
            new_difficulty = max(0.1, current_difficulty - 0.1)
        elif player_performance > 0.8:
            new_difficulty = min(0.9, current_difficulty + 0.05)
        else:
            new_difficulty = current_difficulty

        return {
            'difficulty_adjusted': True,
            'old_difficulty': current_difficulty,
            'new_difficulty': new_difficulty,
            'adjustment_reason': 'performance_based'
        }

    def _recommend_content(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Recommend appropriate content."""
        player_preferences = context.get('player_preferences', {})
        current_engagement = context.get('engagement_level', 0.5)

        # Simple recommendation logic
        if current_engagement < 0.3:
            recommended_content = 'high_reward_quest'
        elif current_engagement < 0.6:
            recommended_content = 'balanced_challenge'
        else:
            recommended_content = 'mastery_opportunity'

        return {
            'content_recommended': True,
            'recommended_type': recommended_content,
            'reason': 'engagement_based'
        }

    def _provide_bonus_reward(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Provide bonus reward to boost motivation."""
        bonus_amount = random.randint(50, 200)
        return {
            'bonus_rewarded': True,
            'bonus_amount': bonus_amount,
            'reward_type': 'motivation_bonus'
        }

    def _unlock_milestone(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Unlock achievement milestone."""
        player_progress = context.get('player_progress', {})
        return {
            'milestone_unlocked': True,
            'milestone_type': 'progress_milestone',
            'progress_percentage': player_progress.get('percentage', 0)
        }

    def _apply_generic_intervention(self, intervention_type: InterventionType, context: Dict[str,
        Any]) -> Dict[str, Any]:
        """Apply generic intervention for other types."""
        return {
            'intervention_applied': True,
            'type': intervention_type.value,
            'context_processed': bool(context)
        }


# Main Gamification System
class GamificationSystem:
    """Main interface for the Modern Gamification System."""

    def __init__(self):
        self.dda = DynamicDifficultyAdjustment()
        self.flow_optimizer = FlowStateOptimizer()
        self.reward_system = RewardSystem()
        self.engagement_system = NeuroadaptiveEngagementSystem()
        self.progress_visualization = ProgressVisualizationSystem()
        self.content_variety = ContentVarietyOptimizer()
        self.intervention_system = InterventionSystem()

        # Player state tracking
        self.player_state = {
            'session_start_time': time.time(),
            'current_session_duration': 0,
            'total_playtime': 0,
            'last_action_time': time.time(),
            'actions_this_session': 0,
            'current_level': 1,
            'total_experience': 0,
            'skill_level': 0.5,
            'motivation_level': 0.7,
            'engagement_history': deque(maxlen=100)
        }

    def initialize_system(self) -> Dict[str, Any]:
        """Initialize the gamification system."""
        return {
            'status': 'initialized',
            'framework_version': '2025',
            'systems_active': [
                'dynamic_difficulty_adjustment',
                'flow_state_optimization',
                'reinforcement_learning_rewards',
                'neuroadaptive_engagement',
                'progress_visualization',
                'content_variety_optimization'
            ],
            'initial_difficulty': self.dda.current_difficulty,
            'target_performance': self.dda.target_performance
        }

    def process_player_action(self, action_type: str, success: bool, time_taken: int,
                             difficulty: float = None,
        metadata: Dict[str,
        Any] = None) -> Dict[str,
        Any]:
        """Process a player action through all gamification systems."""
        metadata = metadata or {}

        # Update player state
        self.player_state['last_action_time'] = time.time()
        self.player_state['actions_this_session'] += 1
        self.player_state['current_session_duration'] = time.time() - self.player_state['session_start_time']

        # Use current difficulty if not provided
        if difficulty is None:
            difficulty = self.dda.current_difficulty

        # Track behavior for engagement analysis
        self.engagement_system.track_behavior(
            action_type, time.time(),
            {**metadata, 'success': success, 'time_taken': time_taken, 'difficulty': difficulty}
        )

        # Update performance metrics
        self.dda.performance.add_encounter(success, time_taken, 0.5)  # Assume 50% resource usage
        performance_score = self.dda.performance.calculate_score()

        # Check for difficulty adjustment
        encounters = self.dda.performance.recent_encounters
        should_adjust, adjustment_amount = self.dda.should_apply_micro_adjustment(encounters)

        if should_adjust:
            new_difficulty = self.dda.apply_statistical_smoothing(
                self.dda.calculate_difficulty_adjustment(performance_score) + adjustment_amount
            )
        else:
            new_difficulty = self.dda.current_difficulty

        # Process reward
        reward_event = self.reward_system.process_action(
            action_type, difficulty, time_taken, self.player_state['skill_level']
        )

        # Update flow state metrics
        self.player_state['motivation_level'] = min(1.0, self.reward_system.total_motivation_index / 100)

        # Check for flow disruption
        session_data = {
            'recent_actions': encounters[-5:],
            'last_action_time': self.player_state['last_action_time'],
            'frustration_level': 1.0 - (performance_score * self.player_state['motivation_level'])
        }

        if self.flow_optimizer.detect_flow_disruption(session_data):
            new_difficulty = self.flow_optimizer.auto_rebalance(new_difficulty)

        # Update content variety
        if 'content_type' in metadata:
            content_type = ContentVarietyType(metadata['content_type'])
            self.content_variety.update_content_exposure(content_type)

        # Check for intervention needs
        engagement_metrics = self.engagement_system.calculate_engagement_metrics()
        should_intervene, intervention_type = self.engagement_system.should_trigger_intervention()

        intervention_result = None
        if should_intervene:
            intervention_result = self.intervention_system.trigger_intervention(
                intervention_type,
                {
                    'player_performance': performance_score,
                    'engagement_level': engagement_metrics.get('session_duration', 0.5),
                    'current_difficulty': new_difficulty,
                    'player_preferences': {'preferred_content': content_type.value if 'content_type' in metadata else 'combat'}
                }
            )

        return {
            'action_processed': True,
            'success': success,
            'performance_score': performance_score,
            'difficulty_adjusted': new_difficulty != self.dda.current_difficulty,
            'new_difficulty': new_difficulty,
            'reward_given': reward_event is not None,
            'reward_details': {
                'amount': reward_event.received_reward if reward_event else 0,
                'motivation_index': reward_event.motivation_index if reward_event else 0
            } if reward_event else None,
            'flow_disruption_detected': self.flow_optimizer.detect_flow_disruption(session_data),
            'engagement_score': engagement_metrics,
            'intervention_triggered': should_intervene,
            'intervention_result': intervention_result
        }

    def get_player_analytics(self) -> Dict[str, Any]:
        """Get comprehensive player analytics."""
        # Calculate current analytics
        engagement_metrics = self.engagement_system.calculate_engagement_metrics()
        churn_risk = self.engagement_system.predict_churn_risk()
        content_analysis = self.content_variety.get_content_variety_analysis()
        reward_analysis = self.reward_system.analyze_player_response()

        # Get progress data
        current_level = self.player_state['current_level']
        level_exp = self.progress_visualization.calculate_experience_requirement(current_level)
        level_progress = self.progress_visualization.calculate_level_progress(
            self.player_state['total_experience'], level_exp
        )

        return {
            'player_state': {
                'current_level': current_level,
                'total_experience': self.player_state['total_experience'],
                'skill_level': self.player_state['skill_level'],
                'motivation_level': self.player_state['motivation_level'],
                'session_duration': self.player_state['current_session_duration'],
                'actions_this_session': self.player_state['actions_this_session']
            },
            'performance': {
                'success_rate': self.dda.performance.success_rate,
                'time_efficiency': self.dda.performance.time_efficiency,
                'resource_efficiency': self.dda.performance.resource_efficiency,
                'overall_score': self.dda.performance.overall_score,
                'current_difficulty': self.dda.current_difficulty,
                'difficulty_history': list(self.dda.adjustment_history)[-10:]  # Last 10 adjustments
            },
            'engagement': {
                'overall_score': self.engagement_system.engagement_score.overall_score,
                'engagement_level': self.engagement_system.engagement_score.engagement_level,
                'individual_metrics': engagement_metrics,
                'churn_risk': churn_risk,
                'intervention_history': list(self.engagement_system.intervention_history)[-5:]  # Last 5 interventions
            },
            'rewards': {
                'total_motivation_index': self.reward_system.total_motivation_index,
                'player_sensitivity': self.reward_system.player_sensitivity,
                'reward_schedule_adjustments': reward_analysis.get('adjustments_needed', []),
                'recent_rewards': len(self.reward_system.reward_history)
            },
            'content': {
                'content_variety': content_analysis,
                'recommendations': self.content_variety.recommend_content().value
            },
            'progress': {
                'level_progress': level_progress,
                'next_level_requirement': self.progress_visualization.calculate_experience_requirement(current_level + 1),
                'mastery_advancement': self.progress_visualization.calculate_mastery_advancement(1)
            }
        }

    def update_player_skill(self, new_skill_level: float) -> None:
        """Update player's skill level."""
        self.player_state['skill_level'] = max(0.1, min(1.0, new_skill_level))

        # Trigger difficulty recalculation
        target_difficulty = self.flow_optimizer.calculate_optimal_difficulty(new_skill_level)
        self.dda.current_difficulty = target_difficulty

    def add_experience(self, exp_amount: int) -> Dict[str, Any]:
        """Add experience to player and handle level progression."""
        old_level = self.player_state['current_level']
        self.player_state['total_experience'] += exp_amount

        # Check for level up
        required_exp = self.progress_visualization.calculate_experience_requirement(old_level)

        level_ups = 0
        while self.player_state['total_experience'] >= required_exp:
            self.player_state['total_experience'] -= required_exp
            level_ups += 1
            self.player_state['current_level'] += 1
            required_exp = self.progress_visualization.calculate_experience_requirement(self.player_state['current_level'])

        return {
            'experience_added': exp_amount,
            'old_level': old_level,
            'new_level': self.player_state['current_level'],
            'levels_gained': level_ups,
            'total_experience': self.player_state['total_experience'],
            'next_level_requirement': required_exp
        }

    def get_system_statistics(self) -> Dict[str, Any]:
        """Get overall system statistics."""
        return {
            'total_sessions_processed': len(self.engagement_system.intervention_history),
            'total_rewards_distributed': len(self.reward_system.reward_history),
            'average_motivation_index': self.reward_system.total_motivation_index / max(1,
        len(self.reward_system.reward_history)),
            'difficulty_adjustments': len(self.dda.adjustment_history),
            'current_player_count': 1,  # Simplified for single-player
            'system_uptime': time.time() - self.player_state['session_start_time'],
            'active_interventions': len([i for i in self.engagement_system.intervention_history if time.time() - i.get('timestamp', 0) < 300])  # Last 5 minutes
        }


# Create global instance
_gamification_system = None

def get_gamification_system() -> GamificationSystem:
    """Get global gamification system instance."""
    global _gamification_system
    if _gamification_system is None:
        _gamification_system = GamificationSystem()
    return _gamification_system

def create_gamification_system() -> GamificationSystem:
    """Create new gamification system instance."""
    return GamificationSystem()
