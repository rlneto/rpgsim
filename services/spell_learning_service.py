from domain.spells import Spell, SpellBook
from core.models import Character

class SpellLearningService:
    def learn_spell(self, character: Character, spell: Spell):
        if not hasattr(character, "spell_book"):
            character.spell_book = SpellBook()
        
        # Basic validation could be added here, e.g., level requirements.
        if character.level >= spell.level_requirement:
            character.spell_book.add_spell(spell)
