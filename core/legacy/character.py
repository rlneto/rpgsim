"""
Backward Compatibility Wrapper for Character System

This file provides backward compatibility while using the new modular architecture.
Old imports will redirect to the new system.
"""

# Redirect imports to new modular system
from ..systems.character.facade import (
    CharacterSystem,
    create_character,
    level_up_character,
    add_experience,
    get_all_character_classes,
    get_class_balance_stats,
)

from ..systems.character.domain.character import (
    Character,
    CharacterClass,
    CharacterStats,
)

# Legacy exports for backward compatibility
__all__ = [
    "Character",
    "CharacterClass",
    "CharacterStats",
    "CharacterSystem",
    "create_character",
    "level_up_character",
    "add_experience",
    "get_all_character_classes",
    "get_class_balance_stats",
]
