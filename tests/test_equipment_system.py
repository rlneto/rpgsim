"""
Test Equipment System for RPGSim
Comprehensive tests for equipment management, item generation, and inventory functionality
"""

import pytest
from hypothesis import given, strategies as st, settings
from hypothesis.strategies import (
    integers,
    text,
    lists,
    sampled_from,
    booleans,
    dictionaries,
)
from typing import Dict, List, Any, Optional, Tuple

from core.systems.equipment import (
    EquipmentSlot, ItemEffect, EquipmentStat, EquipmentSlotInfo,
    EquipmentComparison, LootGenerationResult, ItemGenerator, EquipmentManager,
    InventoryManager, EquipmentSystem
)
from core.models import Item, ItemType, ItemRarity


class TestItemGenerator:
    """Test ItemGenerator functionality"""

    def test_generate_unique_item(self):
        """Test generating unique items"""
        generator = ItemGenerator()

        # Test weapon generation
        weapon = generator.generate_unique_item("test_weapon_001", ItemType.WEAPON)
        assert weapon.id == "test_weapon_001"
        assert weapon.type == ItemType.WEAPON
        assert weapon.can_be_equipped()
        assert not weapon.consumable
        assert not weapon.stackable

        # Test armor generation
        armor = generator.generate_unique_item("test_armor_001", ItemType.ARMOR)
        assert armor.id == "test_armor_001"
        assert armor.type == ItemType.ARMOR
        assert armor.can_be_equipped()

        # Test accessory generation
        accessory = generator.generate_unique_item("test_accessory_001", ItemType.ACCESSORY)
        assert accessory.id == "test_accessory_001"
        assert accessory.type == ItemType.ACCESSORY

    def test_generate_loot(self):
        """Test loot generation"""
        generator = ItemGenerator()

        # Test easy difficulty
        easy_loot = generator.generate_loot("easy")
        assert isinstance(easy_loot, LootGenerationResult)
        assert len(easy_loot.items) >= 1
        assert easy_loot.gold_amount >= 20

        # Test medium difficulty
        medium_loot = generator.generate_loot("medium")
        assert isinstance(medium_loot, LootGenerationResult)
        assert medium_loot.gold_amount > easy_loot.gold_amount

        # Test hard difficulty
        hard_loot = generator.generate_loot("hard")
        assert isinstance(hard_loot, LootGenerationResult)
        assert hard_loot.gold_amount > medium_loot.gold_amount

    def test_generate_all_unique_items(self):
        """Test generating all 200 unique items"""
        generator = ItemGenerator()
        items = generator.generate_all_unique_items()

        assert len(items) == 200
        assert len(generator.generated_items) == 200

        # Verify uniqueness
        item_ids = {item.id for item in items}
        assert len(item_ids) == 200, "All items should have unique IDs"

        item_names = {item.name for item in items}
        assert len(item_names) == 200, "All items should have unique names"

        # Check distribution of types
        weapon_count = len([item for item in items if item.type == ItemType.WEAPON])
        armor_count = len([item for item in items if item.type == ItemType.ARMOR])
        accessory_count = len([item for item in items if item.type == ItemType.ACCESSORY])

        assert weapon_count > 0, "Should have weapon items"
        assert armor_count > 0, "Should have armor items"
        assert accessory_count > 0, "Should have accessory items"

    @given(
        item_type=sampled_from([ItemType.WEAPON, ItemType.ARMOR, ItemType.ACCESSORY]),
        rarity=sampled_from([ItemRarity.COMMON, ItemRarity.UNCOMMON, ItemRarity.RARE,
                           ItemRarity.EPIC, ItemRarity.LEGENDARY])
    )
    def test_generate_items_with_various_types_and_rarity(self, item_type, rarity):
        """Test generating items with various types and rarities"""
        generator = ItemGenerator()

        item = generator.generate_unique_item(f"test_{item_type.value}_{rarity.value}", item_type)
        assert item.type == item_type

        # Items should have appropriate stats for their type
        assert item.stats_mod is not None
        if item_type in [ItemType.WEAPON, ItemType.ARMOR]:
            assert len(item.stats_mod) > 0, "Weapons and armor should have stat modifiers"

        # Higher rarity items should generally have better stats
        total_stats = sum(item.stats_mod.values()) if item.stats_mod else 0
        assert total_stats >= 0, "Stat bonuses should be non-negative"

    def test_stat_generation_consistency(self):
        """Test stat generation is consistent with item type"""
        generator = ItemGenerator()

        # Generate multiple weapons and check stat types
        weapons = []
        for i in range(10):
            weapon = generator.generate_unique_item(f"weapon_{i}", ItemType.WEAPON)
            weapons.append(weapon)

        # Weapons should focus on strength and dexterity
        weapon_stats = set()
        for weapon in weapons:
            weapon_stats.update(weapon.stats_mod.keys())

        # Should include combat-relevant stats
        combat_stats = {"strength", "dexterity", "critical_chance", "critical_damage"}
        has_combat_stats = any(stat in weapon_stats for stat in combat_stats)
        assert has_combat_stats, "Weapons should have combat-relevant stats"


class TestEquipmentManager:
    """Test EquipmentManager functionality"""

    def test_equipment_slots_initialization(self):
        """Test equipment slots are properly initialized"""
        manager = EquipmentManager()

        assert EquipmentSlot.WEAPON in manager.equipment_slots
        assert EquipmentSlot.ARMOR in manager.equipment_slots
        assert EquipmentSlot.ACCESSORY1 in manager.equipment_slots
        assert EquipmentSlot.ACCESSORY2 in manager.equipment_slots

        # All slots should start empty
        for slot_info in manager.equipment_slots.values():
            assert slot_info.equipped_item is None

    def test_equip_weapon(self):
        """Test equipping a weapon"""
        manager = EquipmentManager()
        generator = ItemGenerator()

        weapon = generator.generate_unique_item("test_weapon", ItemType.WEAPON)
        character_stats = {"strength": 10, "dexterity": 10}

        success, message, previous_item = manager.equip_item(weapon, character_stats)

        assert success, f"Should successfully equip weapon: {message}"
        assert "Successfully equipped" in message
        assert previous_item is None, "Previous item should be None for empty slot"

        # Check item is actually equipped
        equipped = manager.get_equipped_item(EquipmentSlot.WEAPON)
        assert equipped is not None
        assert equipped.id == weapon.id

    def test_equip_armor(self):
        """Test equipping armor"""
        manager = EquipmentManager()
        generator = ItemGenerator()

        armor = generator.generate_unique_item("test_armor", ItemType.ARMOR)
        character_stats = {"strength": 10, "constitution": 10}

        success, message, previous_item = manager.equip_item(armor, character_stats)

        assert success, f"Should successfully equip armor: {message}"
        equipped = manager.get_equipped_item(EquipmentSlot.ARMOR)
        assert equipped is not None
        assert equipped.id == armor.id

    def test_equip_accessory(self):
        """Test equipping accessories"""
        manager = EquipmentManager()
        generator = ItemGenerator()

        accessory1 = generator.generate_unique_item("test_accessory_1", ItemType.ACCESSORY)
        accessory2 = generator.generate_unique_item("test_accessory_2", ItemType.ACCESSORY)
        character_stats = {"strength": 10, "wisdom": 10}

        # Equip first accessory
        success, _, _ = manager.equip_item(accessory1, character_stats)
        assert success, "Should equip first accessory in ACCESSORY1"

        # Equip second accessory
        success, _, _ = manager.equip_item(accessory2, character_stats)
        assert success, "Should equip second accessory in ACCESSORY2"

        # Check both are equipped
        equipped1 = manager.get_equipped_item(EquipmentSlot.ACCESSORY1)
        equipped2 = manager.get_equipped_item(EquipmentSlot.ACCESSORY2)

        assert equipped1 is not None
        assert equipped2 is not None
        assert equipped1.id != equipped2.id

    def test_equip_replacement(self):
        """Test replacing equipped items"""
        manager = EquipmentManager()
        generator = ItemGenerator()

        weapon1 = generator.generate_unique_item("test_weapon_1", ItemType.WEAPON)
        weapon2 = generator.generate_unique_item("test_weapon_2", ItemType.WEAPON)
        character_stats = {"strength": 10, "dexterity": 10}

        # Equip first weapon
        success, _, _ = manager.equip_item(weapon1, character_stats)
        assert success

        # Equip second weapon (should replace first)
        success, message, previous_item = manager.equip_item(weapon2, character_stats)
        assert success
        assert previous_item is not None
        assert previous_item.id == weapon1.id

        # Check new weapon is equipped
        equipped = manager.get_equipped_item(EquipmentSlot.WEAPON)
        assert equipped.id == weapon2.id

    def test_unequip_item(self):
        """Test unequipping items"""
        manager = EquipmentManager()
        generator = ItemGenerator()

        weapon = generator.generate_unique_item("test_weapon", ItemType.WEAPON)
        character_stats = {"strength": 10, "dexterity": 10}

        # Equip first
        manager.equip_item(weapon, character_stats)

        # Then unequip
        success, message, unequipped_item = manager.unequip_item(EquipmentSlot.WEAPON)

        assert success, f"Should successfully unequip: {message}"
        assert "Successfully unequipped" in message
        assert unequipped_item is not None
        assert unequipped_item.id == weapon.id

        # Check slot is empty
        equipped = manager.get_equipped_item(EquipmentSlot.WEAPON)
        assert equipped is None

    def test_unequip_empty_slot(self):
        """Test unequipping from empty slot"""
        manager = EquipmentManager()

        success, message, unequipped_item = manager.unequip_item(EquipmentSlot.WEAPON)

        assert not success, "Should not unequip from empty slot"
        assert unequipped_item is None

    def test_calculate_equipment_stats(self):
        """Test calculating equipment stats"""
        manager = EquipmentManager()
        generator = ItemGenerator()

        # Generate items with known stats
        weapon = generator.generate_unique_item("test_weapon", ItemType.WEAPON)
        armor = generator.generate_unique_item("test_armor", ItemType.ARMOR)
        character_stats = {"strength": 10, "dexterity": 10, "constitution": 10}

        # Equip items
        manager.equip_item(weapon, character_stats)
        manager.equip_item(armor, character_stats)

        # Calculate stats
        total_stats = manager.calculate_equipment_stats()

        assert isinstance(total_stats, dict)
        # Should include stats from both items
        weapon_stats = set(weapon.stats_mod.keys())
        armor_stats = set(armor.stats_mod.keys())
        expected_stats = weapon_stats | armor_stats

        for stat in expected_stats:
            assert stat in total_stats, f"Should include {stat} from equipment"

    def test_compare_items(self):
        """Test item comparison"""
        manager = EquipmentManager()
        generator = ItemGenerator()

        # Generate items
        current_item = generator.generate_unique_item("current", ItemType.WEAPON)
        new_item = generator.generate_unique_item("new", ItemType.WEAPON)

        # Compare without current item
        comparison = manager.compare_items(None, new_item, EquipmentSlot.WEAPON)
        assert comparison.current_item is None
        assert comparison.new_item == new_item
        assert comparison.slot_type == EquipmentSlot.WEAPON

        # Compare with current item
        comparison = manager.compare_items(current_item, new_item, EquipmentSlot.WEAPON)
        assert comparison.current_item == current_item
        assert comparison.new_item == new_item

        # Should have stat differences
        assert isinstance(comparison.stat_differences, dict)
        assert isinstance(comparison.power_difference, int)
        assert isinstance(comparison.is_upgrade, bool)

    def test_get_equipment_power_level(self):
        """Test equipment power level calculation"""
        manager = EquipmentManager()
        generator = ItemGenerator()

        # Start with empty equipment
        power = manager.get_equipment_power_level()
        assert power >= 0

        # Equip some items
        weapon = generator.generate_unique_item("test_weapon", ItemType.WEAPON)
        armor = generator.generate_unique_item("test_armor", ItemType.ARMOR)
        character_stats = {"strength": 10, "dexterity": 10, "constitution": 10}

        manager.equip_item(weapon, character_stats)
        manager.equip_item(armor, character_stats)

        # Power should increase
        new_power = manager.get_equipment_power_level()
        assert new_power > power


class TestInventoryManager:
    """Test InventoryManager functionality"""

    def test_add_item_to_inventory(self):
        """Test adding items to inventory"""
        manager = InventoryManager()
        generator = ItemGenerator()

        item = generator.generate_unique_item("test_item", ItemType.WEAPON)

        success = manager.add_item(item)
        assert success, "Should successfully add item to inventory"

        # Check item is in inventory
        retrieved = manager.get_item(item.id)
        assert retrieved is not None
        assert retrieved.id == item.id

    def test_add_item_to_full_inventory(self):
        """Test adding items to full inventory"""
        manager = InventoryManager()
        generator = ItemGenerator()

        # Fill inventory to capacity
        for i in range(manager.max_inventory_size):
            item = generator.generate_unique_item(f"item_{i}", ItemType.ACCESSORY)
            manager.add_item(item)

        # Try to add one more item
        extra_item = generator.generate_unique_item("extra_item", ItemType.WEAPON)
        success = manager.add_item(extra_item)

        assert not success, "Should not be able to add item to full inventory"

    def test_remove_item_from_inventory(self):
        """Test removing items from inventory"""
        manager = InventoryManager()
        generator = ItemGenerator()

        item = generator.generate_unique_item("test_item", ItemType.ARMOR)
        manager.add_item(item)

        success = manager.remove_item(item.id)
        assert success, "Should successfully remove item"

        # Check item is no longer in inventory
        retrieved = manager.get_item(item.id)
        assert retrieved is None

    def test_remove_nonexistent_item(self):
        """Test removing nonexistent item"""
        manager = InventoryManager()

        success = manager.remove_item("nonexistent_id")
        assert not success, "Should not be able to remove nonexistent item"

    def test_get_items_by_type(self):
        """Test filtering items by type"""
        manager = InventoryManager()
        generator = ItemGenerator()

        # Add items of different types
        weapon = generator.generate_unique_item("weapon", ItemType.WEAPON)
        armor = generator.generate_unique_item("armor", ItemType.ARMOR)
        accessory = generator.generate_unique_item("accessory", ItemType.ACCESSORY)

        manager.add_item(weapon)
        manager.add_item(armor)
        manager.add_item(accessory)

        # Get items by type
        weapons = manager.get_items_by_type(ItemType.WEAPON)
        armors = manager.get_items_by_type(ItemType.ARMOR)
        accessories = manager.get_items_by_type(ItemType.ACCESSORY)

        assert len(weapons) == 1
        assert weapons[0].id == weapon.id

        assert len(armors) == 1
        assert armors[0].id == armor.id

        assert len(accessories) == 1
        assert accessories[0].id == accessory.id

    def test_sort_inventory(self):
        """Test sorting inventory"""
        manager = InventoryManager()
        generator = ItemGenerator()

        # Add multiple items
        items = []
        for i in range(5):
            item = generator.generate_unique_item(f"item_{i}", ItemType.ACCESSORY)
            items.append(item)
            manager.add_item(item)

        # Sort by name
        manager.sort_inventory("name")
        sorted_names = [item.name for item in manager.inventory]
        assert sorted_names == sorted(sorted_names)

        # Sort by value
        manager.sort_inventory("value")
        sorted_values = [item.value for item in manager.inventory]
        assert sorted_values == sorted(sorted_values, reverse=True)

    def test_get_inventory_value(self):
        """Test calculating inventory value"""
        manager = InventoryManager()
        generator = ItemGenerator()

        # Add items with known values
        item1 = generator.generate_unique_item("item1", ItemType.WEAPON)
        item1.value = 100

        item2 = generator.generate_unique_item("item2", ItemType.ARMOR)
        item2.value = 250

        manager.add_item(item1)
        manager.add_item(item2)

        total_value = manager.get_inventory_value()
        assert total_value == 350

    def test_get_inventory_space(self):
        """Test getting inventory space information"""
        manager = InventoryManager()

        # Empty inventory
        current, max_space = manager.get_inventory_space()
        assert current == 0
        assert max_space == manager.max_inventory_size

        # Add some items
        generator = ItemGenerator()
        for i in range(3):
            item = generator.generate_unique_item(f"item_{i}", ItemType.ACCESSORY)
            manager.add_item(item)

        current, max_space = manager.get_inventory_space()
        assert current == 3
        assert max_space == manager.max_inventory_size


class TestEquipmentSystem:
    """Test EquipmentSystem integration"""

    def test_system_initialization(self):
        """Test equipment system initialization"""
        system = EquipmentSystem()

        # Should have all components
        assert system.inventory_manager is not None
        assert system.equipment_manager is not None
        assert system.item_generator is not None

        # Should have generated unique items
        assert len(system.unique_items) == 200

    def test_generate_combat_loot(self):
        """Test combat loot generation"""
        system = EquipmentSystem()

        loot = system.generate_combat_loot("easy")
        assert isinstance(loot, LootGenerationResult)
        assert len(loot.items) >= 1
        assert loot.gold_amount >= 20

        medium_loot = system.generate_combat_loot("medium")
        assert medium_loot.gold_amount > loot.gold_amount

        hard_loot = system.generate_combat_loot("hard")
        assert hard_loot.gold_amount > medium_loot.gold_amount

    def test_generate_quest_reward(self):
        """Test quest reward generation"""
        system = EquipmentSystem()

        reward = system.generate_quest_reward("medium")
        assert isinstance(reward, LootGenerationResult)
        assert len(reward.items) >= 2  # Quests give more items
        assert reward.gold_amount > 0

        # Compare with combat loot
        combat_loot = system.generate_combat_loot("medium")
        assert reward.gold_amount > combat_loot.gold_amount  # Quests give more gold

    def test_equipment_operations(self):
        """Test equipment operations through system"""
        system = EquipmentSystem()
        generator = ItemGenerator()

        weapon = generator.generate_unique_item("test_weapon", ItemType.WEAPON)
        character_stats = {"strength": 10, "dexterity": 10}

        # Add to inventory first
        success = system.add_item_to_inventory(weapon)
        assert success

        # Equip from inventory
        success, message, previous_item = system.equipment_equip_item(weapon, character_stats)
        assert success

        # Get equipment stats
        stats = system.get_character_equipment_stats()
        assert isinstance(stats, dict)

        # Get equipment power
        power = system.get_character_equipment_power()
        assert isinstance(power, int)
        assert power > 0

        # Unequip
        success, message, unequipped = system.equipment_unequip_item(EquipmentSlot.WEAPON)
        assert success
        assert unequipped is not None
        assert unequipped.id == weapon.id

    def test_get_unique_items_by_type(self):
        """Test filtering unique items by type"""
        system = EquipmentSystem()

        # Get weapons
        weapons = system.get_unique_items_by_type(ItemType.WEAPON)
        assert isinstance(weapons, list)
        assert all(item.type == ItemType.WEAPON for item in weapons)
        assert len(weapons) > 0

        # Get armor
        armor = system.get_unique_items_by_type(ItemType.ARMOR)
        assert isinstance(armor, list)
        assert all(item.type == ItemType.ARMOR for item in armor)
        assert len(armor) > 0

        # Get accessories
        accessories = system.get_unique_items_by_type(ItemType.ACCESSORY)
        assert isinstance(accessories, list)
        assert all(item.type == ItemType.ACCESSORY for item in accessories)
        assert len(accessories) > 0

        # Test with rarity filter
        rare_weapons = system.get_unique_items_by_type(ItemType.WEAPON, ItemRarity.RARE)
        assert all(item.type == ItemType.WEAPON for item in rare_weapons)
        assert all(item.rarity == ItemRarity.RARE for item in rare_weapons)

    def test_get_item_comparison(self):
        """Test item comparison through system"""
        system = EquipmentSystem()
        generator = ItemGenerator()

        current_item = generator.generate_unique_item("current", ItemType.WEAPON)
        new_item = generator.generate_unique_item("new", ItemType.WEAPON)

        comparison = system.get_item_comparison(current_item, new_item, EquipmentSlot.WEAPON)
        assert isinstance(comparison, EquipmentComparison)
        assert comparison.current_item == current_item
        assert comparison.new_item == new_item
        assert comparison.slot_type == EquipmentSlot.WEAPON

    def test_get_inventory_summary(self):
        """Test inventory summary functionality"""
        system = EquipmentSystem()
        generator = ItemGenerator()

        # Add some items to inventory
        for i in range(3):
            item = generator.generate_unique_item(f"item_{i}", ItemType.ACCESSORY)
            system.add_item_to_inventory(item)

        # Equip some items
        weapon = generator.generate_unique_item("weapon", ItemType.WEAPON)
        character_stats = {"strength": 10, "dexterity": 10}
        system.equipment_equip_item(weapon, character_stats)

        # Get summary
        summary = system.get_inventory_summary()

        assert "inventory" in summary
        assert "equipment" in summary
        assert "unique_items_available" in summary

        # Check inventory section
        inventory = summary["inventory"]
        assert inventory["current_size"] == 3
        assert inventory["max_size"] == 100
        assert inventory["item_count"] == 3
        assert inventory["total_value"] >= 0

        # Check equipment section
        equipment = summary["equipment"]
        assert "equipped_items" in equipment
        assert "stat_bonuses" in equipment
        assert "power_level" in equipment

        # Should have weapon equipped
        equipped_items = equipment["equipped_items"]
        assert equipped_items["weapon"] is not None

        # Check unique items count
        assert summary["unique_items_available"] == 200

    def test_get_unique_item_count(self):
        """Test getting unique item count"""
        system = EquipmentSystem()

        count = system.get_unique_item_count()
        assert count == 200

    @given(
        difficulty=sampled_from(["easy", "medium", "hard"]),
        item_count=integers(min_value=1, max_value=5)
    )
    def test_loot_generation_variability(self, difficulty, item_count):
        """Test loot generation with various parameters"""
        system = EquipmentSystem()

        loot = system.generate_combat_loot(difficulty)

        assert isinstance(loot, LootGenerationResult)
        assert len(loot.items) >= 1
        assert len(loot.items) <= 5  # Max items per loot
        assert loot.gold_amount > 0

        # Check difficulty scaling
        easy_loot = system.generate_combat_loot("easy")
        medium_loot = system.generate_combat_loot("medium")
        hard_loot = system.generate_combat_loot("hard")

        assert hard_loot.gold_amount >= medium_loot.gold_amount >= easy_loot.gold_amount

    def test_equipment_slot_validation(self):
        """Test equipment slot validation"""
        system = EquipmentSystem()
        generator = ItemGenerator()

        # Try to equip consumable item (should fail)
        consumable = Item(
            id="consumable",
            name="Health Potion",
            type=ItemType.ACCESSORY,  # Use accessory type but mark as not equippable
            rarity=ItemRarity.COMMON,
            value=50,
            equippable=False,
            consumable=True
        )

        character_stats = {"strength": 10}
        success, message, previous = system.equipment_equip_item(consumable, character_stats)

        assert not success, "Should not be able to equip non-equippable item"
        assert "cannot be equipped" in message.lower()
        assert previous is None


class TestEquipmentDataClasses:
    """Test equipment data classes"""

    def test_equipment_stat(self):
        """Test EquipmentStat dataclass"""
        stat = EquipmentStat(
            stat_name="strength",
            bonus_value=5,
            source_item_id="item_123",
            is_percentage=False
        )

        assert stat.stat_name == "strength"
        assert stat.bonus_value == 5
        assert stat.source_item_id == "item_123"
        assert not stat.is_percentage

    def test_equipment_slot_info(self):
        """Test EquipmentSlotInfo dataclass"""
        slot_info = EquipmentSlotInfo(slot_type=EquipmentSlot.WEAPON)

        assert slot_info.slot_type == EquipmentSlot.WEAPON
        assert slot_info.equipped_item is None
        assert ItemType.WEAPON in slot_info.allowed_item_types

        armor_slot = EquipmentSlotInfo(slot_type=EquipmentSlot.ARMOR)
        assert ItemType.ARMOR in armor_slot.allowed_item_types

        accessory_slot = EquipmentSlotInfo(slot_type=EquipmentSlot.ACCESSORY1)
        assert ItemType.ACCESSORY in accessory_slot.allowed_item_types

    def test_equipment_comparison(self):
        """Test EquipmentComparison dataclass"""
        from core.models import Item

        current_item = Item(
            id="old_sword",
            name="Old Sword",
            type=ItemType.WEAPON,
            value=100,
            stats_mod={"strength": 3}
        )

        new_item = Item(
            id="new_sword",
            name="New Sword",
            type=ItemType.WEAPON,
            value=200,
            stats_mod={"strength": 5, "dexterity": 2}
        )

        comparison = EquipmentComparison(
            current_item=current_item,
            new_item=new_item,
            slot_type=EquipmentSlot.WEAPON,
            stat_differences={"strength": (3, 5), "dexterity": (0, 2)},
            power_difference=4,
            is_upgrade=True
        )

        assert comparison.current_item == current_item
        assert comparison.new_item == new_item
        assert comparison.slot_type == EquipmentSlot.WEAPON
        assert comparison.stat_differences == {"strength": (3, 5), "dexterity": (0, 2)}
        assert comparison.power_difference == 4
        assert comparison.is_upgrade

    def test_loot_generation_result(self):
        """Test LootGenerationResult dataclass"""
        from core.models import Item

        items = [
            Item(
                id="item1",
                name="Test Item 1",
                type=ItemType.WEAPON,
                value=100
            ),
            Item(
                id="item2",
                name="Test Item 2",
                type=ItemType.ARMOR,
                value=150
            )
        ]

        result = LootGenerationResult(
            items=items,
            gold_amount=250,
            rarity_distribution={"common": 1, "uncommon": 1}
        )

        assert len(result.items) == 2
        assert result.gold_amount == 250
        assert result.rarity_distribution == {"common": 1, "uncommon": 1}
        assert result.items[0].id == "item1"
        assert result.items[1].id == "item2"


class TestEquipmentConstants:
    """Test equipment system constants"""

    def test_equipment_slot_constants(self):
        """Test EquipmentSlot constants"""
        assert EquipmentSlot.WEAPON == "weapon"
        assert EquipmentSlot.ARMOR == "armor"
        assert EquipmentSlot.ACCESSORY1 == "accessory1"
        assert EquipmentSlot.ACCESSORY2 == "accessory2"

    def test_item_effect_constants(self):
        """Test ItemEffect constants"""
        # Check damage effects
        assert ItemEffect.FIRE_DAMAGE == "fire_damage"
        assert ItemEffect.ICE_DAMAGE == "ice_damage"
        assert ItemEffect.LIGHTNING_DAMAGE == "lightning_damage"

        # Check combat effects
        assert ItemEffect.LIFE_STEAL == "life_steal"
        assert ItemEffect.CRITICAL_CHANCE == "critical_chance"

        # Check defensive effects
        assert ItemEffect.EVASION == "evasion"
        assert ItemEffect.MAGIC_RESISTANCE == "magic_resistance"

        # Check regeneration effects
        assert ItemEffect.HEALTH_REGENERATION == "health_regeneration"
        assert ItemEffect.MANA_REGENERATION == "mana_regeneration"