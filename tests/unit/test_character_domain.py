
import pytest
import uuid
from core.systems.character.domain.character import Character, CharacterClass, CharacterStats

def test_all_classes_available():
    assert len(CharacterClass) == 24
    assert CharacterClass.WARRIOR in CharacterClass
    assert CharacterClass.MAGE in CharacterClass
    assert CharacterClass.ROGUE in CharacterClass

def test_class_values_are_strings():
    for character_class in CharacterClass:
        assert isinstance(character_class.value, str)
        assert len(character_class.value.strip()) > 0

def test_class_conversion():
    assert CharacterClass.WARRIOR.value == "Warrior"

def test_default_stats_creation():
    stats = CharacterStats()
    assert stats.strength == 10
    assert stats.dexterity == 10
    assert stats.intelligence == 10
    assert stats.wisdom == 10
    assert stats.charisma == 10
    assert stats.constitution == 10

def test_custom_stats_creation():
    stats = CharacterStats(
        strength=15,
        dexterity=12,
        intelligence=8,
        wisdom=14,
        charisma=10,
        constitution=13,
    )
    assert stats.strength == 15
    assert stats.dexterity == 12
    assert stats.intelligence == 8
    assert stats.wisdom == 14
    assert stats.charisma == 10
    assert stats.constitution == 13

def test_total_power():
    stats = CharacterStats(
        strength=10,
        dexterity=10,
        intelligence=10,
        wisdom=10,
        charisma=10,
        constitution=10,
    )
    assert stats.total_power() == 60

def test_character_creation():
    stats = CharacterStats()
    character = Character(
        id=str(uuid.uuid4()),
        name="Test Character",
        class_type=CharacterClass.WARRIOR,
        level=1,
        experience=0,
        stats=stats,
        hp=100,
        max_hp=100,
        gold=50,
        abilities=[],
        inventory=[],
        created=True
    )

    assert character.name == "Test Character"
    assert character.class_type == CharacterClass.WARRIOR
    assert character.level == 1
    assert character.hp == 100
    assert character.max_hp == 100
    assert character.gold == 50
    assert character.is_alive()

def test_character_is_alive():
    stats = CharacterStats()
    character = Character(
        id=str(uuid.uuid4()),
        name="Test",
        class_type=CharacterClass.WARRIOR,
        level=1,
        experience=0,
        stats=stats,
        hp=0,
        max_hp=100,
        gold=50,
        abilities=[],
        inventory=[],
        created=True
    )
    assert not character.is_alive()

def test_add_to_inventory():
    character = Character()
    character.add_to_inventory("Sword")
    assert "Sword" in character.inventory

def test_remove_from_inventory():
    character = Character(inventory=["Sword"])
    character.remove_from_inventory("Sword")
    assert "Sword" not in character.inventory

def test_level_up():
    character = Character(level=1, created=True, class_type=CharacterClass.WARRIOR)
    character.level_up()
    assert character.level == 2
