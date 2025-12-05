from typing import Optional
from ..domain.spells import Spell, SpellBook
from ..interfaces.repositories import SpellRepository

class SpellService:
    def __init__(self, repository: SpellRepository):
        self.repository = repository

    def create_spell(self, id: str, name: str, mana_cost: int, description: str, damage: int = 0) -> Spell:
        spell = Spell(id, name, mana_cost, description, damage)
        self.repository.add_spell(spell)
        return spell

    def learn_spell(self, character_id: str, spell_id: str) -> bool:
        spell = self.repository.get_spell(spell_id)
        if not spell:
            return False

        spell_book = self.repository.get_spell_book(character_id)
        if not spell_book:
            spell_book = SpellBook(character_id)

        if spell_id not in spell_book.known_spells:
            spell_book.known_spells.append(spell_id)
            self.repository.save_spell_book(spell_book)
            return True
        return False

    def cast_spell(self, character_id: str, spell_id: str, current_mana: int) -> Optional[int]:
        """Returns remaining mana if cast successful, else None"""
        spell = self.repository.get_spell(spell_id)
        spell_book = self.repository.get_spell_book(character_id)

        if not spell or not spell_book:
            return None

        if spell_id not in spell_book.known_spells:
            return None

        if current_mana >= spell.mana_cost:
            return current_mana - spell.mana_cost

        return None
