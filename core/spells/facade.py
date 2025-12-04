from typing import Dict, Any, Union
from core.models import Character, Enemy
from core.spells.domain.spells import Spell
from core.spells.repositories.memory_repository import MemorySpellRepository
from core.spells.services.spell_casting_service import SpellCastingService
from core.spells.services.spell_learning_service import SpellLearningService

class SpellSystem:
    def __init__(self):
        self._spell_repository = MemorySpellRepository()
        self._spell_casting_service = SpellCastingService()
        self._spell_learning_service = SpellLearningService(self._spell_repository)

    def cast_spell(self, caster: Union[Character, Enemy], target: Union[Character, Enemy], spell_name: str) -> Dict[str, Any]:
        spell = self._spell_repository.get_spell_by_name(spell_name)
        if not spell:
            raise ValueError(f"Spell '{spell_name}' not found.")
        
        # In a real implementation, you'd check if the caster knows the spell,
        # has enough mana, etc.
        
        return self._spell_casting_service.cast_spell(caster, target, spell)

    def learn_spell(self, character: Character, spell_name: str) -> bool:
        return self._spell_learning_service.learn_spell(character, spell_name)
