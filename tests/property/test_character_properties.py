"""
Property-based tests for Character system using Hypothesis
"""
import pytest
from hypothesis import given, strategies as st
from core.systems.character import Character, CharacterClass, validate_class_balance, get_class_balance_stats


class TestCharacterProperties:
    """Property-based tests for Character system"""
    
    @given(st.text(min_size=1, max_size=20, alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 -_'"), st.sampled_from([cls.value for cls in CharacterClass]))
    def test_character_creation_properties(self, name, class_name):
        """Test character creation with various valid inputs"""
        char = Character()
        result = char.create_character(name, class_name)
        
        assert result is True
        assert char.name == name.strip()
        assert char.class_type.value == class_name
        assert char.level == 1
        assert char.experience == 0
        assert char.created is True
        assert len(char.abilities) >= 10
        assert len(char.inventory) >= 2  # Basic clothes and rations
        assert char.hp > 0
        assert char.max_hp > 0
        assert char.gold > 0
    
    @given(st.text(min_size=1, max_size=20))
    def test_character_name_property(self, name):
        """Test that character names are properly processed"""
        char = Character()
        char.create_character(name, "Warrior")
        
        # Name should be stripped of whitespace
        assert char.name == name.strip()
        
        # Should never be empty after valid creation
        assert len(char.name) > 0
    
    @given(st.lists(st.text(min_size=1, max_size=10, alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 -_"), min_size=1, max_size=20))
    def test_inventory_management_properties(self, item_list):
        """Test inventory management with various item lists"""
        char = Character()
        initial_count = char.get_inventory_count()
        
        # Add items
        for item in item_list:
            result = char.add_to_inventory(item)
            assert result is True
        
        # Check final count
        final_count = char.get_inventory_count()
        assert final_count == initial_count + len(item_list)
        
        # Remove all items
        for item in item_list:
            result = char.remove_from_inventory(item)
            assert result is True
        
        # Should return to initial count
        assert char.get_inventory_count() == initial_count
    
    @given(st.integers(min_value=1, max_value=100))
    def test_level_up_properties(self, initial_level):
        """Test level up behavior"""
        char = Character()
        char.create_character("Test", "Warrior")
        char.level = initial_level
        
        # Get initial primary stat
        initial_primary = char._stats[char.CLASS_CONFIG[char.class_type]["primary_stat"]]
        
        # Level up
        result = char.level_up()
        assert result is True
        assert char.level == initial_level + 1
        
        # Primary stat should increase
        final_primary = char._stats[char.CLASS_CONFIG[char.class_type]["primary_stat"]]
        assert final_primary == initial_primary + 1
    
    def test_class_balance_properties(self):
        """Test that class balance holds as a mathematical property"""
        balance_stats = get_class_balance_stats()
        
        # Remove Developer class for BDD comparison
        if "Developer" in balance_stats:
            del balance_stats["Developer"]
        
        # Get power levels
        power_levels = list(balance_stats.values())
        
        # Properties that must hold for balanced system
        max_power = max(power_levels)
        min_power = min(power_levels)
        avg_power = sum(power_levels) / len(power_levels)
        
        # 15% balance requirement
        balance_ratio = (max_power - min_power) / min_power if min_power > 0 else 0
        assert balance_ratio <= 0.15
        
        # No class should be dramatically different from average
        for power in power_levels:
            deviation_from_avg = abs(power - avg_power) / avg_power if avg_power > 0 else 0
            assert deviation_from_avg <= 0.2  # Within 20% of average
    
    def test_stat_distributions_properties(self):
        """Test that all stat distributions follow required patterns"""
        temp_char = Character()
        
        for class_name in temp_char.get_all_classes():
            if class_name == "Developer":
                continue  # Skip for BDD compatibility
                
            stats = temp_char.get_class_stats(class_name)
            if not stats:
                continue
                
            stat_values = list(stats.values())
            
            # Should have exactly 6 stats
            assert len(stats) == 6
            
            # All stats should be in reasonable range
            for stat_value in stat_values:
                assert 10 <= stat_value <= 18  # Based on our design
            
            # Should have at least one high stat (>=15)
            has_strength = any(stat >= 15 for stat in stat_values)
            assert has_strength
            
            # Should have at least one low stat (<=12)
            has_weakness = any(stat <= 12 for stat in stat_values)
            assert has_weakness
    
    def test_unique_mechanics_properties(self):
        """Test that all mechanics are unique"""
        temp_char = Character()
        mechanics = []
        
        for class_name in temp_char.get_all_classes():
            if class_name == "Developer":
                continue  # Skip for BDD compatibility
                
            mechanic = temp_char.get_class_mechanic(class_name)
            if mechanic:
                mechanics.append(mechanic)
        
        # All mechanics should be unique
        assert len(set(mechanics)) == len(mechanics)
        
        # Should have correct number of mechanics
        assert len(mechanics) == 23  # Excluding Developer
    
    def test_minimum_abilities_properties(self):
        """Test that all classes have minimum required abilities"""
        temp_char = Character()
        
        for class_name in temp_char.get_all_classes():
            if class_name == "Developer":
                continue  # Skip for BDD compatibility
                
            abilities = temp_char.get_class_abilities(class_name)
            if not abilities:
                continue
                
            # Should have at least 10 abilities
            assert len(abilities) >= 10
            
            # All abilities should be unique within class
            assert len(set(abilities)) == len(abilities)
            
            # All abilities should be strings
            assert all(isinstance(ability, str) for ability in abilities)


class TestCharacterEdgeCases:
    """Property-based tests for edge cases"""
    
    @given(st.text())
    def test_invalid_character_names(self, name):
        """Test character creation with potentially invalid names"""
        char = Character()
        
        # Names that are empty or only whitespace should fail
        if not name or not name.strip():
            result = char.create_character(name, "Warrior")
            assert result is False
            assert char.created is False
    
    @given(st.text(alphabet="!@#$%^&*()+=[]{};:'\",.<>?/\\|~`", min_size=1, max_size=10))
    def test_invalid_class_names(self, invalid_class):
        """Test character creation with invalid class names"""
        char = Character()
        valid_classes = [cls.value for cls in CharacterClass]
        
        # Ensure generated text is not a valid class name
        if invalid_class in valid_classes:
            return  # Skip this iteration - got a valid class name
        
        result = char.create_character("Test", invalid_class)
        assert result is False
        assert char.created is False
    
    @given(st.text(alphabet="0123456789", min_size=1, max_size=20))
    def test_numeric_character_names(self, numeric_name):
        """Test character creation with numeric names"""
        char = Character()
        result = char.create_character(numeric_name, "Warrior")
        
        # Should succeed - names can be numeric
        assert result is True
        assert char.name == numeric_name.strip()
    
    @given(st.lists(st.from_regex(r'[a-zA-Z0-9\s\-_\']+', fullmatch=True), min_size=1, max_size=20))
    def test_complex_character_names(self, name_list):
        """Test character creation with complex valid names"""
        for name in name_list:
            # Skip names that would become empty after strip
            if not name or not name.strip():
                continue
                
            char = Character()
            result = char.create_character(name, "Warrior")
            
            # Should succeed for valid names
            assert result is True
            assert char.name == name.strip()


class TestStatsProperty:
    """Property-based tests for stats property"""
    
    @given(st.dictionaries(
        keys=st.sampled_from(['strength', 'dexterity', 'intelligence', 'wisdom', 'charisma', 'constitution']),
        values=st.integers(min_value=1, max_value=20),
        min_size=6,
        max_size=6
    ))
    def test_stats_dict_property(self, stats_dict):
        """Test stats property with valid dictionaries"""
        char = Character()
        char.stats = stats_dict
        
        # Should preserve all stat values
        for stat_name, stat_value in stats_dict.items():
            assert char._stats[stat_name] == stat_value
        
        # Stats property should return object with attributes
        stats_obj = char.stats
        for stat_name in stats_dict.keys():
            assert hasattr(stats_obj, stat_name)
            assert getattr(stats_obj, stat_name) == stats_dict[stat_name]
    
    def test_invalid_stats_inputs(self):
        """Test stats property with invalid inputs"""
        char = Character()
        
        # List should fail
        with pytest.raises(ValueError):
            char.stats = [1, 2, 3]
        
        # String should fail
        with pytest.raises(ValueError):
            char.stats = "invalid"
        
        # Integer should fail
        with pytest.raises(ValueError):
            char.stats = 123
        
        # None should fail
        with pytest.raises(ValueError):
            char.stats = None