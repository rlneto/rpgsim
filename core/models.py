"""
Core Models for RPGSim
Optimized for LLM agents with explicit, deterministic behavior
"""

from typing import List, Dict, Any, Optional, Union
from enum import Enum
from pydantic import BaseModel, Field, validator
import json
from datetime import datetime


class CharacterClass(str, Enum):
    """Character class enumeration - explicit mapping for agent understanding."""
    WARRIOR = "warrior"
    MAGE = "mage"
    ROGUE = "rogue"
    CLERIC = "cleric"
    RANGER = "ranger"
    PALADIN = "paladin"
    WARLOCK = "warlock"
    DRUID = "druid"
    MONK = "monk"
    BARBARIAN = "barbarian"
    BARD = "bard"
    SORCERER = "sorcerer"
    FIGHTER = "fighter"
    NECROMANCER = "necromancer"
    ILLUSIONIST = "illusionist"
    ALCHEMIST = "alchemist"
    BERSERKER = "berserker"
    ASSASSIN = "assassin"
    HEALER = "healer"
    SUMMONER = "summoner"
    SHAPESHIFTER = "shapeshifter"
    ELEMENTALIST = "elementalist"
    NINJA = "ninja"

    def __str__(self) -> str:
        return self.value


class CharacterStats(BaseModel):
    """Character statistics model with explicit validation for agents."""
    
    strength: int = Field(ge=1, le=20, description="Physical strength")
    dexterity: int = Field(ge=1, le=20, description="Agility and reflexes")
    intelligence: int = Field(ge=1, le=20, description="Mental capacity")
    wisdom: int = Field(ge=1, le=20, description="Perception and insight")
    charisma: int = Field(ge=1, le=20, description="Social influence")
    constitution: int = Field(ge=1, le=20, description="Health and stamina")
    
    class Config:
        """Pydantic configuration for agent optimization."""
        validate_assignment = True
        use_enum_values = True
        extra = "forbid"
    
    @validator('*', pre=True)
    def validate_stats_are_integers(cls, v):
        """Ensure all stats are integers."""
        if not isinstance(v, int):
            raise ValueError("All stats must be integers")
        return v
    
    def get_stat_modifiers(self) -> Dict[str, int]:
        """Calculate stat modifiers based on stat values."""
        modifiers = {}
        for stat_name, stat_value in self.dict().items():
            modifier = (stat_value - 10) // 2
            modifiers[stat_name] = modifier
        return modifiers
    
    def get_total_stats(self) -> int:
        """Calculate total of all stats."""
        return sum(self.dict().values())


class Character(BaseModel):
    """Character model with explicit validation for agents."""
    
    id: str = Field(..., description="Unique character identifier")
    name: str = Field(min_length=1, max_length=50, description="Character name")
    class_type: CharacterClass = Field(..., description="Character class")
    level: int = Field(ge=1, le=100, description="Character level")
    experience: int = Field(ge=0, description="Experience points")
    stats: CharacterStats = Field(..., description="Character statistics")
    hp: int = Field(ge=0, description="Current hit points")
    max_hp: int = Field(ge=0, description="Maximum hit points")
    gold: int = Field(ge=0, description="Gold amount")
    abilities: List[str] = Field(default_factory=list, description="Character abilities")
    inventory: List[Any] = Field(default_factory=list, description="Inventory items")
    quests_completed: List[Any] = Field(default_factory=list, description="Completed quests")
    skills: Dict[str, int] = Field(default_factory=dict, description="Character skills")
    
    class Config:
        """Pydantic configuration for agent optimization."""
        validate_assignment = True
        use_enum_values = True
        extra = "forbid"
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
    
    @validator('name')
    def validate_character_name(cls, v):
        """Validate character name with explicit rules."""
        if not v or not v.strip():
            raise ValueError("Character name cannot be empty")
        
        if len(v.strip()) < 1:
            raise ValueError("Character name cannot be only whitespace")
        
        if len(v) > 50:
            raise ValueError("Character name cannot exceed 50 characters")
        
        # Check for invalid characters
        invalid_chars = ['<', '>', '/', '\\', '|', '?', '*', '"']
        for char in invalid_chars:
            if char in v:
                raise ValueError(f"Character name cannot contain '{char}'")
        
        return v.strip()
    
    @validator('hp')
    def validate_hp_not_exceed_max(cls, v, values):
        """Ensure HP does not exceed max HP."""
        if 'max_hp' in values and v > values['max_hp']:
            raise ValueError("Current HP cannot exceed maximum HP")
        return v
    
    @validator('max_hp')
    def validate_max_hp_positive(cls, v):
        """Ensure max HP is positive."""
        if v <= 0:
            raise ValueError("Maximum HP must be positive")
        return v
    
    def is_defeated(self) -> bool:
        """Check if character is defeated."""
        return self.hp <= 0
    
    def is_alive(self) -> bool:
        """Check if character is alive."""
        return self.hp > 0
    
    def get_hp_percentage(self) -> float:
        """Get HP as percentage of maximum."""
        if self.max_hp == 0:
            return 0.0
        return (self.hp / self.max_hp) * 100.0
    
    def heal(self, amount: int) -> int:
        """Heal character by specified amount."""
        if amount < 0:
            raise ValueError("Heal amount cannot be negative")
        
        old_hp = self.hp
        self.hp = min(self.hp + amount, self.max_hp)
        return self.hp - old_hp
    
    def damage(self, amount: int) -> int:
        """Damage character by specified amount."""
        if amount < 0:
            raise ValueError("Damage amount cannot be negative")
        
        old_hp = self.hp
        self.hp = max(self.hp - amount, 0)
        return old_hp - self.hp
    
    def add_experience(self, amount: int) -> int:
        """Add experience to character."""
        if amount < 0:
            raise ValueError("Experience amount cannot be negative")
        
        old_exp = self.experience
        self.experience += amount
        return self.experience - old_exp
    
    def add_gold(self, amount: int) -> int:
        """Add gold to character."""
        if amount < 0:
            raise ValueError("Gold amount cannot be negative")
        
        old_gold = self.gold
        self.gold += amount
        return self.gold - old_gold
    
    def subtract_gold(self, amount: int) -> int:
        """Subtract gold from character."""
        if amount < 0:
            raise ValueError("Gold amount cannot be negative")
        
        if amount > self.gold:
            raise ValueError("Insufficient gold")
        
        old_gold = self.gold
        self.gold -= amount
        return old_gold - self.gold
    
    def add_ability(self, ability: str) -> bool:
        """Add ability to character."""
        if not ability or not ability.strip():
            raise ValueError("Ability cannot be empty")
        
        if ability not in self.abilities:
            self.abilities.append(ability)
            return True
        return False
    
    def has_ability(self, ability: str) -> bool:
        """Check if character has specific ability."""
        return ability in self.abilities
    
    def get_summary(self) -> Dict[str, Any]:
        """Get character summary for debugging."""
        return {
            'id': self.id,
            'name': self.name,
            'class': self.class_type.value,
            'level': self.level,
            'hp': f"{self.hp}/{self.max_hp}",
            'hp_percentage': self.get_hp_percentage(),
            'gold': self.gold,
            'abilities_count': len(self.abilities),
            'inventory_size': len(self.inventory),
            'quests_completed': len(self.quests_completed),
            'is_alive': self.is_alive(),
            'total_stats': self.stats.get_total_stats()
        }


class ItemRarity(str, Enum):
    """Item rarity enumeration."""
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"
    
    def __str__(self) -> str:
        return self.value


class ItemType(str, Enum):
    """Item type enumeration."""
    WEAPON = "weapon"
    ARMOR = "armor"
    ACCESSORY = "accessory"
    CONSUMABLE = "consumable"
    QUEST = "quest"
    MATERIAL = "material"
    
    def __str__(self) -> str:
        return self.value


class Item(BaseModel):
    """Item model with explicit validation for agents."""
    
    id: str = Field(..., description="Unique item identifier")
    name: str = Field(min_length=1, max_length=100, description="Item name")
    type: ItemType = Field(..., description="Item type")
    rarity: ItemRarity = Field(default=ItemRarity.COMMON, description="Item rarity")
    value: int = Field(ge=0, description="Item value in gold")
    stats_mod: Dict[str, int] = Field(default_factory=dict, description="Stat modifiers")
    abilities: List[str] = Field(default_factory=list, description="Item abilities")
    description: str = Field(default="", max_length=500, description="Item description")
    equippable: bool = Field(default=False, description="Whether item can be equipped")
    consumable: bool = Field(default=False, description="Whether item is consumable")
    stackable: bool = Field(default=False, description="Whether item can be stacked")
    max_stack: int = Field(default=1, ge=1, description="Maximum stack size")
    
    class Config:
        """Pydantic configuration for agent optimization."""
        validate_assignment = True
        use_enum_values = True
        extra = "forbid"
    
    @validator('name')
    def validate_item_name(cls, v):
        """Validate item name."""
        if not v or not v.strip():
            raise ValueError("Item name cannot be empty")
        
        if len(v.strip()) < 1:
            raise ValueError("Item name cannot be only whitespace")
        
        return v.strip()
    
    @validator('max_stack')
    def validate_max_stack_for_non_stackable(cls, v, values):
        """Ensure max_stack is 1 for non-stackable items."""
        if 'stackable' in values and not values['stackable'] and v > 1:
            raise ValueError("Non-stackable items must have max_stack of 1")
        return v
    
    def get_total_value(self) -> int:
        """Get total item value."""
        return self.value
    
    def is_equipment(self) -> bool:
        """Check if item is equipment."""
        return self.type in [ItemType.WEAPON, ItemType.ARMOR, ItemType.ACCESSORY]
    
    def is_consumable(self) -> bool:
        """Check if item is consumable."""
        return self.consumable
    
    def can_be_equipped(self) -> bool:
        """Check if item can be equipped."""
        return self.equippable and self.is_equipment()


class EnemyType(str, Enum):
    """Enemy type enumeration."""
    BEAST = "beast"
    HUMANOID = "humanoid"
    UNDEAD = "undead"
    DEMON = "demon"
    ELEMENTAL = "elemental"
    DRAGON = "dragon"
    CONSTRUCT = "construct"
    PLANT = "plant"
    ABERRATION = "aberration"
    FIEND = "fiend"
    
    def __str__(self) -> str:
        return self.value


class Enemy(BaseModel):
    """Enemy model with explicit validation for agents."""
    
    id: str = Field(..., description="Unique enemy identifier")
    name: str = Field(min_length=1, max_length=100, description="Enemy name")
    type: EnemyType = Field(..., description="Enemy type")
    level: int = Field(ge=1, le=100, description="Enemy level")
    hp: int = Field(ge=0, description="Current hit points")
    max_hp: int = Field(ge=0, description="Maximum hit points")
    attack_power: int = Field(ge=0, description="Attack power")
    defense: int = Field(ge=0, description="Defense value")
    abilities: List[str] = Field(default_factory=list, description="Enemy abilities")
    reward_xp: int = Field(ge=0, description="Experience reward")
    reward_gold: int = Field(ge=0, description="Gold reward")
    reward_items: List[Any] = Field(default_factory=list, description="Item rewards")
    boss: bool = Field(default=False, description="Whether enemy is a boss")
    description: str = Field(default="", max_length=500, description="Enemy description")
    
    class Config:
        """Pydantic configuration for agent optimization."""
        validate_assignment = True
        use_enum_values = True
        extra = "forbid"
    
    @validator('hp')
    def validate_hp_not_exceed_max(cls, v, values):
        """Ensure HP does not exceed max HP."""
        if 'max_hp' in values and v > values['max_hp']:
            raise ValueError("Current HP cannot exceed maximum HP")
        return v
    
    @validator('max_hp')
    def validate_max_hp_positive(cls, v):
        """Ensure max HP is positive."""
        if v <= 0:
            raise ValueError("Maximum HP must be positive")
        return v
    
    def is_defeated(self) -> bool:
        """Check if enemy is defeated."""
        return self.hp <= 0
    
    def is_alive(self) -> bool:
        """Check if enemy is alive."""
        return self.hp > 0
    
    def get_difficulty_rating(self) -> str:
        """Get enemy difficulty rating."""
        if self.boss:
            return "Boss"
        
        if self.level <= 10:
            return "Easy"
        elif self.level <= 30:
            return "Medium"
        elif self.level <= 60:
            return "Hard"
        else:
            return "Legendary"
    
    def get_hp_percentage(self) -> float:
        """Get HP as percentage of maximum."""
        if self.max_hp == 0:
            return 0.0
        return (self.hp / self.max_hp) * 100.0


class QuestStatus(str, Enum):
    """Quest status enumeration."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    ABANDONED = "abandoned"
    
    def __str__(self) -> str:
        return self.value


class QuestObjective(BaseModel):
    """Quest objective model."""
    description: str = Field(..., description="Objective description")
    completed: bool = Field(default=False, description="Whether objective is completed")
    progress: int = Field(default=0, ge=0, description="Current progress")
    target: int = Field(default=1, ge=0, description="Target progress")
    
    class Config:
        """Pydantic configuration for agent optimization."""
        validate_assignment = True
        extra = "forbid"


class Quest(BaseModel):
    """Quest model with explicit validation for agents."""
    
    id: str = Field(..., description="Unique quest identifier")
    name: str = Field(min_length=1, max_length=100, description="Quest name")
    description: str = Field(min_length=1, max_length=1000, description="Quest description")
    type: str = Field(default="side_quest", description="Quest type")
    difficulty: str = Field(default="easy", description="Quest difficulty")
    giver: str = Field(min_length=1, max_length=100, description="Quest giver")
    location: str = Field(min_length=1, max_length=100, description="Quest location")
    objectives: List[QuestObjective] = Field(..., description="Quest objectives")
    rewards: Dict[str, Any] = Field(..., description="Quest rewards")
    status: QuestStatus = Field(default=QuestStatus.NOT_STARTED, description="Quest status")
    time_limit: Optional[int] = Field(default=None, ge=0, description="Time limit in minutes")
    prerequisites: List[str] = Field(default_factory=list, description="Quest prerequisites")
    
    class Config:
        """Pydantic configuration for agent optimization."""
        validate_assignment = True
        use_enum_values = True
        extra = "forbid"
    
    @validator('name')
    def validate_quest_name(cls, v):
        """Validate quest name."""
        if not v or not v.strip():
            raise ValueError("Quest name cannot be empty")
        
        return v.strip()
    
    @validator('objectives')
    def validate_objectives_not_empty(cls, v):
        """Ensure objectives list is not empty."""
        if not v:
            raise ValueError("Quest must have at least one objective")
        return v
    
    def is_completed(self) -> bool:
        """Check if quest is completed."""
        if self.status != QuestStatus.COMPLETED:
            return False
        
        return all(obj.completed for obj in self.objectives)
    
    def is_active(self) -> bool:
        """Check if quest is active."""
        return self.status == QuestStatus.IN_PROGRESS
    
    def get_progress_percentage(self) -> float:
        """Get quest progress as percentage."""
        if not self.objectives:
            return 100.0
        
        completed_objectives = sum(1 for obj in self.objectives if obj.completed)
        return (completed_objectives / len(self.objectives)) * 100.0
    
    def update_objective_progress(self, objective_index: int, progress: int) -> bool:
        """Update progress for specific objective."""
        if 0 <= objective_index < len(self.objectives):
            objective = self.objectives[objective_index]
            objective.progress = max(0, min(progress, objective.target))
            objective.completed = objective.progress >= objective.target
            return True
        return False


class LocationType(str, Enum):
    """Location type enumeration."""
    TOWN = "town"
    DUNGEON = "dungeon"
    FOREST = "forest"
    MOUNTAIN = "mountain"
    DESERT = "desert"
    CASTLE = "castle"
    TEMPLE = "temple"
    CAVE = "cave"
    RUINS = "ruins"
    CAMP = "camp"
    
    def __str__(self) -> str:
        return self.value


class Location(BaseModel):
    """Location model with explicit validation for agents."""
    
    id: str = Field(..., description="Unique location identifier")
    name: str = Field(min_length=1, max_length=100, description="Location name")
    type: LocationType = Field(..., description="Location type")
    description: str = Field(default="", max_length=500, description="Location description")
    level: int = Field(ge=1, le=100, description="Recommended level")
    enemies: List[Any] = Field(default_factory=list, description="Enemies at location")
    npcs: List[Any] = Field(default_factory=list, description="NPCs at location")
    items: List[Any] = Field(default_factory=list, description="Items at location")
    quests: List[Any] = Field(default_factory=list, description="Quests at location")
    connections: List[str] = Field(default_factory=list, description="Connected locations")
    visited: bool = Field(default=False, description="Whether location was visited")
    
    class Config:
        """Pydantic configuration for agent optimization."""
        validate_assignment = True
        use_enum_values = True
        extra = "forbid"
    
    @validator('name')
    def validate_location_name(cls, v):
        """Validate location name."""
        if not v or not v.strip():
            raise ValueError("Location name cannot be empty")
        
        return v.strip()
    
    def is_safe(self) -> bool:
        """Check if location is safe."""
        return self.type in [LocationType.TOWN, LocationType.TEMPLE, LocationType.CAMP]
    
    def is_dangerous(self) -> bool:
        """Check if location is dangerous."""
        return self.type in [LocationType.DUNGEON, LocationType.CAVE, LocationType.RUINS]
    
    def is_visited(self) -> bool:
        """Check if location was visited."""
        return self.visited
    
    def mark_visited(self) -> None:
        """Mark location as visited."""
        self.visited = True
    
    def get_difficulty_rating(self) -> str:
        """Get location difficulty rating."""
        if self.level <= 10:
            return "Easy"
        elif self.level <= 30:
            return "Medium"
        elif self.level <= 60:
            return "Hard"
        else:
            return "Legendary"


class GameState(BaseModel):
    """Game state model with explicit validation for agents."""
    
    current_location: str = Field(default="start", description="Current location")
    player: Optional[Character] = Field(default=None, description="Player character")
    world_time: int = Field(default=0, ge=0, description="World time in minutes")
    day: int = Field(default=1, ge=1, description="Current day")
    difficulty: str = Field(default="normal", description="Game difficulty")
    flags: Dict[str, Any] = Field(default_factory=dict, description="Game flags")
    locations: Dict[str, Any] = Field(default_factory=dict, description="Discovered locations")
    npcs: Dict[str, Any] = Field(default_factory=dict, description="NPCs met")
    items: Dict[str, Any] = Field(default_factory=dict, description="Items found")
    enemies: Dict[str, Any] = Field(default_factory=dict, description="Enemies defeated")
    quests_active: List[Any] = Field(default_factory=list, description="Active quests")
    quests_completed: List[Any] = Field(default_factory=list, description="Completed quests")
    save_timestamp: Optional[str] = Field(default=None, description="Save timestamp")
    save_version: str = Field(default="1.0.0", description="Save version")
    
    class Config:
        """Pydantic configuration for agent optimization."""
        validate_assignment = True
        use_enum_values = True
        extra = "forbid"
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
    
    def is_new_game(self) -> bool:
        """Check if this is a new game."""
        return self.player is None and self.world_time == 0 and self.day == 1
    
    def has_player(self) -> bool:
        """Check if game has a player character."""
        return self.player is not None
    
    def get_game_progress(self) -> Dict[str, Any]:
        """Get game progress summary."""
        progress = {
            'location': self.current_location,
            'world_time': self.world_time,
            'day': self.day,
            'difficulty': self.difficulty
        }
        
        if self.player:
            progress['player'] = self.player.get_summary()
            progress['player_level'] = self.player.level
            progress['player_experience'] = self.player.experience
            progress['player_gold'] = self.player.gold
            progress['quests_active'] = len(self.quests_active)
            progress['quests_completed'] = len(self.quests_completed)
        
        return progress
    
    def add_flag(self, key: str, value: Any) -> None:
        """Add game flag."""
        self.flags[key] = value
    
    def get_flag(self, key: str, default: Any = None) -> Any:
        """Get game flag."""
        return self.flags.get(key, default)
    
    def has_flag(self, key: str) -> bool:
        """Check if game flag exists."""
        return key in self.flags
    
    def advance_world_time(self, minutes: int) -> None:
        """Advance world time by specified minutes."""
        if minutes < 0:
            raise ValueError("Time advancement cannot be negative")
        
        self.world_time += minutes
        
        # Update day (1440 minutes = 1 day)
        new_day = (self.world_time // 1440) + 1
        if new_day > self.day:
            self.day = new_day
    
    def get_time_of_day(self) -> str:
        """Get current time of day."""
        minute_of_day = self.world_time % 1440
        
        if 360 <= minute_of_day < 720:
            return "morning"
        elif 720 <= minute_of_day < 1080:
            return "afternoon"
        elif 1080 <= minute_of_day < 1260:
            return "evening"
        else:
            return "night"


# Export all models for easy access
__all__ = [
    'CharacterClass',
    'CharacterStats',
    'Character',
    'ItemRarity',
    'ItemType',
    'Item',
    'EnemyType',
    'Enemy',
    'QuestStatus',
    'QuestObjective',
    'Quest',
    'LocationType',
    'Location',
    'GameState'
]