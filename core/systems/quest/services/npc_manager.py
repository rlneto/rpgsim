"""
NPC Management Service
"""
from typing import List, Dict, Optional
import random
import uuid
from ..domain.quest import (
    NPCProfile, NPCPersonality, NPCQuirk
)


class NPCManager:
    """Service for managing NPCs"""

    def __init__(self):
        self.npcs: Dict[str, NPCProfile] = {}

    def create_npc_profile(self, npc_id: str, name: str, location: str,
                           personality: NPCPersonality = None,
                           quirk: NPCQuirk = None) -> NPCProfile:
        """Create a new NPC profile"""
        if personality is None:
            personality = random.choice(list(NPCPersonality))
        if quirk is None:
            quirk = random.choice(list(NPCQuirk))

        npc = NPCProfile(
            npc_id=npc_id,
            name=name,
            location=location,
            personality=personality,
            quirk=quirk,
            specialties=["General Knowledge"]
        )
        self.npcs[npc_id] = npc
        return npc

    def generate_npcs(self, count: int, locations: List[str] = None) -> List[NPCProfile]:
        """Generate a batch of NPCs"""
        generated = []
        if not locations:
            locations = ["Default Town"]

        first_names = ["John", "Jane", "Thorin", "Elara", "Gimli", "Legolas", "Aragorn", "Gandalf"]
        last_names = ["Smith", "Doe", "Oakenshield", "Moonwhisper", "Gloomstalker"]

        for i in range(count):
            name = f"{random.choice(first_names)} {random.choice(last_names)}"
            location = random.choice(locations)
            npc_id = f"npc_{uuid.uuid4().hex[:8]}"

            # Setup some basic relationships for tests
            npc = self.create_npc_profile(npc_id, name, location)

            # Add some dummy data for tests
            npc.specialties = ["Trade", "Rumors"]
            npc.relationships = {"player": "neutral"}
            npc.secrets = ["Has a hidden stash"]

            generated.append(npc)

        return generated

    def get_npc_by_id(self, npc_id: str) -> Optional[NPCProfile]:
        """Get NPC by ID"""
        return self.npcs.get(npc_id)

    def get_npcs_by_location(self, location: str) -> List[NPCProfile]:
        """Get NPCs in a specific location"""
        return [npc for npc in self.npcs.values() if npc.location == location]
