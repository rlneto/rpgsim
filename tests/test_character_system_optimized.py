"""
Agent-optimized character system tests
Direct function testing with explicit behavior verification
Optimized for LLM agent development
"""

import pytest
from core.models import Character, CharacterClass, CharacterStats
from core.systems.character import (
    create_character, get_default_stats_for_class, calculate_max_hp,
    get_default_abilities_for_class, level_up_character,
    get_stat_increases_for_class, get_abilities_for_level,
    add_experience, get_experience_for_level, heal_character,
    damage_character, is_character_defeated, add_gold, remove_gold
)
from core.validation import (
    validate_character, validate_character_name, validate_stats,
    validate_experience_amount, validate_gold_amount
)

# Explicit test fixtures - no hidden factory logic
def create_test_warrior(name: str = "TestWarrior", level: int = 1) -> Character:
    """
    Create test warrior character.
    Explicit character creation for tests.
    """
    return Character(
        name=name,
        class_type=CharacterClass.WARRIOR,
        level=level,
        stats=CharacterStats(
            strength=15, dexterity=10, intelligence=8,
            wisdom=10, charisma=8, constitution=14
        ),
        hp=60, max_hp=60, gold=100,
        abilities=["Attack", "Defend", "Power Strike"],
        inventory=[], equipped_items={},
        experience=0, quests_active=[], quests_completed=[],
        reputation={}
    )

def create_test_mage(name: str = "TestMage", level: int = 1) -> Character:
    """
    Create test mage character.
    Explicit character creation for tests.
    """
    return Character(
        name=name,
        class_type=CharacterClass.MAGE,
        level=level,
        stats=CharacterStats(
            strength=8, dexterity=12, intelligence=16,
            wisdom=14, charisma=10, constitution=8
        ),
        hp=30, max_hp=30, gold=100,
        abilities=["Attack", "Defend", "Fireball"],
        inventory=[], equipped_items={},
        experience=0, quests_active=[], quests_completed=[],
        reputation={}
    )


# Direct function testing - no framework overhead

def test_create_character_warrior():
    """
    Test warrior character creation.
    Direct verification of function behavior.
    """
    # Execute function with explicit inputs
    character = create_character("TestWarrior", CharacterClass.WARRIOR)
    
    # Direct verification - single assertion per aspect
    assert character.name == "TestWarrior"
    assert character.class_type == CharacterClass.WARRIOR
    assert character.level == 1
    assert character.stats.strength == 15
    assert character.stats.dexterity == 10
    assert character.stats.intelligence == 8
    assert character.stats.wisdom == 10
    assert character.stats.charisma == 8
    assert character.stats.constitution == 14
    assert character.hp == 60  # 12 + (14-10)//2 = 12+2=14 * (1+1) = 60
    assert character.max_hp == 60
    assert character.gold == 100
    assert character.abilities == ["Attack", "Defend", "Power Strike", "Shield Bash", "Intimidate"]


def test_create_character_mage():
    """
    Test mage character creation.
    Direct verification of function behavior.
    """
    # Execute function with explicit inputs
    character = create_character("TestMage", CharacterClass.MAGE)
    
    # Direct verification
    assert character.name == "TestMage"
    assert character.class_type == CharacterClass.MAGE
    assert character.level == 1
    assert character.stats.strength == 8
    assert character.stats.dexterity == 12
    assert character.stats.intelligence == 16
    assert character.stats.wisdom == 14
    assert character.stats.charisma == 10
    assert character.stats.constitution == 8
    assert character.hp == 24  # 6 + (8-10)//2 = 6+0=6 * (1+3) = 24
    assert character.max_hp == 24
    assert character.gold == 100
    assert character.abilities == ["Attack", "Defend", "Fireball", "Magic Missile", "Teleport", "Mana Shield"]


def test_create_character_invalid_name():
    """
    Test character creation with invalid name.
    Direct error verification.
    """
    # Execute with invalid input
    with pytest.raises(ValueError, match="Character name cannot be empty"):
        create_character("", CharacterClass.WARRIOR)
    
    with pytest.raises(ValueError, match="Character name cannot exceed 50 characters"):
        create_character("x" * 51, CharacterClass.WARRIOR)
    
    with pytest.raises(ValueError, match="Character name can only contain"):
        create_character("Test@Warrior", CharacterClass.WARRIOR)


def test_get_default_stats_for_class():
    """
    Test getting default stats for class.
    Direct verification of deterministic behavior.
    """
    # Execute for warrior
    warrior_stats = get_default_stats_for_class(CharacterClass.WARRIOR)
    
    # Direct verification
    assert isinstance(warrior_stats, CharacterStats)
    assert warrior_stats.strength == 15
    assert warrior_stats.dexterity == 10
    assert warrior_stats.intelligence == 8
    assert warrior_stats.wisdom == 10
    assert warrior_stats.charisma == 8
    assert warrior_stats.constitution == 14
    
    # Execute for mage
    mage_stats = get_default_stats_for_class(CharacterClass.MAGE)
    
    # Direct verification
    assert isinstance(mage_stats, CharacterStats)
    assert mage_stats.strength == 8
    assert mage_stats.dexterity == 12
    assert mage_stats.intelligence == 16
    assert mage_stats.wisdom == 14
    assert mage_stats.charisma == 10
    assert mage_stats.constitution == 8


def test_calculate_max_hp():
    """
    Test max HP calculation.
    Direct verification of deterministic formula.
    """
    # Test warrior with constitution 14
    warrior_hp = calculate_max_hp(CharacterClass.WARRIOR, 14)
    assert warrior_hp == 14  # 12 + (14-10)//2 = 12+2=14
    
    # Test mage with constitution 8
    mage_hp = calculate_max_hp(CharacterClass.MAGE, 8)
    assert mage_hp == 6  # 6 + (8-10)//2 = 6+0=6
    
    # Test rogue with constitution 8
    rogue_hp = calculate_max_hp(CharacterClass.ROGUE, 8)
    assert rogue_hp == 8  # 8 + (8-10)//2 = 8+0=8
    
    # Test with minimum constitution
    min_hp = calculate_max_hp(CharacterClass.WARRIOR, 1)
    assert min_hp == 12  # 12 + (1-10)//2 = 12+0=12
    
    # Test with maximum constitution
    max_hp = calculate_max_hp(CharacterClass.WARRIOR, 20)
    assert max_hp == 17  # 12 + (20-10)//2 = 12+5=17


def test_get_default_abilities_for_class():
    """
    Test getting default abilities for class.
    Direct verification of deterministic behavior.
    """
    # Test warrior abilities
    warrior_abilities = get_default_abilities_for_class(CharacterClass.WARRIOR)
    
    # Direct verification
    assert isinstance(warrior_abilities, list)
    assert len(warrior_abilities) == 5
    assert "Attack" in warrior_abilities
    assert "Defend" in warrior_abilities
    assert "Power Strike" in warrior_abilities
    assert "Shield Bash" in warrior_abilities
    assert "Intimidate" in warrior_abilities
    
    # Test mage abilities
    mage_abilities = get_default_abilities_for_class(CharacterClass.MAGE)
    
    # Direct verification
    assert isinstance(mage_abilities, list)
    assert len(mage_abilities) == 6
    assert "Attack" in mage_abilities
    assert "Defend" in mage_abilities
    assert "Fireball" in mage_abilities
    assert "Magic Missile" in mage_abilities
    assert "Teleport" in mage_abilities
    assert "Mana Shield" in mage_abilities


def test_level_up_character():
    """
    Test character level up.
    Direct verification of state change.
    """
    # Setup explicit initial state
    character = create_test_warrior(level=1)
    initial_stats = character.stats.dict()
    
    # Execute level up
    leveled_character = level_up_character(character)
    
    # Direct verification of level increase
    assert leveled_character.level == 2
    
    # Direct verification of stat increases
    assert leveled_character.stats.strength == initial_stats['strength'] + 2  # +2 for warrior
    assert leveled_character.stats.dexterity == initial_stats['dexterity'] + 1  # +1 for warrior
    assert leveled_character.stats.intelligence == initial_stats['intelligence'] + 0  # +0 for warrior
    assert leveled_character.stats.wisdom == initial_stats['wisdom'] + 0  # +0 for warrior
    assert leveled_character.stats.charisma == initial_stats['charisma'] + 0  # +0 for warrior
    assert leveled_character.stats.constitution == initial_stats['constitution'] + 2  # +2 for warrior
    
    # Direct verification of HP increase
    expected_max_hp = calculate_max_hp(CharacterClass.WARRIOR, leveled_character.stats.constitution)
    assert leveled_character.max_hp == expected_max_hp
    hp_increase = expected_max_hp - character.max_hp
    assert leveled_character.hp == character.hp + hp_increase
    
    # Verify abilities unchanged (warrior learns new abilities at level 5+)
    assert leveled_character.abilities == character.abilities


def test_level_up_character_max_level():
    """
    Test level up at max level.
    Direct error verification.
    """
    # Setup character at max level
    character = create_test_warrior(level=100)
    
    # Execute level up at max level
    with pytest.raises(ValueError, match="already at maximum level"):
        level_up_character(character)


def test_get_stat_increases_for_class():
    """
    Test getting stat increases for class.
    Direct verification of deterministic behavior.
    """
    # Test warrior stat increases
    warrior_increases = get_stat_increases_for_class(CharacterClass.WARRIOR)
    
    # Direct verification
    assert isinstance(warrior_increases, CharacterStats)
    assert warrior_increases.strength == 2
    assert warrior_increases.dexterity == 1
    assert warrior_increases.intelligence == 0
    assert warrior_increases.wisdom == 0
    assert warrior_increases.charisma == 0
    assert warrior_increases.constitution == 2
    
    # Test mage stat increases
    mage_increases = get_stat_increases_for_class(CharacterClass.MAGE)
    
    # Direct verification
    assert isinstance(mage_increases, CharacterStats)
    assert mage_increases.strength == 0
    assert mage_increases.dexterity == 1
    assert mage_increases.intelligence == 2
    assert mage_increases.wisdom == 2
    assert mage_increases.charisma == 1
    assert mage_increases.constitution == 0


def test_get_abilities_for_level():
    """
    Test getting abilities for level.
    Direct verification of deterministic behavior.
    """
    # Test warrior abilities at level 1
    level_1_abilities = get_abilities_for_level(CharacterClass.WARRIOR, 1)
    assert level_1_abilities == []  # No new abilities at level 1
    
    # Test warrior abilities at level 5
    level_5_abilities = get_abilities_for_level(CharacterClass.WARRIOR, 5)
    assert "Whirlwind Attack" in level_5_abilities
    
    # Test warrior abilities at level 10
    level_10_abilities = get_abilities_for_level(CharacterClass.WARRIOR, 10)
    assert "Whirlwind Attack" in level_10_abilities
    assert "Battle Cry" in level_10_abilities
    
    # Test mage abilities at level 5
    level_5_abilities = get_abilities_for_level(CharacterClass.MAGE, 5)
    assert "Lightning Bolt" in level_5_abilities


def test_add_experience():
    """
    Test adding experience to character.
    Direct verification of state change.
    """
    # Setup explicit initial state
    character = create_test_warrior()
    initial_experience = character.experience
    initial_level = character.level
    
    # Execute experience addition (enough for level up)
    updated_character = add_experience(character, 100)  # Level 2 requires ~141, so no level up yet
    
    # Direct verification of experience addition
    assert updated_character.experience == initial_experience + 100
    assert updated_character.level == initial_level  # No level up yet
    
    # Execute experience addition for level up
    leveled_character = add_experience(updated_character, 50)  # Total 150, enough for level 2
    
    # Direct verification of level up
    assert leveled_character.level == initial_level + 1
    assert leveled_character.experience == 150


def test_get_experience_for_level():
    """
    Test getting experience required for level.
    Direct verification of deterministic formula.
    """
    # Test level 1
    level_1_xp = get_experience_for_level(1)
    assert level_1_xp == int(100 * (1 ** 1.5)) == 100
    
    # Test level 2
    level_2_xp = get_experience_for_level(2)
    assert level_2_xp == int(100 * (2 ** 1.5)) == 282
    
    # Test level 3
    level_3_xp = get_experience_for_level(3)
    assert level_3_xp == int(100 * (3 ** 1.5)) == 519
    
    # Test level 10
    level_10_xp = get_experience_for_level(10)
    assert level_10_xp == int(100 * (10 ** 1.5)) == 3162


def test_heal_character():
    """
    Test healing character.
    Direct verification of state change.
    """
    # Setup explicit initial state
    character = create_test_warrior()
    character.hp = 30  # Start with 30/60 HP
    initial_hp = character.hp
    
    # Execute healing
    healed_character = heal_character(character, 20)
    
    # Direct verification of healing
    assert healed_character.hp == initial_hp + 20  # 30 + 20 = 50
    
    # Test overheal prevention
    overhealed_character = heal_character(healed_character, 20)
    assert overhealed_character.hp == overhealed_character.max_hp  # Cap at max HP


def test_damage_character():
    """
    Test damaging character.
    Direct verification of state change.
    """
    # Setup explicit initial state
    character = create_test_warrior()
    initial_hp = character.hp
    
    # Execute damage
    damaged_character = damage_character(character, 20)
    
    # Direct verification of damage
    assert damaged_character.hp == initial_hp - 20  # 60 - 20 = 40
    
    # Test damage below zero prevention
    overdamaged_character = damage_character(damaged_character, 50)
    assert overdamaged_character.hp == 0  # Cap at zero


def test_is_character_defeated():
    """
    Test checking if character is defeated.
    Direct verification of condition.
    """
    # Test healthy character
    healthy_character = create_test_warrior()
    assert is_character_defeated(healthy_character) == False
    
    # Test damaged character
    damaged_character = create_test_warrior()
    damaged_character.hp = 1
    assert is_character_defeated(damaged_character) == False
    
    # Test defeated character
    defeated_character = create_test_warrior()
    defeated_character.hp = 0
    assert is_character_defeated(defeated_character) == True


def test_add_gold():
    """
    Test adding gold to character.
    Direct verification of state change.
    """
    # Setup explicit initial state
    character = create_test_warrior()
    initial_gold = character.gold
    
    # Execute gold addition
    rich_character = add_gold(character, 50)
    
    # Direct verification of gold addition
    assert rich_character.gold == initial_gold + 50


def test_remove_gold():
    """
    Test removing gold from character.
    Direct verification of state change and error handling.
    """
    # Setup explicit initial state
    character = create_test_warrior()
    initial_gold = character.gold
    
    # Execute gold removal
    poorer_character = remove_gold(character, 50)
    
    # Direct verification of gold removal
    assert poorer_character.gold == initial_gold - 50
    
    # Test insufficient gold error
    with pytest.raises(ValueError, match="Insufficient gold"):
        remove_gold(poorer_character, 200)  # Only 50 gold left


# Error case testing - explicit verification
def test_create_character_invalid_class():
    """
    Test character creation with invalid class.
    Direct error verification.
    """
    # Execute with invalid class type
    with pytest.raises(ValueError):
        create_character("Test", "invalid_class")


def test_calculate_max_hp_invalid_values():
    """
    Test max HP calculation with invalid values.
    Direct error verification.
    """
    # Test invalid constitution
    with pytest.raises(ValueError, match="Constitution must be between 1 and 20"):
        calculate_max_hp(CharacterClass.WARRIOR, 0)
    
    with pytest.raises(ValueError, match="Constitution must be between 1 and 20"):
        calculate_max_hp(CharacterClass.WARRIOR, 21)


def test_add_experience_invalid_amount():
    """
    Test adding invalid experience amount.
    Direct error verification.
    """
    character = create_test_warrior()
    
    # Test negative experience
    with pytest.raises(ValueError, match="Experience cannot be negative"):
        add_experience(character, -10)


def test_heal_character_invalid_amount():
    """
    Test healing with invalid amount.
    Direct error verification.
    """
    character = create_test_warrior()
    
    # Test negative healing
    with pytest.raises(ValueError, match="Healing amount cannot be negative"):
        heal_character(character, -10)


def test_damage_character_invalid_amount():
    """
    Test damaging with invalid amount.
    Direct error verification.
    """
    character = create_test_warrior()
    
    # Test negative damage
    with pytest.raises(ValueError, match="Damage amount cannot be negative"):
        damage_character(character, -10)


def test_add_gold_invalid_amount():
    """
    Test adding invalid gold amount.
    Direct error verification.
    """
    character = create_test_warrior()
    
    # Test negative gold
    with pytest.raises(ValueError, match="Gold amount cannot be negative"):
        add_gold(character, -10)


def test_remove_gold_invalid_amount():
    """
    Test removing invalid gold amount.
    Direct error verification.
    """
    character = create_test_warrior()
    
    # Test negative gold removal
    with pytest.raises(ValueError, match="Gold amount cannot be negative"):
        remove_gold(character, -10)


# Integration behavior testing - explicit scenario verification
def test_character_progression_workflow():
    """
    Test complete character progression workflow.
    Direct integration verification.
    """
    # Create new character
    character = create_character("TestHero", CharacterClass.WARRIOR)
    
    # Add experience and level up
    character = add_experience(character, 282)  # Enough for level 2
    character = level_up_character(character)
    
    # Verify progression
    assert character.level == 2
    assert character.stats.strength == 17  # 15 + 2
    assert character.stats.dexterity == 11  # 10 + 1
    assert character.stats.constitution == 16  # 14 + 2
    assert character.hp > 60  # Should have increased HP
    
    # Test combat readiness
    character = damage_character(character, 30)
    assert is_character_defeated(character) == False
    
    character = heal_character(character, 50)
    assert character.hp == character.max_hp
    
    # Test wealth management
    character = add_gold(character, 100)
    assert character.gold == 200
    
    character = remove_gold(character, 50)
    assert character.gold == 150


def test_character_stat_bounds():
    """
    Test character stat bounds enforcement.
    Direct verification of constraints.
    """
    # Create character and level up to max stats
    character = create_character("Test", CharacterClass.WARRIOR)
    
    # Level up multiple times to test stat bounds
    for _ in range(10):
        character = level_up_character(character)
    
    # Verify stats don't exceed maximum (20)
    assert character.stats.strength <= 20
    assert character.stats.dexterity <= 20
    assert character.stats.intelligence <= 20
    assert character.stats.wisdom <= 20
    assert character.stats.charisma <= 20
    assert character.stats.constitution <= 20


def test_character_ability_progression():
    """
    Test character ability acquisition progression.
    Direct verification of ability learning.
    """
    # Create warrior character
    character = create_character("TestWarrior", CharacterClass.WARRIOR)
    initial_abilities = character.abilities.copy()
    
    # Level up to ability acquisition levels
    for level in range(1, 30):
        if level % 5 == 0:  # Abilities learned every 5 levels
            new_abilities = get_abilities_for_level(CharacterClass.WARRIOR, level)
            character = level_up_character(character)
            
            # Verify new abilities learned
            for ability in new_abilities:
                if ability not in initial_abilities:
                    assert ability in character.abilities
    
    # Verify ability progression
    assert len(character.abilities) > len(initial_abilities)


# Performance testing - explicit performance verification
def test_character_creation_performance():
    """
    Test character creation performance.
    Direct performance verification.
    """
    import time
    
    # Measure creation time for multiple characters
    start_time = time.time()
    
    for i in range(100):
        character = create_character(f"Character{i}", CharacterClass.WARRIOR)
        validate_character(character)  # Verify character is valid
    
    end_time = time.time()
    creation_time = end_time - start_time
    
    # Direct performance verification
    assert creation_time < 1.0  # Should create 100 characters in under 1 second
    assert creation_time < 0.5  # Ideally under 0.5 seconds


def test_character_system_memory_usage():
    """
    Test character system memory usage.
    Direct memory usage verification.
    """
    import sys
    
    # Create many characters
    characters = []
    for i in range(1000):
        character = create_character(f"Character{i}", CharacterClass.WARRIOR)
        characters.append(character)
    
    # Measure memory usage
    total_size = sum(sys.getsizeof(char) for char in characters)
    
    # Direct memory usage verification
    assert total_size < 50 * 1024 * 1024  # Should be under 50MB for 1000 characters
    assert len(characters) == 1000  # Verify all characters created


# Test data validation - explicit validation verification
def test_character_data_validation():
    """
    Test character data validation.
    Direct validation verification.
    """
    # Test valid character data
    valid_character = create_character("Valid", CharacterClass.WARRIOR)
    assert validate_character(valid_character) == True
    
    # Test invalid character data
    invalid_character = create_character("Invalid", CharacterClass.WARRIOR)
    invalid_character.hp = -1  # Invalid HP
    try:
        validate_character(invalid_character)
        assert False, "Should have raised ValueError for invalid HP"
    except ValueError:
        pass  # Expected error


def test_character_stats_validation():
    """
    Test character stats validation.
    Direct validation verification.
    """
    # Test valid stats
    valid_stats = {
        'strength': 10, 'dexterity': 10, 'intelligence': 10,
        'wisdom': 10, 'charisma': 10, 'constitution': 10
    }
    assert validate_stats(valid_stats) == True
    
    # Test invalid stats
    invalid_stats = {
        'strength': 25, 'dexterity': 10, 'intelligence': 10,  # Strength too high
        'wisdom': 10, 'charisma': 10, 'constitution': 10
    }
    try:
        validate_stats(invalid_stats)
        assert False, "Should have raised ValueError for invalid stats"
    except ValueError:
        pass  # Expected error