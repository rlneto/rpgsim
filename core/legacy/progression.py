"""
Progression System for RPGSim
Comprehensive character progression with experience, levels, skills, and abilities.
Features dynamic experience curves, class-specific progression paths, and strategic ability choices.
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field

from core.models import Character


class SkillType:
    """Skill type classifications"""

    COMBAT = "combat"
    MAGIC = "magic"
    STEALTH = "stealth"
    SOCIAL = "social"
    CRAFTING = "crafting"
    SURVIVAL = "survival"
    KNOWLEDGE = "knowledge"


class AbilityRarity:
    """Ability rarity levels"""

    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"


@dataclass
class Ability:
    """Character ability with progression mechanics"""

    id: str
    name: str
    description: str
    skill_type: str
    rarity: str
    required_level: int
    max_level: int = 5
    current_level: int = 0
    prerequisites: List[str] = field(default_factory=list)
    effects: Dict[str, Any] = field(default_factory=dict)
    synergy_abilities: List[str] = field(default_factory=list)
    unlock_cost: Dict[str, int] = field(default_factory=dict)

    def can_upgrade(self, character: Character) -> bool:
        """Check if ability can be upgraded."""
        if self.current_level >= self.max_level:
            return False
        if character.level < self.required_level:
            return False

        # Check prerequisites
        for prereq in self.prerequisites:
            if prereq not in character.abilities:
                return False

        return True

    def get_upgrade_cost(self) -> Dict[str, int]:
        """Calculate cost to upgrade ability."""
        base_cost = 100 * (self.current_level + 1)
        rarity_multiplier = {
            AbilityRarity.COMMON: 1.0,
            AbilityRarity.UNCOMMON: 1.5,
            AbilityRarity.RARE: 2.0,
            AbilityRarity.EPIC: 3.0,
            AbilityRarity.LEGENDARY: 5.0,
        }.get(self.rarity, 1.0)

        cost_multiplier = rarity_multiplier * (1.2**self.current_level)

        return {
            "skill_points": int(base_cost * cost_multiplier),
            "gold": int(base_cost * cost_multiplier * 10),
        }


@dataclass
class SkillProgress:
    """Individual skill progression tracking"""

    skill_name: str
    current_level: int = 0
    max_level: int = 100
    experience: int = 0
    experience_to_next: int = 100
    total_experience: int = 0
    bonuses: Dict[str, float] = field(default_factory=dict)

    def add_experience(self, amount: int) -> bool:
        """Add experience and check for level up."""
        self.experience += amount
        self.total_experience += amount

        while (
            self.experience >= self.experience_to_next
            and self.current_level < self.max_level
        ):
            self.experience -= self.experience_to_next
            self.current_level += 1
            self.experience_to_next = self.calculate_experience_to_next()
            return True

        return False

    def calculate_experience_to_next(self) -> int:
        """Calculate experience needed for next skill level."""
        return int(100 * (1.15**self.current_level))

    def get_effectiveness(self) -> float:
        """Get skill effectiveness based on level."""
        return 1.0 + (self.current_level * 0.05)


class LevelCalculator:
    """Handles level progression calculations and rewards."""

    # Experience required for each level (1-100)
    EXPERIENCE_TABLE = []

    @staticmethod
    def generate_experience_table() -> List[int]:
        """Generate experience table for levels 1-100."""
        if LevelCalculator.EXPERIENCE_TABLE:
            return LevelCalculator.EXPERIENCE_TABLE

        table = [0]  # Level 0 (unused, for 1-based indexing)

        for level in range(1, 101):
            if level == 1:
                exp_needed = 0
            else:
                # Exponential curve with slight adjustments for gameplay
                base_exp = 1000
                growth_rate = 1.12
                exp_needed = int(base_exp * (growth_rate ** (level - 1)))

                # Adjust for specific milestone levels
                if level in [10, 20, 30, 40, 50]:
                    exp_needed = int(exp_needed * 0.9)  # Slightly easier at milestones
                elif level in [25, 35, 45, 55]:
                    exp_needed = int(
                        exp_needed * 1.1
                    )  # Slightly harder before milestones

            table.append(exp_needed)

        LevelCalculator.EXPERIENCE_TABLE = table
        return table

    @staticmethod
    def get_experience_for_level(level: int) -> int:
        """Get total experience needed to reach a specific level."""
        table = LevelCalculator.generate_experience_table()
        if 0 <= level < len(table):
            return table[level]
        return table[-1]

    @staticmethod
    def get_level_from_experience(total_experience: int) -> int:
        """Calculate level from total experience."""
        table = LevelCalculator.generate_experience_table()

        for level in range(len(table) - 1, 0, -1):
            if total_experience >= table[level]:
                return level

        return 1

    @staticmethod
    def get_experience_progress(character: Character) -> Tuple[int, int]:
        """Get current level progress (current_exp, exp_needed_for_next)."""
        current_level_exp = LevelCalculator.get_experience_for_level(character.level)
        next_level_exp = LevelCalculator.get_experience_for_level(character.level + 1)

        current_exp = character.experience - current_level_exp
        exp_needed = next_level_exp - current_level_exp

        return current_exp, exp_needed

    @staticmethod
    def can_level_up(character: Character) -> bool:
        """Check if character can level up."""
        if character.level >= 100:
            return False

        exp_needed = LevelCalculator.get_experience_for_level(character.level + 1)
        return character.experience >= exp_needed

    @staticmethod
    def calculate_level_up_rewards(level: int, class_type: str) -> Dict[str, Any]:
        """Calculate rewards for leveling up."""
        rewards = {
            "skill_points": 3,
            "ability_points": 1,
            "stat_increases": {
                "strength": 1,
                "intelligence": 1,
                "dexterity": 1,
                "constitution": 1,
                "wisdom": 1,
                "charisma": 1,
            },
            "hp_increase": 10,
            "new_abilities": [],
            "milestone_reward": None,
        }

        # Class-specific bonuses
        class_bonuses = {
            "Warrior": {"strength": 2, "constitution": 2},
            "Mage": {"intelligence": 2, "wisdom": 1},
            "Rogue": {"dexterity": 2, "charisma": 1},
            "Cleric": {"wisdom": 2, "charisma": 1},
            "Ranger": {"dexterity": 1, "wisdom": 1},
            "Paladin": {"strength": 1, "charisma": 1},
            "Warlock": {"charisma": 2, "intelligence": 1},
            "Druid": {"wisdom": 2, "constitution": 1},
            "Monk": {"dexterity": 1, "wisdom": 1},
            "Barbarian": {"strength": 3, "constitution": 1},
            "Bard": {"charisma": 2, "intelligence": 1},
            "Sorcerer": {"charisma": 2, "constitution": 1},
            "Fighter": {"strength": 1, "constitution": 2},
            "Necromancer": {"intelligence": 2, "wisdom": 1},
            "Illusionist": {"intelligence": 2, "charisma": 1},
            "Alchemist": {"intelligence": 2, "dexterity": 1},
            "Berserker": {"strength": 3, "constitution": 1},
            "Assassin": {"dexterity": 2, "strength": 1},
            "Healer": {"wisdom": 2, "constitution": 1},
            "Summoner": {"intelligence": 2, "charisma": 1},
            "Shapeshifter": {"wisdom": 2, "dexterity": 1},
            "Elementalist": {"intelligence": 3, "constitution": 1},
            "Ninja": {"dexterity": 2, "strength": 1},
        }

        if class_type in class_bonuses:
            for stat, bonus in class_bonuses[class_type].items():
                rewards["stat_increases"][stat] += bonus - 1  # Subtract base 1

        # Milestone rewards at specific levels
        milestone_levels = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        if level in milestone_levels:
            rewards["milestone_reward"] = {
                "level": level,
                "bonus_skill_points": 5,
                "special_ability": True,
                "title": f"Master Level {level}",
            }
            rewards["skill_points"] += 5

        # Ability unlocks at specific levels
        ability_levels = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
        if level in ability_levels:
            rewards["ability_points"] += 1

        return rewards


class SkillTree:
    """Manages skill trees and ability relationships."""

    def __init__(self):
        self.abilities: Dict[str, Ability] = {}
        self.skill_trees: Dict[str, List[str]] = {}
        self._initialize_default_abilities()

    def _initialize_default_abilities(self):
        """Initialize default abilities for all skill types."""

        # Combat Abilities
        combat_abilities = [
            Ability(
                "power_strike",
                "Power Strike",
                "A powerful melee attack",
                SkillType.COMBAT,
                AbilityRarity.COMMON,
                1,
            ),
            Ability(
                "dual_wield",
                "Dual Wield",
                "Fight with two weapons",
                SkillType.COMBAT,
                AbilityRarity.UNCOMMON,
                5,
                prerequisites=["power_strike"],
            ),
            Ability(
                "whirlwind",
                "Whirlwind Attack",
                "Attack all nearby enemies",
                SkillType.COMBAT,
                AbilityRarity.RARE,
                15,
                prerequisites=["dual_wield"],
            ),
            Ability(
                "berserker_rage",
                "Berserker Rage",
                "Enter rage for increased damage",
                SkillType.COMBAT,
                AbilityRarity.EPIC,
                25,
                prerequisites=["whirlwind"],
            ),
        ]

        # Magic Abilities
        magic_abilities = [
            Ability(
                "fireball",
                "Fireball",
                "Launch a fireball",
                SkillType.MAGIC,
                AbilityRarity.COMMON,
                1,
            ),
            Ability(
                "frost_armor",
                "Frost Armor",
                "Protective ice barrier",
                SkillType.MAGIC,
                AbilityRarity.UNCOMMON,
                5,
                prerequisites=["fireball"],
            ),
            Ability(
                "lightning_bolt",
                "Lightning Bolt",
                "Chain lightning attack",
                SkillType.MAGIC,
                AbilityRarity.RARE,
                15,
                prerequisites=["frost_armor"],
            ),
            Ability(
                "meteor",
                "Meteor Strike",
                "Devastating area damage",
                SkillType.MAGIC,
                AbilityRarity.EPIC,
                25,
                prerequisites=["lightning_bolt"],
            ),
        ]

        # Stealth Abilities
        stealth_abilities = [
            Ability(
                "sneak_attack",
                "Sneak Attack",
                "Attack from shadows",
                SkillType.STEALTH,
                AbilityRarity.COMMON,
                1,
            ),
            Ability(
                "invisibility",
                "Invisibility",
                "Become unseen",
                SkillType.STEALTH,
                AbilityRarity.UNCOMMON,
                5,
                prerequisites=["sneak_attack"],
            ),
            Ability(
                "shadow_step",
                "Shadow Step",
                "Teleport through shadows",
                SkillType.STEALTH,
                AbilityRarity.RARE,
                15,
                prerequisites=["invisibility"],
            ),
            Ability(
                "assassin_strike",
                "Assassin Strike",
                "Lethal precision attack",
                SkillType.STEALTH,
                AbilityRarity.EPIC,
                25,
                prerequisites=["shadow_step"],
            ),
        ]

        # Social Abilities
        social_abilities = [
            Ability(
                "persuade",
                "Persuade",
                "Convince others",
                SkillType.SOCIAL,
                AbilityRarity.COMMON,
                1,
            ),
            Ability(
                "intimidate",
                "Intimidate",
                "Force compliance",
                SkillType.SOCIAL,
                AbilityRarity.UNCOMMON,
                5,
                prerequisites=["persuade"],
            ),
            Ability(
                "leadership",
                "Leadership",
                "Inspire allies",
                SkillType.SOCIAL,
                AbilityRarity.RARE,
                15,
                prerequisites=["intimidate"],
            ),
            Ability(
                "charisma",
                "Natural Charisma",
                "Innate influence",
                SkillType.SOCIAL,
                AbilityRarity.EPIC,
                25,
                prerequisites=["leadership"],
            ),
        ]

        # All abilities
        all_abilities = (
            combat_abilities + magic_abilities + stealth_abilities + social_abilities
        )

        for ability in all_abilities:
            self.abilities[ability.id] = ability

        # Organize into skill trees
        self.skill_trees = {
            SkillType.COMBAT: [a.id for a in combat_abilities],
            SkillType.MAGIC: [a.id for a in magic_abilities],
            SkillType.STEALTH: [a.id for a in stealth_abilities],
            SkillType.SOCIAL: [a.id for a in social_abilities],
        }

    def get_available_abilities(
        self, character: Character, skill_type: Optional[str] = None
    ) -> List[Ability]:
        """Get abilities available to character."""
        available = []

        for ability in self.abilities.values():
            if skill_type and ability.skill_type != skill_type:
                continue

            if ability.can_upgrade(character):
                available.append(ability)

        return available

    def get_ability_by_id(self, ability_id: str) -> Optional[Ability]:
        """Get ability by ID."""
        return self.abilities.get(ability_id)

    def get_ability_tree(self, skill_type: str) -> List[Ability]:
        """Get abilities in a specific skill tree."""
        if skill_type not in self.skill_trees:
            return []

        return [
            self.abilities[ability_id] for ability_id in self.skill_trees[skill_type]
        ]

    def check_synergy(self, character: Character, ability_id: str) -> float:
        """Calculate synergy bonus for ability based on character's other abilities."""
        ability = self.get_ability_by_id(ability_id)
        if not ability:
            return 1.0

        synergy_count = 0
        for synergy_ability in ability.synergy_abilities:
            if synergy_ability in character.abilities:
                synergy_count += 1

        # Each synergistic ability provides 10% bonus
        return 1.0 + (synergy_count * 0.1)


class ProgressionManager:
    """Manages all character progression aspects."""

    def __init__(self):
        self.level_calculator = LevelCalculator()
        self.skill_tree = SkillTree()
        self.character_skills: Dict[str, Dict[str, SkillProgress]] = {}

    def add_experience(
        self, character: Character, amount: int, source: str = "general"
    ) -> Dict[str, Any]:
        """Add experience to character and handle level ups."""
        old_level = character.level
        character.experience += amount

        results = {
            "experience_gained": amount,
            "source": source,
            "old_level": old_level,
            "new_level": old_level,
            "level_ups": [],
            "total_levels_gained": 0,
        }

        # Check for multiple level ups
        while self.level_calculator.can_level_up(character):
            level_up_result = self._level_up_character(character)
            results["level_ups"].append(level_up_result)
            character.level += 1
            results["total_levels_gained"] += 1

        results["new_level"] = character.level
        return results

    def _level_up_character(self, character: Character) -> Dict[str, Any]:
        """Handle single level up."""
        rewards = self.level_calculator.calculate_level_up_rewards(
            character.level, character.class_type
        )

        # Apply stat increases
        for stat, increase in rewards["stat_increases"].items():
            if hasattr(character.stats, stat):
                current_value = getattr(character.stats, stat)
                setattr(character.stats, stat, min(20, current_value + increase))

        # Increase HP
        character.max_hp += rewards["hp_increase"]
        character.hp = character.max_hp  # Full heal on level up

        # Add abilities (milestone rewards)
        if rewards["milestone_reward"]:
            character.abilities.append(f"milestone_{character.level}")

        return rewards

    def upgrade_skill(
        self, character: Character, skill_name: str, experience_amount: int
    ) -> Dict[str, Any]:
        """Upgrade a specific skill."""
        character_id = character.id

        if character_id not in self.character_skills:
            self.character_skills[character_id] = {}

        if skill_name not in self.character_skills[character_id]:
            self.character_skills[character_id][skill_name] = SkillProgress(
                skill_name=skill_name
            )

        skill_progress = self.character_skills[character_id][skill_name]
        old_level = skill_progress.current_level

        leveled_up = skill_progress.add_experience(experience_amount)

        # Update character skills dictionary
        character.skills[skill_name] = skill_progress.current_level

        return {
            "skill_name": skill_name,
            "old_level": old_level,
            "new_level": skill_progress.current_level,
            "experience_gained": experience_amount,
            "leveled_up": leveled_up,
            "effectiveness": skill_progress.get_effectiveness(),
        }

    def learn_ability(self, character: Character, ability_id: str) -> Dict[str, Any]:
        """Learn a new ability."""
        ability = self.skill_tree.get_ability_by_id(ability_id)
        if not ability:
            return {"success": False, "error": "Ability not found"}

        if not ability.can_upgrade(character):
            return {"success": False, "error": "Cannot learn this ability"}

        if ability_id in character.abilities:
            return {"success": False, "error": "Ability already known"}

        character.abilities.append(ability_id)
        ability.current_level = 1

        return {
            "success": True,
            "ability": ability,
            "message": f"Learned {ability.name}",
        }

    def upgrade_ability(self, character: Character, ability_id: str) -> Dict[str, Any]:
        """Upgrade an existing ability."""
        ability = self.skill_tree.get_ability_by_id(ability_id)
        if not ability:
            return {"success": False, "error": "Ability not found"}

        if ability_id not in character.abilities:
            return {"success": False, "error": "Ability not learned"}

        if ability.current_level >= ability.max_level:
            return {"success": False, "error": "Ability at max level"}

        cost = ability.get_upgrade_cost()

        # Check if character can afford upgrade
        # (This would integrate with inventory/currency system)

        ability.current_level += 1

        return {
            "success": True,
            "ability": ability,
            "old_level": ability.current_level - 1,
            "new_level": ability.current_level,
            "cost": cost,
            "message": f"Upgraded {ability.name} to level {ability.current_level}",
        }

    def get_character_progression_summary(self, character: Character) -> Dict[str, Any]:
        """Get comprehensive progression summary for character."""
        current_exp, exp_needed = self.level_calculator.get_experience_progress(
            character
        )

        # Get skill progress
        character_skills = self.character_skills.get(character.id, {})
        skill_summary = {}
        for skill_name, skill_progress in character_skills.items():
            skill_summary[skill_name] = {
                "level": skill_progress.current_level,
                "max_level": skill_progress.max_level,
                "experience": skill_progress.experience,
                "experience_to_next": skill_progress.experience_to_next,
                "effectiveness": skill_progress.get_effectiveness(),
            }

        # Get ability summary
        learned_abilities = []
        available_abilities = self.skill_tree.get_available_abilities(character)

        for ability_id in character.abilities:
            ability = self.skill_tree.get_ability_by_id(ability_id)
            if ability:
                learned_abilities.append(
                    {
                        "id": ability.id,
                        "name": ability.name,
                        "level": ability.current_level,
                        "max_level": ability.max_level,
                        "rarity": ability.rarity,
                        "synergy_bonus": self.skill_tree.check_synergy(
                            character, ability_id
                        ),
                    }
                )

        return {
            "character_id": character.id,
            "name": character.name,
            "class": character.class_type,
            "level": character.level,
            "experience": {
                "current": character.experience,
                "current_level_progress": current_exp,
                "exp_needed_for_next": exp_needed,
                "progress_percentage": (
                    (current_exp / exp_needed * 100) if exp_needed > 0 else 100
                ),
            },
            "stats": {
                "hp": {"current": character.hp, "max": character.max_hp},
                "gold": character.gold,
                "abilities_count": len(character.abilities),
            },
            "skills": skill_summary,
            "abilities": {
                "learned": learned_abilities,
                "available": len(available_abilities),
            },
            "progression_milestones": self._get_progression_milestones(character),
        }

    def _get_progression_milestones(self, character: Character) -> List[Dict[str, Any]]:
        """Get progression milestones and achievements."""
        milestones = []

        # Level milestones
        level_milestones = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        for milestone_level in level_milestones:
            if character.level >= milestone_level:
                milestones.append(
                    {
                        "type": "level",
                        "description": f"Reached level {milestone_level}",
                        "achieved_at": milestone_level,
                        "reward": f"Master Level {milestone_level} title",
                    }
                )

        # Ability milestones
        if len(character.abilities) >= 10:
            milestones.append(
                {
                    "type": "abilities",
                    "description": "Learned 10+ abilities",
                    "achieved_at": "Unknown",
                    "reward": "Ability Master",
                }
            )

        # Skill milestones
        total_skill_levels = sum(character.skills.values())
        if total_skill_levels >= 50:
            milestones.append(
                {
                    "type": "skills",
                    "description": "Mastered multiple skills",
                    "achieved_at": "Unknown",
                    "reward": "Skill Expert",
                }
            )

        return milestones


class ProgressionSystem:
    """Main progression system interface."""

    def __init__(self):
        self.progression_manager = ProgressionManager()
        self.character_progress: Dict[str, Dict[str, Any]] = {}

    def add_experience(
        self, character: Character, amount: int, source: str = "general"
    ) -> Dict[str, Any]:
        """Add experience and handle progression."""
        result = self.progression_manager.add_experience(character, amount, source)

        # Track character progression
        if character.id not in self.character_progress:
            self.character_progress[character.id] = {
                "total_experience_gained": 0,
                "levels_gained": 0,
                "abilities_learned": 0,
                "skills_upgraded": 0,
                "progression_history": [],
            }

        character_progress = self.character_progress[character.id]
        character_progress["total_experience_gained"] += amount
        character_progress["levels_gained"] += result["total_levels_gained"]

        # Record progression event
        progression_event = {
            "timestamp": "current_time",  # Would use actual timestamp
            "type": (
                "experience_gain" if result["total_levels_gained"] == 0 else "level_up"
            ),
            "amount": amount,
            "source": source,
            "old_level": result["old_level"],
            "new_level": result["new_level"],
        }

        character_progress["progression_history"].append(progression_event)

        return result

    def learn_ability(self, character: Character, ability_id: str) -> Dict[str, Any]:
        """Learn a new ability."""
        result = self.progression_manager.learn_ability(character, ability_id)

        if result["success"]:
            self.character_progress[character.id]["abilities_learned"] += 1

            progression_event = {
                "timestamp": "current_time",
                "type": "ability_learned",
                "ability_id": ability_id,
                "ability_name": result["ability"].name,
            }

            self.character_progress[character.id]["progression_history"].append(
                progression_event
            )

        return result

    def upgrade_ability(self, character: Character, ability_id: str) -> Dict[str, Any]:
        """Upgrade an existing ability."""
        result = self.progression_manager.upgrade_ability(character, ability_id)

        if result["success"]:
            progression_event = {
                "timestamp": "current_time",
                "type": "ability_upgraded",
                "ability_id": ability_id,
                "old_level": result["old_level"],
                "new_level": result["new_level"],
            }

            self.character_progress[character.id]["progression_history"].append(
                progression_event
            )

        return result

    def get_character_summary(self, character: Character) -> Dict[str, Any]:
        """Get complete character progression summary."""
        summary = self.progression_manager.get_character_progression_summary(character)

        # Add progression statistics
        if character.id in self.character_progress:
            stats = self.character_progress[character.id]
            summary["progression_stats"] = {
                "total_experience_gained": stats["total_experience_gained"],
                "total_levels_gained": stats["levels_gained"],
                "abilities_learned": stats["abilities_learned"],
                "skills_upgraded": stats["skills_upgraded"],
                "progression_events": len(stats["progression_history"]),
            }
        else:
            summary["progression_stats"] = {
                "total_experience_gained": 0,
                "total_levels_gained": 0,
                "abilities_learned": 0,
                "skills_upgraded": 0,
                "progression_events": 0,
            }

        return summary

    def get_available_abilities(
        self, character: Character, skill_type: Optional[str] = None
    ) -> List[Ability]:
        """Get abilities available for character to learn."""
        return self.progression_manager.skill_tree.get_available_abilities(
            character, skill_type
        )

    def get_skill_trees(self) -> Dict[str, List[Ability]]:
        """Get all skill trees."""
        return {
            skill_type: self.progression_manager.skill_tree.get_ability_tree(skill_type)
            for skill_type in self.progression_manager.skill_tree.skill_trees
        }
