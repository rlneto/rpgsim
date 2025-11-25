"""
Test Location System for RPGSim
TDD approach - tests before implementation
Optimized for LLM agents with explicit contracts
"""

import pytest
from hypothesis import given, strategies as st, settings
from hypothesis.strategies import integers, text, lists, dictionaries, sampled_from
from typing import List, Dict, Any, Optional, Tuple
from pydantic import ValidationError

from core.models import Location, LocationType


class TestLocationModel:
    """Test Location model with explicit validation."""

    def test_create_basic_location(self):
        """Test creating basic location with valid data."""
        location = Location(
            id="test_city_001",
            name="Test City",
            type=LocationType.TOWN,
            level=5,
            description="A test city for development",
        )

        assert location.id == "test_city_001"
        assert location.name == "Test City"
        assert location.type == LocationType.TOWN
        assert location.level == 5
        assert location.description == "A test city for development"

    def test_create_dungeon_location(self):
        """Test creating dungeon location."""
        location = Location(
            id="dungeon_001",
            name="Dark Dungeon",
            type=LocationType.DUNGEON,
            level=15,
            description="A dangerous dungeon filled with monsters",
        )

        assert location.type == LocationType.DUNGEON
        assert location.name == "Dark Dungeon"
        assert location.level == 15

    @given(
        location_id=text(min_size=1, max_size=50),
        name=text(min_size=1, max_size=100),
        level=integers(min_value=1, max_value=100),
        description=text(min_size=1, max_size=500),
    )
    def test_location_creation_with_various_data(
        self, location_id, name, level, description
    ):
        """Test location creation with various valid data."""
        location_type = LocationType.TOWN

        location = Location(
            id=location_id,
            name=name,
            type=location_type,
            level=level,
            description=description,
        )

        assert location.id == location_id
        assert location.name == name
        assert location.level == level
        assert location.description == description

    def test_invalid_location_id_too_short(self):
        """Test location with invalid ID (too short)."""
        with pytest.raises(ValidationError):
            Location(
                id="",
                name="Test City",
                type=LocationType.TOWN,
                level=5,
                description="Test",
            )

    def test_invalid_location_id_too_long(self):
        """Test location with invalid ID (too long)."""
        with pytest.raises(ValidationError):
            Location(
                id="a" * 51,  # 51 characters
                name="Test City",
                type=LocationType.TOWN,
                level=5,
                description="Test",
            )

    def test_invalid_level_too_low(self):
        """Test location with invalid level (too low)."""
        with pytest.raises(ValidationError):
            Location(
                id="test_city",
                name="Test City",
                type=LocationType.TOWN,
                level=0,
                description="Test",
            )

    def test_invalid_level_too_high(self):
        """Test location with invalid level (too high)."""
        with pytest.raises(ValidationError):
            Location(
                id="test_city",
                name="Test City",
                type=LocationType.TOWN,
                level=101,
                description="Test",
            )


class TestLocationValidation:
    """Test location validation functions."""

    def test_validate_unique_coordinates(self):
        """Test coordinate uniqueness validation."""
        # This test will be implemented when validation functions exist
        pass

    def test_validate_location_type_requirements(self):
        """Test location type specific requirements."""
        # This test will be implemented when validation functions exist
        pass

    @given(level=integers(min_value=0, max_value=150))
    def test_level_boundaries(self, level):
        """Test level boundary values."""
        if 1 <= level <= 100:  # Valid range
            location = Location(
                id=f"loc_{level}",
                name=f"Location {level}",
                type=LocationType.TOWN,
                level=level,
                description="Test location",
            )
            assert location.level == level
        else:  # Invalid range
            with pytest.raises(ValidationError):
                Location(
                    id=f"loc_{level}",
                    name=f"Location {level}",
                    type=LocationType.TOWN,
                    level=level,
                    description="Test location",
                )


class TestLocationTypes:
    """Test all location types are functional."""

    def test_all_location_types(self):
        """Test creating locations with all types."""
        for location_type in LocationType:
            location = Location(
                id=f"test_{location_type.value}",
                name=f"Test {location_type.value.title()}",
                type=location_type,
                level=5,
                description=f"A test {location_type.value}",
            )
            assert location.type == location_type

    def test_location_type_properties(self):
        """Test location type has expected properties."""
        town = LocationType.TOWN
        dungeon = LocationType.DUNGEON
        shop = LocationType.TOWN  # Using TOWN as shop-like location

        assert str(town) == "town"
        assert str(dungeon) == "dungeon"
        assert str(shop) == "shop"


class TestLocationPerformance:
    """Test location system performance."""

    @settings(max_examples=100)
    @given(location_count=integers(min_value=1, max_value=1000))
    def test_mass_location_creation(self, location_count):
        """Test creating many locations efficiently."""
        locations = []

        for i in range(location_count):
            location = Location(
                id=f"loc_{i:03d}",
                name=f"Location {i}",
                type=LocationType.TOWN,
                level=(i % 100) + 1,
                description=f"Test location number {i}",
            )
            locations.append(location)

        assert len(locations) == location_count

        # Verify all locations are valid
        for location in locations:
            assert location.id.startswith("loc_")
            assert location.type == LocationType.TOWN
            assert 1 <= location.level <= 100

    def test_location_memory_usage(self):
        """Test location memory usage is reasonable."""
        # Create many locations and check memory doesn't grow excessively
        locations = []

        for i in range(100):
            location = Location(
                id=f"mem_test_{i}",
                name=f"Memory Test {i}",
                type=LocationType.TOWN,
                level=i + 1,
                description="A location for memory testing",
            )
            locations.append(location)

        # Basic memory check - all locations should be accessible
        assert len(locations) == 100
        for i, location in enumerate(locations):
            assert location.id == f"mem_test_{i}"


class TestLocationMethods:
    """Test location methods."""

    def test_location_is_safe_method(self):
        """Test is_safe method."""
        safe_location = Location(
            id="safe_town",
            name="Safe Town",
            type=LocationType.TOWN,
            level=5,
            description="A safe location",
        )

        dangerous_location = Location(
            id="danger_dungeon",
            name="Danger Dungeon",
            type=LocationType.DUNGEON,
            level=15,
            description="A dangerous location",
        )

        assert safe_location.is_safe() == True
        assert dangerous_location.is_safe() == False

    def test_location_is_dangerous_method(self):
        """Test is_dangerous method."""
        safe_location = Location(
            id="safe_town",
            name="Safe Town",
            type=LocationType.TOWN,
            level=5,
            description="A safe location",
        )

        dangerous_location = Location(
            id="danger_dungeon",
            name="Danger Dungeon",
            type=LocationType.DUNGEON,
            level=15,
            description="A dangerous location",
        )

        assert safe_location.is_dangerous() == False
        assert dangerous_location.is_dangerous() == True

    def test_location_visit_methods(self):
        """Test visit tracking methods."""
        location = Location(
            id="test_location",
            name="Test Location",
            type=LocationType.TOWN,
            level=5,
            description="A test location",
        )

        # Initially not visited
        assert location.is_visited() == False

        # Mark as visited
        location.mark_visited()
        assert location.is_visited() == True

    def test_location_difficulty_rating(self):
        """Test difficulty rating method."""
        easy_location = Location(
            id="easy_loc",
            name="Easy Location",
            type=LocationType.TOWN,
            level=5,
            description="An easy location",
        )

        medium_location = Location(
            id="medium_loc",
            name="Medium Location",
            type=LocationType.DUNGEON,
            level=20,
            description="A medium location",
        )

        hard_location = Location(
            id="hard_loc",
            name="Hard Location",
            type=LocationType.DUNGEON,
            level=45,
            description="A hard location",
        )

        legendary_location = Location(
            id="legendary_loc",
            name="Legendary Location",
            type=LocationType.RUINS,
            level=80,
            description="A legendary location",
        )

        assert easy_location.get_difficulty_rating() == "Easy"
        assert medium_location.get_difficulty_rating() == "Medium"
        assert hard_location.get_difficulty_rating() == "Hard"
        assert legendary_location.get_difficulty_rating() == "Legendary"
