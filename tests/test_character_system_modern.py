"""
Unit Tests for Character System - Modern API
Updated to work with new modular architecture using core.models and core.engine
>90% coverage requirement for PROJECT.md quality gates
"""

import pytest
import uuid
from core.models import (
    Character,
    CharacterClass,
    CharacterStats,
    Item,
    ItemType,
    ItemRarity,
    GameState,
)
from core.engine import get_game_engine, reset_game_engine


class TestCharacterClass:
    """Test CharacterClass enum functionality."""

    def test_all_23_classes_available(self):
        """Test that all 23 required character classes are available."""
        # Count actual classes in enum
        actual_count = len(CharacterClass)

        # Should have 23 classes total
        assert actual_count == 23, f"Expected 23 classes, got {actual_count}"

        # Check specific important classes exist
        assert CharacterClass.WARRIOR in CharacterClass
        assert CharacterClass.MAGE in CharacterClass
        assert CharacterClass.ROGUE in CharacterClass

    def test_class_values_are_strings(self):
        """Test that all class values are proper strings."""
        for character_class in CharacterClass:
            assert isinstance(character_class.value, str)
            assert len(character_class.value.strip()) > 0

    def test_class_conversion(self):
        """Test class enum conversion works correctly."""
        assert str(CharacterClass.WARRIOR) == "warrior"
        assert CharacterClass("warrior") == CharacterClass.WARRIOR


class TestCharacterStats:
    """Test CharacterStats model functionality."""

    def test_default_stats_creation(self):
        """Test creating character stats with default values."""
        stats = CharacterStats()
        assert stats.strength == 10
        assert stats.dexterity == 10
        assert stats.intelligence == 10
        assert stats.wisdom == 10
        assert stats.charisma == 10
        assert stats.constitution == 10

    def test_custom_stats_creation(self):
        """Test creating character stats with custom values."""
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

    def test_stat_validation(self):
        """Test that stats are validated properly."""
        # Test valid range
        stats = CharacterStats(strength=1, dexterity=20)
        assert stats.strength == 1
        assert stats.dexterity == 20

        # Test invalid range
        with pytest.raises(ValueError):
            CharacterStats(strength=0)  # Too low

        with pytest.raises(ValueError):
            CharacterStats(strength=21)  # Too high

    def test_stat_modifiers(self):
        """Test stat modifier calculation."""
        stats = CharacterStats(strength=14)  # +2 modifier
        modifiers = stats.get_stat_modifiers()
        assert modifiers["strength"] == 2

        stats = CharacterStats(strength=8)  # -1 modifier
        modifiers = stats.get_stat_modifiers()
        assert modifiers["strength"] == -1

    def test_total_stats(self):
        """Test total stats calculation."""
        stats = CharacterStats(
            strength=10,
            dexterity=10,
            intelligence=10,
            wisdom=10,
            charisma=10,
            constitution=10,
        )
        assert stats.get_total_stats() == 60


class TestCharacterModel:
    """Test Character model functionality."""

    def test_character_creation(self):
        """Test creating a character with all required fields."""
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
            quests_completed=[],
            skills={},
        )

        assert character.name == "Test Character"
        assert character.class_type == CharacterClass.WARRIOR
        assert character.level == 1
        assert character.hp == 100
        assert character.max_hp == 100
        assert character.gold == 50

    def test_character_validation(self):
        """Test character model validation."""
        stats = CharacterStats()

        # Test empty name
        with pytest.raises(ValueError):
            Character(
                id=str(uuid.uuid4()),
                name="",
                class_type=CharacterClass.WARRIOR,
                level=1,
                experience=0,
                stats=stats,
                hp=100,
                max_hp=100,
                gold=50,
                abilities=[],
                inventory=[],
                quests_completed=[],
                skills={},
            )

        # Test HP exceeding max
        with pytest.raises(ValueError):
            Character(
                id=str(uuid.uuid4()),
                name="Test",
                class_type=CharacterClass.WARRIOR,
                level=1,
                experience=0,
                stats=stats,
                hp=150,
                max_hp=100,
                gold=50,
                abilities=[],
                inventory=[],
                quests_completed=[],
                skills={},
            )

    def test_character_hp_methods(self):
        """Test character HP manipulation methods."""
        stats = CharacterStats()
        character = Character(
            id=str(uuid.uuid4()),
            name="Test",
            class_type=CharacterClass.WARRIOR,
            level=1,
            experience=0,
            stats=stats,
            hp=100,
            max_hp=100,
            gold=50,
            abilities=[],
            inventory=[],
            quests_completed=[],
            skills={},
        )

        # Test healing
        healed = character.heal(20)
        assert healed == 0  # Already at max HP
        assert character.hp == 100

        # Test damage
        character.hp = 80
        damaged = character.damage(30)
        assert damaged == 30
        assert character.hp == 50

        # Test defeat
        damaged = character.damage(60)
        assert damaged == 50
        assert character.hp == 0
        assert character.is_defeated()
        assert not character.is_alive()

    def test_character_experience_methods(self):
        """Test character experience methods."""
        stats = CharacterStats()
        character = Character(
            id=str(uuid.uuid4()),
            name="Test",
            class_type=CharacterClass.WARRIOR,
            level=1,
            experience=0,
            stats=stats,
            hp=100,
            max_hp=100,
            gold=50,
            abilities=[],
            inventory=[],
            quests_completed=[],
            skills={},
        )

        # Test adding experience
        gained = character.add_experience(100)
        assert gained == 100
        assert character.experience == 100

        # Test negative experience
        with pytest.raises(ValueError):
            character.add_experience(-50)

    def test_character_gold_methods(self):
        """Test character gold methods."""
        stats = CharacterStats()
        character = Character(
            id=str(uuid.uuid4()),
            name="Test",
            class_type=CharacterClass.WARRIOR,
            level=1,
            experience=0,
            stats=stats,
            hp=100,
            max_hp=100,
            gold=50,
            abilities=[],
            inventory=[],
            quests_completed=[],
            skills={},
        )

        # Test adding gold
        gained = character.add_gold(25)
        assert gained == 25
        assert character.gold == 75

        # Test subtracting gold
        spent = character.subtract_gold(30)
        assert spent == 30
        assert character.gold == 45

        # Test insufficient gold
        with pytest.raises(ValueError):
            character.subtract_gold(100)

    def test_character_abilities(self):
        """Test character ability methods."""
        stats = CharacterStats()
        character = Character(
            id=str(uuid.uuid4()),
            name="Test",
            class_type=CharacterClass.WARRIOR,
            level=1,
            experience=0,
            stats=stats,
            hp=100,
            max_hp=100,
            gold=50,
            abilities=[],
            inventory=[],
            quests_completed=[],
            skills={},
        )

        # Test adding ability
        added = character.add_ability("Power Strike")
        assert added == True
        assert "Power Strike" in character.abilities
        assert character.has_ability("Power Strike")

        # Test duplicate ability
        added = character.add_ability("Power Strike")
        assert added == False
        assert len(character.abilities) == 1

    def test_character_summary(self):
        """Test character summary method."""
        stats = CharacterStats(strength=15, dexterity=12)
        character = Character(
            id=str(uuid.uuid4()),
            name="Test Character",
            class_type=CharacterClass.WARRIOR,
            level=5,
            experience=250,
            stats=stats,
            hp=80,
            max_hp=100,
            gold=150,
            abilities=["Power Strike"],
            inventory=["sword"],
            quests_completed=[],
            skills={},
        )

        summary = character.get_summary()
        assert summary["name"] == "Test Character"
        assert summary["class"] == "warrior"
        assert summary["level"] == 5
        assert summary["hp"] == "80/100"
        assert summary["hp_percentage"] == 80.0
        assert summary["gold"] == 150
        assert summary["abilities_count"] == 1
        assert summary["inventory_size"] == 1
        assert summary["is_alive"] == True


class TestGameEngine:
    """Test GameEngine functionality."""

    def setup_method(self):
        """Setup for each test method."""
        reset_game_engine()

    def test_game_engine_creation(self):
        """Test game engine creation."""
        engine = get_game_engine()
        assert engine is not None
        assert engine.game_state is None
        assert engine.is_running == False

    def test_start_new_game(self):
        """Test starting a new game."""
        engine = get_game_engine()
        success = engine.start_new_game("Aragorn", "warrior")

        assert success == True
        assert engine.is_running == True
        assert engine.game_state is not None
        assert engine.game_state.player.name == "Aragorn"
        assert engine.game_state.player.class_type == CharacterClass.WARRIOR

    def test_start_new_game_invalid_class(self):
        """Test starting new game with invalid class (should fallback to warrior)."""
        engine = get_game_engine()
        success = engine.start_new_game("Aragorn", "invalid_class")

        assert success == True
        assert engine.game_state.player.class_type == CharacterClass.WARRIOR

    def test_game_status(self):
        """Test getting game status."""
        engine = get_game_engine()

        # Test no game status
        status = engine.get_game_status()
        assert status["status"] == "no_game"

        # Test running game status
        engine.start_new_game("Test", "mage")
        status = engine.get_game_status()
        assert status["status"] == "running"
        assert "game_state" in status

    def test_advance_time(self):
        """Test advancing game time."""
        engine = get_game_engine()
        engine.start_new_game("Test", "rogue")

        success = engine.advance_time(60)
        assert success == True
        assert engine.game_state.world_time == 540  # 480 + 60

        # Test negative time
        success = engine.advance_time(-30)
        assert success == False

    def test_travel_to_location(self):
        """Test traveling to locations."""
        engine = get_game_engine()
        engine.start_new_game("Test", "cleric")

        success = engine.travel_to_location("forest")
        assert success == True
        assert engine.game_state.current_location == "forest"
        assert engine.game_state.world_time == 510  # 480 + 30

    def test_save_load_game(self):
        """Test saving and loading game."""
        engine = get_game_engine()
        engine.start_new_game("Test", "ranger")

        # Test save
        save_data = engine.save_game()
        assert save_data is not None
        assert "player" in save_data
        assert save_data["player"]["name"] == "Test"

        # Test load
        reset_game_engine()
        new_engine = get_game_engine()
        success = new_engine.load_game(save_data)
        assert success == True
        assert new_engine.game_state.player.name == "Test"

    def test_shutdown(self):
        """Test shutting down game engine."""
        engine = get_game_engine()
        engine.start_new_game("Test", "paladin")

        assert engine.is_running == True
        assert engine.game_state is not None

        engine.shutdown()

        assert engine.is_running == False
        assert engine.game_state is None


class TestGameState:
    """Test GameState model functionality."""

    def test_game_state_creation(self):
        """Test creating game state."""
        stats = CharacterStats()
        player = Character(
            id=str(uuid.uuid4()),
            name="Test",
            class_type=CharacterClass.WARRIOR,
            level=1,
            experience=0,
            stats=stats,
            hp=100,
            max_hp=100,
            gold=50,
            abilities=[],
            inventory=[],
            quests_completed=[],
            skills={},
        )

        game_state = GameState(
            current_location="town",
            player=player,
            world_time=600,
            day=2,
            difficulty="hard",
        )

        assert game_state.current_location == "town"
        assert game_state.player == player
        assert game_state.world_time == 600
        assert game_state.day == 2
        assert game_state.difficulty == "hard"

    def test_game_state_time_methods(self):
        """Test game state time methods."""
        game_state = GameState()

        # Test advance time
        game_state.advance_world_time(120)
        assert game_state.world_time == 120
        assert game_state.day == 1

        # Test day advancement
        game_state.advance_world_time(1400)  # Total 1520 minutes
        assert game_state.world_time == 1520
        assert game_state.day == 2  # Should advance to day 2

    def test_time_of_day(self):
        """Test time of day calculation."""
        game_state = GameState()

        # Test morning (6:00 AM - 12:00 PM)
        game_state.world_time = 420  # 7:00 AM
        assert game_state.get_time_of_day() == "morning"

        # Test afternoon (12:00 PM - 6:00 PM)
        game_state.world_time = 720  # 12:00 PM
        assert game_state.get_time_of_day() == "afternoon"

        # Test evening (6:00 PM - 9:00 PM)
        game_state.world_time = 1080  # 6:00 PM
        assert game_state.get_time_of_day() == "evening"

        # Test night (9:00 PM - 6:00 AM)
        game_state.world_time = 1320  # 10:00 PM
        assert game_state.get_time_of_day() == "night"

    def test_game_flags(self):
        """Test game flag functionality."""
        game_state = GameState()

        # Test adding flags
        game_state.add_flag("dragon_defeated", True)
        game_state.add_flag("current_quest", "find_sword")

        assert game_state.has_flag("dragon_defeated")
        assert game_state.get_flag("dragon_defeated") == True
        assert game_state.get_flag("current_quest") == "find_sword"
        assert game_state.get_flag("nonexistent") is None

    def test_game_progress(self):
        """Test game progress summary."""
        stats = CharacterStats()
        player = Character(
            id=str(uuid.uuid4()),
            name="Test",
            class_type=CharacterClass.WARRIOR,
            level=5,
            experience=500,
            stats=stats,
            hp=80,
            max_hp=100,
            gold=200,
            abilities=["slash"],
            inventory=["sword"],
            quests_completed=[],
            skills={},
        )

        game_state = GameState(
            current_location="dungeon",
            player=player,
            world_time=1000,
            day=3,
            difficulty="normal",
            quests_active=["quest1"],
            quests_completed=["quest0"],
        )

        progress = game_state.get_game_progress()
        assert progress["location"] == "dungeon"
        assert progress["world_time"] == 1000
        assert progress["day"] == 3
        assert progress["difficulty"] == "normal"
        assert progress["player_level"] == 5
        assert progress["player_experience"] == 500
        assert progress["player_gold"] == 200
        assert progress["quests_active"] == 1
        assert progress["quests_completed"] == 1


class TestCharacterWithItems:
    """Test character with items integration."""

    def test_character_with_inventory(self):
        """Test character with inventory items."""
        stats = CharacterStats()
        character = Character(
            id=str(uuid.uuid4()),
            name="Test",
            class_type=CharacterClass.ROGUE,
            level=1,
            experience=0,
            stats=stats,
            hp=100,
            max_hp=100,
            gold=50,
            abilities=[],
            inventory=[],
            quests_completed=[],
            skills={},
        )

        # Create test items
        sword = Item(
            id="sword_001",
            name="Iron Sword",
            type=ItemType.WEAPON,
            rarity=ItemRarity.COMMON,
            value=100,
            equippable=True,
            consumable=False,
            stackable=False,
        )

        potion = Item(
            id="potion_001",
            name="Health Potion",
            type=ItemType.CONSUMABLE,
            rarity=ItemRarity.COMMON,
            value=25,
            equippable=False,
            consumable=True,
            stackable=True,
            max_stack=10,
        )

        # Add items to inventory
        character.inventory.append(sword)
        character.inventory.append(potion)

        assert len(character.inventory) == 2
        assert character.inventory[0].name == "Iron Sword"
        assert character.inventory[1].name == "Health Potion"

    def test_character_equipment(self):
        """Test character equipment functionality."""
        stats = CharacterStats()
        character = Character(
            id=str(uuid.uuid4()),
            name="Test",
            class_type=CharacterClass.WARRIOR,
            level=1,
            experience=0,
            stats=stats,
            hp=100,
            max_hp=100,
            gold=50,
            abilities=[],
            inventory=[],
            quests_completed=[],
            skills={},
        )

        # Create equipment
        armor = Item(
            id="armor_001",
            name="Iron Armor",
            type=ItemType.ARMOR,
            rarity=ItemRarity.COMMON,
            value=200,
            equippable=True,
            consumable=False,
            stackable=False,
        )

        # Add to inventory
        character.inventory.append(armor)

        # Test equipment properties
        assert armor.is_equipment() == True
        assert armor.is_consumable() == False
        assert armor.get_total_value() == 200


class TestCharacterProgression:
    """Test character progression mechanics."""

    def test_character_leveling(self):
        """Test character leveling mechanics."""
        stats = CharacterStats()
        character = Character(
            id=str(uuid.uuid4()),
            name="Test",
            class_type=CharacterClass.MAGE,
            level=1,
            experience=0,
            stats=stats,
            hp=100,
            max_hp=100,
            gold=50,
            abilities=[],
            inventory=[],
            quests_completed=[],
            skills={},
        )

        # Test experience progression
        initial_level = character.level
        initial_exp = character.experience

        # Add significant experience
        character.add_experience(1000)

        assert character.experience > initial_exp
        # Note: Leveling logic would be implemented in progression system

    def test_character_abilities_progression(self):
        """Test ability progression."""
        stats = CharacterStats()
        character = Character(
            id=str(uuid.uuid4()),
            name="Test",
            class_type=CharacterClass.ROGUE,
            level=1,
            experience=0,
            stats=stats,
            hp=100,
            max_hp=100,
            gold=50,
            abilities=[],
            inventory=[],
            quests_completed=[],
            skills={},
        )

        # Test ability acquisition
        abilities = ["Stealth", "Lockpicking", "Backstab"]
        for ability in abilities:
            added = character.add_ability(ability)
            assert added == True

        assert len(character.abilities) == 3
        for ability in abilities:
            assert character.has_ability(ability) == True

    def test_character_gold_management(self):
        """Test gold management in character progression."""
        stats = CharacterStats()
        character = Character(
            id=str(uuid.uuid4()),
            name="Test",
            class_type=CharacterClass.CLERIC,
            level=1,
            experience=0,
            stats=stats,
            hp=100,
            max_hp=100,
            gold=100,
            abilities=[],
            inventory=[],
            quests_completed=[],
            skills={},
        )

        # Test gold operations
        initial_gold = character.gold

        # Add gold from quest
        quest_reward = character.add_gold(50)
        assert quest_reward == 50
        assert character.gold == initial_gold + 50

        # Spend gold on items
        item_cost = character.subtract_gold(30)
        assert item_cost == 30
        assert character.gold == initial_gold + 20

        # Test insufficient funds
        with pytest.raises(ValueError):
            character.subtract_gold(200)  # More than available


class TestCharacterClasses:
    """Test different character classes."""

    def test_warrior_characteristics(self):
        """Test warrior class characteristics."""
        stats = CharacterStats(
            strength=15,  # Warriors typically have high strength
            constitution=13,
            dexterity=10,
            intelligence=8,
            wisdom=10,
            charisma=10,
        )

        character = Character(
            id=str(uuid.uuid4()),
            name="Warrior",
            class_type=CharacterClass.WARRIOR,
            level=1,
            experience=0,
            stats=stats,
            hp=120,  # Warriors typically have more HP
            max_hp=120,
            gold=50,
            abilities=["Power Strike", "Shield Bash"],
            inventory=[],
            quests_completed=[],
            skills={},
        )

        assert character.class_type == CharacterClass.WARRIOR
        assert character.stats.strength == 15
        assert character.hp == 120

    def test_mage_characteristics(self):
        """Test mage class characteristics."""
        stats = CharacterStats(
            strength=8,
            constitution=10,
            dexterity=10,
            intelligence=15,  # Mages typically have high intelligence
            wisdom=13,
            charisma=10,
        )

        character = Character(
            id=str(uuid.uuid4()),
            name="Mage",
            class_type=CharacterClass.MAGE,
            level=1,
            experience=0,
            stats=stats,
            hp=80,  # Mages typically have less HP
            max_hp=80,
            gold=50,
            abilities=["Fireball", "Magic Missile"],
            inventory=[],
            quests_completed=[],
            skills={},
        )

        assert character.class_type == CharacterClass.MAGE
        assert character.stats.intelligence == 15
        assert character.hp == 80

    def test_rogue_characteristics(self):
        """Test rogue class characteristics."""
        stats = CharacterStats(
            strength=10,
            constitution=10,
            dexterity=15,  # Rogues typically have high dexterity
            intelligence=10,
            wisdom=10,
            charisma=12,
        )

        character = Character(
            id=str(uuid.uuid4()),
            name="Rogue",
            class_type=CharacterClass.ROGUE,
            level=1,
            experience=0,
            stats=stats,
            hp=90,
            max_hp=90,
            gold=50,
            abilities=["Stealth", "Backstab"],
            inventory=[],
            quests_completed=[],
            skills={},
        )

        assert character.class_type == CharacterClass.ROGUE
        assert character.stats.dexterity == 15
        assert character.hp == 90
