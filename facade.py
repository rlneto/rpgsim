from repositories.memory_repository import MemorySpellRepository
from services.spell_casting_service import SpellCastingService
from services.spell_learning_service import SpellLearningService
from services.spell_creation_service import SpellCreationService
from domain.spells import Spell

class SpellSystem:
    def __init__(self):
        self._spell_repository = MemorySpellRepository()
        self._spell_casting_service = SpellCastingService(self._spell_repository)
        self._spell_learning_service = SpellLearningService()
        self._spell_creation_service = SpellCreationService(self._spell_repository)

    def cast_spell(self, caster, target, spell_name):
        return self._spell_casting_service.cast_spell(caster, target, spell_name)

    def learn_spell(self, character, spell_name):
        spell = self._spell_repository.get_spell(spell_name)
        if spell:
            self._spell_learning_service.learn_spell(character, spell)

    def create_spell(self, name, school, power, mana_cost, description, effects, level_requirement=1) -> Spell:
        return self._spell_creation_service.create_spell(name, school, power, mana_cost, description, effects, level_requirement)

    def get_spell(self, spell_name: str) -> Spell:
        return self._spell_repository.get_spell(spell_name)

    def get_all_spells(self):
        return self._spell_repository.get_all_spells()

    def calculate_spell_duration(self, spell_name: str, caster_level: int = 1) -> int:
        return self._spell_casting_service.calculate_spell_duration(spell_name, caster_level)

    def get_spell_range(self, spell_name: str) -> int:
        return self._spell_casting_service.get_spell_range(spell_name)
