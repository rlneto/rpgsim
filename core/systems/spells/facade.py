from typing import Optional
from .domain.spells import Spell, SpellBook
from .services.spell_service import SpellService
from .repositories.memory_repository import MemorySpellRepository

class SpellSystem:
    def __init__(self):
        self.repository = MemorySpellRepository()
        self.service = SpellService(self.repository)

    def create_spell(self, id: str, name: str, mana_cost: int, description: str, damage: int = 0) -> Spell:
        return self.service.create_spell(id, name, mana_cost, description, damage)

    def learn_spell(self, character_id: str, spell_id: str) -> bool:
        return self.service.learn_spell(character_id, spell_id)

    def cast_spell(self, character_id: str, spell_id: str, current_mana: int) -> Optional[int]:
        return self.service.cast_spell(character_id, spell_id, current_mana)
