"""
Repository interfaces for the Dungeon System
"""
from abc import ABC, abstractmethod
from typing import Optional, List
from ..domain.dungeon import Dungeon


class DungeonRepository(ABC):
    """Interface for a dungeon repository"""

    @abstractmethod
    def add(self, dungeon: Dungeon) -> None:
        """Add a dungeon to the repository"""
        pass

    @abstractmethod
    def get(self, dungeon_id: str) -> Optional[Dungeon]:
        """Get a dungeon by ID"""
        pass

    @abstractmethod
    def list(self) -> List[Dungeon]:
        """List all dungeons"""
        pass
