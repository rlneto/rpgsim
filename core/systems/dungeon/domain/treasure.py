"""
Domain entities for treasure in a dungeon
"""
from dataclasses import dataclass
from enum import Enum


class RewardTier(Enum):
    """Tiers of rewards"""
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"


@dataclass
class Treasure:
    """A treasure item within a dungeon room"""
    id: str
    name: str
    tier: RewardTier
    value: int
