from abc import ABC, abstractmethod
from typing import List, Optional

from ..domain.gamification import Achievement, Badge, Progress, Reward


class AchievementRepository(ABC):
    @abstractmethod
    def add(self, achievement: Achievement) -> None:
        pass

    @abstractmethod
    def get(self, achievement_id: str) -> Optional[Achievement]:
        pass

    @abstractmethod
    def list(self) -> List[Achievement]:
        pass

    @abstractmethod
    def update(self, achievement: Achievement) -> None:
        pass


class BadgeRepository(ABC):
    @abstractmethod
    def add(self, badge: Badge) -> None:
        pass

    @abstractmethod
    def get(self, badge_id: str) -> Optional[Badge]:
        pass

    @abstractmethod
    def list(self) -> List[Badge]:
        pass


class ProgressRepository(ABC):
    @abstractmethod
    def get(self, player_id: str) -> Optional[Progress]:
        pass

    @abstractmethod
    def update(self, progress: Progress) -> None:
        pass


class RewardRepository(ABC):
    @abstractmethod
    def add(self, reward: Reward) -> None:
        pass

    @abstractmethod
    def list(self, player_id: str) -> List[Reward]:
        pass
