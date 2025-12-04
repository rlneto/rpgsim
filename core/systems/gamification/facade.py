"""
Facade for the Gamification System.
"""
from .services.achievement_service import AchievementService
from .services.progress_service import ProgressService
from .services.reward_service import RewardService
from .repositories.memory_repository import MemoryAchievementRepository, MemoryBadgeRepository, MemoryProgressRepository, MemoryRewardRepository

class GamificationSystem:
    """Facade for the Gamification System."""
    def __init__(self):
        # In a real application, you would use a dependency injection container
        # to manage the creation and lifecycle of these objects.
        self._achievement_repo = MemoryAchievementRepository()
        self._badge_repo = MemoryBadgeRepository()
        self._progress_repo = MemoryProgressRepository()
        self._reward_repo = MemoryRewardRepository()

        self._achievement_service = AchievementService(self._achievement_repo, self._progress_repo)
        self._progress_service = ProgressService(self._progress_repo)
        self._reward_service = RewardService(self._reward_repo, self._progress_repo)

    def process_event(self, player_id: str, event: dict):
        """Process a game event and update player progress."""
        unlocked_achievements = self._achievement_service.check_and_unlock(player_id, event)
        # You could also grant rewards or badges based on the event.
        return unlocked_achievements

    def add_experience(self, player_id: str, amount: int):
        """Add experience to a player."""
        return self._progress_service.add_experience(player_id, amount)

    def grant_reward(self, player_id: str, reward_id: str):
        """Grant a reward to a player."""
        return self._reward_service.grant_reward(player_id, reward_id)

    def get_progress(self, player_id: str):
        """Get a player's progress."""
        return self._progress_service.get_progress(player_id)

_gamification_system = None

def get_gamification_system():
    """Get the global gamification system instance."""
    global _gamification_system
    if _gamification_system is None:
        _gamification_system = GamificationSystem()
    return _gamification_system

def create_gamification_system():
    """Create a new gamification system instance."""
    return GamificationSystem()
