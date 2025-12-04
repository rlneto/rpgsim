from typing import List, Optional, Dict
from core.spells.domain.spells import Spell, SpellSchool, SpellEffect
from core.spells.interfaces.repositories import SpellRepository

class MemorySpellRepository(SpellRepository):
    def __init__(self):
        self._spells: Dict[str, Spell] = self._load_spells()

    def get_spell_by_name(self, spell_name: str) -> Optional[Spell]:
        return self._spells.get(spell_name)

    def get_all_spells(self) -> List[Spell]:
        return list(self._spells.values())

    def add_spell(self, spell: Spell):
        if spell.name in self._spells:
            # Handle error or update logic
            pass
        self._spells[spell.name] = spell

    def _load_spells(self) -> Dict[str, Spell]:
        # Data from the original _get_spell_configuration function
        return {
            "fireball": Spell(
                name="fireball",
                school=SpellSchool.FIRE,
                mana_cost=0, # Will be calculated by a service
                level_requirement=3,
                effects=[SpellEffect(effect_type="damage", value=30), SpellEffect(effect_type="status_effect", value="burn")],
                description="Hurls a fiery explosion at target",
                area_of_effect=True,
                range=5,
                radius=2,
                casting_time=2,
                components=["verbal", "somatic"],
            ),
            "ice_lance": Spell(
                name="ice_lance",
                school=SpellSchool.WATER,
                mana_cost=0, # Will be calculated by a service
                level_requirement=2,
                effects=[SpellEffect(effect_type="damage", value=25), SpellEffect(effect_type="status_effect", value="freeze")],
                description="Launches a shard of ice at target",
                range=4,
                casting_time=1,
                components=["verbal", "somatic"],
            ),
            "lightning_bolt": Spell(
                name="lightning_bolt",
                school=SpellSchool.AIR,
                mana_cost=0, # Will be calculated by a service
                level_requirement=5,
                effects=[SpellEffect(effect_type="damage", value=40), SpellEffect(effect_type="status_effect", value="stun")],
                description="Calls down a bolt of lightning",
                range=8,
                casting_time=1,
                components=["verbal", "somatic"],
            ),
            "heal": Spell(
                name="heal",
                school=SpellSchool.HEALING,
                mana_cost=0, # Will be calculated by a service
                level_requirement=2,
                effects=[SpellEffect(effect_type="healing", value=25)],
                description="Restores health to target",
                target_type="ally",
                casting_time=1,
                components=["verbal", "somatic"],
            ),
            "holy_light": Spell(
                name="holy_light",
                school=SpellSchool.LIGHT,
                mana_cost=0, # Will be calculated by a service
                level_requirement=4,
                effects=[SpellEffect(effect_type="damage", value=35), SpellEffect(effect_type="healing", value=20)],
                description="Radiant holy light damages enemies and heals allies",
                area_of_effect=True,
                range=6,
                radius=3,
                target_type="both",
                casting_time=2,
                components=["verbal", "somatic", "divine_focus"],
                requirements={"class_requirement": "cleric"}
            ),
            "poison_cloud": Spell(
                name="poison_cloud",
                school=SpellSchool.DARK,
                mana_cost=0, # Will be calculated by a service
                level_requirement=3,
                effects=[SpellEffect(effect_type="damage", value=20), SpellEffect(effect_type="status_effect", value="poison")],
                description="Creates a cloud of poisonous gas",
                area_of_effect=True,
                range=3,
                radius=2,
                casting_time=2,
                components=["verbal", "somatic", "material"],
            ),
            "shield": Spell(
                name="shield",
                school=SpellSchool.PROTECTION,
                mana_cost=0, # Will be calculated by a service
                level_requirement=1,
                effects=[SpellEffect(effect_type="status_effect", value="defense_boost")],
                description="Creates a magical shield that reduces damage",
                target_type="ally",
                casting_time=1,
                components=["verbal", "somatic"],
            ),
            "teleport": Spell(
                name="teleport",
                school=SpellSchool.ILLUSION,
                mana_cost=0, # Will be calculated by a service
                level_requirement=6,
                effects=[],
                description="Instantly transports caster to another location",
                target_type="self",
                range=10,
                casting_time=3,
                components=["verbal", "somatic"],
                requirements={"stat_requirement": ("intelligence", 15)}
            )
        }
