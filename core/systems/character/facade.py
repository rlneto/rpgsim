"""
Facade for character system operations
"""

from typing import List, Dict, Optional
from .domain.character import Character, CharacterClass
from .services.character_service import (
    CharacterCreationService,
    CharacterProgressionService,
    CharacterInventoryService,
    CharacterBalanceService,
)
from .repositories.memory_repository import MemoryCharacterRepository
from .exceptions.character_exceptions import (
    CharacterCreationError,
    CharacterNotFoundError,
)


class CharacterSystem:
    """Facade for all character system operations"""

    def __init__(self, repository=None):
        # Dependency injection
        self.repository = repository or MemoryCharacterRepository()
        self.creation_service = CharacterCreationService()
        self.progression_service = CharacterProgressionService()
        self.inventory_service = CharacterInventoryService()
        self.balance_service = CharacterBalanceService()

    def create_character(self, name: str, class_type: str) -> Character:
        """Create a new character"""
        character = self.creation_service.create_character(name, class_type)

        if not character.created:
            raise CharacterCreationError(
                f"Failed to create character: {name} ({class_type})"
            )

        # Save to repository
        self.repository.save(character)
        return character

    def get_character(self, character_id: str) -> Optional[Character]:
        """Get character by ID"""
        return self.repository.load(character_id)

    def get_character_by_name(self, name: str) -> Optional[Character]:
        """Get character by name"""
        return self.repository.load_by_name(name)

    def level_up_character(self, character_id: str) -> bool:
        """Level up character by ID"""
        character = self.repository.load(character_id)
        if not character:
            raise CharacterNotFoundError(f"Character not found: {character_id}")

        success = self.progression_service.level_up(character)
        if success:
            self.repository.save(character)

        return success

    def add_to_inventory(self, character_id: str, item: str) -> bool:
        """Add item to character inventory"""
        character = self.repository.load(character_id)
        if not character:
            raise CharacterNotFoundError(f"Character not found: {character_id}")

        success = self.inventory_service.add_item(character, item)
        if success:
            self.repository.save(character)

        return success

    def remove_from_inventory(self, character_id: str, item: str) -> bool:
        """Remove item from character inventory"""
        character = self.repository.load(character_id)
        if not character:
            raise CharacterNotFoundError(f"Character not found: {character_id}")

        success = self.inventory_service.remove_item(character, item)
        if success:
            self.repository.save(character)

        return success

    def get_inventory_count(self, character_id: str) -> int:
        """Get character inventory count"""
        character = self.repository.load(character_id)
        if not character:
            raise CharacterNotFoundError(f"Character not found: {character_id}")

        return self.inventory_service.get_inventory_count(character)

    def get_class_stats(self, class_name: str) -> Optional[Dict]:
        """Get stats for specific class"""
        try:
            character_class = self.creation_service._parse_class(class_name)
        except ValueError:
            return None

        config_repo = self.creation_service.config_repo

        config_repo = MemoryClassConfigRepository()
        return config_repo.get_config(character_class)

    def get_class_mechanic(self, class_name: str) -> Optional[str]:
        """Get mechanic for specific class"""
        stats = self.get_class_stats(class_name)
        return stats.get("mechanic") if stats else None

    def get_class_abilities(self, class_name: str) -> Optional[List[str]]:
        """Get abilities for specific class"""
        stats = self.get_class_stats(class_name)
        return stats.get("abilities") if stats else None

    def get_all_classes(self) -> List[str]:
        """Get list of all available character classes"""
        return [cls.value for cls in CharacterClass]

    def validate_class_balance(self) -> bool:
        """Validate that all classes are balanced"""
        return self.balance_service.validate_balance()

    def verify_unique_mechanics(self) -> bool:
        """Verify that all classes have unique mechanics"""
        return self.balance_service.verify_unique_mechanics()

    def verify_minimum_abilities(self) -> bool:
        """Verify that all classes have minimum abilities"""
        return self.balance_service.verify_minimum_abilities()

    def list_all_characters(self) -> List[Character]:
        """List all characters"""
        return self.repository.list_all()


# Global facade instance for backward compatibility
_character_system = CharacterSystem()


# Backward compatibility functions
def create_character(name: str, class_type: str) -> Character:
    """Create a character (backward compatibility)"""
    return _character_system.create_character(name, class_type)


def level_up_character(character: Character) -> bool:
    """Level up character (backward compatibility)"""
    return character.level_up()


def add_experience(character: Character, exp_amount: int) -> bool:
    """Add experience to character (backward compatibility)"""
    if exp_amount <= 0:
        return False

    character.experience += exp_amount
    return True


def get_all_character_classes() -> List[str]:
    """Get all character classes (backward compatibility)"""
    return _character_system.get_all_classes()


def get_class_balance_stats() -> Dict[str, int]:
    """Get class balance statistics"""
    from .repositories.memory_repository import MemoryClassConfigRepository
    from .domain.character import CHARACTER_CLASSES

    balance_stats = {}
    for char_class, config in CHARACTER_CLASSES.items():
        balance_stats[char_class.value] = config.base_stats.total_power()

    return balance_stats


# Export main class and compatibility functions
__all__ = [
    "CharacterSystem",
    "create_character",
    "level_up_character",
    "add_experience",
    "get_all_character_classes",
    "get_class_balance_stats",
]
