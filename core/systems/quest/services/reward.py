from typing import Optional
from core.systems.quest.domain.quest import Quest, QuestReward
from core.systems.quest.interfaces.repositories import QuestRepository

class QuestRewardService:
    def __init__(self, quest_repository: QuestRepository):
        self._quest_repository = quest_repository

    def grant_reward(self, quest_id: str) -> Optional[QuestReward]:
        quest = self._quest_repository.get(quest_id)
        if quest and quest.completed:
            return quest.reward
        return None
