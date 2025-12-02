"""
Character Module for RPGSim
Provides character creation and management functionality
"""

# Re-export from systems.character for backward compatibility
from ..systems.character import (
    Character,
    CharacterClass,
    CharacterStats,
    CharacterSystem,
)

__all__ = [
    "Character",
    "CharacterClass",
    "CharacterStats",
    "CharacterSystem",
]
