from typing import List, Optional
from core.systems.quest.domain.quest import Quest, QuestReward
from core.systems.quest.domain.npc import NPCProfile, DialogueOption, DialogueResponse
from core.systems.quest.repositories.memory_repository import MemoryQuestRepository
from core.systems.quest.services.creation import QuestCreationService
from core.systems.quest.services.progress import QuestProgressService
from core.systems.quest.services.reward import QuestRewardService
from core.systems.quest.services.generation import QuestGenerationService, QuestType, QuestDifficulty
from core.systems.quest.services.npc import NPCService

class QuestSystem:
    def __init__(self):
        self.quest_repository = MemoryQuestRepository()
        self.quest_creation_service = QuestCreationService(self.quest_repository)
        self.quest_progress_service = QuestProgressService(self.quest_repository)
        self.quest_reward_service = QuestRewardService(self.quest_repository)
        self.quest_generation_service = QuestGenerationService()
        self.npc_service = NPCService()
        self.npcs: Dict[str, NPCProfile] = {}

    def generate_quest(self, quest_id: str, quest_type: Optional[QuestType] = None, difficulty: Optional[QuestDifficulty] = None) -> Quest:
        quest = self.quest_generation_service.generate_quest(quest_id, quest_type, difficulty)
        self.quest_repository.add(quest)
        return quest

    def generate_npc(self, npc_id: str, location: str) -> NPCProfile:
        npc = self.npc_service.generate_npc(npc_id, location)
        self.npcs[npc_id] = npc
        return npc

    def get_dialogue_options(self, npc_id: str) -> List[DialogueOption]:
        return self.npc_service.get_dialogue_options()

    def get_npc_response(self, npc_id: str, option: DialogueOption) -> DialogueResponse:
        npc = self.npcs.get(npc_id)
        if npc:
            return self.npc_service.get_npc_response(option, npc)
        return DialogueResponse(text="NPC not found.")

    def complete_step(self, quest_id: str, step_description: str) -> Optional[Quest]:
        return self.quest_progress_service.complete_step(quest_id, step_description)

    def get_quest_reward(self, quest_id: str) -> Optional[QuestReward]:
        return self.quest_reward_service.grant_reward(quest_id)
