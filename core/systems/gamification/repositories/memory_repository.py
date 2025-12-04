from typing import List, Optional

from ..domain.gamification import Achievement, Badge, Progress, Reward
from ..interfaces.repositories import (
    AchievementRepository,
    BadgeRepository,
    ProgressRepository,
    RewardRepository,
)


class MemoryAchievementRepository(AchievementRepository):
    def __init__(self):
        self._achievements = {}

    def add(self, achievement: Achievement) -> None:
        self._achievements[achievement.id] = achievement

    def get(self, achievement_id: str) -> Optional[Achievement]:
        return self._achievements.get(achievement_id)

    def list(self) -> List[Achievement]:
        return list(self._achievements.values())

    def update(self, achievement: Achievement) -> None:
        if achievement.id in self._achievements:
            self._achievements[achievement.id] = achievement


class MemoryBadgeRepository(BadgeRepository):
    def __init__(self):
        self._badges = {}

    def add(self, badge: Badge) -> None:
        self._badges[badge.id] = badge

    def get(self, badge_id: str) -> Optional[Badge]:
        return self._badges.get(badge_id)

    def list(self) -> List[Badge]:
        return list(self._badges.values())


class MemoryProgressRepository(ProgressRepository):
    def __init__(self):
        self._progress = {}

    def get(self, player_id: str) -> Optional[Progress]:
        return self._progress.get(player_id)

    def update(self, progress: Progress) -> None:
        self._progress[progress.player_id] = progress


class MemoryRewardRepository(RewardRepository):
    def __init__(self):
        self._rewards = {}

    def add(self, reward: Reward) -> None:
        if reward.player_id not in self._rewards:
            self._rewards[reward.player_id] = []
        self._rewards[reward.player_id].append(reward)

    def list(self, player_id: str) -> List[Reward]:
        return self._rewards.get(player_id, [])
