"""
Character data repository interfaces
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from ..domain.character import Character, CharacterClass


class CharacterRepository(ABC):
    """Repository interface for character data access"""
    
    @abstractmethod
    def save(self, character: Character) -> bool:
        """Save character to storage"""
        pass
    
    @abstractmethod
    def load(self, character_id: str) -> Optional[Character]:
        """Load character by ID"""
        pass
    
    @abstractmethod
    def load_by_name(self, name: str) -> Optional[Character]:
        """Load character by name"""
        pass
    
    @abstractmethod
    def delete(self, character_id: str) -> bool:
        """Delete character by ID"""
        pass
    
    @abstractmethod
    def list_all(self) -> List[Character]:
        """List all characters"""
        pass


class ClassConfigRepository(ABC):
    """Repository interface for class configuration data"""
    
    @abstractmethod
    def get_config(self, character_class: CharacterClass) -> Optional[Dict]:
        """Get configuration for specific class"""
        pass
    
    @abstractmethod
    def get_all_configs(self) -> Dict[CharacterClass, Dict]:
        """Get all class configurations"""
        pass