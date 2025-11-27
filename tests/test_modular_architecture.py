"""
Modular System Tests for RPGSim
Tests for the new modular architecture
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
)
from core.engine import get_game_engine, reset_game_engine


class TestModularArchitecture:
    """Test the new modular architecture"""

    def setup_method(self):
        """Setup for each test method"""
        reset_game_engine()

    def test_engine_modular_creation(self):
        """Test that engine can be created in modular way"""
        engine = get_game_engine()
        assert engine is not None
        assert engine.game_state is None
        assert engine.is_running == False

    def test_modular_character_creation(self):
        """Test character creation through modular engine"""
        engine = get_game_engine()
        success = engine.start_new_game("ModularTest", "warrior")

        assert success == True
        assert engine.is_running == True
        assert engine.game_state is not None
        assert engine.game_state.player.name == "ModularTest"
        assert engine.game_state.player.class_type == CharacterClass.WARRIOR

    def test_modular_game_state_management(self):
        """Test game state management in modular architecture"""
        engine = get_game_engine()
        engine.start_new_game("StateTest", "mage")

        # Test time advancement
        initial_time = engine.game_state.world_time
        engine.advance_time(60)
        assert engine.game_state.world_time == initial_time + 60

        # Test travel
        success = engine.travel_to_location("forest")
        assert success == True
        assert engine.game_state.current_location == "forest"

        # Test save/load
        save_data = engine.save_game()
        assert save_data is not None
        assert "player" in save_data

        # Reset and load
        reset_game_engine()
        new_engine = get_game_engine()
        load_success = new_engine.load_game(save_data)
        assert load_success == True
        assert new_engine.game_state.player.name == "StateTest"

    def test_modular_character_stats(self):
        """Test character stats in modular system"""
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
        assert stats.get_total_stats() == 72

        # Test stat modifiers
        modifiers = stats.get_stat_modifiers()
        assert modifiers["strength"] == 2  # (15-10)//2
        assert modifiers["intelligence"] == -1  # (8-10)//2

    def test_modular_item_system(self):
        """Test item system integration"""
        item = Item(
            id="test_sword",
            name="Test Sword",
            type=ItemType.WEAPON,
            rarity=ItemRarity.COMMON,
            value=100,
            stats_mod={"attack": 10, "weight": 5},
            equippable=True,
            consumable=False,
            stackable=False,
        )

        assert item.name == "Test Sword"
        assert item.type == ItemType.WEAPON
        assert item.is_equipment() == True
        assert item.is_consumable() == False
        assert item.get_total_value() == 100

    def test_modular_character_with_items(self):
        """Test character with items in modular system"""
        engine = get_game_engine()
        engine.start_new_game("ItemTest", "rogue")

        character = engine.game_state.player

        # Test adding abilities
        success = character.add_ability("Stealth")
        assert success == True
        assert character.has_ability("Stealth") == True

        # Test adding items to inventory
        item = Item(
            id="test_potion",
            name="Health Potion",
            type=ItemType.CONSUMABLE,
            rarity=ItemRarity.COMMON,
            value=25,
            consumable=True,
            stackable=True,
            max_stack=10,
        )

        character.inventory.append(item)
        assert len(character.inventory) == 1
        assert character.inventory[0].name == "Health Potion"

    def test_modular_error_handling(self):
        """Test error handling in modular system"""
        engine = get_game_engine()

        # Test invalid character class
        success = engine.start_new_game("ErrorTest", "invalid_class")
        assert success == True  # Should fallback to warrior

        # Test negative time advancement
        engine.start_new_game("TimeTest", "cleric")
        success = engine.advance_time(-30)
        assert success == False

        # Test negative gold
        character = engine.game_state.player
        with pytest.raises(ValueError):
            character.add_gold(-10)

    def test_modular_system_integration(self):
        """Test integration between modular components"""
        engine = get_game_engine()
        engine.start_new_game("IntegrationTest", "paladin")

        character = engine.game_state.player

        # Test character progression
        initial_level = character.level
        initial_exp = character.experience

        gained_exp = character.add_experience(1000)
        assert gained_exp == 1000
        assert character.experience == initial_exp + 1000

        # Test HP management
        character.hp = 50
        healed = character.heal(30)
        assert healed == 30
        assert character.hp == 80

        # Test damage
        damage_taken = character.damage(20)
        assert damage_taken == 20
        assert character.hp == 60

        # Test gold management
        initial_gold = character.gold
        added_gold = character.add_gold(50)
        assert added_gold == 50
        assert character.gold == initial_gold + 50

        spent_gold = character.subtract_gold(25)
        assert spent_gold == 25
        assert character.gold == initial_gold + 25

    def test_modular_summary_functions(self):
        """Test summary functions in modular system"""
        engine = get_game_engine()
        engine.start_new_game("SummaryTest", "druid")

        # Test character summary
        character = engine.game_state.player
        summary = character.get_summary()

        assert "name" in summary
        assert "class" in summary
        assert "level" in summary
        assert "hp" in summary
        assert "gold" in summary
        assert summary["name"] == "SummaryTest"
        assert summary["class"] == "druid"

        # Test game state summary
        game_progress = engine.game_state.get_game_progress()
        assert "player" in game_progress
        assert "location" in game_progress
        assert "world_time" in game_progress
        assert "day" in game_progress


class TestModularSeparation:
    """Test that modules are properly separated"""

    def test_character_model_independence(self):
        """Test that character model is independent"""
        # Character should be creatable without engine
        stats = CharacterStats()
        character = Character(
            id=str(uuid.uuid4()),
            name="IndependentTest",
            class_type=CharacterClass.WARRIOR,
            level=1,
            experience=0,
            stats=stats,
            hp=100,
            max_hp=100,
            gold=0,
            abilities=[],
            inventory=[],
            quests_completed=[],
            skills={},
        )

        assert character.name == "IndependentTest"
        assert character.class_type == CharacterClass.WARRIOR

    def test_item_model_independence(self):
        """Test that item model is independent"""
        item = Item(
            id="independent_item",
            name="Independent Item",
            type=ItemType.ACCESSORY,
            rarity=ItemRarity.RARE,
            value=500,
            equippable=True,
        )

        assert item.name == "Independent Item"
        assert item.type == ItemType.ACCESSORY
        assert item.rarity == ItemRarity.RARE

    def test_game_state_independence(self):
        """Test that game state model is independent"""
        from core.models import GameState

        stats = CharacterStats()
        character = Character(
            id=str(uuid.uuid4()),
            name="StateTest",
            class_type=CharacterClass.MAGE,
            level=1,
            experience=0,
            stats=stats,
            hp=100,
            max_hp=100,
            gold=0,
            abilities=[],
            inventory=[],
            quests_completed=[],
            skills={},
        )

        game_state = GameState(
            current_location="test_location",
            player=character,
            world_time=1000,
            day=2,
            difficulty="hard",
        )

        assert game_state.current_location == "test_location"
        assert game_state.player == character
        assert game_state.difficulty == "hard"


class TestModularPerformance:
    """Test performance of modular system"""

    def test_multiple_character_creation(self):
        """Test creating multiple characters efficiently"""
        engine = get_game_engine()

        creation_times = []
        for i in range(10):
            import time

            start_time = time.time()

            success = engine.start_new_game(f"PerfTest{i}", "warrior")

            end_time = time.time()
            creation_times.append(end_time - start_time)

            assert success == True

            # Reset for next iteration
            reset_game_engine()

        # All creations should be fast (< 0.1 seconds each)
        avg_time = sum(creation_times) / len(creation_times)
        assert avg_time < 0.1, f"Average creation time {avg_time:.3f}s is too slow"

    def test_large_inventory_handling(self):
        """Test handling large inventories efficiently"""
        engine = get_game_engine()
        engine.start_new_game("InventoryTest", "rogue")

        character = engine.game_state.player

        # Add many items to inventory
        for i in range(100):
            item = Item(
                id=f"item_{i}",
                name=f"Item {i}",
                type=ItemType.CONSUMABLE,
                value=i,
                stackable=True,
            )
            character.inventory.append(item)

        assert len(character.inventory) == 100

        # Test summary performance
        import time

        start_time = time.time()

        summary = character.get_summary()

        end_time = time.time()
        summary_time = end_time - start_time

        assert summary["inventory_size"] == 100
        assert summary_time < 0.1, (
            f"Summary generation time {summary_time:.3f}s is too slow"
        )
