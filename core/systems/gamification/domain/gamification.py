"""
Domain entities for the Gamification System.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class Achievement:
    """Represents an achievement that a player can unlock."""
    id: str
    name: str
    description: str
    criteria: Dict[str, Any]
    unlocked: bool = False

@dataclass
class Badge:
    """Represents a badge awarded for an achievement."""
    id: str
    name: str
    icon_url: str
    achievement_id: str

@dataclass
class Progress:
    """Represents a player's progress."""
    player_id: str
    achievements: List[Achievement] = field(default_factory=list)
    badges: List[Badge] = field(default_factory=list)
    experience: int = 0
    level: int = 1

@dataclass
class Reward:
    """Represents a reward given to a player."""
    id: str
    name: str
    description: str
    value: int
