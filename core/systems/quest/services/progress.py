from typing import Optional
from core.systems.quest.domain.quest import Quest
from core.systems.quest.interfaces.repositories import QuestRepository

class QuestProgressService:
    def __init__(self, quest_repository: QuestRepository):
        self._quest_repository = quest_repository

    def complete_step(self, quest_id: str, step_description: str) -> Optional[Quest]:
        quest = self._quest_repository.get(quest_id)
        if quest:
            for step in quest.steps:
                if step.description == step_description:
                    step.completed = True
            if all(step.completed for step in quest.steps):
                quest.completed = True
        return quest
