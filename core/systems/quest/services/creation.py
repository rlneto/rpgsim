from typing import List
from core.systems.quest.domain.quest import Quest, QuestStep, QuestReward
from core.systems.quest.interfaces.repositories import QuestRepository

class QuestCreationService:
    def __init__(self, quest_repository: QuestRepository):
        self._quest_repository = quest_repository

    def create_quest(self, quest_id: str, name: str, description: str, steps: List[str], reward: dict) -> Quest:
        quest_steps = [QuestStep(description=step) for step in steps]
        quest_reward = QuestReward(**reward)
        quest = Quest(id=quest_id, name=name, description=description, steps=quest_steps, reward=quest_reward)
        self._quest_repository.add(quest)
        return quest
