"""
Service for handling achievements.
"""
from ..domain.gamification import Achievement, Progress
from ..interfaces.repositories import IAchievementRepository, IProgressRepository

class AchievementService:
    """Service for managing achievements."""
    def __init__(self, achievement_repo: IAchievementRepository, progress_repo: IProgressRepository):
        self._achievement_repo = achievement_repo
        self._progress_repo = progress_repo

    def check_and_unlock(self, player_id: str, event: dict) -> list[Achievement]:
        """Check for and unlock achievements based on a player action."""
        progress = self._progress_repo.get_by_player_id(player_id)
        if not progress:
            progress = Progress(player_id=player_id)

        unlocked_achievements = []
        all_achievements = self._achievement_repo.get_all()

        for achievement in all_achievements:
            if not achievement.unlocked and self._check_criteria(achievement, event):
                achievement.unlocked = True
                progress.achievements.append(achievement)
                unlocked_achievements.append(achievement)

        self._progress_repo.save(progress)
        return unlocked_achievements

    def _check_criteria(self, achievement: Achievement, event: dict) -> bool:
        """Check if the event meets the achievement's criteria."""
        # This is a simple example. A real implementation would have more complex criteria checking.
        for key, value in achievement.criteria.items():
            if event.get(key) != value:
                return False
        return True
