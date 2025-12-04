from enum import Enum
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

class SpellSchool(Enum):
    FIRE = "fire"
    WATER = "water"
    EARTH = "earth"
    AIR = "air"
    LIGHT = "light"
    DARK = "dark"
    HEALING = "healing"
    PROTECTION = "protection"
    ILLUSION = "illusion"

@dataclass
class SpellEffect:
    effect_type: str  # e.g., "damage", "healing", "status_effect"
    value: Any # int for damage/healing, str for status effect
    duration: Optional[int] = None

@dataclass
class Spell:
    name: str
    school: SpellSchool
    mana_cost: int
    level_requirement: int
    effects: List[SpellEffect]
    description: str = ""
    casting_time: int = 1
    cooldown: int = 0
    area_of_effect: bool = False
    range: int = 1
    radius: int = 0
    target_type: str = "enemy"
    components: List[str] = field(default_factory=list)
    requirements: Dict[str, Any] = field(default_factory=dict)

class SpellBook:
    def __init__(self):
        self._spells: Dict[str, Spell] = {}

    def add_spell(self, spell: Spell):
        if spell.name in self._spells:
            # Handle error or update logic
            pass
        self._spells[spell.name] = spell

    def get_spell(self, spell_name: str) -> Optional[Spell]:
        return self._spells.get(spell_name)

    def get_all_spells(self) -> List[Spell]:
        return list(self._spells.values())

    def knows_spell(self, spell_name: str) -> bool:
        return spell_name in self._spells
