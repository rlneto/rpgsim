from abc import ABC, abstractmethod
from typing import List
from domain.spells import Spell

class ISpellRepository(ABC):
    @abstractmethod
    def get_spell(self, spell_name: str) -> Spell:
        pass

    @abstractmethod
    def get_all_spells(self) -> List[Spell]:
        pass

    @abstractmethod
    def add_spell(self, spell: Spell):
        pass
