"""
Inventory System Boundary and Edge Case Tests for RPGSim
Property-based testing using Hypothesis for inventory mechanics
TDD-focused: testing only what currently exists
"""

import pytest
from hypothesis import given, strategies as st, assume, settings
from hypothesis.strategies import (
    integers,
    text,
    lists,
    dictionaries,
    floats,
    booleans,
    sampled_from,
)
from typing import List, Dict, Any, Optional, Union
from pydantic import ValidationError

from core.models import Character, CharacterClass, CharacterStats


class TestInventoryBoundary:
    """Property-based tests for inventory system boundaries."""

    @given(
        gold_amount=integers(min_value=-1000, max_value=1000000),
        inventory_size=integers(min_value=0, max_value=1000),
    )
    def test_gold_and_inventory_boundaries(self, gold_amount, inventory_size):
        """Test gold and inventory size boundaries."""
        # Test invalid gold amounts
        if gold_amount < 0:
            with pytest.raises(ValidationError):
                character = Character(
                    id="test",
                    name="TestChar",
                    class_type=CharacterClass.WARRIOR,
                    level=1,
                    experience=0,
                    stats=CharacterStats(
                        strength=10,
                        dexterity=10,
                        intelligence=10,
                        wisdom=10,
                        charisma=10,
                        constitution=10,
                    ),
                    hp=100,
                    max_hp=100,
                    gold=gold_amount,
                    inventory=[],
                )
            return

        # Test valid gold amounts
        character = Character(
            id="test",
            name="TestChar",
            class_type=CharacterClass.WARRIOR,
            level=1,
            experience=0,
            stats=CharacterStats(
                strength=10,
                dexterity=10,
                intelligence=10,
                wisdom=10,
                charisma=10,
                constitution=10,
            ),
            hp=100,
            max_hp=100,
            gold=gold_amount,
            inventory=[],
        )

        assert character.gold == gold_amount
        assert character.gold >= 0

        # Test inventory size
        test_items = [f"item_{i}" for i in range(inventory_size)]

        # Create character with inventory
        character_with_inventory = Character(
            id="test2",
            name="TestChar2",
            class_type=CharacterClass.WARRIOR,
            level=1,
            experience=0,
            stats=CharacterStats(
                strength=10,
                dexterity=10,
                intelligence=10,
                wisdom=10,
                charisma=10,
                constitution=10,
            ),
            hp=100,
            max_hp=100,
            gold=0,
            inventory=test_items,
        )

        assert len(character_with_inventory.inventory) == inventory_size

        # Test reasonable inventory limits
        # (Most games limit inventory to reasonable sizes)
        if inventory_size > 500:
            # Very large inventories might be problematic
            # This test documents the boundary
            assert len(character_with_inventory.inventory) == inventory_size

    @given(
        items_list=lists(text(min_size=1, max_size=50), min_size=0, max_size=200),
        abilities_list=lists(text(min_size=1, max_size=30), min_size=0, max_size=100),
        quests_list=lists(text(min_size=1, max_size=50), min_size=0, max_size=2000),
    )
    def test_collection_boundaries(self, items_list, abilities_list, quests_list):
        """Test character collection boundaries."""
        character = Character(
            id="test",
            name="TestChar",
            class_type=CharacterClass.WARRIOR,
            level=1,
            experience=0,
            stats=CharacterStats(
                strength=10,
                dexterity=10,
                intelligence=10,
                wisdom=10,
                charisma=10,
                constitution=10,
            ),
            hp=100,
            max_hp=100,
            gold=0,
            inventory=items_list,
            abilities=abilities_list,
            quests_completed=quests_list,
        )

        # Verify collection sizes
        assert len(character.inventory) == len(items_list)
        assert len(character.abilities) == len(abilities_list)
        assert len(character.quests_completed) == len(quests_list)

        # Test boundary conditions
        if len(items_list) == 200:
            # Maximum inventory size tested
            assert len(character.inventory) == 200

        if len(abilities_list) == 100:
            # Maximum abilities tested
            assert len(character.abilities) == 100

        if len(quests_list) == 2000:
            # Maximum quests tested
            assert len(character.quests_completed) == 2000

    @given(
        skills_dict=dictionaries(
            keys=text(min_size=1, max_size=30),
            values=integers(min_value=0, max_value=1000),
            min_size=0,
            max_size=100,
        )
    )
    def test_skills_boundaries(self, skills_dict):
        """Test skills dictionary boundaries."""
        character = Character(
            id="test",
            name="TestChar",
            class_type=CharacterClass.WARRIOR,
            level=1,
            experience=0,
            stats=CharacterStats(
                strength=10,
                dexterity=10,
                intelligence=10,
                wisdom=10,
                charisma=10,
                constitution=10,
            ),
            hp=100,
            max_hp=100,
            gold=0,
            skills=skills_dict,
        )

        # Verify skills
        assert len(character.skills) == len(skills_dict)

        # Test boundary conditions
        for skill_name, skill_value in skills_dict.items():
            assert character.skills[skill_name] == skill_value

            # Test skill value boundaries
            if skill_value < 0:
                # Negative skills might be invalid in some contexts
                # This test documents the boundary
                assert character.skills[skill_name] < 0
            elif skill_value > 100:
                # Very high skill values
                assert character.skills[skill_name] > 100

        # Test maximum skills
        if len(skills_dict) == 100:
            # Maximum number of skills tested
            assert len(character.skills) == 100


class TestInventoryEdgeCases:
    """Property-based tests for inventory edge cases."""

    @given(
        item_names=lists(text(min_size=1, max_size=100), min_size=0, max_size=50),
        duplicate_ratio=floats(min_value=0.0, max_value=1.0),
    )
    def test_duplicate_items(self, item_names, duplicate_ratio):
        """Test inventory with duplicate items."""
        # Create some duplicates based on ratio
        inventory = []
        for i, name in enumerate(item_names):
            inventory.append(name)
            # Add duplicates based on ratio
            if i < len(item_names) * duplicate_ratio:
                inventory.append(name)

        character = Character(
            id="test",
            name="TestChar",
            class_type=CharacterClass.WARRIOR,
            level=1,
            experience=0,
            stats=CharacterStats(
                strength=10,
                dexterity=10,
                intelligence=10,
                wisdom=10,
                charisma=10,
                constitution=10,
            ),
            hp=100,
            max_hp=100,
            gold=0,
            inventory=inventory,
        )

        assert len(character.inventory) == len(inventory)

        # Count duplicates
        from collections import Counter

        item_counts = Counter(character.inventory)

        # Verify duplicates exist when ratio > 0
        if duplicate_ratio > 0 and len(item_names) > 0:
            assert any(count > 1 for count in item_counts.values())

    @given(
        special_characters=lists(
            sampled_from(
                [
                    "!",
                    "@",
                    "#",
                    "$",
                    "%",
                    "^",
                    "&",
                    "*",
                    "(",
                    ")",
                    "-",
                    "+",
                    "=",
                    "[",
                    "]",
                    "{",
                    "}",
                    "|",
                    "\\",
                    ":",
                    ";",
                    '"',
                    "'",
                    "<",
                    ">",
                    ",",
                    ".",
                    "?",
                    "/",
                    "~",
                    "`",
                ]
            ),
            min_size=0,
            max_size=10,
        ),
        base_text=text(min_size=1, max_size=20),
    )
    def test_special_characters_in_inventory(self, special_characters, base_text):
        """Test inventory items with special characters."""
        # Create item names with special characters
        item_names = []
        for i, char in enumerate(special_characters):
            item_names.append(f"{base_text}_{char}_{i}")

        if not item_names:
            item_names = [base_text]

        character = Character(
            id="test",
            name="TestChar",
            class_type=CharacterClass.WARRIOR,
            level=1,
            experience=0,
            stats=CharacterStats(
                strength=10,
                dexterity=10,
                intelligence=10,
                wisdom=10,
                charisma=10,
                constitution=10,
            ),
            hp=100,
            max_hp=100,
            gold=0,
            inventory=item_names,
        )

        assert len(character.inventory) == len(item_names)

        # Verify special characters are preserved
        for original, stored in zip(item_names, character.inventory):
            assert original == stored

    @given(large_numbers=integers(min_value=1000000, max_value=1000000000))
    def test_extreme_gold_values(self, large_numbers):
        """Test character with extremely large gold values."""
        character = Character(
            id="test",
            name="TestChar",
            class_type=CharacterClass.WARRIOR,
            level=1,
            experience=0,
            stats=CharacterStats(
                strength=10,
                dexterity=10,
                intelligence=10,
                wisdom=10,
                charisma=10,
                constitution=10,
            ),
            hp=100,
            max_hp=100,
            gold=large_numbers,
        )

        assert character.gold == large_numbers
        assert character.gold >= 1000000  # Verify it's actually large

        # Test that large gold values don't cause issues
        # (This documents the boundary behavior)
        assert isinstance(character.gold, int)
        assert character.gold > 0


class TestInventoryPerformanceStress:
    """Stress tests for inventory performance."""

    @settings(max_examples=50)
    @given(item_count=integers(min_value=1, max_value=10000))
    def test_large_inventory_performance(self, item_count):
        """Test performance with large inventories."""
        # Create large inventory
        large_inventory = [f"item_{i}" for i in range(item_count)]

        character = Character(
            id="test",
            name="TestChar",
            class_type=CharacterClass.WARRIOR,
            level=1,
            experience=0,
            stats=CharacterStats(
                strength=10,
                dexterity=10,
                intelligence=10,
                wisdom=10,
                charisma=10,
                constitution=10,
            ),
            hp=100,
            max_hp=100,
            gold=0,
            inventory=large_inventory,
        )

        # Test inventory operations
        assert len(character.inventory) == item_count

        # Test item lookup (should be O(1) for list access)
        if item_count > 0:
            first_item = character.inventory[0]
            last_item = character.inventory[-1]
            assert first_item == "item_0"
            assert last_item == f"item_{item_count - 1}"

        # Test item counting
        item_count_actual = len(character.inventory)
        assert item_count_actual == item_count

    @settings(max_examples=30)
    @given(operation_count=integers(min_value=1, max_value=1000))
    def test_rapid_inventory_operations(self, operation_count):
        """Test rapid inventory operations."""
        character = Character(
            id="test",
            name="TestChar",
            class_type=CharacterClass.WARRIOR,
            level=1,
            experience=0,
            stats=CharacterStats(
                strength=10,
                dexterity=10,
                intelligence=10,
                wisdom=10,
                charisma=10,
                constitution=10,
            ),
            hp=100,
            max_hp=100,
            gold=0,
            inventory=[],
        )

        # Perform many operations
        for i in range(operation_count):
            # Add item
            character.inventory.append(f"item_{i}")

            # Occasionally remove items
            if i % 10 == 0 and len(character.inventory) > 0:
                character.inventory.pop(0)

        # Verify final state
        assert len(character.inventory) >= 0
        assert len(character.inventory) <= operation_count

        # Verify all items are valid strings
        for item in character.inventory:
            assert isinstance(item, str)
            assert item.startswith("item_")

    @settings(max_examples=20)
    @given(
        character_count=integers(min_value=1, max_value=100),
        items_per_character=integers(min_value=1, max_value=100),
    )
    def test_multiple_characters_inventory(self, character_count, items_per_character):
        """Test inventory management across multiple characters."""
        characters = []

        # Create multiple characters
        for i in range(character_count):
            inventory = [f"char_{i}_item_{j}" for j in range(items_per_character)]

            character = Character(
                id=f"char_{i}",
                name=f"Char{i}",
                class_type=CharacterClass.WARRIOR,
                level=1,
                experience=0,
                stats=CharacterStats(
                    strength=10,
                    dexterity=10,
                    intelligence=10,
                    wisdom=10,
                    charisma=10,
                    constitution=10,
                ),
                hp=100,
                max_hp=100,
                gold=i * 100,  # Different gold for each
                inventory=inventory,
            )
            characters.append(character)

        # Verify all characters
        assert len(characters) == character_count

        total_items = 0
        total_gold = 0

        for i, character in enumerate(characters):
            assert len(character.inventory) == items_per_character
            assert character.gold == i * 100

            total_items += len(character.inventory)
            total_gold += character.gold

            # Verify item ownership
            for item in character.inventory:
                assert item.startswith(f"char_{i}_item_")

        # Verify totals
        expected_total_items = character_count * items_per_character
        expected_total_gold = sum(i * 100 for i in range(character_count))

        assert total_items == expected_total_items
        assert total_gold == expected_total_gold
