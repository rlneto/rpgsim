from typing import List, Optional

from ..domain.gamification import Achievement
from ..interfaces.repositories import AchievementRepository


class AchievementService:
    def __init__(self, achievement_repository: AchievementRepository):
        self._repository = achievement_repository

    def grant_achievement(self, player_id: str, achievement_id: str) -> bool:
        achievement = self._repository.get(achievement_id)
        if achievement and not achievement.unlocked:
            achievement.unlocked = True
            self._repository.update(achievement)
            return True
        return False

    def get_achievement(self, achievement_id: str) -> Optional[Achievement]:
        return self._repository.get(achievement_id)

    def list_achievements(self) -> List[Achievement]:
        return self._repository.list()
