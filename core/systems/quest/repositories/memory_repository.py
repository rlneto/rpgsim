"""
Memory implementations of quest repositories
"""
from typing import List, Dict, Optional
from ..domain.quest import Quest, QuestProgress
from ..interfaces.repositories import QuestRepository, QuestProgressRepository

class MemoryQuestRepository(QuestRepository):
    def __init__(self):
        self._quests: Dict[str, Quest] = {}

    def save(self, quest: Quest) -> bool:
        self._quests[quest.quest_id] = quest
        return True

    def get(self, quest_id: str) -> Optional[Quest]:
        return self._quests.get(quest_id)

    def list_all(self) -> List[Quest]:
        return list(self._quests.values())

class MemoryQuestProgressRepository(QuestProgressRepository):
    def __init__(self):
        self._progress: Dict[str, QuestProgress] = {}

    def save(self, progress: QuestProgress) -> bool:
        key = f"{progress.player_id}_{progress.quest_id}"
        self._progress[key] = progress
        return True

    def get(self, player_id: str, quest_id: str) -> Optional[QuestProgress]:
        key = f"{player_id}_{quest_id}"
        return self._progress.get(key)

    def list_by_player(self, player_id: str) -> List[QuestProgress]:
        return [p for p in self._progress.values() if p.player_id == player_id]
