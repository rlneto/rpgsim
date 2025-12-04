
import pytest
from core.systems.character.domain.character import Character, CharacterClass, CharacterStats, CHARACTER_CLASSES

def test_character_init():
    char = Character()
    assert char.id == ""
    assert char.name == ""
    assert char.class_type is None
    assert char.level == 1
    assert char.experience == 0
    assert char.hp == 0 
    assert char.max_hp == 100
    assert char.gold == 0
    assert char.inventory == []
    assert char.abilities == []
    assert char.created is False
    assert char.visual_customization == {}
    assert char.is_alive() is False

def test_character_stats_property():
    stats = CharacterStats(strength=15)
    char = Character(stats=stats)
    assert char.stats.strength == 15

def test_is_alive():
    char = Character(hp=50, created=True)
    assert char.is_alive() is True
    char.hp = 0
    assert char.is_alive() is False

def test_get_strengths_and_weaknesses():
    stats = CharacterStats(strength=18, dexterity=8)
    char = Character(stats=stats)
    assert "strength" in char.stats.get_strengths()
    assert "dexterity" in char.stats.get_weaknesses()

def test_get_inventory_count():
    char = Character(inventory=["sword", "shield"])
    assert len(char.inventory) == 2

def test_level_up():
    char = Character(level=5, created=True, class_type=CharacterClass.WARRIOR)
    result = char.level_up()
    assert result is True
    assert char.level == 6

def test_set_visual_customization():
    char = Character()
    customization = {"hair_color": "black", "eye_color": "blue"}
    char.visual_customization = customization
    assert char.visual_customization["hair_color"] == "black"

def test_all_classes_have_stats():
    for char_class in CHARACTER_CLASSES:
        assert char_class in CharacterClass

def test_class_balance_within_15_percent():
    balance_stats = {}
    for char_class, config in CHARACTER_CLASSES.items():
        if char_class.value == "Developer": continue
        balance_stats[char_class.value] = config.base_stats.total_power()

    max_power = max(balance_stats.values())
    min_power = min(balance_stats.values())
    assert (max_power - min_power) / min_power <= 0.15
