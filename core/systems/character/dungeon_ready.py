"""
Character System Update for Dungeon Exploration
FOCUS: Add dungeon-ready features to existing characters
"""

from typing import Dict, List, Optional

# Add dungeon exploration methods to existing Character class
def add_dungeon_exploration_to_character():
    """Add dungeon exploration methods to Character class"""
    
    # Import existing Character class
    try:
        from .domain.character import Character
    except ImportError:
        # Create mock Character for testing
        class Character:
            def __init__(self, name: str, level: int = 1, hp: int = 100, max_hp: int = 100, gold: int = 50):
                self.name = name
                self.level = level
                self.hp = hp
                self.max_hp = max_hp
                self.gold = gold
        
        # Add to module namespace for import
        import sys
        sys.modules[__name__].Character = Character
    
    # Import Character (now available)
    from .domain.character import Character
    
    def can_enter_dungeon(self, difficulty: str) -> bool:
        """Check if character can enter dungeon"""
        # Basic requirements
        if self.level < 1:
            return False
        if self.hp < self.max_hp * 0.5:  # Need at least 50% HP
            return False
        return True
    
    def prepare_for_dungeon(self) -> Dict:
        """Prepare character for dungeon exploration"""
        preparation = {
            "potions": 2 if self.gold >= 30 else 1,
            "weapons_sharpened": True,
            "armor_repaired": True,
            "cost": 30 if self.gold >= 30 else 15
        }
        
        if self.gold >= preparation["cost"]:
            self.gold -= preparation["cost"]
            self.hp = min(self.max_hp, self.hp + 20)  # Rest bonus
        
        return preparation
    
    def get_dungeon_readiness(self) -> Dict:
        """Get character's readiness for dungeon"""
        return {
            "level_ready": self.level >= 1,
            "hp_ready": self.hp >= self.max_hp * 0.5,
            "gold_ready": self.gold >= 15,
            "overall_ready": self.can_enter_dungeon("normal")
        }
    
    # Add methods to Character class
    Character.can_enter_dungeon = can_enter_dungeon
    Character.prepare_for_dungeon = prepare_for_dungeon
    Character.get_dungeon_readiness = get_dungeon_readiness

# Apply update
add_dungeon_exploration_to_character()
