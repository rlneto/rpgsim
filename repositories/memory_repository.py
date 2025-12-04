from typing import List, Dict
from domain.spells import Spell, SpellSchool, SpellEffect
from interfaces.repositories import ISpellRepository

class MemorySpellRepository(ISpellRepository):
    def __init__(self):
        self._spells = self._load_spells()

    def get_spell(self, spell_name: str) -> Spell:
        return self._spells.get(spell_name)

    def get_all_spells(self) -> List[Spell]:
        return list(self._spells.values())

    def add_spell(self, spell: Spell):
        self._spells[spell.name] = spell

    def _load_spells(self) -> Dict[str, Spell]:
        # Data moved from core/legacy/spells.py _get_spell_configuration
        spell_data = {
            "fireball": {
                "school": SpellSchool.FIRE,
                "power": 30,
                "mana_cost": 20,
                "description": "Hurls a fiery explosion at target",
                "effects": [
                    SpellEffect(name="damage", description="", parameters={"amount": 30}),
                    SpellEffect(name="status", description="", parameters={"name": "burn"}),
                ],
                "level_requirement": 3,
                "duration": 0, "range": 5, "radius": 2, "target_type": "enemy",
            },
            "ice_lance": {
                "school": SpellSchool.WATER,
                "power": 25,
                "mana_cost": 15,
                "description": "Launches a shard of ice at target",
                "effects": [
                    SpellEffect(name="damage", description="", parameters={"amount": 25}),
                    SpellEffect(name="status", description="", parameters={"name": "freeze"}),
                ],
                "level_requirement": 2,
                "duration": 2, "range": 4, "radius": 0, "target_type": "enemy",
            },
            "lightning_bolt": {
                "school": SpellSchool.AIR,
                "power": 40,
                "mana_cost": 25,
                "description": "Calls down a bolt of lightning",
                "effects": [
                    SpellEffect(name="damage", description="", parameters={"amount": 40}),
                    SpellEffect(name="status", description="", parameters={"name": "stun"}),
                ],
                "level_requirement": 5,
                "duration": 1, "range": 8, "radius": 0, "target_type": "enemy",
            },
            "heal": {
                "school": SpellSchool.HEALING,
                "power": 25,
                "mana_cost": 10,
                "description": "Restores health to target",
                "effects": [
                    SpellEffect(name="healing", description="", parameters={"amount": 25}),
                ],
                "level_requirement": 2,
                "duration": 0, "range": 1, "radius": 0, "target_type": "ally",
            },
            "holy_light": {
                "school": SpellSchool.LIGHT,
                "power": 35,
                "mana_cost": 30,
                "description": "Radiant holy light damages enemies and heals allies",
                "effects": [
                    SpellEffect(name="damage", description="", parameters={"amount": 35}),
                    SpellEffect(name="healing", description="", parameters={"amount": 20}),
                ],
                "level_requirement": 4,
                "class_requirement": "cleric",
                "duration": 0, "range": 6, "radius": 3, "target_type": "both",
            },
            "poison_cloud": {
                "school": SpellSchool.DARK,
                "power": 20,
                "mana_cost": 15,
                "description": "Creates a cloud of poisonous gas",
                "effects": [
                    SpellEffect(name="damage", description="", parameters={"amount": 20}),
                    SpellEffect(name="status", description="", parameters={"name": "poison"}),
                ],
                "level_requirement": 3,
                "duration": 3, "range": 3, "radius": 2, "target_type": "enemy",
            },
            "shield": {
                "school": SpellSchool.PROTECTION,
                "power": 0,
                "mana_cost": 10,
                "description": "Creates a magical shield that reduces damage",
                "effects": [
                    SpellEffect(name="status", description="", parameters={"name": "defense_boost"}),
                ],
                "level_requirement": 1,
                "duration": 5, "range": 1, "radius": 0, "target_type": "ally",
            },
            "teleport": {
                "school": SpellSchool.ILLUSION,
                "power": 0,
                "mana_cost": 50,
                "description": "Instantly transports caster to another location",
                "effects": [],
                "level_requirement": 6,
                "class_requirement": "mage",
                "stat_requirement": ("intelligence", 15),
                "duration": 0, "range": 10, "radius": 0, "target_type": "self",
            },
        }

        spells = {}
        for name, data in spell_data.items():
            spells[name] = Spell(name=name, **data)

        return spells
