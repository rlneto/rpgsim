from typing import Dict, List, Optional
from core.systems.quest.domain.quest import Quest
from core.systems.quest.interfaces.repositories import QuestRepository

class MemoryQuestRepository(QuestRepository):
    def __init__(self) -> None:
        self._quests: Dict[str, Quest] = {}

    def add(self, quest: Quest) -> None:
        self._quests[quest.id] = quest

    def get(self, quest_id: str) -> Optional[Quest]:
        return self._quests.get(quest_id)

    def get_all(self) -> List[Quest]:
        return list(self._quests.values())
