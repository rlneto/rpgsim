from typing import Optional
from core.spells.domain.spells import Spell
from core.spells.interfaces.repositories import SpellRepository

class SpellCreationService:
    def __init__(self, spell_repository: SpellRepository):
        self._spell_repository = spell_repository

    def create_spell(self, spell_name: str) -> Optional[Spell]:
        return self._spell_repository.get_spell_by_name(spell_name)
