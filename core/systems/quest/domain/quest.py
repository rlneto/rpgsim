"""
Quest system domain entities and value objects
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
from datetime import datetime


class QuestType(Enum):
    """Types of quests"""
    KILL = "kill"
    FETCH = "fetch"
    ESCORT = "escort"
    EXPLORE = "explore"
    DELIVER = "deliver"
    PROTECT = "protect"
    SOLVE = "solve"
    RESCUE = "rescue"


class QuestDifficulty(Enum):
    """Difficulty levels for quests"""
    TRIVIAL = "trivial"
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    VERY_HARD = "very_hard"
    EPIC = "epic"


class NPCPersonality(Enum):
    """NPC personality types"""
    FRIENDLY = "friendly"
    GRUMPY = "grumpy"
    MYSTERIOUS = "mysterious"
    BOASTFUL = "boastful"
    HUMBLE = "humble"
    WISE = "wise"
    CUNNING = "cunning"
    CHAOTIC = "chaotic"
    NOBLE = "noble"
    MISCHIEVOUS = "mischievous"


class NPCQuirk(Enum):
    """NPC speech and behavior quirks"""
    NONE = "none"
    STUTTERS = "stutters"
    RHYMES = "rhymes"
    USES_ANCIENT_WORDS = "uses_ancient_words"
    SPEAKS_IN_RIDDLES = "speaks_in_riddles"
    ALWAYS_HUNGRY = "always_hungry"
    COLLECTS_THINGS = "collects_things"
    OVERLY_DRAMATIC = "overly_dramatic"
    SPEAKS_IN_THIRD_PERSON = "speaks_in_third_person"
    HAS_PET = "has_pet"
    SINGS_RESPONSES = "sings_responses"


@dataclass
class QuestObjective:
    """Objective within a quest"""
    description: str
    target_count: int = 1
    current_count: int = 0
    completed: bool = False
    target_id: Optional[str] = None
    target_type: Optional[str] = None


@dataclass
class QuestTemplate:
    """Template for generating quests"""
    name_template: str
    description_template: str
    objective_templates: List[str]
    quest_type: QuestType
    base_difficulty: QuestDifficulty
    reward_multipliers: Dict[str, float] = field(default_factory=lambda: {"experience": 1.0, "gold": 1.0})


@dataclass
class NPCProfile:
    """NPC profile data"""
    npc_id: str
    name: str
    location: str
    personality: NPCPersonality
    quirk: NPCQuirk
    specialties: List[str] = field(default_factory=list)
    relationships: Dict[str, str] = field(default_factory=dict)
    daily_schedule: Dict[str, str] = field(default_factory=dict)
    secrets: List[str] = field(default_factory=list)


@dataclass
class DialogueOption:
    """Option for player dialogue"""
    text: str
    requirements: Dict[str, Any] = field(default_factory=dict)
    responses: List[str] = field(default_factory=list)


@dataclass
class DialogueResponse:
    """NPC response to dialogue"""
    text: str
    npc_reaction: str
    quest_unlock: Optional[str] = None
    reputation_change: int = 0


@dataclass
class Quest:
    """Active quest data"""
    quest_id: str
    name: str
    description: str
    quest_type: QuestType
    difficulty: QuestDifficulty
    giver: str
    location: str
    objectives: List[QuestObjective]
    rewards: Dict[str, int]
    requirements: Dict[str, Any] = field(default_factory=dict)


@dataclass
class QuestProgress:
    """Player progress on a quest"""
    quest_id: str
    player_id: str
    status: str  # active, completed, failed, abandoned
    progress: Dict[str, Any] = field(default_factory=dict) # Can store raw progress data
    objectives: List[QuestObjective] = field(default_factory=list) # Store active objectives state
    start_date: datetime = field(default_factory=datetime.now)
    completion_date: Optional[datetime] = None
