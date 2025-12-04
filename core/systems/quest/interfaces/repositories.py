"""
Quest repository interfaces
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from ..domain.quest import Quest, QuestProgress

class QuestRepository(ABC):
    @abstractmethod
    def save(self, quest: Quest) -> bool:
        pass

    @abstractmethod
    def get(self, quest_id: str) -> Optional[Quest]:
        pass

    @abstractmethod
    def list_all(self) -> List[Quest]:
        pass

class QuestProgressRepository(ABC):
    @abstractmethod
    def save(self, progress: QuestProgress) -> bool:
        pass

    @abstractmethod
    def get(self, player_id: str, quest_id: str) -> Optional[QuestProgress]:
        pass

    @abstractmethod
    def list_by_player(self, player_id: str) -> List[QuestProgress]:
        pass
