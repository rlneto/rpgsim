import pytest
from core.systems.quest.services.generation import QuestGenerationService, QuestType, QuestDifficulty
from core.systems.quest.services.npc import NPCService, NPCPersonality
from core.systems.quest.facade import QuestSystem

class TestQuestGenerationService:
    def test_generate_kill_quest(self):
        service = QuestGenerationService()
        quest = service.generate_quest("q1", quest_type=QuestType.KILL, difficulty=QuestDifficulty.MEDIUM)
        assert quest.id == "q1"
        assert "Defeat" in quest.name
        assert len(quest.steps) == 1

    def test_generate_fetch_quest(self):
        service = QuestGenerationService()
        quest = service.generate_quest("q2", quest_type=QuestType.FETCH, difficulty=QuestDifficulty.EASY)
        assert quest.id == "q2"
        assert len(quest.steps) == 2

class TestNPCService:
    def test_generate_npc(self):
        service = NPCService()
        npc = service.generate_npc("npc1", "Test Location")
        assert npc.id == "npc1"
        assert npc.location == "Test Location"
        assert isinstance(npc.personality, NPCPersonality)

class TestQuestSystem:
    def test_full_quest_cycle(self):
        system = QuestSystem()

        # 1. Generate a quest
        quest = system.generate_quest("quest1", quest_type=QuestType.KILL, difficulty=QuestDifficulty.EASY)
        assert quest is not None

        # 2. Complete a step
        step_desc = quest.steps[0].description
        updated_quest = system.complete_step("quest1", step_desc)
        assert updated_quest.steps[0].completed is True
        assert updated_quest.completed is True

        # 3. Get the reward
        reward = system.get_quest_reward("quest1")
        assert reward is not None
        assert reward.experience > 0
