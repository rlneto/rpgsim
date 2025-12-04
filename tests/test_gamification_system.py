"""
Unit tests for the refactored Gamification System.
"""
import unittest
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.systems.gamification.facade import GamificationSystem, create_gamification_system
from core.systems.gamification.domain.gamification import Achievement, Reward

class TestGamificationSystem(unittest.TestCase):
    """Test the GamificationSystem facade."""

    def setUp(self):
        """Set up a new gamification system for each test."""
        self.system = create_gamification_system()

    def test_process_event_unlocks_achievement(self):
        """Test that processing an event unlocks an achievement."""
        # Add a sample achievement to the repository
        achievement = Achievement(
            id="test_achievement",
            name="Test Achievement",
            description="A test achievement.",
            criteria={"action": "test_action"}
        )
        self.system._achievement_repo.add(achievement)

        # Process an event that should unlock the achievement
        unlocked = self.system.process_event("player1", {"action": "test_action"})

        # Check that the achievement was unlocked
        self.assertEqual(len(unlocked), 1)
        self.assertEqual(unlocked[0].id, "test_achievement")

        # Check the player's progress
        progress = self.system.get_progress("player1")
        self.assertEqual(len(progress.achievements), 1)
        self.assertTrue(progress.achievements[0].unlocked)

    def test_add_experience_and_level_up(self):
        """Test that adding experience increases the player's level."""
        # Add enough experience to level up
        progress = self.system.add_experience("player1", 150)

        # Check that the player leveled up
        self.assertEqual(progress.level, 2)
        self.assertEqual(progress.experience, 50)

    def test_grant_reward(self):
        """Test that granting a reward increases the player's experience."""
        # Add a sample reward to the repository
        reward = Reward(
            id="test_reward",
            name="Test Reward",
            description="A test reward.",
            value=50
        )
        self.system._reward_repo.add(reward)

        # Grant the reward to the player
        self.system.grant_reward("player1", "test_reward")

        # Check that the player's experience increased
        progress = self.system.get_progress("player1")
        self.assertEqual(progress.experience, 50)

    def test_get_progress(self):
        """Test that we can retrieve a player's progress."""
        # Add some experience to the player
        self.system.add_experience("player1", 50)

        # Get the player's progress
        progress = self.system.get_progress("player1")

        # Check that the progress is correct
        self.assertEqual(progress.player_id, "player1")
        self.assertEqual(progress.experience, 50)
        self.assertEqual(progress.level, 1)

if __name__ == '__main__':
    unittest.main()
