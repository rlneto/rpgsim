from typing import Dict, Optional, List
from ..domain.spells import Spell, SpellBook
from ..interfaces.repositories import SpellRepository

class MemorySpellRepository(SpellRepository):
    def __init__(self):
        self._spells: Dict[str, Spell] = {}
        self._spell_books: Dict[str, SpellBook] = {}

    def get_spell(self, spell_id: str) -> Optional[Spell]:
        return self._spells.get(spell_id)

    def add_spell(self, spell: Spell) -> None:
        self._spells[spell.id] = spell

    def list_spells(self) -> List[Spell]:
        return list(self._spells.values())

    def get_spell_book(self, character_id: str) -> Optional[SpellBook]:
        return self._spell_books.get(character_id)

    def save_spell_book(self, spell_book: SpellBook) -> None:
        self._spell_books[spell_book.character_id] = spell_book
