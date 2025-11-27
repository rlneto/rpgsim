"""
Core systems for RPGSim
"""

from .character.facade import CharacterSystem
from .combat.facade import CombatSystem
from .shop.facade import ShopSystem
from .world.facade import WorldSystem

# New modular systems
try:
    from .inventory.facade import InventorySystem

    __all__ = [
        "CharacterSystem",
        "CombatSystem",
        "ShopSystem",
        "WorldSystem",
        "InventorySystem",
    ]
except ImportError:
    __all__ = [
        "CharacterSystem",
        "CombatSystem",
        "ShopSystem",
        "WorldSystem",
    ]
