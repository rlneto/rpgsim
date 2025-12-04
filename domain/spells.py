from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any

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
    name: str
    description: str
    parameters: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Spell:
    name: str
    school: SpellSchool
    power: int
    mana_cost: int
    description: str
    effects: List[SpellEffect] = field(default_factory=list)
    level_requirement: int = 1
    class_requirement: str = None
    stat_requirement: tuple = None

@dataclass
class SpellBook:
    spells: Dict[str, Spell] = field(default_factory=dict)

    def add_spell(self, spell: Spell):
        self.spells[spell.name] = spell

    def get_spell(self, spell_name: str) -> Spell:
        return self.spells.get(spell_name)

    def get_spells_by_school(self, school: SpellSchool) -> List[Spell]:
        return [spell for spell in self.spells.values() if spell.school == school]
