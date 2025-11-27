"""
Memory repository implementations for character data
"""
from typing import List, Dict, Optional
from ..interfaces.repositories import CharacterRepository, ClassConfigRepository
from ..domain.character import Character, CharacterClass
from ..exceptions.character_exceptions import CharacterNotFoundError


class MemoryCharacterRepository(CharacterRepository):
    """In-memory character repository"""

    def __init__(self):
        self._characters: Dict[str, Character] = {}

    def save(self, character: Character) -> bool:
        """Save character to memory storage"""
        if not character.id:
            return False

        self._characters[character.id] = character
        return True

    def load(self, character_id: str) -> Optional[Character]:
        """Load character by ID"""
        return self._characters.get(character_id)

    def load_by_name(self, name: str) -> Optional[Character]:
        """Load character by name"""
        for character in self._characters.values():
            if character.name == name:
                return character
        return None

    def delete(self, character_id: str) -> bool:
        """Delete character by ID"""
        if character_id in self._characters:
            del self._characters[character_id]
            return True
        return False

    def list_all(self) -> List[Character]:
        """List all characters"""
        return list(self._characters.values())


class MemoryClassConfigRepository(ClassConfigRepository):
    """In-memory class configuration repository"""

    def __init__(self):
        from ..domain.character import CHARACTER_CLASSES
        self._configs = CHARACTER_CLASSES

    def get_config(self, character_class: CharacterClass) -> Optional[Dict]:
        """Get configuration for specific class"""
        if character_class in self._configs:
            config = self._configs[character_class]
            return {
                "mechanic": config.mechanic,
                "base_stats": config.base_stats.__dict__,
                "primary_stat": config.primary_stat,
                "abilities": config.abilities
            }
        return None

    def get_all_configs(self) -> Dict[CharacterClass, Dict]:
        """Get all class configurations"""
        configs = {}
        for char_class, config in self._configs.items():
            configs[char_class] = self.get_config(char_class)
        return configs
