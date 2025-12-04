"""
Interfaces for the dungeon system repositories
"""
from abc import ABC, abstractmethod
from typing import Optional, List
from ..domain.dungeon import Dungeon


class DungeonRepository(ABC):
    """Interface for a dungeon repository"""

    @abstractmethod
    def get_by_id(self, dungeon_id: str) -> Optional[Dungeon]:
        """Get a dungeon by its ID"""
        pass

    @abstractmethod
    def get_all(self) -> List[Dungeon]:
        """Get all dungeons"""
        pass

    @abstractmethod
    def save(self, dungeon: Dungeon) -> None:
        """Save a dungeon"""
        pass
