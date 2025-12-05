from dataclasses import dataclass, field
from typing import List, Dict, Optional

@dataclass
class Spell:
    id: str
    name: str
    mana_cost: int
    description: str
    damage: int = 0
    effect_type: str = "damage"

@dataclass
class SpellBook:
    character_id: str
    known_spells: List[str] = field(default_factory=list)
