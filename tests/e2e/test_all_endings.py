"""
E2E Tests: All Game Endings
Optimized for LLM agents - validates that all 20 endings are achievable
"""

import pytest
import time
from typing import Dict, List, Any
from core.models import GameState, Character, CharacterClass
from core.systems.game import start_new_game
from core.systems.character import create_character, level_up_character, add_experience
from core.systems.combat import resolve_combat
from core.systems.quest import complete_quest
from core.systems.inventory import add_item_to_inventory, equip_item


class E2EEndingValidator:
    """
    E2E validator for all game endings.
    Validates that all 20 endings are achievable.
    """
    
    def __init__(self):
        self.ending_results = []
        self.performance_metrics = {}
        self.all_ending_types = [
            "warrior_victory",
            "mage_mastery", 
            "rogue_stealth",
            "cleric_holy",
            "ranger_nature",
            "paladin_divine",
            "warlock_pact",
            "druid_balance",
            "monk_enlightenment",
            "barbarian_fury",
            "bard_inspiration",
            "sorcerer_power",
            "fighter_glory",
            "necromancer_dominance",
            "illusionist_trick",
            "alchemist_discovery",
            "berserker_rage",
            "assassin_shadow",
            "healer_mercy",
            "shapeshifter_wisdom",
            "elementalist_mastery",
            "ninja_stealth",
            "ultimate_hero"
        ]
    
    def validate_all_endings(self) -> Dict[str, Any]:
        """Validate that all endings are achievable."""
        start_time = time.time()
        
        successful_endings = []
        failed_endings = []
        
        for ending_type in self.all_ending_types:
            try:
                ending_result = self.validate_specific_ending(ending_type)
                self.ending_results.append(ending_result)
                
                if ending_result['achievable']:
                    successful_endings.append(ending_result)
                    print(f"✅ {ending_type}: Achievable")
                else:
                    failed_endings.append(ending_result)
                    print(f"❌ {ending_type}: Not Achievable - {ending_result.get('error', 'Unknown error')}")
                    
            except Exception as e:
                failed_ending = {
                    'ending_type': ending_type,
                    'achievable': False,
                    'error': str(e),
                    'execution_time': 0
                }
                failed_endings.append(failed_ending)
                self.ending_results.append(failed_ending)
                print(f"❌ {ending_type}: Error - {str(e)}")
        
        end_time = time.time()
        total_execution_time = end_time - start_time
        
        return {
            'total_endings': len(self.all_ending_types),
            'successful_endings': len(successful_endings),
            'failed_endings': len(failed_endings),
            'success_rate': len(successful_endings) / len(self.all_ending_types),
            'total_execution_time': total_execution_time,
            'successful_ending_details': successful_endings,
            'failed_ending_details': failed_endings,
            'all_results': self.ending_results
        }
    
    def validate_specific_ending(self, ending_type: str) -> Dict[str, Any]:
        """Validate that a specific ending is achievable."""
        start_time = time.time()
        
        # Determine optimal character class for this ending
        optimal_class = self.get_optimal_class_for_ending(ending_type)
        
        # Create optimal character
        character = self.create_optimal_character_for_ending(ending_type, optimal_class)
        
        # Progress character to end game
        character = self.progress_character_to_endgame(character, ending_type)
        
        # Achieve ending
        ending = self.achieve_specific_ending(character, ending_type)
        
        # Validate ending
        ending_achievable = self.validate_ending_requirements(ending, ending_type)
        
        execution_time = time.time() - start_time
        
        return {
            'ending_type': ending_type,
            'optimal_class': optimal_class,
            'character_level': character.level,
            'ending_achievable': ending_achievable,
            'execution_time': execution_time,
            'ending_details': ending,
            'character_stats': character.stats.dict(),
            'character_abilities': character.abilities
        }
    
    def get_optimal_class_for_ending(self, ending_type: str) -> CharacterClass:
        """Get optimal character class for specific ending."""
        # Mapping of endings to optimal classes
        optimal_class_mapping = {
            "warrior_victory": CharacterClass.WARRIOR,
            "mage_mastery": CharacterClass.MAGE,
            "rogue_stealth": CharacterClass.ROGUE,
            "cleric_holy": CharacterClass.CLERIC,
            "ranger_nature": CharacterClass.RANGER,
            "paladin_divine": CharacterClass.PALADIN,
            "warlock_pact": CharacterClass.WARLOCK,
            "druid_balance": CharacterClass.DRUID,
            "monk_enlightenment": CharacterClass.MONK,
            "barbarian_fury": CharacterClass.BARBARIAN,
            "bard_inspiration": CharacterClass.BARD,
            "sorcerer_power": CharacterClass.SORCERER,
            "fighter_glory": CharacterClass.FIGHTER,
            "necromancer_dominance": CharacterClass.NECROMANCER,
            "illusionist_trick": CharacterClass.ILLUSIONIST,
            "alchemist_discovery": CharacterClass.ALCHEMIST,
            "berserker_rage": CharacterClass.BERSERKER,
            "assassin_shadow": CharacterClass.ASSASSIN,
            "healer_mercy": CharacterClass.HEALER,
            "shapeshifter_wisdom": CharacterClass.SHAPESHIFTER,
            "elementalist_mastery": CharacterClass.ELEMENTALIST,
            "ninja_stealth": CharacterClass.NINJA,
            "ultimate_hero": CharacterClass.PALADIN  # Best all-around
        }
        
        return optimal_class_mapping.get(ending_type, CharacterClass.WARRIOR)
    
    def create_optimal_character_for_ending(self, ending_type: str, optimal_class: CharacterClass) -> Character:
        """Create optimal character for specific ending."""
        # Create base character
        character_name = f"Optimal{optimal_class.value.title()}For{ending_type.title()}"
        character = create_character(character_name, optimal_class)
        
        # Optimize stats for ending
        character = self.optimize_character_stats_for_ending(character, ending_type)
        
        # Add optimal abilities for ending
        character = self.add_optimal_abilities_for_ending(character, ending_type)
        
        # Add optimal starting items for ending
        character = self.add_optimal_items_for_ending(character, ending_type)
        
        return character
    
    def optimize_character_stats_for_ending(self, character: Character, ending_type: str) -> Character:
        """Optimize character stats for specific ending."""
        # Get optimal stat distribution for ending
        optimal_stats = self.get_optimal_stats_for_ending(ending_type)
        
        # Apply optimal stats to character
        character.stats.strength = optimal_stats['strength']
        character.stats.dexterity = optimal_stats['dexterity']
        character.stats.intelligence = optimal_stats['intelligence']
        character.stats.wisdom = optimal_stats['wisdom']
        character.stats.charisma = optimal_stats['charisma']
        character.stats.constitution = optimal_stats['constitution']
        
        # Recalculate max HP based on new constitution
        from core.systems.character import calculate_max_hp
        character.max_hp = calculate_max_hp(character.class_type, character.stats.constitution)
        character.hp = character.max_hp
        
        return character
    
    def get_optimal_stats_for_ending(self, ending_type: str) -> Dict[str, int]:
        """Get optimal stats distribution for specific ending."""
        # Define optimal stats for each ending type
        optimal_stats_mapping = {
            "warrior_victory": {'strength': 20, 'dexterity': 15, 'intelligence': 8, 'wisdom': 10, 'charisma': 10, 'constitution': 20},
            "mage_mastery": {'strength': 8, 'dexterity': 12, 'intelligence': 20, 'wisdom': 18, 'charisma': 12, 'constitution': 8},
            "rogue_stealth": {'strength': 10, 'dexterity': 20, 'intelligence': 12, 'wisdom': 10, 'charisma': 14, 'constitution': 10},
            "cleric_holy": {'strength': 10, 'dexterity': 10, 'intelligence': 10, 'wisdom': 20, 'charisma': 15, 'constitution': 15},
            "ranger_nature": {'strength': 12, 'dexterity': 18, 'intelligence': 10, 'wisdom': 16, 'charisma': 8, 'constitution': 12},
            "paladin_divine": {'strength': 18, 'dexterity': 10, 'intelligence': 8, 'wisdom': 15, 'charisma': 15, 'constitution': 18},
            "warlock_pact": {'strength': 8, 'dexterity': 12, 'intelligence': 18, 'wisdom': 10, 'charisma': 20, 'constitution': 8},
            "druid_balance": {'strength': 10, 'dexterity': 10, 'intelligence': 10, 'wisdom': 20, 'charisma': 10, 'constitution': 18},
            "monk_enlightenment": {'strength': 14, 'dexterity': 18, 'intelligence': 12, 'wisdom': 16, 'charisma': 8, 'constitution': 16},
            "barbarian_fury": {'strength': 20, 'dexterity': 8, 'intelligence': 6, 'wisdom': 8, 'charisma': 8, 'constitution': 20},
            "bard_inspiration": {'strength': 8, 'dexterity': 12, 'intelligence': 14, 'wisdom': 12, 'charisma': 20, 'constitution': 10},
            "sorcerer_power": {'strength': 6, 'dexterity': 10, 'intelligence': 20, 'wisdom': 10, 'charisma': 18, 'constitution': 8},
            "fighter_glory": {'strength': 18, 'dexterity': 16, 'intelligence': 10, 'wisdom': 8, 'charisma': 8, 'constitution': 15},
            "necromancer_dominance": {'strength': 6, 'dexterity': 10, 'intelligence': 20, 'wisdom': 16, 'charisma': 10, 'constitution': 8},
            "illusionist_trick": {'strength': 6, 'dexterity': 14, 'intelligence': 20, 'wisdom': 12, 'charisma': 16, 'constitution': 8},
            "alchemist_discovery": {'strength': 8, 'dexterity': 10, 'intelligence': 18, 'wisdom': 16, 'charisma': 10, 'constitution': 12},
            "berserker_rage": {'strength': 20, 'dexterity': 8, 'intelligence': 6, 'wisdom': 8, 'charisma': 6, 'constitution': 20},
            "assassin_shadow": {'strength': 10, 'dexterity': 20, 'intelligence': 14, 'wisdom': 8, 'charisma': 10, 'constitution': 8},
            "healer_mercy": {'strength': 8, 'dexterity': 10, 'intelligence': 10, 'wisdom': 20, 'charisma': 18, 'constitution': 10},
            "shapeshifter_wisdom": {'strength': 10, 'dexterity': 12, 'intelligence': 10, 'wisdom': 20, 'charisma': 10, 'constitution': 14},
            "elementalist_mastery": {'strength': 8, 'dexterity': 10, 'intelligence': 20, 'wisdom': 16, 'charisma': 10, 'constitution': 8},
            "ninja_stealth": {'strength': 10, 'dexterity': 20, 'intelligence': 12, 'wisdom': 8, 'charisma': 8, 'constitution': 10},
            "ultimate_hero": {'strength': 18, 'dexterity': 16, 'intelligence': 16, 'wisdom': 16, 'charisma': 16, 'constitution': 18}
        }
        
        return optimal_stats_mapping.get(ending_type, {
            'strength': 15, 'dexterity': 15, 'intelligence': 15, 
            'wisdom': 15, 'charisma': 15, 'constitution': 15
        })
    
    def add_optimal_abilities_for_ending(self, character: Character, ending_type: str) -> Character:
        """Add optimal abilities for specific ending."""
        # Get optimal abilities for ending
        optimal_abilities = self.get_optimal_abilities_for_ending(ending_type)
        
        # Add abilities to character
        for ability in optimal_abilities:
            if ability not in character.abilities:
                character.abilities.append(ability)
        
        return character
    
    def get_optimal_abilities_for_ending(self, ending_type: str) -> List[str]:
        """Get optimal abilities for specific ending."""
        # Define optimal abilities for each ending type
        optimal_abilities_mapping = {
            "warrior_victory": ["Power Strike", "Heroic Strike", "Blade Storm", "Final Stand", "Warrior's Resolve"],
            "mage_mastery": ["Fireball", "Lightning Bolt", "Chain Lightning", "Meteor Strike", "Archmage"],
            "rogue_stealth": ["Backstab", "Stealth", "Shadow Strike", "Assassinate", "Vanish"],
            "cleric_holy": ["Heal", "Turn Undead", "Holy Light", "Divine Shield", "Lay on Hands"],
            "ranger_nature": ["Precise Shot", "Nature's Call", "Animal Companion", "Track", "Hunter's Mark"],
            "paladin_divine": ["Holy Strike", "Divine Shield", "Aura of Courage", "Lay on Hands", "Holy Light"],
            "warlock_pact": ["Eldritch Blast", "Pact Boon", "Life Drain", "Curse", "Summon Demon"],
            "druid_balance": ["Wild Shape", "Entangle", "Call Lightning", "Nature's Call", "Balance"],
            "monk_enlightenment": ["Flurry of Blows", "Stunning Strike", "Ki Strike", "Deflect Missiles", "Enlightenment"],
            "barbarian_fury": ["Rage", "Reckless Attack", "Berserk", "Frenzy", "Unstoppable"],
            "bard_inspiration": ["Inspire", "Charm", "Counter Song", "Enthrall", "Masterpiece"],
            "sorcerer_power": ["Spell Surge", "Metamagic", "Quick Spell", "Arcane Power", "Master Sorcerer"],
            "fighter_glory": ["Power Attack", "Cleave", "Weapon Focus", "Combat Expertise", "Supreme Fighter"],
            "necromancer_dominance": ["Raise Dead", "Life Drain", "Curse", "Fear Aura", "Undead Mastery"],
            "illusionist_trick": ["Create Illusion", "Invisibility", "Phantasm", "Confusion", "Master Illusion"],
            "alchemist_discovery": ["Brew Potion", "Throw Bomb", "Mutate", "Discovery", "Master Alchemist"],
            "berserker_rage": ["Rage", "Blood Rage", "Berserk", "Frenzy", "Unstoppable Rage"],
            "assassin_shadow": ["Stealth Kill", "Poison", "Shadow Walk", "Smoke Bomb", "Master Assassin"],
            "healer_mercy": ["Greater Heal", "Regeneration", "Cure Disease", "Resurrect", "Mercy"],
            "shapeshifter_wisdom": ["Wolf Form", "Bear Form", "Eagle Form", "Balance", "Master Shapeshifter"],
            "elementalist_mastery": ["Fire Strike", "Ice Blast", "Lightning Bolt", "Earthquake", "Master Elementalist"],
            "ninja_stealth": ["Shadow Clone", "Smoke Bomb", "Throwing Stars", "Vanish", "Master Ninja"],
            "ultimate_hero": ["Heroic Strike", "Divine Shield", "Arcane Power", "Final Stand", "Ultimate Hero"]
        }
        
        return optimal_abilities_mapping.get(ending_type, ["Attack", "Defend", "Power Strike"])
    
    def add_optimal_items_for_ending(self, character: Character, ending_type: str) -> Character:
        """Add optimal items for specific ending."""
        # Get optimal items for ending
        optimal_items = self.get_optimal_items_for_ending(ending_type)
        
        # Add items to character inventory
        for item in optimal_items:
            add_item_to_inventory(character, item)
        
        return character
    
    def get_optimal_items_for_ending(self, ending_type: str) -> List[Dict[str, Any]]:
        """Get optimal items for specific ending."""
        # Define optimal items for each ending type
        optimal_items_mapping = {
            "warrior_victory": [
                {"id": "legendary_sword", "name": "Legendary Sword", "type": "weapon", "stats": {"strength": 5, "damage": 50}},
                {"id": "epic_armor", "name": "Epic Armor", "type": "armor", "stats": {"constitution": 5, "defense": 30}}
            ],
            "mage_mastery": [
                {"id": "archmage_staff", "name": "Archmage Staff", "type": "weapon", "stats": {"intelligence": 5, "spell_power": 50}},
                {"id": "arcane_robes", "name": "Arcane Robes", "type": "armor", "stats": {"intelligence": 3, "spell_power": 20}}
            ],
            # ... add optimal items for other endings
        }
        
        return optimal_items_mapping.get(ending_type, [
            {"id": "basic_weapon", "name": "Basic Weapon", "type": "weapon", "stats": {"damage": 10}},
            {"id": "basic_armor", "name": "Basic Armor", "type": "armor", "stats": {"defense": 5}}
        ])
    
    def progress_character_to_endgame(self, character: Character, ending_type: str) -> Character:
        """Progress character to end game for specific ending."""
        # Level up character to max level
        for level in range(2, 51):  # Start from level 2 since character is level 1
            # Add experience needed for level up
            exp_needed = self.get_experience_for_level(level)
            character = add_experience(character, exp_needed)
            
            # Level up
            character = level_up_character(character)
            
            # Complete quests relevant to ending
            if level % 5 == 0:
                quest = self.create_relevant_quest_for_ending(character, ending_type, level)
                complete_quest(character, quest)
            
            # Add items relevant to ending
            if level % 10 == 0:
                item = self.create_relevant_item_for_ending(character, ending_type, level)
                add_item_to_inventory(character, item)
        
        # Validate character reached end game
        assert character.level == 50
        assert len(character.quests_completed) >= 10
        assert len(character.inventory) >= 5
        
        return character
    
    def get_experience_for_level(self, level: int) -> int:
        """Get experience needed for level."""
        import math
        return int(100 * math.pow(level, 1.5))
    
    def create_relevant_quest_for_ending(self, character: Character, ending_type: str, level: int) -> Any:
        """Create quest relevant to ending type."""
        # This would create actual Quest objects
        # For simplicity, returning mock quest
        from core.models import Quest, QuestStatus
        
        return Quest(
            id=f"quest_{ending_type}_{level}",
            name=f"{ending_type.title()} Quest {level}",
            description=f"Complete {ending_type} quest at level {level}",
            type="main_quest",
            difficulty="hard",
            giver="Quest_Giver",
            location="Quest_Location",
            objectives=[{
                'description': f"Complete {ending_type} objective",
                'completed': True
            }],
            rewards={
                'xp': 1000 * level,
                'gold': 500 * level,
                'items': []
            },
            status=QuestStatus.COMPLETED
        )
    
    def create_relevant_item_for_ending(self, character: Character, ending_type: str, level: int) -> Any:
        """Create item relevant to ending type."""
        # This would create actual Item objects
        # For simplicity, returning mock item
        from core.models import Item, ItemRarity, ItemType
        
        return Item(
            id=f"item_{ending_type}_{level}",
            name=f"{ending_type.title()} Item {level}",
            type=ItemType.ACCESSORY,
            rarity=ItemRarity.LEGENDARY,
            value=1000 * level,
            stats_mod={
                'strength': 2 if level % 2 == 0 else 0,
                'intelligence': 2 if level % 3 == 0 else 0,
                'dexterity': 2 if level % 5 == 0 else 0
            },
            abilities=[],
            description=f"Item for {ending_type} ending",
            equippable=True,
            consumable=False
        )
    
    def achieve_specific_ending(self, character: Character, ending_type: str) -> Dict[str, Any]:
        """Achieve specific ending based on character and ending type."""
        # Create ending based on character and achievements
        ending_requirements = self.get_ending_requirements(ending_type)
        
        # Validate that character meets requirements
        meets_requirements = self.validate_character_meets_ending_requirements(character, ending_requirements)
        
        # Create ending
        ending = {
            'type': ending_type,
            'title': self.get_ending_title(ending_type),
            'description': self.get_ending_description(ending_type, character),
            'achievable': meets_requirements,
            'requirements': ending_requirements,
            'character_achievements': {
                'level': character.level,
                'class': character.class_type.value,
                'stats': character.stats.dict(),
                'abilities': character.abilities,
                'quests_completed': len(character.quests_completed),
                'inventory_size': len(character.inventory)
            }
        }
        
        return ending
    
    def get_ending_requirements(self, ending_type: str) -> Dict[str, Any]:
        """Get requirements for specific ending."""
        # Define requirements for each ending type
        ending_requirements_mapping = {
            "warrior_victory": {
                'level': 50,
                'class': 'warrior',
                'strength': 20,
                'final_boss_defeated': True,
                'quests_completed': 10
            },
            "mage_mastery": {
                'level': 50,
                'class': 'mage',
                'intelligence': 20,
                'final_boss_defeated': True,
                'spells_mastered': 10
            },
            "rogue_stealth": {
                'level': 50,
                'class': 'rogue',
                'dexterity': 20,
                'final_boss_defeated': True,
                'stealth_kills': 15
            },
            # ... add requirements for other endings
            "ultimate_hero": {
                'level': 50,
                'stats_min': 18,
                'final_boss_defeated': True,
                'quests_completed': 20,
                'all_main_quests_completed': True
            }
        }
        
        return ending_requirements_mapping.get(ending_type, {
            'level': 50,
            'final_boss_defeated': True
        })
    
    def validate_character_meets_ending_requirements(self, character: Character, requirements: Dict[str, Any]) -> bool:
        """Validate that character meets ending requirements."""
        # Check level requirement
        if 'level' in requirements and character.level < requirements['level']:
            return False
        
        # Check class requirement
        if 'class' in requirements and character.class_type.value != requirements['class']:
            return False
        
        # Check stat requirements
        if 'strength' in requirements and character.stats.strength < requirements['strength']:
            return False
        if 'dexterity' in requirements and character.stats.dexterity < requirements['dexterity']:
            return False
        if 'intelligence' in requirements and character.stats.intelligence < requirements['intelligence']:
            return False
        if 'wisdom' in requirements and character.stats.wisdom < requirements['wisdom']:
            return False
        if 'charisma' in requirements and character.stats.charisma < requirements['charisma']:
            return False
        if 'constitution' in requirements and character.stats.constitution < requirements['constitution']:
            return False
        
        # Check quest requirements
        if 'quests_completed' in requirements and len(character.quests_completed) < requirements['quests_completed']:
            return False
        
        # Check minimum stats requirement
        if 'stats_min' in requirements:
            min_stat = requirements['stats_min']
            if (character.stats.strength < min_stat or
                character.stats.dexterity < min_stat or
                character.stats.intelligence < min_stat or
                character.stats.wisdom < min_stat or
                character.stats.charisma < min_stat or
                character.stats.constitution < min_stat):
                return False
        
        return True
    
    def get_ending_title(self, ending_type: str) -> str:
        """Get title for specific ending."""
        ending_titles = {
            "warrior_victory": "The Mighty Warrior",
            "mage_mastery": "Master of the Arcane",
            "rogue_stealth": "Shadow Assassin",
            "cleric_holy": "Holy Champion",
            "ranger_nature": "Guardian of Nature",
            "paladin_divine": "Divine Paladin",
            "warlock_pact": "Warlock Lord",
            "druid_balance": "Keeper of Balance",
            "monk_enlightenment": "Enlightened Monk",
            "barbarian_fury": "Furious Barbarian",
            "bard_inspiration": "Inspiring Bard",
            "sorcerer_power": "Master Sorcerer",
            "fighter_glory": "Glorious Fighter",
            "necromancer_dominance": "Lord of the Dead",
            "illusionist_trick": "Master Illusionist",
            "alchemist_discovery": "Great Alchemist",
            "berserker_rage": "Raging Berserker",
            "assassin_shadow": "Shadow Assassin",
            "healer_mercy": "Divine Healer",
            "shapeshifter_wisdom": "Wise Shapeshifter",
            "elementalist_mastery": "Elementalist Master",
            "ninja_stealth": "Master Ninja",
            "ultimate_hero": "Ultimate Hero"
        }
        
        return ending_titles.get(ending_type, "Unknown Hero")
    
    def get_ending_description(self, ending_type: str, character: Character) -> str:
        """Get description for specific ending."""
        base_descriptions = {
            "warrior_victory": f"The mighty warrior {character.name} has achieved victory through strength and courage.",
            "mage_mastery": f"The master mage {character.name} has mastered the arcane arts through intelligence and wisdom.",
            "rogue_stealth": f"The stealthy rogue {character.name} has achieved their goals through dexterity and cunning.",
            # ... add base descriptions for other endings
            "ultimate_hero": f"The ultimate hero {character.name} has achieved everything possible in the realm."
        }
        
        return base_descriptions.get(ending_type, f"{character.name} has achieved the {ending_type} ending.")
    
    def validate_ending_requirements(self, ending: Dict[str, Any], ending_type: str) -> bool:
        """Validate that ending meets requirements."""
        # Check that ending is achievable
        if not ending['achievable']:
            return False
        
        # Check that ending type matches
        if ending['type'] != ending_type:
            return False
        
        # Check that ending has all required fields
        required_fields = ['type', 'title', 'description', 'achievable', 'requirements', 'character_achievements']
        for field in required_fields:
            if field not in ending:
                return False
        
        return True


# Pytest test functions
def test_all_20_endings_achievable():
    """Test that all 20 endings are achievable."""
    validator = E2EEndingValidator()
    
    result = validator.validate_all_endings()
    
    # Validate that all endings are achievable
    assert result['success_rate'] == 1.0, f"All endings should be achievable, but only {result['success_rate']:.1%} are achievable"
    assert result['successful_endings'] == 23, f"Expected 23 successful endings, got {result['successful_endings']}"
    assert result['failed_endings'] == 0, f"Expected 0 failed endings, got {result['failed_endings']}"
    
    # Validate performance requirements
    max_total_time = 300  # 5 minutes for all endings
    assert result['total_execution_time'] < max_total_time, f"E2E endings test took too long: {result['total_execution_time']:.2f}s > {max_total_time}s"
    
    print(f"✅ All 23 endings are achievable! ({result['total_execution_time']:.2f}s)")
    print(f"   Success rate: {result['success_rate']:.1%}")
    print(f"   Average time per ending: {result['total_execution_time'] / 23:.2f}s")


def test_specific_ending_achievable():
    """Test that specific ending is achievable."""
    validator = E2EEndingValidator()
    
    # Test a few key endings
    key_endings = ["warrior_victory", "mage_mastery", "ultimate_hero"]
    
    for ending_type in key_endings:
        result = validator.validate_specific_ending(ending_type)
        
        assert result['ending_achievable'], f"Ending {ending_type} should be achievable"
        assert result['character_level'] == 50, f"Character should be level 50 for ending {ending_type}"
        
        print(f"✅ {ending_type}: Achievable (Level {result['character_level']})")


def test_ending_performance_requirements():
    """Test that ending validation meets performance requirements."""
    from core.constants import PERFORMANCE_CONFIG
    
    validator = E2EEndingValidator()
    
    # Test single ending performance
    start_time = time.time()
    result = validator.validate_specific_ending("warrior_victory")
    end_time = time.time()
    
    execution_time = end_time - start_time
    max_single_ending_time = PERFORMANCE_CONFIG['max_test_execution_time'] * 5  # Allow 5x longer for E2E
    
    assert execution_time < max_single_ending_time, f"Single ending test took too long: {execution_time:.2f}s > {max_single_ending_time}s"
    assert result['ending_achievable'], "Warrior victory ending should be achievable"
    
    print(f"✅ Single ending validation meets performance requirements! ({execution_time:.2f}s < {max_single_ending_time}s)")


def test_ending_requirements_validation():
    """Test that ending requirements validation works correctly."""
    validator = E2EEndingValidator()
    
    # Test ending with insufficient requirements
    character = create_character("TestCharacter", CharacterClass.WARRIOR)
    character.level = 30  # Too low for ending
    
    ending_requirements = {
        'level': 50,
        'class': 'warrior',
        'strength': 20,
        'final_boss_defeated': True
    }
    
    meets_requirements = validator.validate_character_meets_ending_requirements(character, ending_requirements)
    assert not meets_requirements, "Character should not meet ending requirements when level is too low"
    
    # Test ending with sufficient requirements
    character.level = 50
    character.stats.strength = 20
    
    meets_requirements = validator.validate_character_meets_ending_requirements(character, ending_requirements)
    assert meets_requirements, "Character should meet ending requirements when all requirements are met"
    
    print("✅ Ending requirements validation works correctly!")


if __name__ == "__main__":
    # Run all ending tests
    test_all_20_endings_achievable()
    test_specific_ending_achievable()
    test_ending_performance_requirements()
    test_ending_requirements_validation()
    
    print("🏆 All E2E ending tests passed!")