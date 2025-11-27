"""
Character business logic services
"""
from typing import Dict, List, Optional
from ..domain.character import Character, CharacterClass, CharacterStats


class CharacterCreationService:
    """Service for character creation logic"""
    
    def __init__(self):
        from ..domain.character import CHARACTER_CLASSES
        self.class_configs = CHARACTER_CLASSES
    
    def create_character(self, name: str, class_name: str) -> Character:
        """Create a new character with given name and class"""
        if not name or len(name.strip()) == 0:
            return Character()
        
        # Parse class name
        try:
            character_class = self._parse_class(class_name)
        except ValueError:
            return Character()
        
        # Get class configuration
        if character_class not in self.class_configs:
            return Character()
        
        config = self.class_configs[character_class]
        
        # Create character with proper stats
        character = Character(
            id=self._generate_id(),
            name=name.strip(),
            class_type=character_class,
            stats=config.base_stats,
            hp=config.base_stats.constitution * 10,
            max_hp=config.base_stats.constitution * 10,
            gold=100,
            inventory=["Basic Clothes", "Travel Rations"],
            abilities=config.abilities.copy(),
            created=True
        )
        
        return character
    
    def _parse_class(self, class_name: str) -> CharacterClass:
        """Parse class name string to enum value"""
        class_str = class_name.strip().lower()
        
        for char_class in CharacterClass:
            if char_class.value.lower() == class_str:
                return char_class
        
        raise ValueError(f"Unknown character class: {class_name}")
    
    def _generate_id(self) -> str:
        """Generate unique character ID"""
        import uuid
        return str(uuid.uuid4())[:8]


class CharacterProgressionService:
    """Service for character progression logic"""
    
    def level_up(self, character: Character) -> bool:
        """Level up character with stat improvements"""
        if not character.created or character.level < 1:
            return False
        
        character.level += 1
        
        # Improve primary stat
        if character.class_type:
            from ..domain.character import CHARACTER_CLASSES
            config = CHARACTER_CLASSES[character.class_type]
            primary_stat_value = character.stats.primary_stat_value(config.primary_stat)
            primary_stat_value += 1
            
        return True
    
    def add_experience(self, character: Character, exp_amount: int) -> bool:
        """Add experience to character"""
        if exp_amount <= 0:
            return False
        
        character.experience += exp_amount
        return True


class CharacterInventoryService:
    """Service for character inventory management"""
    
    def add_item(self, character: Character, item: str) -> bool:
        """Add item to character inventory"""
        if not item or not item.strip():
            return False
        
        character.inventory.append(item.strip())
        return True
    
    def remove_item(self, character: Character, item: str) -> bool:
        """Remove item from character inventory"""
        try:
            character.inventory.remove(item)
            return True
        except ValueError:
            return False
    
    def get_inventory_count(self, character: Character) -> int:
        """Get number of items in inventory"""
        return len(character.inventory)


class CharacterBalanceService:
    """Service for character class balance analysis"""
    
    def __init__(self):
        from ..domain.character import CHARACTER_CLASSES
        self.class_configs = CHARACTER_CLASSES
    
    def get_balance_stats(self) -> Dict[str, int]:
        """Calculate power levels for all classes"""
        balance_stats = {}
        
        for char_class, config in self.class_configs.items():
            power = config.base_stats.total_power()
            balance_stats[char_class.value] = power
        
        return balance_stats
    
    def validate_balance(self) -> bool:
        """Check if all classes are within 15% power difference"""
        balance_stats = self.get_balance_stats()
        
        if not balance_stats:
            return False
        
        max_power = max(balance_stats.values())
        min_power = min(balance_stats.values())
        
        balance_ratio = (max_power - min_power) / min_power if min_power > 0 else 0
        return balance_ratio <= 0.15
    
    def verify_unique_mechanics(self) -> bool:
        """Check if all classes have unique mechanics"""
        mechanics = [
            config.mechanic for config in self.class_configs.values()
        ]
        
        return len(set(mechanics)) == len(mechanics)
    
    def verify_minimum_abilities(self) -> bool:
        """Check if all classes have at least 10 abilities"""
        for config in self.class_configs.values():
            if len(config.abilities) < 10:
                return False
        
        return True