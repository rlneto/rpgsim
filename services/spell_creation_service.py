from domain.spells import Spell, SpellEffect, SpellSchool
from interfaces.repositories import ISpellRepository
from typing import List

class SpellCreationService:
    def __init__(self, spell_repository: ISpellRepository):
        self._spell_repository = spell_repository

    def create_spell(
        self,
        name: str,
        school: SpellSchool,
        power: int,
        mana_cost: int,
        description: str,
        effects: List[SpellEffect],
        level_requirement: int = 1,
    ) -> Spell:
        spell = Spell(
            name=name,
            school=school,
            power=power,
            mana_cost=mana_cost,
            description=description,
            effects=effects,
            level_requirement=level_requirement,
        )
        self._spell_repository.add_spell(spell)
        return spell
