"""
Progression system domain entities and value objects
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
import math


class SkillType(str, Enum):
    """Skill types"""
    COMBAT = "combat"
    MAGIC = "magic"
    STEALTH = "stealth"
    SOCIAL = "social"
    CRAFTING = "crafting"
    SURVIVAL = "survival"
    KNOWLEDGE = "knowledge"

    def __str__(self):
        return self.value


class AbilityRarity(str, Enum):
    """Ability rarity levels"""
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"

    def __str__(self):
        return self.value


@dataclass
class Ability:
    """Represents an ability in the skill tree"""
    id: str
    name: str
    description: str
    skill_type: SkillType
    rarity: AbilityRarity = AbilityRarity.COMMON
    required_level: int = 1
    max_level: int = 5
    current_level: int = 0
    prerequisites: List[str] = field(default_factory=list)
    synergy_abilities: List[str] = field(default_factory=list)
    effects: Dict[str, Any] = field(default_factory=dict)

    def can_upgrade(self, character: Any) -> bool:
        """Check if character can upgrade this ability"""
        # Check max level
        if self.current_level >= self.max_level:
            return False

        # Check level requirement
        if character.level < self.required_level:
            return False

        # Check prerequisites
        if self.prerequisites:
            for prereq in self.prerequisites:
                if prereq not in character.abilities:
                    return False

        return True

    def get_upgrade_cost(self) -> Dict[str, int]:
        """Calculate upgrade cost"""
        # Base cost logic from test expectation: 100 * (current + 1) * rarity_mult
        rarity_mult = {
            AbilityRarity.COMMON: 1.0,
            AbilityRarity.UNCOMMON: 1.5,
            AbilityRarity.RARE: 2.0,
            AbilityRarity.EPIC: 3.0,
            AbilityRarity.LEGENDARY: 5.0
        }.get(self.rarity, 1.0)

        skill_points = int(100 * (self.current_level + 1) * rarity_mult)
        gold = skill_points * 10

        return {
            "skill_points": skill_points,
            "gold": gold
        }


@dataclass
class SkillProgress:
    """Tracks progress for a specific skill"""
    skill_name: str
    current_level: int = 0
    max_level: int = 100
    experience: int = 0
    total_experience: int = 0

    def add_experience(self, amount: int) -> bool:
        """Add experience and check for level up"""
        if self.current_level >= self.max_level:
            return False

        self.experience += amount
        self.total_experience += amount

        exp_needed = self.calculate_experience_to_next()

        leveled_up = False
        while self.experience >= exp_needed and self.current_level < self.max_level:
            self.experience -= exp_needed
            self.current_level += 1
            leveled_up = True
            exp_needed = self.calculate_experience_to_next()

        return leveled_up

    def calculate_experience_to_next(self) -> int:
        """Calculate experience needed for next level"""
        # Test expectation: 100 * 1.15^level
        return int(100 * (1.15 ** self.current_level))

    def get_effectiveness(self) -> float:
        """Calculate skill effectiveness multiplier"""
        # Test expectation: 1.0 + level * 0.05
        return 1.0 + (self.current_level * 0.05)
