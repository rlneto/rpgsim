"""
Inventory Module for RPGSim
Manages player inventory and item operations
"""

try:
    from .domain.inventory import Inventory, InventorySlot
    from .services.inventory_service import InventoryService
    from .repositories.memory_repository import MemoryInventoryRepository
    from .facade import InventorySystem

    __all__ = [
        "Inventory",
        "InventorySlot",
        "InventoryService",
        "MemoryInventoryRepository",
        "InventorySystem",
    ]
except ImportError:
    # Fallback if components are not fully implemented
    __all__ = []
