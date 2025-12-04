"""
Quest System Facade
"""
from typing import List, Dict, Any, Optional
from .services.quest_generator import QuestGenerator
from .services.npc_manager import NPCManager
from .services.dialogue_manager import DialogueManager
from .services.quest_manager import QuestManager
from .domain.quest import Quest, QuestProgress, NPCProfile, QuestType, QuestDifficulty

class QuestSystem:
    """Facade for the Quest System"""

    def __init__(self):
        self.quest_generator = QuestGenerator()
        self.npc_manager = NPCManager()
        self.dialogue_manager = DialogueManager()
        self.quest_manager = QuestManager()
        self.available_quests: Dict[str, List[Quest]] = {} # Location -> Quests

    def initialize_world(self, locations: List[str], npc_count: int = 20) -> Dict[str, Any]:
        """Initialize world with quests and NPCs"""
        # Generate NPCs
        npcs = self.npc_manager.generate_npcs(npc_count, locations)

        # Generate Quests for locations
        generated_quests = []
        for location in locations:
            # Generate 1-3 quests per location
            for _ in range(2):
                quest = self.quest_generator.generate_quest(location=location)
                if location not in self.available_quests:
                    self.available_quests[location] = []
                self.available_quests[location].append(quest)
                generated_quests.append(quest)

        return {
            "npcs": npcs,
            "available_quests": generated_quests
        }

    def get_available_quests_for_location(self, location: str) -> List[Quest]:
        """Get available quests for a location"""
        return self.available_quests.get(location, [])

    def get_npcs_in_location(self, location: str) -> List[NPCProfile]:
        """Get NPCs in a location"""
        return self.npc_manager.get_npcs_by_location(location)

    def start_quest_from_npc(self, player_id: str, quest_id: str, npc_id: str) -> Optional[QuestProgress]:
        """Start a quest given by an NPC"""
        # Find the quest
        quest_to_start = None
        for quests in self.available_quests.values():
            for q in quests:
                if q.quest_id == quest_id:
                    quest_to_start = q
                    break
            if quest_to_start:
                break

        if quest_to_start:
            return self.quest_manager.start_quest(player_id, quest_to_start)
        return None
