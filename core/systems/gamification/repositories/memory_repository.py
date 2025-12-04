"""
In-memory repository implementations for the Gamification System.
"""
from typing import List
from ..domain.gamification import Achievement, Badge, Progress, Reward
from ..interfaces.repositories import IAchievementRepository, IBadgeRepository, IProgressRepository, IRewardRepository

class MemoryAchievementRepository(IAchievementRepository):
    """In-memory implementation of an achievement repository."""
    def __init__(self):
        self._achievements: List[Achievement] = []

    def get_all(self) -> List[Achievement]:
        return self._achievements

    def get_by_id(self, id: str) -> Achievement:
        for achievement in self._achievements:
            if achievement.id == id:
                return achievement
        return None

    def add(self, achievement: Achievement) -> None:
        self._achievements.append(achievement)

class MemoryBadgeRepository(IBadgeRepository):
    """In-memory implementation of a badge repository."""
    def __init__(self):
        self._badges: List[Badge] = []

    def get_all(self) -> List[Badge]:
        return self._badges

    def get_by_id(self, id: str) -> Badge:
        for badge in self._badges:
            if badge.id == id:
                return badge
        return None

    def add(self, badge: Badge) -> None:
        self._badges.append(badge)

class MemoryProgressRepository(IProgressRepository):
    """In-memory implementation of a progress repository."""
    def __init__(self):
        self._progress: List[Progress] = []

    def get_by_player_id(self, player_id: str) -> Progress:
        for progress in self._progress:
            if progress.player_id == player_id:
                return progress
        return None

    def save(self, progress: Progress) -> None:
        for i, p in enumerate(self._progress):
            if p.player_id == progress.player_id:
                self._progress[i] = progress
                return
        self._progress.append(progress)

class MemoryRewardRepository(IRewardRepository):
    """In-memory implementation of a reward repository."""
    def __init__(self):
        self._rewards: List[Reward] = []

    def get_all(self) -> List[Reward]:
        return self._rewards

    def get_by_id(self, id: str) -> Reward:
        for reward in self._rewards:
            if reward.id == id:
                return reward
        return None

    def add(self, reward: Reward) -> None:
        self._rewards.append(reward)
