"""
In-memory implementation of the dungeon repository
"""
from typing import Dict, Optional, List
from ..domain.dungeon import Dungeon
from ..interfaces.repositories import DungeonRepository


class MemoryDungeonRepository(DungeonRepository):
    """In-memory implementation of a dungeon repository"""

    def __init__(self):
        self._dungeons: Dict[str, Dungeon] = {}

    def get_by_id(self, dungeon_id: str) -> Optional[Dungeon]:
        """Get a dungeon by its ID"""
        return self._dungeons.get(dungeon_id)

    def get_all(self) -> List[Dungeon]:
        """Get all dungeons"""
        return list(self._dungeons.values())

    def save(self, dungeon: Dungeon) -> None:
        """Save a dungeon"""
        self._dungeons[dungeon.id] = dungeon
