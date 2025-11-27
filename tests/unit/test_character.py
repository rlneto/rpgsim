"""
Unit tests for Character system
"""
import pytest
from unittest.mock import patch, MagicMock
from core.systems.character import (
    Character, CharacterClass, 
    get_all_character_classes, get_class_balance_stats, validate_class_balance,
    verify_unique_mechanics, verify_minimum_abilities,
    create_character, level_up_character, add_experience
)


class TestCharacter:
    """Test Character class functionality"""
    
    def test_init(self):
        """Test character initialization"""
        char = Character()
        
        assert char.id == ""
        assert char.name == ""
        assert char.class_type is None
        assert char.level == 1
        assert char.experience == 0
        assert char.hp == 0
        assert char.max_hp == 0
        assert char.gold == 0
        assert char.inventory == []
        assert char.abilities == []
        assert char.created is False
        assert char.visual_customization == {}
    
    def test_stats_property(self):
        """Test stats property and setter"""
        char = Character()
        
        # Test setter with dict
        test_stats = {"strength": 15, "dexterity": 14}
        char.stats = test_stats
        assert char._stats == test_stats
        
        # Test getter as object
        stats_obj = char.stats
        assert stats_obj.strength == 15
        assert stats_obj.dexterity == 14
        
        # Test setter with object (note: this creates a dict from all non-underscore attributes)
        class MockStats:
            strength = 16
            dexterity = 13
            other_attr = "ignored"
        
        char.stats = MockStats()
        assert char._stats["strength"] == 16
        assert char._stats["dexterity"] == 13
    
    def test_create_character_valid(self):
        """Test successful character creation"""
        char = Character()
        result = char.create_character("Test Character", "Warrior")
        
        assert result is True
        assert char.name == "Test Character"
        assert char.class_type == CharacterClass.WARRIOR
        assert char.level == 1
        assert char.experience == 0
        assert char.created is True
        
        # Check stats are set
        assert char._stats["strength"] == 17
        assert char._stats["constitution"] == 16
        
        # Check abilities are set
        assert len(char.abilities) >= 10
        assert "Power Strike" in char.abilities
        
        # Check basic inventory
        assert "Basic Clothes" in char.inventory
        assert "Travel Rations" in char.inventory
        
        # Check HP and gold
        assert char.hp > 0
        assert char.max_hp > 0
        assert char.gold > 0
    
    def test_create_character_invalid_class(self):
        """Test character creation with invalid class"""
        char = Character()
        result = char.create_character("Test Character", "InvalidClass")
        
        assert result is False
        assert char.created is False
    
    def test_create_character_empty_name(self):
        """Test character creation with empty name"""
        char = Character()
        result = char.create_character("", "Warrior")
        
        assert result is False
        assert char.created is False
    
    def test_create_character_case_insensitive(self):
        """Test character creation with different case class names"""
        char = Character()
        result = char.create_character("Test", "warrior")
        
        assert result is True
        assert char.class_type == CharacterClass.WARRIOR
    
    def test_is_alive(self):
        """Test is_alive method"""
        char = Character()
        
        # Not created character should be dead
        assert char.is_alive() is False
        
        # Create character with HP > 0 should be alive
        char.create_character("Test", "Warrior")
        assert char.is_alive() is True
        
        # Character with 0 HP should be dead
        char.hp = 0
        assert char.is_alive() is False
    
    def test_get_summary(self):
        """Test get_summary method"""
        char = Character()
        char.create_character("Test", "Warrior")
        
        summary = char.get_summary()
        
        assert summary["name"] == "Test"
        assert summary["level"] == 1
        assert summary["class"] == "Warrior"
        assert summary["hp"] > 0
        assert summary["max_hp"] > 0
    
    def test_get_class_stats(self):
        """Test getting class stats"""
        char = Character()
        
        # Test valid class
        stats = char.get_class_stats("Warrior")
        assert stats is not None
        assert "strength" in stats
        assert "dexterity" in stats
        assert stats["strength"] > stats["dexterity"]
        
        # Test invalid class
        stats = char.get_class_stats("InvalidClass")
        assert stats is None
    
    def test_get_class_mechanic(self):
        """Test getting class mechanic"""
        char = Character()
        
        # Test valid class
        mechanic = char.get_class_mechanic("Warrior")
        assert mechanic == "Weapon Mastery"
        
        # Test invalid class
        mechanic = char.get_class_mechanic("InvalidClass")
        assert mechanic is None
    
    def test_get_class_abilities(self):
        """Test getting class abilities"""
        char = Character()
        
        # Test valid class
        abilities = char.get_class_abilities("Warrior")
        assert abilities is not None
        assert len(abilities) >= 10
        assert "Power Strike" in abilities
        
        # Test invalid class
        abilities = char.get_class_abilities("InvalidClass")
        assert abilities is None
    
    def test_get_all_classes(self):
        """Test getting all classes"""
        char = Character()
        classes = char.get_all_classes()
        
        assert len(classes) >= 23
        assert "Warrior" in classes
        assert "Mage" in classes
    
    def test_calculate_power_level(self):
        """Test power level calculation"""
        char = Character()
        char.create_character("Test", "Warrior")
        
        power = char.calculate_power_level()
        expected = sum(char._stats.values())
        assert power == expected
    
    def test_get_strengths_and_weaknesses(self):
        """Test getting strengths and weaknesses"""
        char = Character()
        char.create_character("Test", "Warrior")
        
        result = char.get_strengths_and_weaknesses()
        
        assert "strengths" in result
        assert "weaknesses" in result
        assert len(result["strengths"]) > 0
        assert len(result["weaknesses"]) > 0
    
    def test_add_to_inventory(self):
        """Test adding items to inventory"""
        char = Character()
        
        # Test valid item
        result = char.add_to_inventory("Sword")
        assert result is True
        assert "Sword" in char.inventory
        
        # Test empty item
        result = char.add_to_inventory("")
        assert result is False
        
        # Test whitespace item
        result = char.add_to_inventory("   ")
        assert result is False
    
    def test_remove_from_inventory(self):
        """Test removing items from inventory"""
        char = Character()
        char.inventory = ["Sword", "Shield"]
        
        # Test existing item
        result = char.remove_from_inventory("Sword")
        assert result is True
        assert "Sword" not in char.inventory
        
        # Test non-existing item
        result = char.remove_from_inventory("Potion")
        assert result is False
    
    def test_get_inventory_count(self):
        """Test getting inventory count"""
        char = Character()
        
        # Empty inventory
        assert char.get_inventory_count() == 0
        
        # Non-empty inventory
        char.inventory = ["Sword", "Shield"]
        assert char.get_inventory_count() == 2
    
    def test_level_up(self):
        """Test character level up"""
        char = Character()
        char.create_character("Test", "Warrior")
        original_level = char.level
        original_str = char._stats["strength"]
        
        result = char.level_up()
        
        assert result is True
        assert char.level == original_level + 1
        assert char._stats["strength"] > original_str
    
    def test_set_visual_customization(self):
        """Test setting visual customization"""
        char = Character()
        
        # Test valid customization
        result = char.set_visual_customization("hair_color", "red")
        assert result is True
        assert char.visual_customization["hair_color"] == "red"
        
        # Test invalid type
        result = char.set_visual_customization("invalid_type", "red")
        assert result is False
        
        # Test empty value
        result = char.set_visual_customization("hair_color", "")
        assert result is False


class TestCharacterClass:
    """Test CharacterClass enum"""
    
    def test_character_class_values(self):
        """Test that all expected classes exist"""
        expected_classes = [
            "Warrior", "Mage", "Rogue", "Cleric", "Ranger", "Paladin", "Warlock",
            "Druid", "Monk", "Barbarian", "Bard", "Sorcerer", "Fighter", "Necromancer",
            "Illusionist", "Alchemist", "Berserker", "Assassin", "Healer", "Summoner",
            "Shapeshifter", "Elementalist", "Ninja", "Developer"
        ]
        
        for class_name in expected_classes:
            assert hasattr(CharacterClass, class_name.upper())
    
    def test_character_class_values_consistency(self):
        """Test that enum values match expected strings"""
        assert CharacterClass.WARRIOR.value == "Warrior"
        assert CharacterClass.MAGE.value == "Mage"
        assert CharacterClass.ROGUE.value == "Rogue"


class TestUtilityFunctions:
    """Test utility functions"""
    
    def test_get_all_character_classes(self):
        """Test get_all_character_classes utility function"""
        classes = get_all_character_classes()
        
        assert len(classes) >= 23
        assert isinstance(classes, list)
        assert "Warrior" in classes
        assert "Mage" in classes
    
    def test_get_class_balance_stats(self):
        """Test get_class_balance_stats utility function"""
        balance_stats = get_class_balance_stats()
        
        assert len(balance_stats) >= 23
        assert "Warrior" in balance_stats
        assert "Mage" in balance_stats
        
        # Verify values are reasonable power levels
        for class_name, power_level in balance_stats.items():
            assert isinstance(power_level, int)
            assert power_level > 0
    
    def test_validate_class_balance(self):
        """Test validate_class_balance utility function"""
        # Should return True with properly balanced classes
        assert validate_class_balance() is True
    
    def test_verify_unique_mechanics(self):
        """Test verify_unique_mechanics utility function"""
        # Should return True with unique mechanics for all classes
        assert verify_unique_mechanics() is True
    
    def test_verify_minimum_abilities(self):
        """Test verify_minimum_abilities utility function"""
        # Should return True with 10+ abilities for all classes
        assert verify_minimum_abilities() is True
    
    def test_create_character_utility(self):
        """Test create_character utility function"""
        char = create_character("Test", "Warrior")
        
        assert isinstance(char, Character)
        assert char.name == "Test"
        assert char.class_type == CharacterClass.WARRIOR
        assert char.created is True
        
        # Test invalid parameters raise exception
        with pytest.raises(ValueError):
            create_character("Test", "InvalidClass")
    
    def test_level_up_character_utility(self):
        """Test level_up_character utility function"""
        char = Character()
        char.level = 5
        
        result = level_up_character(char)
        
        assert result is True
        assert char.level == 6
    
    def test_add_experience_utility(self):
        """Test add_experience utility function"""
        char = Character()
        char.experience = 100
        
        # Test valid experience
        result = add_experience(char, 50)
        assert result is True
        assert char.experience == 150
        
        # Test invalid experience (zero or negative)
        result = add_experience(char, 0)
        assert result is False
        
        result = add_experience(char, -10)
        assert result is False


class TestCharacterEdgeCases:
    """Test edge cases and error handling"""
    
    def test_character_creation_with_whitespace_name(self):
        """Test character creation with whitespace-only name"""
        char = Character()
        result = char.create_character("   ", "Warrior")
        assert result is False
    
    def test_character_creation_with_none_values(self):
        """Test character creation with None values"""
        char = Character()
        
        # Test with None name
        result = char.create_character(None, "Warrior")
        assert result is False
        
        # Test with None class
        result = char.create_character("Test", None)
        assert result is False
    
    def test_stats_property_with_invalid_input(self):
        """Test stats property with invalid input"""
        char = Character()
        
        # Test with None
        with pytest.raises(ValueError):
            char.stats = None
        
        # Test with string
        with pytest.raises(ValueError):
            char.stats = "invalid"
    
    def test_create_character_exception_handling(self):
        """Test that create_character handles exceptions gracefully"""
        char = Character()
        
        # Test with invalid input that might cause exception
        result = char.create_character(123, "Warrior")
        assert result is False
    
    def test_get_methods_with_class_object(self):
        """Test get methods work with class objects as well as strings"""
        char = Character()
        
        # Test with CharacterClass enum
        stats = char.get_class_stats(CharacterClass.WARRIOR)
        assert stats is not None
        
        mechanic = char.get_class_mechanic(CharacterClass.WARRIOR)
        assert mechanic == "Weapon Mastery"
        
        abilities = char.get_class_abilities(CharacterClass.WARRIOR)
        assert len(abilities) >= 10


class TestCharacterStatsBalance:
    """Test character balance requirements"""
    
    def test_all_classes_have_stats(self):
        """Test that all classes have base stats defined"""
        for char_class in CharacterClass:
            if char_class == CharacterClass.DEVELOPER:
                continue  # Skip Developer class for BDD tests
                
            assert char_class in Character.CLASS_CONFIG
            assert "base_stats" in Character.CLASS_CONFIG[char_class]
            assert len(Character.CLASS_CONFIG[char_class]["base_stats"]) == 6
    
    def test_all_classes_have_primary_stat(self):
        """Test that all classes have a primary stat defined"""
        for char_class in CharacterClass:
            assert char_class in Character.CLASS_CONFIG
            assert "primary_stat" in Character.CLASS_CONFIG[char_class]
    
    def test_all_classes_have_mechanics(self):
        """Test that all classes have unique mechanics"""
        for char_class in CharacterClass:
            if char_class == CharacterClass.DEVELOPER:
                continue
                
            assert char_class in Character.CLASS_CONFIG
            assert "mechanic" in Character.CLASS_CONFIG[char_class]
    
    def test_all_classes_have_abilities(self):
        """Test that all classes have at least 10 abilities"""
        for char_class in CharacterClass:
            if char_class == CharacterClass.DEVELOPER:
                continue
                
            assert char_class in Character.CLASS_CONFIG
            assert "abilities" in Character.CLASS_CONFIG[char_class]
            assert len(Character.CLASS_CONFIG[char_class]["abilities"]) >= 10
    
    def test_class_balance_within_15_percent(self):
        """Test that no class is more than 15% more powerful than any other"""
        balance_stats = get_class_balance_stats()
        
        # Remove Developer class for BDD test comparison
        if "Developer" in balance_stats:
            del balance_stats["Developer"]
        
        max_power = max(balance_stats.values())
        min_power = min(balance_stats.values())
        balance_ratio = (max_power - min_power) / min_power
        
        assert balance_ratio <= 0.15, f"Class imbalance detected: ratio {balance_ratio:.2f} exceeds 0.15"
    
    def test_all_classes_have_strengths_and_weaknesses(self):
        """Test that all classes have at least one high and one low stat"""
        temp_char = Character()
        
        for class_name in get_all_character_classes():
            if class_name == "Developer":
                continue  # Skip Developer class
                
            stats = temp_char.get_class_stats(class_name)
            if not stats:
                continue
                
            has_strength = any(stat >= 15 for stat in stats.values())
            has_weakness = any(stat <= 12 for stat in stats.values())
            
            assert has_strength, f"Class {class_name} should have at least one strength"
            assert has_weakness, f"Class {class_name} should have at least one weakness"