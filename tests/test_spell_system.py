import pytest
from unittest.mock import patch
from facade import SpellSystem
from domain.spells import Spell, SpellSchool, SpellEffect, SpellBook
from core.models import Character, CharacterStats, CharacterClass

# Rebuild the Character model to resolve the forward reference to SpellBook
Character.model_rebuild()

@pytest.fixture
def spell_system():
    return SpellSystem()

@pytest.fixture
def character():
    stats = CharacterStats(strength=10, dexterity=10, intelligence=15, wisdom=12, charisma=8, constitution=14)
    return Character(
        id="test_char",
        name="Test Mage",
        class_type=CharacterClass.MAGE,
        level=5,
        experience=1000,
        stats=stats,
        hp=50,
        max_hp=50,
        mana=100,
        max_mana=100,
        spell_book=SpellBook(),
        gold=100
    )

@pytest.fixture
def target_character():
    stats = CharacterStats()
    return Character(
        id="target_char",
        name="Target",
        class_type=CharacterClass.WARRIOR,
        level=5,
        experience=1000,
        stats=stats,
        hp=10,
        max_hp=50,
        gold=100,
    )

def test_get_spell(spell_system):
    fireball = spell_system.get_spell("fireball")
    assert fireball is not None
    assert fireball.name == "fireball"
    assert fireball.school == SpellSchool.FIRE

@patch('services.spell_casting_service.random.randint', return_value=1)
def test_cast_spell_damage(mock_randint, spell_system, character, target_character):
    spell_system.learn_spell(character, "fireball")
    result = spell_system.cast_spell(character, target_character, "fireball")
    assert result["spell_cast"]
    assert result["damage"] == 60
    assert target_character.hp == 0

@patch('services.spell_casting_service.random.randint', return_value=1)
def test_cast_spell_healing(mock_randint, spell_system, character, target_character):
    spell_system.learn_spell(character, "heal")
    result = spell_system.cast_spell(character, target_character, "heal")
    assert result["spell_cast"]
    assert result["healing"] > 0
    assert target_character.hp > 10

def test_cast_spell_insufficient_mana(spell_system, character):
    character.mana = 10
    with pytest.raises(ValueError, match="Insufficient mana."):
        spell_system.cast_spell(character, None, "fireball")

@patch('services.spell_casting_service.random.randint', return_value=100)
def test_cast_spell_miss(mock_randint, spell_system, character, target_character):
    spell_system.learn_spell(character, "fireball")
    result = spell_system.cast_spell(character, target_character, "fireball")
    assert not result["spell_hits"]
    assert result["damage"] == 0
    assert target_character.hp == 10

@patch('services.spell_casting_service.random.randint', return_value=1)
def test_cast_spell_status_effect(mock_randint, spell_system, character, target_character):
    spell_system.learn_spell(character, "poison_cloud")
    result = spell_system.cast_spell(character, target_character, "poison_cloud")
    assert "poison" in result["status_effects_applied"]
    assert "poison" in target_character.status_effects

@patch('services.spell_casting_service.random.randint', return_value=1)
def test_spell_cooldown(mock_randint, spell_system, character, target_character):
    spell_system.learn_spell(character, "fireball")
    spell_system.cast_spell(character, target_character, "fireball")
    with pytest.raises(ValueError, match="is on cooldown"):
        spell_system.cast_spell(character, target_character, "fireball")

def test_learn_spell_requirements_not_met(spell_system, character):
    character.level = 1
    spell_system.learn_spell(character, "fireball")
    assert "fireball" not in character.spell_book.spells
