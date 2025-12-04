from dataclasses import dataclass, field
from typing import List
from enum import Enum

class QuestType(Enum):
    KILL = "kill"
    FETCH = "fetch"
    ESCORT = "escort"
    EXPLORE = "explore"
    DELIVER = "deliver"
    PROTECT = "protect"
    SOLVE = "solve"
    RESCUE = "rescue"

class QuestDifficulty(Enum):
    TRIVIAL = "trivial"
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    VERY_HARD = "very_hard"
    EPIC = "epic"

@dataclass
class QuestStep:
    description: str
    completed: bool = False

@dataclass
class QuestReward:
    experience: int = 0
    gold: int = 0
    items: List[str] = field(default_factory=list)

@dataclass
class Quest:
    id: str
    name: str
    description: str
    steps: List[QuestStep] = field(default_factory=list)
    reward: QuestReward = field(default_factory=QuestReward)
    completed: bool = False
