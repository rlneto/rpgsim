from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum

class NPCPersonality(Enum):
    FRIENDLY = "friendly"
    GRUMPY = "grumpy"
    MYSTERIOUS = "mysterious"

class NPCQuirk(Enum):
    STUTTERS = "stutters"
    RHYMES = "rhymes"
    USES_ANCIENT_WORDS = "uses_ancient_words"

@dataclass
class NPCProfile:
    id: str
    name: str
    location: str
    personality: NPCPersonality
    quirks: List[NPCQuirk] = field(default_factory=list)
    dialogue_responses: Dict[str, str] = field(default_factory=dict)

@dataclass
class DialogueOption:
    text: str
    requires_quest_status: Optional[str] = None

@dataclass
class DialogueResponse:
    text: str
    gives_quest: Optional[str] = None
