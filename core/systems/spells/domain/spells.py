from typing import List, Dict, Optional

from pydantic import BaseModel, Field


class Spell(BaseModel):
    """Simple Spell model"""
    id: str = Field(..., description="Unique spell identifier")
    name: str = Field(..., description="Spell name")
    mana_cost: int = Field(ge=0, description="Mana cost to cast spell")
    description: str = Field(..., description="Spell description")
    damage: int = Field(default=0, ge=0, description="Spell damage")
    effect_type: str = Field(default="damage", description="Type of spell effect")


class SpellBook(BaseModel):
    """Pydantic SpellBook model for Character compatibility"""
    character_id: str = Field(..., description="Character ID this spellbook belongs to")
    known_spells: List[str] = Field(default_factory=list, description="List of known spell IDs")
