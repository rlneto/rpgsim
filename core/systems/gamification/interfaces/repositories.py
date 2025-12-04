"""
Repository interfaces for the Gamification System.
"""
from abc import ABC, abstractmethod
from typing import List
from ..domain.gamification import Achievement, Badge, Progress, Reward

class IAchievementRepository(ABC):
    """Interface for an achievement repository."""
    @abstractmethod
    def get_all(self) -> List[Achievement]:
        pass

    @abstractmethod
    def get_by_id(self, id: str) -> Achievement:
        pass

    @abstractmethod
    def add(self, achievement: Achievement) -> None:
        pass

class IBadgeRepository(ABC):
    """Interface for a badge repository."""
    @abstractmethod
    def get_all(self) -> List[Badge]:
        pass

    @abstractmethod
    def get_by_id(self, id: str) -> Badge:
        pass

    @abstractmethod
    def add(self, badge: Badge) -> None:
        pass

class IProgressRepository(ABC):
    """Interface for a progress repository."""
    @abstractmethod
    def get_by_player_id(self, player_id: str) -> Progress:
        pass

    @abstractmethod
    def save(self, progress: Progress) -> None:
        pass

class IRewardRepository(ABC):
    """Interface for a reward repository."""
    @abstractmethod
    def get_all(self) -> List[Reward]:
        pass

    @abstractmethod
    def get_by_id(self, id: str) -> Reward:
        pass

    @abstractmethod
    def add(self, reward: Reward) -> None:
        pass
