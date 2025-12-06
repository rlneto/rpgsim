from typing import Optional, Dict, Any
from core.models import Character
from .domain.spells import Spell
from .services.spell_service import SpellService
from .repositories.memory_repository import MemorySpellRepository

class SpellSystem:
    def __init__(self):
        self.repository = MemorySpellRepository()
        self.service = SpellService(self.repository)

    def get_spell(self, spell_id: str) -> Optional[Spell]:
        return self.repository.get_spell(spell_id)

    def learn_spell(self, character: Character, spell_id: str) -> bool:
        return self.service.learn_spell(character, spell_id)

    def cast_spell(self, character: Character, target: Character, spell_id: str) -> Dict[str, Any]:
        return self.service.cast_spell(character, target, spell_id)
