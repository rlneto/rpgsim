from core.spells.domain.spells import SpellBook, Spell
from core.spells.interfaces.repositories import SpellRepository
from core.models import Character

class SpellLearningService:
    def __init__(self, spell_repository: SpellRepository):
        self._spell_repository = spell_repository

    def learn_spell(self, character: Character, spell_name: str) -> bool:
        spell = self._spell_repository.get_spell_by_name(spell_name)
        if spell and self._can_learn_spell(character, spell):
            character.spell_book.add_spell(spell)
            return True
        return False

    def _can_learn_spell(self, character: Character, spell: Spell) -> bool:
        if character.level < spell.level_requirement:
            return False
        
        # Add more complex logic here, e.g., class requirements, stat requirements
        # For now, we'll keep it simple.
        
        return True
