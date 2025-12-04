"""
Progression System Facade
"""
from typing import Dict, List, Any, Optional
from core.models import Character
from .domain.progression import SkillType
from .services.progression_service import (
    ProgressionManager, SkillTree, LevelCalculator
)


class ProgressionSystem:
    """Facade for Progression System"""

    def __init__(self):
        self.progression_manager = ProgressionManager()
        self.character_progress: Dict[str, Any] = {} # Track stats per character

    def add_experience(self, character: Character, amount: int, source: str) -> Dict[str, Any]:
        """Add experience"""
        result = self.progression_manager.add_experience(character, amount, source)

        # Track progress locally
        char_id = str(character.id)
        if char_id not in self.character_progress:
            self.character_progress[char_id] = {
                "total_experience_gained": 0,
                "abilities_learned": 0
            }
        self.character_progress[char_id]["total_experience_gained"] += amount

        return result

    def learn_ability(self, character: Character, ability_id: str) -> Dict[str, Any]:
        """Learn ability"""
        result = self.progression_manager.learn_ability(character, ability_id)

        if result["success"]:
            char_id = str(character.id)
            if char_id not in self.character_progress:
                self.character_progress[char_id] = {
                    "total_experience_gained": 0,
                    "abilities_learned": 0
                }
            self.character_progress[char_id]["abilities_learned"] += 1

        return result

    def get_character_summary(self, character: Character) -> Dict[str, Any]:
        """Get summary"""
        base_summary = self.progression_manager.get_character_progression_summary(character)
        base_summary["progression_stats"] = self.character_progress.get(str(character.id), {})
        return base_summary

    def get_available_abilities(self, character: Character, skill_type: SkillType = None) -> List[Any]:
        """Get available abilities"""
        all_available = self.progression_manager.skill_tree.get_available_abilities(character)
        if skill_type:
            return [a for a in all_available if a.skill_type == skill_type]
        return all_available

    def get_skill_trees(self) -> Dict[SkillType, List[Any]]:
        """Get skill trees"""
        result = {}
        # Iterate over SkillType enum
        for st in SkillType:
            result[st] = self.progression_manager.skill_tree.get_ability_tree(st)
        return result
