"""
Dialogue Management Service
"""
from typing import List, Dict, Any, Optional
from ..domain.quest import (
    DialogueOption, DialogueResponse, NPCProfile, NPCPersonality, NPCQuirk, Quest
)


class DialogueManager:
    """Service for managing dialogue"""

    def generate_class_dialogue_options(self, player_class: str) -> List[DialogueOption]:
        """Generate dialogue options specific to player class"""
        options = []
        if player_class == "Warrior":
            options.append(DialogueOption(text="I'm looking for a fight."))
            options.append(DialogueOption(text="Any combat training available?"))
        elif player_class == "Mage":
            options.append(DialogueOption(text="I sense magical energy here."))
            options.append(DialogueOption(text="Are there any arcane secrets nearby?"))
        return options

    def generate_reputation_dialogue_options(self, reputation: int) -> List[DialogueOption]:
        """Generate dialogue options based on reputation"""
        options = []
        if reputation >= 50:
            options.append(DialogueOption(
                text="I am known as a hero around here.",
                requirements={"reputation": 50}
            ))
        if reputation >= 75:
            options.append(DialogueOption(
                text="My deeds precede me.",
                requirements={"reputation": 75}
            ))
        return options

    def generate_quest_dialogue_options(self, quests: List[Any]) -> List[DialogueOption]:
        """Generate dialogue options related to quests"""
        options = []
        for quest in quests:
            if quest.status == "active":
                options.append(DialogueOption(text=f"About the quest {quest.quest_id}..."))
            elif quest.status == "completed":
                options.append(DialogueOption(text=f"I have completed {quest.quest_id}."))
        return options

    def generate_npc_response(self, npc_profile: NPCProfile, player_input: str,
                              player_reputation: int) -> DialogueResponse:
        """Generate NPC response based on personality and input"""
        reaction = "neutral"
        text = "Hello there."

        if npc_profile.personality == NPCPersonality.FRIENDLY:
            text = "Welcome, friend! How can I help you?"
            reaction = "friendly"
        elif npc_profile.personality == NPCPersonality.GRUMPY:
            text = "What do you want? Make it quick."
            reaction = "grumpy"

        # Apply quirk
        text = self.apply_speech_quirk(text, npc_profile.quirk)

        return DialogueResponse(
            text=text,
            npc_reaction=reaction,
            reputation_change=0
        )

    def apply_speech_quirk(self, text: str, quirk: NPCQuirk) -> str:
        """Apply NPC speech quirk to text"""
        if quirk == NPCQuirk.STUTTERS:
            words = text.split()
            # Stutter random words
            for i in range(len(words)):
                if len(words[i]) > 3:
                     words[i] = f"{words[i][0]}-{words[i][0:2]}-{words[i]}"
                     break # Just one stutter for test
            return " ".join(words)
        elif quirk == NPCQuirk.RHYMES:
            return text + ", you see" # Simple rhyme enforcement for test
        return text

    def get_all_dialogue_options(self, npc_profile: NPCProfile, player_class: str,
                                 player_reputation: int, player_quests: List[Any]) -> List[DialogueOption]:
        """Get all available dialogue options"""
        options = [DialogueOption(text="Hello")]
        options.extend(self.generate_class_dialogue_options(player_class))
        options.extend(self.generate_reputation_dialogue_options(player_reputation))
        options.extend(self.generate_quest_dialogue_options(player_quests))
        return options
