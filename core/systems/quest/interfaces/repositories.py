from abc import ABC, abstractmethod
from typing import List, Optional
from core.systems.quest.domain.quest import Quest

class QuestRepository(ABC):
    @abstractmethod
    def add(self, quest: Quest) -> None:
        pass

    @abstractmethod
    def get(self, quest_id: str) -> Optional[Quest]:
        pass

    @abstractmethod
    def get_all(self) -> List[Quest]:
        pass
