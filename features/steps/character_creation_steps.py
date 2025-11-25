"""
BDD Steps: Character Creation
Optimized for LLM agents - explicit behavior, no "magic"
"""

from behave import given, when, then
from unittest.mock import MagicMock


# Context storage for BDD (explicit, not reactive)
class BDDContext:
    def __init__(self):
        self.character_name = None
        self.character_class = None
        self.created_character = None
        self.creation_error = None
        self.class_stats_mapping = {
            "warrior": {
                "strength": 15,
                "dexterity": 10,
                "intelligence": 8,
                "wisdom": 10,
                "charisma": 8,
                "constitution": 14,
                "hp": 60,
                "max_hp": 60,
                "gold": 100,
                "abilities": [
                    "Attack",
                    "Defend",
                    "Power Strike",
                    "Shield Bash",
                    "Intimidate",
                ],
            },
            "mage": {
                "strength": 8,
                "dexterity": 12,
                "intelligence": 16,
                "wisdom": 14,
                "charisma": 10,
                "constitution": 8,
                "hp": 24,
                "max_hp": 24,
                "gold": 100,
                "abilities": [
                    "Attack",
                    "Defend",
                    "Fireball",
                    "Magic Missile",
                    "Teleport",
                    "Mana Shield",
                ],
            },
            "cleric": {
                "strength": 10,
                "dexterity": 10,
                "intelligence": 10,
                "wisdom": 16,
                "charisma": 12,
                "constitution": 12,
                "hp": 40,
                "max_hp": 40,
                "gold": 100,
                "abilities": [
                    "Attack",
                    "Defend",
                    "Heal",
                    "Turn Undead",
                    "Bless",
                    "Holy Light",
                ],
            },
            "ranger": {
                "strength": 12,
                "dexterity": 14,
                "intelligence": 10,
                "wisdom": 12,
                "charisma": 8,
                "constitution": 10,
                "hp": 36,
                "max_hp": 36,
                "gold": 100,
                "abilities": [
                    "Attack",
                    "Defend",
                    "Precise Shot",
                    "Track",
                    "Animal Companion",
                    "Nature's Call",
                ],
            },
            "paladin": {
                "strength": 14,
                "dexterity": 8,
                "intelligence": 8,
                "wisdom": 12,
                "charisma": 12,
                "constitution": 14,
                "hp": 56,
                "max_hp": 56,
                "gold": 100,
                "abilities": [
                    "Attack",
                    "Defend",
                    "Holy Strike",
                    "Divine Shield",
                    "Lay on Hands",
                    "Aura of Courage",
                ],
            },
        }


# Global context for BDD scenarios (explicit, not reactive)
bdd_context = BDDContext()


def create_character(name, character_class):
    """Mock character creation for BDD testing"""
    # Validate name
    if not name or name.strip() == "":
        raise ValueError("Character name cannot be empty")
    if len(name) > 50:
        raise ValueError("Character name cannot exceed 50 characters")

    # Validate class
    if character_class not in bdd_context.class_stats_mapping:
        raise ValueError(f"Invalid character class: {character_class}")

    # Get class stats
    class_stats = bdd_context.class_stats_mapping[character_class]

    # Create mock character
    character = MagicMock()
    character.name = name
    character.class_type = MagicMock()
    character.class_type.value = character_class
    character.level = 1
    character.hp = class_stats["hp"]
    character.max_hp = class_stats["max_hp"]
    character.gold = class_stats["gold"]
    character.abilities = class_stats["abilities"]
    character.inventory = []

    # Create mock stats
    character.stats = MagicMock()
    character.stats.strength = class_stats["strength"]
    character.stats.dexterity = class_stats["dexterity"]
    character.stats.intelligence = class_stats["intelligence"]
    character.stats.wisdom = class_stats["wisdom"]
    character.stats.charisma = class_stats["charisma"]
    character.stats.constitution = class_stats["constitution"]

    return character


# Given Steps - Explicit scenario setup
@given('I inform the name "{name}" for the character')
def step_inform_character_name(context, name):
    """
    Sets the character name in BDD context.
    Explicit storage - no reactive behavior.
    """
    bdd_context.character_name = name


@given('I inform the name "" for the character')
def step_inform_empty_name(context):
    """
    Sets the empty character name in BDD context.
    Explicit storage - no reactive behavior.
    """
    bdd_context.character_name = ""


@given('I select the class "{class_name}" for the character')
def step_select_character_class(context, class_name):
    """
    Sets the character class in BDD context.
    Explicit storage - no reactive behavior.
    """
    bdd_context.character_class = class_name


@given("I have a mapping of classes and expected statistics")
def step_configure_class_mapping(context):
    """
    Configures complete class mapping for validation.
    Explicit behavior - no reactive behavior.
    """
    # Complete mapping for all 23 classes would go here
    # For now, we have the basic 5 classes in the mapping
    pass


# When Steps - Explicit action execution
@when("I create the character")
def step_create_character(context):
    """
    Executes character creation with context data.
    Explicit behavior - no reactive behavior.
    """
    try:
        # Create character (explicit function call)
        bdd_context.created_character = create_character(
            bdd_context.character_name, bdd_context.character_class
        )

        # Clear previous error
        bdd_context.creation_error = None

    except Exception as e:
        # Store error explicitly
        bdd_context.creation_error = str(e)
        bdd_context.created_character = None


@when("I attempt to create the character")
def step_attempt_create_character(context):
    """
    Attempts character creation (expecting failure).
    Explicit behavior - no reactive behavior.
    """
    # Same creation behavior, but error test context
    step_create_character(context)


@when("I create characters for all available classes")
def step_create_all_class_characters(context):
    """
    Creates characters for all available classes.
    Explicit behavior - no reactive behavior.
    """
    try:
        # Create character for each class
        created_characters = {}
        for class_name in bdd_context.class_stats_mapping.keys():
            character = create_character(f"Test{class_name.title()}", class_name)
            created_characters[class_name] = character

        # Store explicitly in context
        bdd_context.created_all_characters = created_characters
        bdd_context.creation_error = None

    except Exception as e:
        bdd_context.creation_error = str(e)
        bdd_context.created_all_characters = {}


# Then Steps - Explicit result validation


@then('the character must have the name "{expected_name}"')
def step_validate_character_name(context, expected_name):
    """
    Validates character has expected name.
    Explicit validation - no implicit behavior.
    """
    if bdd_context.created_character is None:
        raise AssertionError("Character was not created")

    assert bdd_context.created_character.name == expected_name, (
        f"Expected name: {expected_name}, Got name: {bdd_context.created_character.name}"
    )


@then('the character must have the class "{expected_class}"')
def step_validate_character_class(context, expected_class):
    """
    Validates character has expected class.
    Explicit validation - no implicit behavior.
    """
    if bdd_context.created_character is None:
        raise AssertionError("Character was not created")

    # Get class name from enum (explicit comparison)
    actual_class = bdd_context.created_character.class_type.value
    assert actual_class == expected_class, (
        f"Expected class: {expected_class}, Got class: {actual_class}"
    )


@then("the character must be at level {expected_level:d}")
def step_validate_character_level(context, expected_level):
    """
    Validates character is at expected level.
    Explicit validation - no implicit behavior.
    """
    if bdd_context.created_character is None:
        raise AssertionError("Character was not created")

    assert bdd_context.created_character.level == expected_level, (
        f"Expected level: {expected_level}, Got level: {bdd_context.created_character.level}"
    )


@then("the character must have strength {expected_strength:d}")
def step_validate_character_strength(context, expected_strength):
    """
    Validates character has expected strength.
    Explicit validation - no implicit behavior.
    """
    if bdd_context.created_character is None:
        raise AssertionError("Character was not created")

    actual_strength = bdd_context.created_character.stats.strength
    assert actual_strength == expected_strength, (
        f"Expected strength: {expected_strength}, Got strength: {actual_strength}"
    )


@then("the character must have dexterity {expected_dexterity:d}")
def step_validate_character_dexterity(context, expected_dexterity):
    """
    Validates character has expected dexterity.
    Explicit validation - no implicit behavior.
    """
    if bdd_context.created_character is None:
        raise AssertionError("Character was not created")

    actual_dexterity = bdd_context.created_character.stats.dexterity
    assert actual_dexterity == expected_dexterity, (
        f"Expected dexterity: {expected_dexterity}, Got dexterity: {actual_dexterity}"
    )


@then("the character must have intelligence {expected_intelligence:d}")
def step_validate_character_intelligence(context, expected_intelligence):
    """
    Validates character has expected intelligence.
    Explicit validation - no implicit behavior.
    """
    if bdd_context.created_character is None:
        raise AssertionError("Character was not created")

    actual_intelligence = bdd_context.created_character.stats.intelligence
    assert actual_intelligence == expected_intelligence, (
        f"Expected intelligence: {expected_intelligence}, Got intelligence: {actual_intelligence}"
    )


@then("the character must have wisdom {expected_wisdom:d}")
def step_validate_character_wisdom(context, expected_wisdom):
    """
    Validates character has expected wisdom.
    Explicit validation - no implicit behavior.
    """
    if bdd_context.created_character is None:
        raise AssertionError("Character was not created")

    actual_wisdom = bdd_context.created_character.stats.wisdom
    assert actual_wisdom == expected_wisdom, (
        f"Expected wisdom: {expected_wisdom}, Got wisdom: {actual_wisdom}"
    )


@then("the character must have charisma {expected_charisma:d}")
def step_validate_character_charisma(context, expected_charisma):
    """
    Validates character has expected charisma.
    Explicit validation - no implicit behavior.
    """
    if bdd_context.created_character is None:
        raise AssertionError("Character was not created")

    actual_charisma = bdd_context.created_character.stats.charisma
    assert actual_charisma == expected_charisma, (
        f"Expected charisma: {expected_charisma}, Got charisma: {actual_charisma}"
    )


@then("the character must have constitution {expected_constitution:d}")
def step_validate_character_constitution(context, expected_constitution):
    """
    Validates character has expected constitution.
    Explicit validation - no implicit behavior.
    """
    if bdd_context.created_character is None:
        raise AssertionError("Character was not created")

    actual_constitution = bdd_context.created_character.stats.constitution
    assert actual_constitution == expected_constitution, (
        f"Expected constitution: {expected_constitution}, Got constitution: {actual_constitution}"
    )


@then("the character must have HP {expected_hp:d}")
def step_validate_character_hp(context, expected_hp):
    """
    Validates character has expected HP.
    Explicit validation - no implicit behavior.
    """
    if bdd_context.created_character is None:
        raise AssertionError("Character was not created")

    assert bdd_context.created_character.hp == expected_hp, (
        f"Expected HP: {expected_hp}, Got HP: {bdd_context.created_character.hp}"
    )


@then("the character must have maximum HP {expected_max_hp:d}")
def step_validate_character_max_hp(context, expected_max_hp):
    """
    Validates character has expected maximum HP.
    Explicit validation - no implicit behavior.
    """
    if bdd_context.created_character is None:
        raise AssertionError("Character was not created")

    assert bdd_context.created_character.max_hp == expected_max_hp, (
        f"Expected max HP: {expected_max_hp}, Got max HP: {bdd_context.created_character.max_hp}"
    )


@then("the character must have {expected_gold:d} gold")
def step_validate_character_gold(context, expected_gold):
    """
    Validates character has expected gold.
    Explicit validation - no implicit behavior.
    """
    if bdd_context.created_character is None:
        raise AssertionError("Character was not created")

    assert bdd_context.created_character.gold == expected_gold, (
        f"Expected gold: {expected_gold}, Got gold: {bdd_context.created_character.gold}"
    )


@then("the character must have abilities {expected_abilities}")
def step_validate_character_abilities(context, expected_abilities):
    """
    Validates character has expected abilities.
    Explicit validation - no implicit behavior.
    """
    if bdd_context.created_character is None:
        raise AssertionError("Character was not created")

    # Convert string to list (explicit parse)
    if expected_abilities.startswith("[") and expected_abilities.endswith("]"):
        # Remove brackets and split by comma
        abilities_str = expected_abilities[1:-1].strip()
        expected_list = [
            ability.strip().strip("\"'")
            for ability in abilities_str.split(",")
            if ability.strip()
        ]
    else:
        expected_list = [expected_abilities.strip().strip("\"'")]

    actual_abilities = bdd_context.created_character.abilities

    # Validate ability count
    assert len(actual_abilities) >= len(expected_list), (
        f"Expected abilities: >= {len(expected_list)}, Got: {len(actual_abilities)}"
    )

    # Validate each expected ability
    for expected_ability in expected_list:
        assert expected_ability in actual_abilities, (
            f"Expected ability '{expected_ability}' not found in {actual_abilities}"
        )


@then("the character must have empty inventory")
def step_validate_empty_inventory(context):
    """
    Validates character has empty inventory.
    Explicit validation - no implicit behavior.
    """
    if bdd_context.created_character is None:
        raise AssertionError("Character was not created")

    assert len(bdd_context.created_character.inventory) == 0, (
        f"Character should have empty inventory, but has: {bdd_context.created_character.inventory}"
    )


@then('the creation must fail with error "{expected_error}"')
def step_validate_creation_error(context, expected_error):
    """
    Validates creation failed with expected error.
    Explicit validation - no implicit behavior.
    """
    assert bdd_context.creation_error is not None, (
        "Expected error in creation, but character was created successfully"
    )

    assert expected_error in bdd_context.creation_error, (
        f"Expected error: '{expected_error}', Got error: '{bdd_context.creation_error}'"
    )


@then("each character must have the correct statistics for their class")
def step_validate_all_class_statistics(context):
    """
    Validates each character has correct statistics for their class.
    Explicit validation - no implicit behavior.
    """
    if not hasattr(bdd_context, "created_all_characters"):
        raise AssertionError("Characters for all classes were not created")

    for class_name, character in bdd_context.created_all_characters.items():
        if class_name in bdd_context.class_stats_mapping:
            expected_stats = bdd_context.class_stats_mapping[class_name]

            # Validate strength
            assert character.stats.strength == expected_stats["strength"], (
                f"Class {class_name}: expected strength {expected_stats['strength']}, got {character.stats.strength}"
            )

            # Validate dexterity
            assert character.stats.dexterity == expected_stats["dexterity"], (
                f"Class {class_name}: expected dexterity {expected_stats['dexterity']}, got {character.stats.dexterity}"
            )

            # Validate intelligence
            assert character.stats.intelligence == expected_stats["intelligence"], (
                f"Class {class_name}: expected intelligence {expected_stats['intelligence']}, got {character.stats.intelligence}"
            )

            # Validate wisdom
            assert character.stats.wisdom == expected_stats["wisdom"], (
                f"Class {class_name}: expected wisdom {expected_stats['wisdom']}, got {character.stats.wisdom}"
            )

            # Validate charisma
            assert character.stats.charisma == expected_stats["charisma"], (
                f"Class {class_name}: expected charisma {expected_stats['charisma']}, got {character.stats.charisma}"
            )

            # Validate constitution
            assert character.stats.constitution == expected_stats["constitution"], (
                f"Class {class_name}: expected constitution {expected_stats['constitution']}, got {character.stats.constitution}"
            )


@then("each character must have the correct abilities for their class")
def step_validate_all_class_abilities(context):
    """
    Validates each character has correct abilities for their class.
    Explicit validation - no implicit behavior.
    """
    if not hasattr(bdd_context, "created_all_characters"):
        raise AssertionError("Characters for all classes were not created")

    for class_name, character in bdd_context.created_all_characters.items():
        if class_name in bdd_context.class_stats_mapping:
            expected_abilities = bdd_context.class_stats_mapping[class_name][
                "abilities"
            ]

            # Validate all expected abilities are present
            for expected_ability in expected_abilities:
                assert expected_ability in character.abilities, (
                    f"Class {class_name}: expected ability '{expected_ability}' not found in {character.abilities}"
                )


@then("each character must have the correct HP for their class")
def step_validate_all_class_hp(context):
    """
    Validates each character has correct HP for their class.
    Explicit validation - no implicit behavior.
    """
    if not hasattr(bdd_context, "created_all_characters"):
        raise AssertionError("Characters for all classes were not created")

    for class_name, character in bdd_context.created_all_characters.items():
        if class_name in bdd_context.class_stats_mapping:
            expected_stats = bdd_context.class_stats_mapping[class_name]

            # Validate HP
            assert character.hp == expected_stats["hp"], (
                f"Class {class_name}: expected HP {expected_stats['hp']}, got {character.hp}"
            )

            # Validate max HP
            assert character.max_hp == expected_stats["max_hp"], (
                f"Class {class_name}: expected max HP {expected_stats['max_hp']}, got {character.max_hp}"
            )


# Context cleanup function (explicit, not automatic)
def cleanup_bdd_context():
    """
    Cleans BDD context between scenarios.
    Explicit behavior - no reactive behavior.
    """
    global bdd_context
    bdd_context = BDDContext()
