"""
In-memory repository for the Dungeon System
"""
from typing import Dict, Optional, List
from ..domain.dungeon import Dungeon
from ..interfaces.repositories import DungeonRepository


class MemoryDungeonRepository(DungeonRepository):
    """In-memory implementation of a dungeon repository"""

    def __init__(self):
        self._dungeons: Dict[str, Dungeon] = {}

    def add(self, dungeon: Dungeon) -> None:
        """Add a dungeon to the repository"""
        self._dungeons[dungeon.id] = dungeon

    def get(self, dungeon_id: str) -> Optional[Dungeon]:
        """Get a dungeon by ID"""
        return self._dungeons.get(dungeon_id)

    def list(self) -> List[Dungeon]:
        """List all dungeons"""
        return list(self._dungeons.values())
