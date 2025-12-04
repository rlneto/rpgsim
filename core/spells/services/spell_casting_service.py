from typing import Dict, Any, Union
from core.models import Character, Enemy
from core.spells.domain.spells import Spell
import random

class SpellCastingService:
    def cast_spell(self, caster: Union[Character, Enemy], target: Union[Character, Enemy], spell: Spell) -> Dict[str, Any]:
        # This is where the core logic from the old `cast_spell` function will go.
        # For now, I'll put in a placeholder implementation.
        
        hit_chance = self._calculate_hit_chance(caster, target, spell)
        hit_roll = random.randint(1, 100)
        spell_hits = hit_roll <= hit_chance

        damage = 0
        healing = 0
        status_effects_applied = []

        if spell_hits:
            for effect in spell.effects:
                if effect.effect_type == "damage":
                    damage += effect.value
                elif effect.effect_type == "healing":
                    healing += effect.value
                elif effect.effect_type == "status_effect":
                    status_effects_applied.append(effect.value)

        return {
            "spell_cast": True,
            "spell_name": spell.name,
            "spell_hits": spell_hits,
            "damage": damage,
            "healing": healing,
            "status_effects_applied": status_effects_applied,
        }

    def _calculate_hit_chance(self, caster, target, spell) -> int:
        # Simplified hit chance calculation
        return 80
