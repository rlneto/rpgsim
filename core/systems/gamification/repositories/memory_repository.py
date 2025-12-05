from typing import List, Optional, Dict

from ..domain.gamification import Achievement, Badge, Progress, Reward

class MemoryGamificationRepository:
    def __init__(self):
        self._achievements: Dict[str, Achievement] = {}
        self._progress: Dict[str, Progress] = {}
        self._badges: Dict[str, Badge] = {}
        self._rewards: Dict[str, List[Reward]] = {}

    def save_achievement(self, achievement: Achievement) -> None:
        self._achievements[achievement.id] = achievement

    def get_achievement(self, achievement_id: str) -> Optional[Achievement]:
        return self._achievements.get(achievement_id)

    def get_progress(self, user_id: str) -> Optional[Progress]:
        return self._progress.get(user_id)

    def save_progress(self, progress: Progress) -> None:
        self._progress[progress.user_id] = progress

    # Alias for legacy tests
    def get(self, user_id: str) -> Optional[Progress]:
        return self.get_progress(user_id)
