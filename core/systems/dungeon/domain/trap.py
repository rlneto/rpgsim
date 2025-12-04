"""
Domain entities for traps in a dungeon
"""
from dataclasses import dataclass
from enum import Enum


class TrapType(Enum):
    """Types of traps"""
    MECHANICAL = "mechanical"
    MAGICAL = "magical"
    NATURAL = "natural"


@dataclass
class Trap:
    """A trap within a dungeon room"""
    id: str
    type: TrapType
    description: str
    disarmed: bool = False
