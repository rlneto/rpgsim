import random
from typing import Union, Dict, Any
from domain.spells import Spell
from interfaces.repositories import ISpellRepository
from core.models import Character, Enemy, CharacterStats

class SpellCastingService:
    def __init__(self, spell_repository: ISpellRepository):
        self._spell_repository = spell_repository

    def cast_spell(
        self,
        caster: Union[Character, Enemy],
        target: Union[Character, Enemy, None],
        spell_name: str,
    ) -> Dict[str, Any]:
        spell = self._spell_repository.get_spell(spell_name)
        if not spell:
            raise ValueError(f"Spell '{spell_name}' not found.")

        if not self._check_spell_requirements(caster, spell):
            raise ValueError(f"Spell requirements not met for {spell_name}")

        if hasattr(caster, "spell_cooldowns") and caster.spell_cooldowns.get(spell_name, 0) > 0:
            raise ValueError(f"Spell '{spell_name}' is on cooldown.")

        if hasattr(caster, "mana") and caster.mana < spell.mana_cost:
            raise ValueError("Insufficient mana.")

        hit_chance = self._calculate_spell_hit_chance(caster, target, spell.school.value)
        hit_roll = random.randint(1, 100)
        spell_hits = hit_roll <= hit_chance

        total_damage = 0
        total_healing = 0
        status_effects_applied = []

        if spell_hits and target:
            for effect in spell.effects:
                if effect.name == "damage":
                    damage_result = self._calculate_spell_damage(caster, target, spell)
                    total_damage = damage_result["damage"]
                    if hasattr(target, "hp"):
                        target.hp = max(0, target.hp - total_damage)
                elif effect.name == "healing":
                    healing_result = self._calculate_spell_healing(caster, target, spell)
                    total_healing = healing_result["healing"]
                    if hasattr(target, "hp"):
                        target.hp = min(target.max_hp, target.hp + total_healing)
                elif effect.name == "status":
                    if self._apply_status_effect(target, effect.parameters.get("name"), spell.power, caster):
                        status_effects_applied.append(effect.parameters.get("name"))

        if hasattr(caster, "mana"):
            caster.mana -= spell.mana_cost

        if hasattr(caster, "spell_cooldowns"):
            cooldown = self._calculate_spell_cooldown(spell)
            caster.spell_cooldowns[spell_name] = cooldown

        return {
            "spell_cast": True,
            "spell_name": spell.name,
            "spell_hits": spell_hits,
            "hit_chance": hit_chance,
            "damage": total_damage,
            "healing": total_healing,
            "status_effects_applied": status_effects_applied,
            "mana_used": spell.mana_cost,
        }

    def calculate_spell_duration(self, spell_name: str, caster_level: int = 1) -> int:
        spell = self._spell_repository.get_spell(spell_name)
        if not spell:
            raise ValueError(f"Spell '{spell_name}' not found.")

        base_duration = 0 # Domain model doesn't have duration yet.
        power_scaling = spell.power // 20
        level_bonus = (caster_level - 1) // 3
        
        school_bonus = 0
        if spell.school == "holy":
            school_bonus = 1
        elif spell.school == "dark":
            school_bonus = 2
            
        total_duration = base_duration + power_scaling + level_bonus + school_bonus
        total_duration = max(total_duration, 0)
        total_duration = min(total_duration, 20)
        return total_duration
    
    def get_spell_range(self, spell_name: str) -> int:
        spell = self._spell_repository.get_spell(spell_name)
        if not spell:
            raise ValueError(f"Spell '{spell_name}' not found.")

        base_range = 1 # Domain model doesn't have range yet.
        power_scaling = spell.power // 25

        school_modifier = 1.0
        if spell.school.value == "fire":
            school_modifier = 1.2
        elif spell.school.value == "ice":
            school_modifier = 0.8
        elif spell.school.value == "lightning":
            school_modifier = 1.5

        total_range = int((base_range + power_scaling) * school_modifier)
        total_range = max(total_range, 1)
        total_range = min(total_range, 50)
        return total_range

    def _check_spell_requirements(self, caster, spell):
        if caster.level < spell.level_requirement:
            return False
        
        if spell.class_requirement and isinstance(caster, Character) and caster.class_type.value != spell.class_requirement:
            return False

        if spell.stat_requirement:
            stat_name, stat_value = spell.stat_requirement
            if hasattr(caster.stats, stat_name) and getattr(caster.stats, stat_name) < stat_value:
                return False
        
        return True

    def _get_spell_schools_config(self):
        return {
            "fire": {"primary_stat": "intelligence", "secondary_stat": "wisdom", "mana_multiplier": 1.2, "cooldown_modifier": 0.8},
            "water": {"primary_stat": "wisdom", "secondary_stat": "intelligence", "mana_multiplier": 1.1, "cooldown_modifier": 1.0},
            "earth": {"primary_stat": "constitution", "secondary_stat": "strength", "mana_multiplier": 1.0, "cooldown_modifier": 1.1},
            "air": {"primary_stat": "dexterity", "secondary_stat": "intelligence", "mana_multiplier": 1.1, "cooldown_modifier": 0.9},
            "light": {"primary_stat": "wisdom", "secondary_stat": "charisma", "mana_multiplier": 1.3, "cooldown_modifier": 1.2},
            "dark": {"primary_stat": "charisma", "secondary_stat": "intelligence", "mana_multiplier": 1.4, "cooldown_modifier": 1.3},
            "healing": {"primary_stat": "wisdom", "secondary_stat": "constitution", "mana_multiplier": 0.8, "cooldown_modifier": 0.7},
            "protection": {"primary_stat": "constitution", "secondary_stat": "wisdom", "mana_multiplier": 1.0, "cooldown_modifier": 1.0},
            "illusion": {"primary_stat": "intelligence", "secondary_stat": "charisma", "mana_multiplier": 1.1, "cooldown_modifier": 1.0},
        }

    def _get_status_effects_config(self):
        return {
            "stun": {"duration": 2, "immune_classes": ["warrior", "barbarian"]},
            "poison": {"duration": 3, "damage_per_turn": 2, "immune_classes": ["rogue", "ranger"]},
            "freeze": {"duration": 1, "immune_classes": ["mage", "wizard"]},
            "burn": {"duration": 2, "damage_per_turn": 1, "immune_classes": ["fire_elemental"]},
            "heal": {"duration": 0, "heal_amount": 5},
            "shield": {"duration": 3, "damage_reduction": 2},
            "haste": {"duration": 2, "speed_bonus": 2},
            "slow": {"duration": 2, "speed_penalty": 1},
        }

    def _apply_status_effect(self, target, status_effect, spell_power, caster):
        if not hasattr(target, "status_effects"):
            return False

        effect_config = self._get_status_effects_config().get(status_effect)
        if not effect_config:
            return False

        if isinstance(target, Character):
            immune_classes = effect_config.get("immune_classes", [])
            if target.class_type.value in immune_classes:
                return False

        base_duration = effect_config.get("duration", 3)
        power_duration = spell_power // 10
        total_duration = base_duration + power_duration

        target.status_effects[status_effect] = {
            "duration": total_duration,
            "damage_per_round": effect_config.get("damage_per_round", 0),
            "stackable": effect_config.get("stackable", False),
            "applied_by": getattr(caster, "name", "Unknown"),
        }
        return True

    def _calculate_spell_damage(self, caster, target, spell):
        caster_stats = getattr(caster, "stats", CharacterStats())
        school_config = self._get_spell_schools_config().get(spell.school.value, {})
        primary_stat = school_config.get("primary_stat", "intelligence")
        secondary_stat = school_config.get("secondary_stat", "intelligence")
        
        base_damage = spell.power
        primary_bonus = getattr(caster_stats, primary_stat, 10) // 2
        secondary_bonus = getattr(caster_stats, secondary_stat, 10) // 4
        
        raw_damage = base_damage + primary_bonus + secondary_bonus
        school_multiplier = school_config.get("mana_multiplier", 1.0)
        modified_damage = raw_damage * school_multiplier
        
        caster_level = getattr(caster, "level", 1)
        level_multiplier = 1.0 + (caster_level * 0.05)
        scaled_damage = modified_damage * level_multiplier
        
        target_resistance = self._get_spell_resistance(target, spell.school.value)
        resisted_damage = scaled_damage * target_resistance
        
        final_damage = int(resisted_damage)
        final_damage = max(final_damage, 1)
        final_damage = min(final_damage, 999)
        
        return {"damage": final_damage}

    def _calculate_spell_healing(self, caster, target, spell):
        caster_stats = getattr(caster, "stats", CharacterStats())
        school_config = self._get_spell_schools_config().get(spell.school.value, {})
        primary_stat = school_config.get("primary_stat", "wisdom")
        secondary_stat = school_config.get("secondary_stat", "charisma")

        base_healing = spell.power
        primary_bonus = getattr(caster_stats, primary_stat, 10) // 2
        secondary_bonus = getattr(caster_stats, secondary_stat, 10) // 4

        raw_healing = base_healing + primary_bonus + secondary_bonus
        school_multiplier = school_config.get("mana_multiplier", 1.0)
        modified_healing = raw_healing * school_multiplier

        caster_level = getattr(caster, "level", 1)
        level_multiplier = 1.0 + (caster_level * 0.03)
        scaled_healing = modified_healing * level_multiplier

        healing_bonus = 1.2
        final_healing = int(scaled_healing * healing_bonus)

        if hasattr(target, "hp") and hasattr(target, "max_hp"):
            missing_hp = target.max_hp - target.hp
            final_healing = min(final_healing, missing_hp)

        final_healing = max(final_healing, 0)
        return {"healing": final_healing}

    def _calculate_spell_hit_chance(self, caster, target, spell_school):
        school_config = self._get_spell_schools_config().get(spell_school, {})
        difficulty = school_config.get("difficulty", 3)
        base_hit = 100 - (difficulty * 5)
        caster_level = getattr(caster, "level", 1)
        level_bonus = min(caster_level, 20)
        target_resistance = self._get_spell_resistance(target, spell_school)
        resistance_penalty = (1.0 - target_resistance) * 20
        hit_chance = base_hit + level_bonus - resistance_penalty
        hit_chance = max(25, hit_chance)
        hit_chance = min(95, hit_chance)
        return int(hit_chance)

    def _get_spell_resistance(self, target, spell_school):
        school_config = self._get_spell_schools_config().get(spell_school, {})
        damage_type = school_config.get("damage_type", "magical")
        if hasattr(target, "resistances"):
            return target.resistances.get(damage_type, 1.0)
        return 1.0

    def _calculate_spell_cooldown(self, spell):
        base_cooldown = 3
        power_cooldown = spell.power // 50
        school_config = self._get_spell_schools_config().get(spell.school.value, {})
        school_modifier = school_config.get("cooldown_modifier", 1.0)
        final_cooldown = int((base_cooldown + power_cooldown) * school_modifier)
        final_cooldown = max(final_cooldown, 1)
        final_cooldown = min(final_cooldown, 20)
        return final_cooldown
