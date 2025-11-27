"""
Unit tests for Modern Gamification System.

Tests dynamic difficulty adjustment, flow state optimization,
reinforcement learning reward schedules, neuroadaptive engagement systems,
progress visualization with Weber-Fechner law, and advanced psychological principles.
"""

import unittest
import random
import time
import math
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.systems.gamification import (
    DifficultyAdjustmentType, EngagementMetricType, RewardScheduleType,
    InterventionType, ContentVarietyType, MotivationPillar,
    ProgressVisualizationType, PerformanceMetrics, FlowStateMetrics,
    RewardEvent, RewardSchedule, EngagementScore, ChurnRiskAnalysis,
    ProgressVisualization, DynamicDifficultyAdjustment,
    FlowStateOptimizer, RewardSystem, NeuroadaptiveEngagementSystem,
    ProgressVisualizationSystem, ContentVarietyOptimizer,
    InterventionSystem, GamificationSystem,
    get_gamification_system, create_gamification_system
)


class TestPerformanceMetrics(unittest.TestCase):
    """Test PerformanceMetrics functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.metrics = PerformanceMetrics()

    def test_initialization(self):
        """Test metrics initialization."""
        self.assertEqual(self.metrics.success_rate, 0.0)
        self.assertEqual(self.metrics.time_efficiency, 0.0)
        self.assertEqual(self.metrics.resource_efficiency, 0.0)
        self.assertEqual(self.metrics.overall_score, 0.0)
        self.assertEqual(len(self.metrics.recent_encounters), 0)

    def test_calculate_score(self):
        """Test performance score calculation."""
        self.metrics.success_rate = 0.8
        self.metrics.time_efficiency = 0.7
        self.metrics.resource_efficiency = 0.9

        score = self.metrics.calculate_score()
        expected = 0.8 * 0.4 + 0.7 * 0.3 + 0.9 * 0.3  # 0.32 + 0.21 + 0.27 = 0.80

        self.assertEqual(score, 0.8)
        self.assertEqual(self.metrics.overall_score, 0.8)

    def test_add_encounter(self):
        """Test adding encounter data."""
        self.metrics.add_encounter(success=True, time_taken=120, resources_used=0.5)
        self.metrics.add_encounter(success=False, time_taken=180, resources_used=0.7)

        self.assertEqual(len(self.metrics.recent_encounters), 2)
        self.assertEqual(self.metrics.recent_encounters[0]['success'], True)
        self.assertEqual(self.metrics.recent_encounters[1]['success'], False)

    def test_encounter_limit(self):
        """Test that encounters are limited to last 10."""
        # Add 15 encounters
        for i in range(15):
            self.metrics.add_encounter(success=i % 2 == 0, time_taken=120, resources_used=0.5)

        self.assertEqual(len(self.metrics.recent_encounters), 10)
        # Should keep the most recent 10
        self.assertEqual(self.metrics.recent_encounters[-1]['success'], True)  # 14th encounter (even index)

    def test_metrics_update_after_encounters(self):
        """Test that metrics are updated after adding encounters."""
        # Add encounters with known patterns
        successes = [True, True, True, False, True]  # 80% success rate
        for success in successes:
            self.metrics.add_encounter(success=success, time_taken=120, resources_used=0.5)

        self.metrics.calculate_score()

        self.assertAlmostEqual(self.metrics.success_rate, 0.8, places=2)


class TestFlowStateMetrics(unittest.TestCase):
    """Test FlowStateMetrics functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.metrics = FlowStateMetrics()

    def test_initialization(self):
        """Test metrics initialization."""
        self.assertEqual(self.metrics.challenge_skill_ratio, 1.0)
        self.assertEqual(self.metrics.engagement_level, 0.5)
        self.assertIsInstance(self.metrics.focus_metrics, dict)
        self.assertIsInstance(self.metrics.emotional_indicators, dict)
        self.assertIsInstance(self.metrics.flow_indicators, list)

    def test_calculate_flow_score_optimal(self):
        """Test flow score calculation in optimal range."""
        self.metrics.challenge_skill_ratio = 1.05  # In optimal range
        score = self.metrics.calculate_flow_score()
        self.assertEqual(score, 1.0)

    def test_calculate_flow_score_below_optimal(self):
        """Test flow score calculation below optimal range."""
        self.metrics.challenge_skill_ratio = 0.6
        score = self.metrics.calculate_flow_score()
        self.assertAlmostEqual(score, 0.6 / 0.9, places=2)

    def test_calculate_flow_score_above_optimal(self):
        """Test flow score calculation above optimal range."""
        self.metrics.challenge_skill_ratio = 1.5
        score = self.metrics.calculate_flow_score()
        self.assertLess(score, 1.0)
        self.assertGreaterEqual(score, 0.0)

    def test_update_engagement(self):
        """Test engagement metrics update."""
        self.metrics.update_engagement(
            actions_per_minute=15.0,
            decision_accuracy=0.85,
            error_rate=0.15,
            enjoyment=0.8,
            frustration=0.2,
            motivation=0.9
        )

        self.assertEqual(self.metrics.focus_metrics['actions_per_minute'], 15.0)
        self.assertEqual(self.metrics.focus_metrics['decision_accuracy'], 0.85)
        self.assertEqual(self.metrics.focus_metrics['error_rate'], 0.15)
        self.assertEqual(self.metrics.emotional_indicators['enjoyment_level'], 0.8)
        self.assertEqual(self.metrics.emotional_indicators['frustration_level'], 0.2)
        self.assertEqual(self.metrics.emotional_indicators['motivation_level'], 0.9)


class TestRewardSchedule(unittest.TestCase):
    """Test RewardSchedule functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.schedule = RewardSchedule(RewardScheduleType.VARIABLE_RATIO)

    def test_initialization(self):
        """Test schedule initialization."""
        self.assertEqual(self.schedule.schedule_type, RewardScheduleType.VARIABLE_RATIO)
        self.assertEqual(self.schedule.variable_ratio_min, 5)
        self.assertEqual(self.schedule.variable_ratio_max, 10)
        self.assertTrue(self.schedule.adaptation_enabled)

    def test_should_reward_variable_ratio(self):
        """Test variable ratio reward determination."""
        # Should not reward initially
        self.assertFalse(self.schedule.should_reward(3))

        # Should reward when exceeding variable ratio
        with patch('random.randint', return_value=5):
            self.assertTrue(self.schedule.should_reward(5))

    def test_calculate_rare_reward_probability(self):
        """Test rare reward probability calculation."""
        # P = 0.05 * (1 - e^(-n/20))

        # Test with 0 encounters
        prob = self.schedule.calculate_rare_reward_probability(0)
        self.assertEqual(prob, 0.0)  # e^0 = 1, so (1 - 1) = 0

        # Test with some encounters
        prob = self.schedule.calculate_rare_reward_probability(20)
        expected = 0.05 * (1 - math.exp(-1.0))
        self.assertAlmostEqual(prob, expected, places=4)

        # Test with many encounters (should approach 0.05)
        prob = self.schedule.calculate_rare_reward_probability(100)
        self.assertLess(prob, 0.05)
        self.assertGreater(prob, 0.04)


class TestEngagementScore(unittest.TestCase):
    """Test EngagementScore functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.engagement = EngagementScore()

    def test_initialization(self):
        """Test engagement score initialization."""
        self.assertIsInstance(self.engagement.individual_metrics, dict)
        self.assertIsInstance(self.engagement.weights, dict)
        self.assertEqual(self.engagement.overall_score, 0.0)
        self.assertEqual(self.engagement.engagement_level, "medium")

    def test_calculate_score_default_weights(self):
        """Test score calculation with default weights."""
        metrics = {
            'session_duration': 0.8,
            'action_frequency': 0.7,
            'success_rate': 0.9,
            'exploration_rate': 0.6,
            'social_interaction': 0.5,
            'achievement_progress': 0.8
        }

        score = self.engagement.calculate_score(metrics)

        # Expected: 0.8*0.25 + 0.7*0.20 + 0.9*0.15 + 0.6*0.15 + 0.5*0.10 + 0.8*0.15
        expected = 0.20 + 0.14 + 0.135 + 0.09 + 0.05 + 0.12  # 0.735
        self.assertAlmostEqual(score, expected, places=3)
        self.assertEqual(self.engagement.engagement_level, "high")

    def test_engagement_levels(self):
        """Test engagement level determination."""
        # Test low engagement
        self.engagement.calculate_score({'session_duration': 0.1, 'action_frequency': 0.1,
                                        'success_rate': 0.1, 'exploration_rate': 0.1,
                                        'social_interaction': 0.1, 'achievement_progress': 0.1})
        self.assertEqual(self.engagement.engagement_level, "low")

        # Test high engagement
        self.engagement.calculate_score({'session_duration': 0.9, 'action_frequency': 0.9,
                                        'success_rate': 0.9, 'exploration_rate': 0.9,
                                        'social_interaction': 0.9, 'achievement_progress': 0.9})
        self.assertEqual(self.engagement.engagement_level, "high")


class TestChurnRiskAnalysis(unittest.TestCase):
    """Test ChurnRiskAnalysis functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.churn = ChurnRiskAnalysis()

    def test_initialization(self):
        """Test churn analysis initialization."""
        self.assertIsInstance(self.churn.behavioral_markers, dict)
        self.assertEqual(self.churn.weighted_score, 0.0)
        self.assertEqual(self.churn.churn_probability, 0.0)
        self.assertEqual(self.churn.risk_level, "low")
        self.assertEqual(self.churn.model_confidence, 0.85)

    def test_calculate_risk_low(self):
        """Test low risk calculation."""
        markers = {
            'decreasing_session_length': 0.1,
            'reduced_social_interaction': 0.2,
            'achievement_stagnation': 0.1,
            'increasing_failure_rate': 0.1,
            'login_frequency_decline': 0.1,
            'negative_sentiment_indicators': 0.0
        }

        risk = self.churn.calculate_risk(markers)

        self.assertLess(risk, 0.3)
        self.assertEqual(self.churn.risk_level, "low")

    def test_calculate_risk_high(self):
        """Test high risk calculation."""
        markers = {
            'decreasing_session_length': 0.9,
            'reduced_social_interaction': 0.8,
            'achievement_stagnation': 0.9,
            'increasing_failure_rate': 0.8,
            'login_frequency_decline': 0.9,
            'negative_sentiment_indicators': 0.7
        }

        risk = self.churn.calculate_risk(markers)

        self.assertGreater(risk, 0.7)
        self.assertEqual(self.churn.risk_level, "high")

    def test_sigmoid_function(self):
        """Test sigmoid function properties."""
        # Weighted score of 0.5 should give churn probability of 0.5
        markers = {
            'decreasing_session_length': 0.5,
            'reduced_social_interaction': 0.5,
            'achievement_stagnation': 0.5,
            'increasing_failure_rate': 0.5,
            'login_frequency_decline': 0.5,
            'negative_sentiment_indicators': 0.5
        }

        risk = self.churn.calculate_risk(markers)
        self.assertAlmostEqual(risk, 0.5, places=2)


class TestProgressVisualization(unittest.TestCase):
    """Test ProgressVisualization functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.progress = ProgressVisualization()

    def test_initialization(self):
        """Test progress visualization initialization."""
        self.assertEqual(self.progress.level_progress, 0.0)
        self.assertEqual(self.progress.scaling_type, ProgressVisualizationType.LOGARITHMIC)

    def test_apply_logarithmic_scaling(self):
        """Test logarithmic scaling application."""
        # Test zero input
        result = self.progress.apply_logarithmic_scaling(0)
        self.assertEqual(result, 0.0)

        # Test positive input
        result = self.progress.apply_logarithmic_scaling(0.5)
        self.assertGreater(result, 0.0)
        self.assertLessEqual(result, 1.0)

        # Test higher input should have compressed scaling
        low_result = self.progress.apply_logarithmic_scaling(0.2)
        high_result = self.progress.apply_logarithmic_scaling(0.8)

        # Logarithmic scaling should compress high values more
        self.assertLess(high_result / 0.8, low_result / 0.2)

    def test_calculate_scaled_progress(self):
        """Test scaled progress calculation."""
        raw_metrics = {
            'level_progress': 0.3,
            'skill_progress': 0.6,
            'achievement_progress': 0.9
        }

        scaled = self.progress.calculate_scaled_progress(raw_metrics)

        self.assertIn('level_progress', scaled)
        self.assertIn('skill_progress', scaled)
        self.assertIn('achievement_progress', scaled)

        # With logarithmic scaling, lower values should be proportionally higher
        self.assertGreater(scaled['level_progress'] / 0.3, scaled['achievement_progress'] / 0.9)


class TestDynamicDifficultyAdjustment(unittest.TestCase):
    """Test DynamicDifficultyAdjustment functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.dda = DynamicDifficultyAdjustment()

    def test_initialization(self):
        """Test DDA initialization."""
        self.assertEqual(self.dda.base_difficulty, 0.5)
        self.assertEqual(self.dda.current_difficulty, 0.5)
        self.assertEqual(self.dda.target_performance, 0.75)

    def test_calculate_difficulty_adjustment_formula(self):
        """Test DDA formula implementation."""
        # Test with performance exactly at target
        adjustment = self.dda.calculate_difficulty_adjustment(0.75)
        expected = 0.5 * (0.7 + 0.3 * (0.75 / 0.75))  # 0.5 * 1.0 = 0.5
        self.assertEqual(adjustment, expected)

        # Test with performance below target (should increase difficulty)
        adjustment = self.dda.calculate_difficulty_adjustment(0.5)
        expected = 0.5 * (0.7 + 0.3 * (0.75 / 0.5))  # 0.5 * (0.7 + 0.45) = 0.575
        self.assertAlmostEqual(adjustment, expected, places=3)

    def test_maximum_15_percent_adjustment(self):
        """Test that difficulty adjustment is limited to 15%."""
        base_difficulty = self.dda.base_difficulty
        max_allowed = base_difficulty * 0.15

        # Test with very low performance (should try to increase significantly)
        adjustment = self.dda.calculate_difficulty_adjustment(0.1)
        max_increase = base_difficulty + max_allowed
        self.assertLessEqual(adjustment, max_increase)

        # Test with very high performance (should try to decrease significantly)
        adjustment = self.dda.calculate_difficulty_adjustment(1.0)
        min_allowed = base_difficulty - max_allowed
        self.assertGreaterEqual(adjustment, min_allowed)

    def test_statistical_smoothing(self):
        """Test statistical smoothing application."""
        old_difficulty = self.dda.current_difficulty
        new_difficulty = 0.7
        smoothing_factor = 0.7

        smoothed = self.dda.apply_statistical_smoothing(new_difficulty, smoothing_factor)
        expected = new_difficulty * smoothing_factor + old_difficulty * (1 - smoothing_factor)

        self.assertAlmostEqual(smoothed, expected, places=3)
        self.assertEqual(self.dda.current_difficulty, smoothed)

    def test_gaussian_difficulty_generation(self):
        """Test Gaussian difficulty generation."""
        player_skill = 0.5
        sigma = 0.15

        # Generate multiple difficulties
        difficulties = [self.dda.generate_encounter_difficulty(player_skill, sigma) for _ in range(100)]

        # All difficulties should be in valid range
        for difficulty in difficulties:
            self.assertGreaterEqual(difficulty, 0.1)
            self.assertLessEqual(difficulty, 0.9)

        # Calculate mean and standard deviation
        mean_difficulty = sum(difficulties) / len(difficulties)
        variance = sum((d - mean_difficulty) ** 2 for d in difficulties) / len(difficulties)
        std_dev = math.sqrt(variance)

        # Should be close to player skill and target sigma
        self.assertLess(abs(mean_difficulty - player_skill), 0.05)
        self.assertLess(abs(std_dev - sigma), 0.03)

    def test_micro_adjustment_detection(self):
        """Test micro-adjustment detection."""
        # Test high success rate (should increase difficulty)
        high_success_encounters = [{'success': True} for _ in range(6)]
        should_adjust, amount = self.dda.should_apply_micro_adjustment(high_success_encounters)
        self.assertTrue(should_adjust)
        self.assertGreater(amount, 0)

        # Test low success rate (should decrease difficulty)
        low_success_encounters = [{'success': False} for _ in range(6)]
        should_adjust, amount = self.dda.should_apply_micro_adjustment(low_success_encounters)
        self.assertTrue(should_adjust)
        self.assertLess(amount, 0)

        # Test mixed success rate (should not adjust)
        mixed_encounters = [{'success': i % 2 == 0} for i in range(6)]
        should_adjust, amount = self.dda.should_apply_micro_adjustment(mixed_encounters)
        self.assertFalse(should_adjust)
        self.assertEqual(amount, 0)


class TestFlowStateOptimizer(unittest.TestCase):
    """Test FlowStateOptimizer functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.optimizer = FlowStateOptimizer()

    def test_initialization(self):
        """Test optimizer initialization."""
        self.assertTrue(self.optimizer.disruption_monitoring)
        self.assertEqual(self.optimizer.last_rebalance_time, 0.0)

    def test_calculate_optimal_difficulty(self):
        """Test optimal difficulty calculation."""
        player_skill = 0.6
        optimal_difficulty = self.optimizer.calculate_optimal_difficulty(player_skill)

        # Should be player_skill / target_ratio (1.05)
        expected = player_skill / 1.05
        self.assertAlmostEqual(optimal_difficulty, expected, places=3)

    def test_flow_disruption_detection(self):
        """Test flow disruption detection."""
        # Test normal session (no disruption)
        normal_session = {
            'recent_actions': [{'success': True} for _ in range(10)],
            'last_action_time': time.time() - 30,
            'frustration_level': 0.2
        }
        self.assertFalse(self.optimizer.detect_flow_disruption(normal_session))

        # Test disrupted session (multiple failure indicators)
        disrupted_session = {
            'recent_actions': [{'success': False} for _ in range(5)],
            'last_action_time': time.time() - 300,  # 5 minutes ago
            'frustration_level': 0.8
        }
        self.assertTrue(self.optimizer.detect_flow_disruption(disrupted_session))

    def test_auto_rebalance_frequency_limit(self):
        """Test that auto-rebalance respects frequency limits."""
        current_difficulty = 0.5

        # First rebalance should work
        self.optimizer.last_rebalance_time = time.time() - 40  # 40 seconds ago
        result = self.optimizer.auto_rebalance(current_difficulty)
        self.assertIsNotNone(result)

        # Immediate second rebalance should not work
        self.optimizer.last_rebalance_time = time.time() - 10  # 10 seconds ago
        result = self.optimizer.auto_rebalance(current_difficulty)
        self.assertEqual(result, current_difficulty)

    def test_auto_rebalance_adjustments(self):
        """Test auto-rebalance difficulty adjustments."""
        current_difficulty = 0.5
        self.optimizer.last_rebalance_time = time.time() - 40  # Allow rebalance

        # Test too hard (ratio < 0.9)
        self.optimizer.metrics.challenge_skill_ratio = 0.8
        result = self.optimizer.auto_rebalance(current_difficulty)
        self.assertLess(result, current_difficulty)

        # Test too easy (ratio > 1.2)
        self.optimizer.metrics.challenge_skill_ratio = 1.4
        result = self.optimizer.auto_rebalance(current_difficulty)
        self.assertGreater(result, current_difficulty)


class TestRewardSystem(unittest.TestCase):
    """Test RewardSystem functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.reward_system = RewardSystem()

    def test_initialization(self):
        """Test reward system initialization."""
        self.assertEqual(self.reward_system.schedule.schedule_type, RewardScheduleType.VARIABLE_RATIO)
        self.assertEqual(self.reward_system.actions_since_last_reward, 0)
        self.assertEqual(self.reward_system.encounters_since_last_rare, 0)

    def test_process_action_with_reward(self):
        """Test processing action that results in reward."""
        with patch('random.randint', return_value=5):  # Will trigger reward
            reward = self.reward_system.process_action('combat', 0.5, 120, 0.7)

        self.assertIsNotNone(reward)
        self.assertEqual(reward.type, 'combat')
        self.assertEqual(reward.difficulty, 0.5)
        self.assertEqual(reward.time_investment, 120)
        self.assertEqual(reward.skill_required, 0.7)
        self.assertGreater(reward.received_reward, 0)
        self.assertEqual(self.reward_system.actions_since_last_reward, 0)

    def test_process_action_without_reward(self):
        """Test processing action without reward."""
        with patch('random.randint', return_value=10):  # Won't trigger reward
            reward = self.reward_system.process_action('quest', 0.5, 120, 0.7)

        self.assertIsNone(reward)
        self.assertEqual(self.reward_system.actions_since_last_reward, 1)

    def test_prediction_error_modeling(self):
        """Test prediction error calculation."""
        with patch('random.randint', return_value=5):
            with patch('random.random', return_value=0.9):  # High novelty factor
                reward = self.reward_system.process_action('combat', 0.5, 120, 0.7)

        # Verify prediction error formula: Motivation_Index = Prediction_Error * Novelty_Factor * 0.73
        expected_motivation = reward.prediction_error * reward.novelty_factor * 0.73
        self.assertAlmostEqual(reward.motivation_index, expected_motivation, places=2)

    def test_analyze_player_response_insufficient_data(self):
        """Test player response analysis with insufficient data."""
        analysis = self.reward_system.analyze_player_response()
        self.assertEqual(analysis['player_sensitivity'], 'unknown')

    def test_analyze_player_response_with_data(self):
        """Test player response analysis with sufficient data."""
        # Add some mock rewards
        for i in range(10):
            with patch('random.randint', return_value=5):
                reward = self.reward_system.process_action('combat', 0.5, 120, 0.7)
                if reward:
                    reward.motivation_index = 25.0 if i < 5 else 5.0  # Vary motivation

        analysis = self.reward_system.analyze_player_response()
        self.assertIn(analysis['player_sensitivity'], ['low', 'medium', 'high'])
        self.assertIsInstance(analysis['adjustments_needed'], list)


class TestNeuroadaptiveEngagementSystem(unittest.TestCase):
    """Test NeuroadaptiveEngagementSystem functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.engagement_system = NeuroadaptiveEngagementSystem()

    def test_initialization(self):
        """Test engagement system initialization."""
        self.assertIsInstance(self.engagement_system.engagement_score, EngagementScore)
        self.assertIsInstance(self.engagement_system.churn_analysis, ChurnRiskAnalysis)

    def test_track_behavior(self):
        """Test behavior tracking."""
        action_type = 'combat_victory'
        timestamp = time.time()
        metadata = {'success': True, 'damage_dealt': 100}

        initial_count = len(self.engagement_system.behavioral_data)
        self.engagement_system.track_behavior(action_type, timestamp, metadata)

        self.assertEqual(len(self.engagement_system.behavioral_data), initial_count + 1)

        latest_entry = self.engagement_system.behavioral_data[-1]
        self.assertEqual(latest_entry['action_type'], action_type)
        self.assertEqual(latest_entry['timestamp'], timestamp)
        self.assertEqual(latest_entry['metadata'], metadata)

    def test_calculate_engagement_metrics_no_data(self):
        """Test engagement calculation with no recent data."""
        metrics = self.engagement_system.calculate_engagement_metrics()

        for metric_value in metrics.values():
            self.assertEqual(metric_value, 0.5)  # Default values when no data

    def test_calculate_engagement_metrics_with_data(self):
        """Test engagement calculation with behavioral data."""
        # Add some behavioral data
        base_time = time.time() - 3600  # 1 hour ago
        for i in range(20):
            timestamp = base_time + (i * 60)  # 1 minute intervals
            self.engagement_system.track_behavior(
                'action', timestamp, {'success': i % 3 != 0}  # 67% success rate
            )

        metrics = self.engagement_system.calculate_engagement_metrics()

        self.assertIn('session_duration', metrics)
        self.assertIn('action_frequency', metrics)
        self.assertIn('success_rate', metrics)
        self.assertGreaterEqual(metrics['action_frequency'], 0.0)
        self.assertLessEqual(metrics['action_frequency'], 1.0)

    def test_predict_churn_risk_with_insufficient_data(self):
        """Test churn prediction with insufficient data."""
        risk_analysis = self.engagement_system.predict_churn_risk()

        self.assertEqual(risk_analysis['risk_level'], 'low')
        self.assertLess(risk_analysis['churn_probability'], 0.2)
        self.assertLess(risk_analysis['confidence'], 0.6)

    def test_should_trigger_intervention_low_engagement(self):
        """Test intervention trigger with low engagement."""
        # Set low engagement score
        self.engagement_system.engagement_score.calculate_score({
            'session_duration': 0.2,  # Low session duration
            'action_frequency': 0.1,
            'success_rate': 0.3,
            'exploration_rate': 0.1,
            'social_interaction': 0.0,
            'achievement_progress': 0.2
        })

        should_intervene, intervention_type = self.engagement_system.should_trigger_intervention()
        self.assertTrue(should_intervene)
        self.assertIn(intervention_type, [InterventionType.REWARD_BONUS, InterventionType.CONTENT_RECOMMENDATION,
                                         InterventionType.ACHIEVEMENT_MILESTONE])

    def test_should_not_trigger_intervention_high_engagement(self):
        """Test no intervention with high engagement."""
        # Set high engagement score
        self.engagement_system.engagement_score.calculate_score({
            'session_duration': 0.8,
            'action_frequency': 0.9,
            'success_rate': 0.8,
            'exploration_rate': 0.7,
            'social_interaction': 0.6,
            'achievement_progress': 0.8
        })

        should_intervene, intervention_type = self.engagement_system.should_trigger_intervention()
        self.assertFalse(should_intervene)
        self.assertIsNone(intervention_type)


class TestProgressVisualizationSystem(unittest.TestCase):
    """Test ProgressVisualizationSystem functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.progress_system = ProgressVisualizationSystem()

    def test_initialization(self):
        """Test progress system initialization."""
        self.assertEqual(self.progress_system.experience_multiplier, 1.12)
        self.assertEqual(self.progress_system.base_experience, 100)

    def test_calculate_experience_requirement(self):
        """Test experience requirement calculation."""
        # Level 1 should be base experience
        exp_1 = self.progress_system.calculate_experience_requirement(1)
        self.assertEqual(exp_1, 100)

        # Level 2 should be base * 1.12
        exp_2 = self.progress_system.calculate_experience_requirement(2)
        self.assertEqual(exp_2, int(100 * 1.12))

        # Level 3 should be base * 1.12^2
        exp_3 = self.progress_system.calculate_experience_requirement(3)
        self.assertEqual(exp_3, int(100 * (1.12 ** 2)))

    def test_experience_progression_geometric(self):
        """Test geometric progression of experience requirements."""
        # Verify geometric progression ratio
        exp_5 = self.progress_system.calculate_experience_requirement(5)
        exp_6 = self.progress_system.calculate_experience_requirement(6)
        ratio = exp_6 / exp_5

        self.assertAlmostEqual(ratio, 1.12, places=2)

    def test_calculate_level_progress(self):
        """Test level progress calculation with logarithmic scaling."""
        level_exp = 500
        current_exp = 250  # 50% progress

        raw_progress = 0.5
        scaled_progress = self.progress_system.calculate_level_progress(current_exp, level_exp)

        # With logarithmic scaling, progress should be compressed
        self.assertLess(scaled_progress, raw_progress)
        self.assertGreaterEqual(scaled_progress, 0.0)
        self.assertLessEqual(scaled_progress, 1.0)

    def test_calculate_mastery_advancement(self):
        """Test mastery advancement calculation."""
        # Level 1 mastery
        mastery_1 = self.progress_system.calculate_mastery_advancement(1)
        self.assertEqual(mastery_1['visible_advancement'], 1.0)

        # Higher level mastery should require more effort
        mastery_5 = self.progress_system.calculate_mastery_advancement(5)
        mastery_10 = self.progress_system.calculate_mastery_advancement(10)

        self.assertGreater(mastery_10['effort_required'], mastery_5['effort_required'])
        self.assertLess(mastery_10['visible_advancement'], mastery_5['visible_advancement'])

        # Visible advancement should remain perceptible
        self.assertGreater(mastery_10['visible_advancement'], 0.1)

    def test_calculate_constant_perceived_effort(self):
        """Test constant perceived effort calculation."""
        progression_levels = [0.1, 0.25, 0.5, 0.75, 0.9]
        variance_ratio = self.progress_system.calculate_constant_perceived_effort(progression_levels)

        # Variance ratio should be relatively low (constant perceived effort)
        self.assertLess(variance_ratio, 0.3)
        self.assertGreaterEqual(variance_ratio, 0.0)


class TestContentVarietyOptimizer(unittest.TestCase):
    """Test ContentVarietyOptimizer functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.optimizer = ContentVarietyOptimizer()

    def test_initialization(self):
        """Test optimizer initialization."""
        self.assertEqual(len(self.optimizer.content_exposure), len(ContentVarietyType))
        self.assertEqual(self.optimizer.exploration_epsilon, 0.1)
        self.assertEqual(self.optimizer.wundt_optimal_range, (0.8, 1.0))

    def test_calculate_content_novelty(self):
        """Test content novelty calculation using Wundt curve."""
        # Test with low exposure (high novelty)
        self.optimizer.content_exposure[ContentVarietyType.COMBAT.value] = 0.1
        novelty = self.optimizer.calculate_content_novelty(ContentVarietyType.COMBAT)
        self.assertGreater(novelty, 0.8)  # Should be high

        # Test with high exposure (low novelty)
        self.optimizer.content_exposure[ContentVarietyType.EXPLORATION.value] = 0.9
        novelty = self.optimizer.calculate_content_novelty(ContentVarietyType.EXPLORATION)
        self.assertLess(novelty, 0.8)  # Should be low

    def test_wundt_curve_properties(self):
        """Test Wundt curve mathematical properties."""
        # Novelty should be maximum at standardized_novelty = 0
        self.optimizer.content_exposure[ContentVarietyType.PUZZLES.value] = 0.5  # Standardized novelty = 0
        max_novelty = self.optimizer.calculate_content_novelty(ContentVarietyType.PUZZLES)
        self.assertEqual(max_novelty, 1.0)  # e^(-0^2) = 1

        # Novelty should decrease as we move away from 0.5 exposure
        self.optimizer.content_exposure[ContentVarietyType.SOCIAL.value] = 0.0  # Very low exposure
        low_novelty = self.optimizer.calculate_content_novelty(ContentVarietyType.SOCIAL)
        self.assertLess(low_novelty, max_novelty)

    def test_should_exploit_or_explore(self):
        """Test exploration-exploitation balance."""
        # With 0.1 epsilon, should exploit most of the time
        explore_count = 0
        for _ in range(1000):
            if self.optimizer.should_exploit_or_explore():
                explore_count += 1

        # Should explore approximately 10% of the time
        explore_rate = explore_count / 1000
        self.assertGreater(explore_rate, 0.05)
        self.assertLess(explore_rate, 0.15)

    def test_recommend_content_exploration(self):
        """Test content recommendation in exploration mode."""
        # Set up different novelty levels
        self.optimizer.content_exposure[ContentVarietyType.COMBAT.value] = 0.8  # Low novelty
        self.optimizer.content_exposure[ContentVarietyType.CRAFTING.value] = 0.1  # High novelty

        with patch('random.random', return_value=0.05):  # Force exploration
            recommendation = self.optimizer.recommend_content()

        # Should recommend high novelty content
        self.assertEqual(recommendation, ContentVarietyType.CRAFTING)

    def test_update_content_exposure(self):
        """Test content exposure updates."""
        initial_exposure = self.optimizer.content_exposure[ContentVarietyType.STORY.value]

        self.optimizer.update_content_exposure(ContentVarietyType.STORY, 0.1)
        new_exposure = self.optimizer.content_exposure[ContentVarietyType.STORY.value]

        self.assertEqual(new_exposure, min(1.0, initial_exposure + 0.1))

        # Other content types should decay slightly
        for ct in ContentVarietyType:
            if ct != ContentVarietyType.STORY:
                self.assertLess(self.optimizer.content_exposure[ct.value], initial_exposure + 0.01)

    def test_get_content_variety_analysis(self):
        """Test content variety analysis."""
        analysis = self.optimizer.get_content_variety_analysis()

        self.assertIn('content_novelty_scores', analysis)
        self.assertIn('under_stimulated_content', analysis)
        self.assertIn('optimally_stimulated_content', analysis)
        self.assertIn('over_stimulated_content', analysis)
        self.assertIn('variety_balance', analysis)

        # Should have scores for all content types
        self.assertEqual(len(analysis['content_novelty_scores']), len(ContentVarietyType))


class TestInterventionSystem(unittest.TestCase):
    """Test InterventionSystem functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.intervention_system = InterventionSystem()

    def test_initialization(self):
        """Test intervention system initialization."""
        self.assertEqual(len(self.intervention_system.available_interventions), len(InterventionType))

    def test_trigger_difficulty_adjustment_intervention(self):
        """Test difficulty adjustment intervention."""
        context = {
            'current_difficulty': 0.7,
            'player_performance': 0.3  # Low performance
        }

        result = self.intervention_system.trigger_intervention(
            InterventionType.DYNAMIC_DIFFICULTY, context
        )

        self.assertEqual(result['type'], InterventionType.DYNAMIC_DIFFICULTY)
        self.assertTrue(result['outcome']['difficulty_adjusted'])
        self.assertLess(result['outcome']['new_difficulty'], result['outcome']['old_difficulty'])

    def test_trigger_content_recommendation_intervention(self):
        """Test content recommendation intervention."""
        context = {
            'engagement_level': 0.2,  # Low engagement
            'player_preferences': {'preferred_content': 'combat'}
        }

        result = self.intervention_system.trigger_intervention(
            InterventionType.CONTENT_RECOMMENDATION, context
        )

        self.assertEqual(result['type'], InterventionType.CONTENT_RECOMMENDATION)
        self.assertTrue(result['outcome']['content_recommended'])
        self.assertIn(result['outcome']['recommended_type'], ['high_reward_quest', 'balanced_challenge', 'mastery_opportunity'])

    def test_trigger_reward_bonus_intervention(self):
        """Test reward bonus intervention."""
        context = {'current_motivation': 0.3}

        result = self.intervention_system.trigger_intervention(
            InterventionType.REWARD_BONUS, context
        )

        self.assertEqual(result['type'], InterventionType.REWARD_BONUS)
        self.assertTrue(result['outcome']['bonus_rewarded'])
        self.assertGreater(result['outcome']['bonus_amount'], 0)
        self.assertEqual(result['outcome']['reward_type'], 'motivation_bonus')

    def test_trigger_achievement_milestone_intervention(self):
        """Test achievement milestone intervention."""
        context = {'player_progress': {'percentage': 75.0}}

        result = self.intervention_system.trigger_intervention(
            InterventionType.ACHIEVEMENT_MILESTONE, context
        )

        self.assertEqual(result['type'], InterventionType.ACHIEVEMENT_MILESTONE)
        self.assertTrue(result['outcome']['milestone_unlocked'])
        self.assertEqual(result['outcome']['milestone_type'], 'progress_milestone')

    def test_trigger_generic_intervention(self):
        """Test generic intervention for other types."""
        context = {'some_data': 'value'}

        result = self.intervention_system.trigger_intervention(
            InterventionType.SOCIAL_CONNECTION_PROMPT, context
        )

        self.assertEqual(result['type'], InterventionType.SOCIAL_CONNECTION_PROMPT)
        self.assertTrue(result['outcome']['intervention_applied'])


class TestGamificationSystem(unittest.TestCase):
    """Test main GamificationSystem functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.system = GamificationSystem()

    def test_initialization(self):
        """Test system initialization."""
        self.assertIsNotNone(self.system.dda)
        self.assertIsNotNone(self.system.flow_optimizer)
        self.assertIsNotNone(self.system.reward_system)
        self.assertIsNotNone(self.system.engagement_system)
        self.assertIsNotNone(self.system.progress_visualization)
        self.assertIsNotNone(self.system.content_variety)
        self.assertIsNotNone(self.system.intervention_system)

    def test_initialize_system(self):
        """Test system initialization method."""
        result = self.system.initialize_system()

        self.assertEqual(result['status'], 'initialized')
        self.assertEqual(result['framework_version'], '2025')
        self.assertIn('dynamic_difficulty_adjustment', result['systems_active'])
        self.assertEqual(result['initial_difficulty'], 0.5)
        self.assertEqual(result['target_performance'], 0.75)

    def test_process_player_action(self):
        """Test processing player action through all systems."""
        action_result = self.system.process_player_action(
            action_type='combat_victory',
            success=True,
            time_taken=120,
            difficulty=0.5,
            metadata={'content_type': 'combat'}
        )

        self.assertTrue(action_result['action_processed'])
        self.assertEqual(action_result['success'], True)
        self.assertIsInstance(action_result['performance_score'], float)
        self.assertGreaterEqual(action_result['performance_score'], 0.0)
        self.assertLessEqual(action_result['performance_score'], 1.0)

    def test_process_player_action_with_difficulty_adjustment(self):
        """Test action processing that triggers difficulty adjustment."""
        # Add multiple successful encounters to trigger adjustment
        for i in range(5):
            self.system.process_player_action(
                'quest_completion', True, 60, 0.3  # Low difficulty, high success
            )

        # Next action should potentially trigger adjustment
        result = self.system.process_player_action('quest_completion', True, 60, 0.3)
        self.assertIsInstance(result['difficulty_adjusted'], bool)

    def test_process_player_action_with_reward(self):
        """Test action processing that results in reward."""
        with patch('random.randint', return_value=5):  # Force reward
            result = self.system.process_player_action(
                'exploration_discovery', True, 180, 0.7
            )

        self.assertTrue(result['reward_given'])
        self.assertIsNotNone(result['reward_details'])
        self.assertGreater(result['reward_details']['amount'], 0)

    def test_process_player_action_with_intervention(self):
        """Test action processing that triggers intervention."""
        # Simulate low engagement by processing actions with poor performance
        for i in range(10):
            self.system.process_player_action(
                'combat_victory', False, 300, 0.8  # Low success, high difficulty
            )

        # Process more actions to potentially trigger intervention
        result = self.system.process_player_action(
            'combat_victory', False, 300, 0.8,
            metadata={'frustration': 0.8}
        )

        self.assertIsInstance(result['intervention_triggered'], bool)
        if result['intervention_triggered']:
            self.assertIsNotNone(result['intervention_result'])

    def test_get_player_analytics(self):
        """Test getting comprehensive player analytics."""
        # Process some actions to generate data
        for i in range(5):
            self.system.process_player_action(
                f'action_{i}', i % 2 == 0, 120, 0.5,
                metadata={'content_type': 'combat' if i % 2 == 0 else 'exploration'}
            )

        analytics = self.system.get_player_analytics()

        self.assertIn('player_state', analytics)
        self.assertIn('performance', analytics)
        self.assertIn('engagement', analytics)
        self.assertIn('rewards', analytics)
        self.assertIn('content', analytics)
        self.assertIn('progress', analytics)

        # Check specific analytics components
        self.assertIsInstance(analytics['player_state']['current_level'], int)
        self.assertIsInstance(analytics['performance']['success_rate'], float)
        self.assertIsInstance(analytics['engagement']['overall_score'], float)
        self.assertIsInstance(analytics['rewards']['total_motivation_index'], float)

    def test_update_player_skill(self):
        """Test updating player skill level."""
        new_skill = 0.8
        self.system.update_player_skill(new_skill)

        self.assertEqual(self.system.player_state['skill_level'], new_skill)

        # Should trigger difficulty recalculation
        target_difficulty = self.system.flow_optimizer.calculate_optimal_difficulty(new_skill)
        self.assertEqual(self.system.dda.current_difficulty, target_difficulty)

    def test_add_experience(self):
        """Test adding experience and level progression."""
        initial_level = self.system.player_state['current_level']
        initial_exp = self.system.player_state['total_experience']

        # Add experience that should trigger level up
        exp_amount = 150  # Should be enough for level 1 (100 exp)
        result = self.system.add_experience(exp_amount)

        self.assertEqual(result['experience_added'], exp_amount)
        self.assertGreater(result['levels_gained'], 0)
        self.assertGreater(result['new_level'], initial_level)

    def test_get_system_statistics(self):
        """Test getting system statistics."""
        # Process some actions to generate statistics
        for i in range(3):
            self.system.process_player_action(f'test_action_{i}', True, 120, 0.5)

        stats = self.system.get_system_statistics()

        self.assertIn('total_sessions_processed', stats)
        self.assertIn('total_rewards_distributed', stats)
        self.assertIn('average_motivation_index', stats)
        self.assertIn('difficulty_adjustments', stats)
        self.assertIn('system_uptime', stats)

        self.assertGreaterEqual(stats['system_uptime'], 0)


class TestGlobalFunctions(unittest.TestCase):
    """Test global functions."""

    def test_get_gamification_system(self):
        """Test global gamification system getter."""
        system1 = get_gamification_system()
        system2 = get_gamification_system()
        self.assertIs(system1, system2)  # Should return same instance

    def test_create_gamification_system(self):
        """Test global gamification system creator."""
        system1 = create_gamification_system()
        system2 = create_gamification_system()
        self.assertIsNot(system1, system2)  # Should return different instances


class TestSystemIntegration(unittest.TestCase):
    """Test integration between gamification system components."""

    def setUp(self):
        """Set up test fixtures."""
        self.system = GamificationSystem()

    def test_full_gamification_workflow(self):
        """Test complete gamification workflow."""
        # Initialize system
        init_result = self.system.initialize_system()
        self.assertEqual(init_result['status'], 'initialized')

        # Process variety of actions
        actions = [
            ('combat_victory', True, 120, 0.4, {'content_type': 'combat'}),
            ('quest_completion', True, 300, 0.6, {'content_type': 'story'}),
            ('exploration_discovery', False, 180, 0.7, {'content_type': 'exploration'}),
            ('skill_improvement', True, 90, 0.3, {'content_type': 'crafting'}),
            ('social_interaction', True, 150, 0.5, {'content_type': 'social'})
        ]

        for action_type, success, time_taken, difficulty, metadata in actions:
            result = self.system.process_player_action(
                action_type, success, time_taken, difficulty, metadata
            )
            self.assertTrue(result['action_processed'])

        # Get comprehensive analytics
        analytics = self.system.get_player_analytics()

        # Verify system integration
        self.assertGreater(analytics['performance']['overall_score'], 0.0)
        self.assertGreater(analytics['engagement']['overall_score'], 0.0)
        self.assertIsInstance(analytics['content']['content_variety'], dict)

        # Test skill update integration
        self.system.update_player_skill(0.75)
        updated_analytics = self.system.get_player_analytics()
        self.assertEqual(updated_analytics['player_state']['skill_level'], 0.75)

    def test_mathematical_formula_verification(self):
        """Test verification of key mathematical formulas from BDD."""
        # Test DDA formula
        self.system.dda.performance.success_rate = 0.6
        self.system.dda.performance.time_efficiency = 0.7
        self.system.dda.performance.resource_efficiency = 0.8
        performance = self.system.dda.performance.calculate_score()

        # Formula: New_Difficulty = Base_Difficulty * (0.7 + 0.3 * (Target_Performance / Measured_Performance))
        base_diff = 0.5
        target_perf = 0.75
        expected_diff = base_diff * (0.7 + 0.3 * (target_perf / performance))

        calculated_diff = self.system.dda.calculate_difficulty_adjustment(performance)
        self.assertAlmostEqual(calculated_diff, expected_diff, places=3)

        # Test prediction error formula
        with patch('random.randint', return_value=5):
            reward = self.system.reward_system.process_action('test', 0.5, 120, 0.7)

        if reward:
            # Formula: Motivation_Index = Prediction_Error * Novelty_Factor * 0.73
            expected_motivation = reward.prediction_error * reward.novelty_factor * 0.73
            self.assertAlmostEqual(reward.motivation_index, expected_motivation, places=2)

    def test_statistical_properties(self):
        """Test statistical properties and distributions."""
        # Test Gaussian difficulty generation
        player_skill = 0.5
        difficulties = [self.system.dda.generate_encounter_difficulty(player_skill) for _ in range(100)]

        # Verify distribution properties
        mean_diff = sum(difficulties) / len(difficulties)
        variance = sum((d - mean_diff) ** 2 for d in difficulties) / len(difficulties)
        std_dev = math.sqrt(variance)

        self.assertLess(abs(mean_diff - player_skill), 0.05)  # Mean should be close to player skill
        self.assertLess(abs(std_dev - 0.15), 0.03)  # Std dev should be close to sigma=0.15

        # Test rare reward probability distribution
        probabilities = []
        for n in range(1, 51):
            prob = self.system.reward_system.schedule.calculate_rare_reward_probability(n)
            probabilities.append(prob)

        # Should be monotonically increasing
        for i in range(1, len(probabilities)):
            self.assertGreaterEqual(probabilities[i], probabilities[i-1])

        # Should approach 0.05 asymptotically
        self.assertLess(probabilities[-1], 0.05)
        self.assertGreater(probabilities[-1], 0.04)


if __name__ == '__main__':
    unittest.main()