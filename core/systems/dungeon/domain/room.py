"""
Domain entities for rooms in a dungeon
"""
from dataclasses import dataclass, field
from typing import List, Optional, Any, Dict
from enum import Enum
from .treasure import Treasure
from .trap import Trap


class RoomType(Enum):
    """Types of rooms"""
    ENTRANCE = "entrance"
    CHAMBER = "chamber"
    CORRIDOR = "corridor"
    BOSS_ROOM = "boss_room"
    TREASURE_ROOM = "treasure_room"
    PUZZLE_ROOM = "puzzle_room"
    TRAP_ROOM = "trap_room"
    SHRINE = "shrine"
    SHOP = "shop"
    REST_AREA = "rest_area"


class EnvironmentalChallenge(Enum):
    """Environmental hazards"""
    DARKNESS = "darkness"
    POISON = "poison"
    FIRE = "fire"
    ICE = "ice"
    ELECTRICITY = "electricity"
    WIND = "wind"
    GRAVITY = "gravity"
    TIME_WARP = "time_warp"


class PuzzleType(Enum):
    """Types of puzzles encountered"""
    MECHANICAL = "mechanical"
    MAGICAL = "magical"
    LOGICAL = "logical"
    SPATIAL = "spatial"
    TEMPORAL = "temporal"
    PATTERN = "pattern"
    RIDDLE = "riddle"
    ENVIRONMENTAL = "environmental"


class LoreType(Enum):
    """Types of lore elements"""
    INSCRIPTIONS = "inscriptions"
    BOOKS = "books"
    SCROLLS = "scrolls"
    MURALS = "murals"
    STATUES = "statues"
    GHOSTS = "ghosts"
    ARTIFACTS = "artifacts"


@dataclass
class Room:
    """A room within a dungeon"""
    id: str
    type: RoomType
    x: int
    y: int
    connections: List[str] = field(default_factory=list)
    contents: List[str] = field(default_factory=list)
    secrets: List[str] = field(default_factory=list)
    treasures: List[Treasure] = field(default_factory=list)
    traps: List[Trap] = field(default_factory=list)
    challenge: Optional[EnvironmentalChallenge] = None
    puzzle: Optional[PuzzleType] = None
    lore: Optional[LoreType] = None
    explored: bool = False

    def add_connection(self, room_id: str) -> None:
        """Add a connection to another room"""
        if room_id not in self.connections:
            self.connections.append(room_id)

    def explore(self) -> Dict[str, Any]:
        """Explore the room and return contents"""
        if self.explored:
            return {}

        self.explored = True
        return {
            'room_id': self.id,
            'type': self.type.value if hasattr(self.type, 'value') else str(self.type),
            'contents': self.contents,
            'secrets': self.secrets,
            'treasures': [t.__dict__ for t in self.treasures],
            'traps': [t.__dict__ for t in self.traps],
            'challenge': self.challenge.value if self.challenge else None,
            'puzzle': self.puzzle.value if self.puzzle else None,
            'lore': self.lore.value if self.lore else None
        }
