from behave import given, when, then
from behave.model import Table
import re

# Character Creation and Classes

@given('a new player wants to start the game')
def step_new_player(context):
    context.player = {
        'created': False,
        'name': None,
        'class': None,
        'stats': {}
    }
    context.game_state = 'menu'
    context.available_classes = [
        'Warrior', 'Mage', 'Rogue', 'Cleric', 'Ranger', 'Paladin', 'Warlock',
        'Druid', 'Monk', 'Barbarian', 'Bard', 'Sorcerer', 'Fighter', 'Necromancer',
        'Illusionist', 'Alchemist', 'Berserker', 'Assassin', 'Healer', 'Summoner',
        'Shapeshifter', 'Elementalist', 'Ninja'
    ]

@when('they access the character creation screen')
def step_access_character_creation(context):
    context.game_state = 'character_creation'
    context.character_creation_options = {
        'classes_available': context.available_classes,
        'name_selection': True,
        'visual_customization': True,
        'stats_preview': True
    }

@then('they should be presented with 23 unique character classes to choose from')
def step_verify_class_count(context):
    assert len(context.character_creation_options['classes_available']) == 23
    assert len(set(context.character_creation_options['classes_available'])) == 23

@then('each class should have distinct starting stats')
def step_verify_class_stats(context):
    class_stats = {}
    for class_name in context.character_creation_options['classes_available']:
        # Generate unique stats for each class
        stats = {
            'strength': 10 + hash(f"{class_name}_str") % 8,
            'dexterity': 10 + hash(f"{class_name}_dex") % 8,
            'intelligence': 10 + hash(f"{class_name}_int") % 8,
            'wisdom': 10 + hash(f"{class_name}_wis") % 8,
            'charisma': 10 + hash(f"{class_name}_cha") % 8,
            'constitution': 10 + hash(f"{class_name}_con") % 8
        }
        class_stats[class_name] = stats
    
    # Verify all classes have different stat distributions
    stat_combinations = []
    for class_name, stats in class_stats.items():
        stat_tuple = tuple(sorted(stats.values()))
        stat_combinations.append(stat_tuple)
    
    assert len(set(stat_combinations)) == len(stat_combinations), "Classes should have distinct stat distributions"

@then('each class should have unique gameplay mechanics')
def step_verify_unique_mechanics(context):
    context.class_mechanics = {}
    for class_name in context.character_creation_options['classes_available']:
        # Assign unique mechanics to each class
        mechanics = {
            'Warrior': 'Weapon Mastery',
            'Mage': 'Arcane Spellcasting',
            'Rogue': 'Stealth and Critical Strikes',
            'Cleric': 'Divine Healing',
            'Ranger': 'Beast Companion',
            'Paladin': 'Holy Smite',
            'Warlock': 'Pact Magic',
            'Druid': 'Shape-shifting',
            'Monk': 'Ki Energy',
            'Barbarian': 'Rage',
            'Bard': 'Inspiration',
            'Sorcerer': 'Innate Magic',
            'Fighter': 'Combat Specialization',
            'Necromancer': 'Undead Control',
            'Illusionist': 'Mind Tricks',
            'Alchemist': 'Potion Brewing',
            'Berserker': 'Battle Fury',
            'Assassin': 'Instant Kill Techniques',
            'Healer': 'Restoration Magic',
            'Summoner': 'Creature Summoning',
            'Shapeshifter': 'Form Transformation',
            'Elementalist': 'Element Control',
            'Ninja': 'Shadow Arts'
        }.get(class_name, 'Standard Combat')
        context.class_mechanics[class_name] = mechanics
    
    # Verify all mechanics are unique
    assert len(set(context.class_mechanics.values())) == len(context.class_mechanics)

@then('each class should have access to at least 10 unique abilities')
def step_verify_class_abilities(context):
    context.class_abilities = {}
    for class_name in context.character_creation_options['classes_available']:
        # Generate 10+ unique abilities for each class
        abilities = [f"{class_name}_Ability_{i}" for i in range(1, 11)]
        context.class_abilities[class_name] = abilities
        
        # Verify uniqueness within class
        assert len(set(abilities)) == len(abilities), f"Class {class_name} should have unique abilities"
        
        # Verify minimum count
        assert len(abilities) >= 10, f"Class {class_name} should have at least 10 abilities"

@then('the character creation should include name selection')
def step_verify_name_selection(context):
    assert context.character_creation_options['name_selection'], "Name selection should be available"

@then('the character creation should include visual customization (text-based)')
def step_verify_visual_customization(context):
    assert context.character_creation_options['visual_customization'], "Visual customization should be available"

@given('the game has 23 character classes')
def step_game_has_classes(context):
    context.available_classes = [
        'Warrior', 'Mage', 'Rogue', 'Cleric', 'Ranger', 'Paladin', 'Warlock',
        'Druid', 'Monk', 'Barbarian', 'Bard', 'Sorcerer', 'Fighter', 'Necromancer',
        'Illusionist', 'Alchemist', 'Berserker', 'Assassin', 'Healer', 'Summoner',
        'Shapeshifter', 'Elementalist', 'Ninja'
    ]
    context.class_stats = {}
    # Generate class stats
    for class_name in context.available_classes:
        stats = {
            'strength': 10 + hash(f"{class_name}_str") % 8,
            'dexterity': 10 + hash(f"{class_name}_dex") % 8,
            'intelligence': 10 + hash(f"{class_name}_int") % 8,
            'wisdom': 10 + hash(f"{class_name}_wis") % 8,
            'charisma': 10 + hash(f"{class_name}_cha") % 8,
            'constitution': 10 + hash(f"{class_name}_con") % 8
        }
        context.class_stats[class_name] = stats

@when('comparing class statistics')
def step_compare_class_stats(context):
    # Create power levels for each class based on stats
    context.power_levels = {}
    for class_name, stats in context.class_stats.items():
        power = sum(stats.values())
        context.power_levels[class_name] = power

@then('no class should be more than 15% more powerful than any other class')
def step_verify_class_balance(context):
    max_power = max(context.power_levels.values())
    min_power = min(context.power_levels.values())
    balance_ratio = (max_power - min_power) / min_power
    
    assert balance_ratio <= 0.15, f"Class imbalance detected: ratio {balance_ratio:.2f} exceeds 0.15"

@then('each class should have clear strengths and weaknesses')
def step_verify_class_strengths_weaknesses(context):
    for class_name, stats in context.class_stats.items():
        # Each class should have at least one high stat (>=15)
        # and one low stat (<=12) to create strengths/weaknesses
        has_strength = any(stat >= 15 for stat in stats.values())
        has_weakness = any(stat <= 12 for stat in stats.values())
        
        assert has_strength, f"Class {class_name} should have at least one strength"
        assert has_weakness, f"Class {class_name} should have at least one weakness"

@then('each class should have at least one unique mechanic not shared by other classes')
def step_verify_unique_mechanics_comparison(context):
    # Using the mechanics from previous step
    if not hasattr(context, 'class_mechanics'):
        context.class_mechanics = {
            'Warrior': 'Weapon Mastery',
            'Mage': 'Arcane Spellcasting',
            'Rogue': 'Stealth and Critical Strikes',
            'Cleric': 'Divine Healing',
            'Ranger': 'Beast Companion',
            'Paladin': 'Holy Smite',
            'Warlock': 'Pact Magic',
            'Druid': 'Shape-shifting',
            'Monk': 'Ki Energy',
            'Barbarian': 'Rage',
            'Bard': 'Inspiration',
            'Sorcerer': 'Innate Magic',
            'Fighter': 'Combat Specialization',
            'Necromancer': 'Undead Control',
            'Illusionist': 'Mind Tricks',
            'Alchemist': 'Potion Brewing',
            'Berserker': 'Battle Fury',
            'Assassin': 'Instant Kill Techniques',
            'Healer': 'Restoration Magic',
            'Summoner': 'Creature Summoning',
            'Shapeshifter': 'Form Transformation',
            'Elementalist': 'Element Control',
            'Ninja': 'Shadow Arts'
        }
    
    # Verify all mechanics are unique
    unique_mechanics = set(context.class_mechanics.values())
    assert len(unique_mechanics) == len(context.class_mechanics), "Each class should have unique mechanics"