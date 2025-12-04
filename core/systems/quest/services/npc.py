import random
from typing import List, Optional
from core.systems.quest.domain.npc import NPCProfile, NPCPersonality, NPCQuirk, DialogueOption, DialogueResponse

class NPCService:
    NAME_PREFIXES = ["Guard", "Merchant", "Scholar"]
    NAME_SUFFIXES = ["John", "Mary", "William"]

    def generate_npc(self, npc_id: str, location: str) -> NPCProfile:
        name = f"{random.choice(self.NAME_PREFIXES)} {random.choice(self.NAME_SUFFIXES)}"
        personality = random.choice(list(NPCPersonality))
        quirks = random.sample(list(NPCQuirk), random.randint(0, 1))
        dialogue_responses = self._generate_dialogue_responses(personality)

        npc = NPCProfile(
            id=npc_id,
            name=name,
            location=location,
            personality=personality,
            quirks=quirks,
            dialogue_responses=dialogue_responses,
        )
        return npc

    def get_dialogue_options(self) -> List[DialogueOption]:
        return [DialogueOption("Hello"), DialogueOption("Goodbye")]

    def get_npc_response(self, option: DialogueOption, npc: NPCProfile) -> DialogueResponse:
        if "Hello" in option.text:
            response_text = npc.dialogue_responses.get("greeting", "Hello.")
        else:
            response_text = npc.dialogue_responses.get("farewell", "Goodbye.")

        return DialogueResponse(text=response_text)

    def _generate_dialogue_responses(self, personality: NPCPersonality) -> dict:
        if personality == NPCPersonality.GRUMPY:
            return {"greeting": "What do you want?", "farewell": "Leave me alone."}
        elif personality == NPCPersonality.FRIENDLY:
            return {"greeting": "Greetings, traveler!", "farewell": "Safe travels!"}
        else:
            return {"greeting": "The winds whisper of your arrival...", "farewell": "Our paths may cross again..."}
