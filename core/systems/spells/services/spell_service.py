import random
from typing import Dict, Any
from core.models import Character
from ..domain.spells import SpellBook
from ..interfaces.repositories import SpellRepository

class SpellService:
    def __init__(self, repository: SpellRepository):
        self.repository = repository

    def learn_spell(self, character: Character, spell_id: str) -> bool:
        spell = self.repository.get_spell(spell_id)
        if not spell:
            return False

        if character.level < 5: # Just an example requirement
            return False

        spell_book = character.spell_book
        if not spell_book:
            spell_book = SpellBook(character_id=character.id)
            character.spell_book = spell_book

        if spell_id not in spell_book.known_spells:
            spell_book.known_spells.append(spell_id)
            return True
        return False

    def cast_spell(self, character: Character, target: Character, spell_id: str) -> Dict[str, Any]:
        spell = self.repository.get_spell(spell_id)
        if not spell:
            raise ValueError("Spell not found.")

        if spell_id in character.spell_cooldowns and character.spell_cooldowns[spell_id] > 0:
            raise ValueError(f"{spell.name} is on cooldown.")

        if character.mana < spell.mana_cost:
            raise ValueError("Insufficient mana.")

        character.mana -= spell.mana_cost
        character.spell_cooldowns[spell_id] = 2 # Example cooldown of 2 turns

        result = {"spell_cast": True, "spell_hits": False, "damage": 0, "healing": 0, "status_effects_applied": []}

        if random.randint(1, 100) > 90: # 10% chance to miss
            return result

        result["spell_hits"] = True
        if spell.damage > 0:
            target.hp = max(0, target.hp - spell.damage)
            result["damage"] = spell.damage

        if spell.effect:
            if spell.effect.effect_type == "heal":
                target.hp = min(target.max_hp, target.hp + spell.effect.value)
                result["healing"] = spell.effect.value
            elif spell.effect.effect_type == "poison":
                target.status_effects["poison"] = spell.effect.value
                result["status_effects_applied"].append("poison")

        return result
