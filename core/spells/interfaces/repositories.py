from abc import ABC, abstractmethod
from typing import List, Optional
from core.spells.domain.spells import Spell

class SpellRepository(ABC):
    @abstractmethod
    def get_spell_by_name(self, spell_name: str) -> Optional[Spell]:
        pass

    @abstractmethod
    def get_all_spells(self) -> List[Spell]:
        pass

    @abstractmethod
    def add_spell(self, spell: Spell):
        pass
