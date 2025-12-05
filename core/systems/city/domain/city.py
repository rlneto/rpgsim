from typing import List, Optional, Dict
from dataclasses import dataclass, field

@dataclass
class Building:
    id: str
    name: str
    type: str
    level: int = 1

@dataclass
class City:
    id: str
    name: str
    population: int
    buildings: List[Building] = field(default_factory=list)
    resources: Dict[str, int] = field(default_factory=dict)
