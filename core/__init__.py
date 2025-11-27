"""
Core Module for RPGSim
Provides centralized access to all core systems and models
"""

from .models import (
    CharacterClass,
    CharacterStats,
    Character,
    ItemRarity,
    ItemType,
    Item,
    EnemyType,
    Enemy,
    QuestStatus,
    QuestObjective,
    Quest,
    LocationType,
    Location,
    GameState,
)

from .engine import get_game_engine, GameEngine

from .systems import (
    CharacterSystem,
    CombatSystem,
    ShopSystem,
    WorldSystem,
)

__all__ = [
    # Models
    "CharacterClass",
    "CharacterStats",
    "Character",
    "ItemRarity",
    "ItemType",
    "Item",
    "EnemyType",
    "Enemy",
    "QuestStatus",
    "QuestObjective",
    "Quest",
    "LocationType",
    "Location",
    "GameState",
    # Engine
    "get_game_engine",
    "GameEngine",
    # Systems
    "CharacterSystem",
    "CombatSystem",
    "ShopSystem",
    "WorldSystem",
]
