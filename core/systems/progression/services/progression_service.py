"""
Progression services
"""
from typing import Dict, List, Optional, Any, Tuple
from core.models import Character, CharacterClass
from ..domain.progression import (
    SkillType, AbilityRarity, Ability, SkillProgress
)
from ..interfaces.repositories import ProgressionRepository


class LevelCalculator:
    """Service for level calculations"""

    @staticmethod
    def generate_experience_table() -> List[int]:
        """Generate XP requirement table"""
        table = [0] * 101
        base_xp = 100
        for i in range(2, 101):
            xp_needed = int(base_xp * (i - 1) * 1.5)
            table[i] = table[i-1] + xp_needed
        return table

    @staticmethod
    def get_experience_for_level(level: int) -> int:
        """Get total XP required for level"""
        if level <= 1:
            return 0
        if level > 100: return 999999999
        return 100 * (level - 1) * level

    @staticmethod
    def get_level_from_experience(experience: int) -> int:
        """Get level from total XP"""
        level = 1
        while LevelCalculator.get_experience_for_level(level + 1) <= experience:
            level += 1
            if level >= 100: break
        return level

    @staticmethod
    def get_experience_progress(character: Any) -> Tuple[int, int]:
        """Get current level progress (current, needed)"""
        current_level_xp = LevelCalculator.get_experience_for_level(character.level)
        next_level_xp = LevelCalculator.get_experience_for_level(character.level + 1)

        current_progress = character.experience - current_level_xp
        needed = next_level_xp - current_level_xp

        return current_progress, needed

    @staticmethod
    def can_level_up(character: Any) -> bool:
        """Check if character can level up"""
        if character.level >= 100:
            return False
        next_level_xp = LevelCalculator.get_experience_for_level(character.level + 1)
        return character.experience >= next_level_xp

    @staticmethod
    def calculate_level_up_rewards(level: int, class_type: str) -> Dict[str, Any]:
        """Calculate rewards for reaching a level"""
        rewards = {
            "skill_points": 3,
            "ability_points": 0,
            "stat_increases": {},
            "hp_increase": 10,
            "milestone_reward": None
        }

        if level % 5 == 0:
            rewards["ability_points"] = 1

        class_type = str(class_type).lower()
        if "warrior" in class_type:
            rewards["stat_increases"] = {"strength": 2, "constitution": 1}
        elif "mage" in class_type:
            rewards["stat_increases"] = {"intelligence": 2, "wisdom": 1}
        else:
            rewards["stat_increases"] = {"dexterity": 1, "charisma": 1}

        if level % 20 == 0:
            rewards["milestone_reward"] = {
                "level": level,
                "bonus_skill_points": 5
            }

        return rewards


class SkillTree:
    """Service for managing skills and abilities"""

    def __init__(self):
        self.abilities: Dict[str, Ability] = {}
        self.skill_trees: Dict[SkillType, List[str]] = {st: [] for st in SkillType}
        self._initialize_abilities()

    def _initialize_abilities(self):
        """Initialize default abilities"""
        self._add_ability(Ability("power_strike", "Power Strike", "Strong hit", SkillType.COMBAT, required_level=1))
        self._add_ability(Ability("dual_wield", "Dual Wield", "Use two weapons", SkillType.COMBAT, required_level=5, rarity=AbilityRarity.UNCOMMON))
        self._add_ability(Ability("fireball", "Fireball", "Fire damage", SkillType.MAGIC, required_level=1))
        self._add_ability(Ability("stealth_mastery", "Stealth Mastery", "Silent moves", SkillType.STEALTH))
        self._add_ability(Ability("persuasion", "Persuasion", "Convincing talk", SkillType.SOCIAL))

    def _add_ability(self, ability: Ability):
        self.abilities[ability.id] = ability
        self.skill_trees[ability.skill_type].append(ability.id)

    def get_ability_by_id(self, ability_id: str) -> Optional[Ability]:
        """Get ability by ID"""
        return self.abilities.get(ability_id)

    def get_available_abilities(self, character: Any) -> List[Ability]:
        """Get abilities available for character to learn"""
        available = []
        for ability in self.abilities.values():
            if ability.id in character.abilities:
                continue
            if ability.required_level <= character.level:
                prereqs_met = True
                for p in ability.prerequisites:
                    if p not in character.abilities:
                        prereqs_met = False
                        break
                if prereqs_met:
                    available.append(ability)
        return available

    def get_ability_tree(self, skill_type: SkillType) -> List[Ability]:
        """Get all abilities for a skill type"""
        return [self.abilities[aid] for aid in self.skill_trees.get(skill_type, [])]

    def check_synergy(self, character: Any, ability_id: str) -> float:
        """Check synergy multiplier"""
        ability = self.get_ability_by_id(ability_id)
        if not ability:
            return 1.0

        synergy = 1.0
        for syn_id in ability.synergy_abilities:
            if syn_id in character.abilities:
                synergy += 0.1

        return synergy


class ProgressionManager:
    """Service for managing character progression"""

    def __init__(self, repository: ProgressionRepository):
        self.level_calculator = LevelCalculator()
        self.skill_tree = SkillTree()
        self.repository = repository

    def add_experience(self, character: Any, amount: int, source: str) -> Dict[str, Any]:
        """Add experience to character"""
        old_level = character.level
        character.experience += amount

        level_ups = []
        while self.level_calculator.can_level_up(character):
            character.level += 1
            rewards = self.level_calculator.calculate_level_up_rewards(character.level, character.class_type)
            self._level_up_character(character, rewards)
            level_ups.append(rewards)

        return {
            "experience_gained": amount,
            "source": source,
            "total_levels_gained": character.level - old_level,
            "level_ups": level_ups,
            "old_level": old_level,
            "new_level": character.level
        }

    def _level_up_character(self, character: Any, rewards: Dict[str, Any]):
        """Apply level up rewards"""
        character.max_hp += rewards.get("hp_increase", 0)
        character.hp = character.max_hp

    def upgrade_skill(self, character: Any, skill_name: str, exp_amount: int) -> Dict[str, Any]:
        """Upgrade a specific skill"""
        char_id = str(character.id)

        progress = self.repository.get_skill_progress(char_id, skill_name)
        if not progress:
            progress = SkillProgress(skill_name)
            self.repository.save_skill_progress(char_id, progress)

        old_level = progress.current_level
        progress.add_experience(exp_amount)
        self.repository.save_skill_progress(char_id, progress)

        if isinstance(character.skills, dict):
            character.skills[skill_name] = progress.current_level

        return {
            "skill_name": skill_name,
            "experience_gained": exp_amount,
            "old_level": old_level,
            "new_level": progress.current_level,
            "effectiveness": progress.get_effectiveness()
        }

    def learn_ability(self, character: Any, ability_id: str) -> Dict[str, Any]:
        """Learn a new ability"""
        ability = self.skill_tree.get_ability_by_id(ability_id)
        if not ability:
            return {"success": False, "error": "Ability not found"}

        if ability.id in character.abilities:
            return {"success": False, "error": "Ability already learned"}

        character.abilities.append(ability.id)

        return {
            "success": True,
            "ability": ability
        }

    def upgrade_ability(self, character: Any, ability_id: str) -> Dict[str, Any]:
        """Upgrade an existing ability"""
        ability = self.skill_tree.get_ability_by_id(ability_id)
        if not ability:
            return {"success": False, "error": "Ability not found"}

        ability.current_level += 1

        return {
            "success": True,
            "new_level": ability.current_level
        }

    def get_character_progression_summary(self, character: Any) -> Dict[str, Any]:
        """Get summary"""
        char_id = str(character.id)
        current_exp, needed = self.level_calculator.get_experience_progress(character)

        skills_data = {}
        all_skills = self.repository.get_all_skills(char_id)
        for skill in all_skills:
            skills_data[skill.skill_name] = skill.current_level

        return {
            "character_id": char_id,
            "name": character.name,
            "level": character.level,
            "experience": {
                "current": current_exp,
                "needed": needed,
                "total": character.experience,
                "progress_percentage": (current_exp / needed * 100) if needed > 0 else 100
            },
            "skills": skills_data,
            "abilities": character.abilities
        }
