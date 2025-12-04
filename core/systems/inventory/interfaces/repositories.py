"""
Inventory repository interface
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from core.systems.inventory.domain.inventory import Inventory


class InventoryRepository(ABC):
    """Abstract repository for inventory persistence"""

    @abstractmethod
    def save(self, character_id: str, inventory: Inventory) -> bool:
        """Save inventory to repository"""
        pass

    @abstractmethod
    def load(self, character_id: str) -> Optional[Inventory]:
        """Load inventory from repository"""
        pass

    @abstractmethod
    def delete(self, character_id: str) -> bool:
        """Delete inventory from repository"""
        pass

    @abstractmethod
    def exists(self, character_id: str) -> bool:
        """Check if inventory exists"""
        pass
