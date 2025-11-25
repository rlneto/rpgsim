"""
Unit Tests for World System
>90% coverage requirement for PROJECT.md quality gates
Tests for world exploration, cities, geography, and travel system
"""

import pytest
from core.systems.world import (
    GeographyType, BuildingType, TravelMethod, CultureType, ShopType,
    Building, Shop, City, TravelTime, WorldMap, World,
    create_world, get_city_balance_stats, validate_world_structure,
    verify_unique_geography, verify_unique_cultures
)


class TestGeographyType:
    """Test GeographyType enum functionality."""

    def test_all_geography_types_available(self):
        """Test that all required geography types are available."""
        expected_types = [
            "coastal", "mountainous", "plains", "forest", "desert", "swamp",
            "island", "volcanic", "arctic", "tropical", "cave", "floating"
        ]

        actual_types = [geo.value for geo in GeographyType]
        assert len(actual_types) == len(expected_types)

        for expected in expected_types:
            assert expected in actual_types, f"Missing geography type: {expected}"

    def test_geography_type_values(self):
        """Test that geography type values are strings."""
        for geo_type in GeographyType:
            assert isinstance(geo_type.value, str)
            assert len(geo_type.value.strip()) > 0


class TestBuildingType:
    """Test BuildingType enum functionality."""

    def test_all_building_types_available(self):
        """Test that all required building types are available."""
        expected_types = [
            "Inn", "Shop", "Temple", "Blacksmith", "Tavern", "Guild", "Library", "Market",
            "Arena", "Bank", "Guard Tower", "Castle", "Farm", "Stable", "Docks", "Alchemy Lab"
        ]

        actual_types = [building.value for building in BuildingType]
        assert len(actual_types) == len(expected_types)

        for expected in expected_types:
            assert expected in actual_types, f"Missing building type: {expected}"


class TestTravelMethod:
    """Test TravelMethod enum functionality."""

    def test_all_travel_methods_available(self):
        """Test that all required travel methods are available."""
        expected_methods = ["walk", "horse", "carriage", "ship", "teleport"]

        actual_methods = [method.value for method in TravelMethod]
        assert len(actual_methods) == len(expected_methods)

        for expected in expected_methods:
            assert expected in actual_methods, f"Missing travel method: {expected}"


class TestCultureType:
    """Test CultureType enum functionality."""

    def test_all_culture_types_available(self):
        """Test that all required culture types are available."""
        expected_cultures = [
            "militaristic", "scholarly", "mercantile", "religious", "agricultural",
            "artistic", "industrial", "mysterious", "nomadic", "hierarchical"
        ]

        actual_cultures = [culture.value for culture in CultureType]
        assert len(actual_cultures) == len(expected_cultures)

        for expected in expected_cultures:
            assert expected in actual_cultures, f"Missing culture type: {expected}"


class TestBuilding:
    """Test Building class functionality."""

    def test_building_initialization(self):
        """Test creating a building with basic parameters."""
        building = Building(BuildingType.INN, "Test Inn", "Rest and recovery")

        assert building.building_type == BuildingType.INN
        assert building.name == "Test Inn"
        assert building.function_desc == "Rest and recovery"
        assert building.description is not None
        assert len(building.description) > 0

    def test_building_description_generation(self):
        """Test that building descriptions are generated correctly."""
        building_types = [BuildingType.INN, BuildingType.SHOP, BuildingType.TEMPLE,
                         BuildingType.BLACKSMITH, BuildingType.TAVERN]

        for building_type in building_types:
            building = Building(building_type, f"Test {building_type.value}", "Test function")
            assert building.description is not None
            assert len(building.description) > 10

    def test_building_get_info(self):
        """Test getting building information."""
        building = Building(BuildingType.GUILD, "Test Guild", "Quests and training")
        info = building.get_info()

        assert isinstance(info, dict)
        assert info["type"] == "Guild"
        assert info["name"] == "Test Guild"
        assert info["function"] == "Quests and training"
        assert "description" in info


class TestShop:
    """Test Shop class functionality."""

    def test_shop_initialization(self):
        """Test creating a shop with basic parameters."""
        shop = Shop("Test Shop", ShopType.WEAPONS, "TestCity")

        assert shop.name == "Test Shop"
        assert shop.shop_type == ShopType.WEAPONS
        assert shop.city_name == "TestCity"
        assert isinstance(shop.inventory, list)
        assert isinstance(shop.prices, dict)

    def test_shop_inventory_generation(self):
        """Test that shop inventories are generated based on type."""
        shop_types = [ShopType.WEAPONS, ShopType.ARMOR, ShopType.MAGIC, ShopType.GENERAL]

        for shop_type in shop_types:
            shop = Shop(f"Test {shop_type.value}", shop_type, "TestCity")

            assert len(shop.inventory) >= 3
            assert len(shop.inventory) <= 6
            assert all(isinstance(item, str) for item in shop.inventory)

    def test_shop_price_generation(self):
        """Test that shop prices are generated correctly."""
        shop = Shop("Test Shop", ShopType.WEAPONS, "TestCity")

        assert len(shop.prices) == len(shop.inventory)
        for item, price in shop.prices.items():
            assert isinstance(price, int)
            assert price > 0

    def test_shop_price_modifiers(self):
        """Test that shop prices are modified based on type."""
        weapons_shop = Shop("Weapons Shop", ShopType.WEAPONS, "TestCity")
        general_shop = Shop("General Shop", ShopType.GENERAL, "TestCity")

        # Weapons shop should have higher prices
        if weapons_shop.inventory and general_shop.inventory:
            weapons_price = list(weapons_shop.prices.values())[0]
            general_price = list(general_shop.prices.values())[0]
            assert weapons_price > general_price

    def test_shop_get_info(self):
        """Test getting shop information."""
        shop = Shop("Test Shop", ShopType.MAGIC, "TestCity")
        info = shop.get_info()

        assert isinstance(info, dict)
        assert info["name"] == "Test Shop"
        assert info["type"] == "magic"
        assert "inventory" in info
        assert "prices" in info


class TestCity:
    """Test City class functionality."""

    def test_city_initialization(self):
        """Test creating a city with basic parameters."""
        city = City("Test City", "city_1", GeographyType.COASTAL, CultureType.MERCANTILE)

        assert city.name == "Test City"
        assert city.city_id == "city_1"
        assert city.geography == GeographyType.COASTAL
        assert city.culture == CultureType.MERCANTILE
        assert city.connections == []

    def test_city_building_generation(self):
        """Test that cities generate correct number of buildings."""
        city = City("Test City", "city_1", GeographyType.MOUNTAINOUS, CultureType.MILITARISTIC)

        assert len(city.buildings) >= 8
        assert len(city.buildings) <= 12
        assert all(isinstance(building, Building) for building in city.buildings)

    def test_city_shop_generation(self):
        """Test that cities generate correct number of shops."""
        city = City("Test City", "city_1", GeographyType.FOREST, CultureType.SCHOLARLY)

        assert len(city.shops) >= 2
        assert len(city.shops) <= 4
        assert all(isinstance(shop, Shop) for shop in city.shops)

    def test_city_description_generation(self):
        """Test that city descriptions are generated based on culture."""
        culture_tests = [
            (CultureType.MILITARISTIC, "militaristic"),
            (CultureType.MERCANTILE, "mercantile"),
            (CultureType.RELIGIOUS, "religious")
        ]

        for culture, keyword in culture_tests:
            city = City("Test City", "city_1", GeographyType.PLAINS, culture)

            assert city.description is not None
            assert len(city.description) > 20
            assert keyword in city.description

    def test_city_layout_generation(self):
        """Test that city layouts are generated correctly."""
        city = City("Test City", "city_1", GeographyType.DESERT, CultureType.NOMADIC)

        layout = city.layout
        assert isinstance(layout, dict)
        assert "description" in layout
        assert "districts" in layout
        assert "landmarks" in layout
        assert len(layout["districts"]) >= 3
        assert len(layout["districts"]) <= 8

    def test_city_connections(self):
        """Test adding connections to cities."""
        city = City("Test City", "city_1", GeographyType.ARCTIC, CultureType.AGRICULTURAL)

        # Add connections
        city.add_connection("City2")
        city.add_connection("City3")
        city.add_connection("City2")  # Duplicate should not be added

        assert len(city.connections) == 2
        assert "City2" in city.connections
        assert "City3" in city.connections

    def test_city_get_building_types(self):
        """Test getting building types from city."""
        city = City("Test City", "city_1", GeographyType.VOLCANIC, CultureType.INDUSTRIAL)

        building_types = city.get_building_types()
        assert isinstance(building_types, list)
        assert len(building_types) >= 8
        assert all(isinstance(bt, str) for bt in building_types)

    def test_city_get_building_info(self):
        """Test getting building information from city."""
        city = City("Test City", "city_1", GeographyType.TROPICAL, CultureType.ARTISTIC)

        building_info = city.get_building_info()
        assert isinstance(building_info, list)
        assert len(building_info) >= 8
        assert all(isinstance(info, dict) for info in building_info)

    def test_city_get_shop_info(self):
        """Test getting shop information from city."""
        city = City("Test City", "city_1", GeographyType.SWAMP, CultureType.MYSTERIOUS)

        shop_info = city.get_shop_info()
        assert isinstance(shop_info, list)
        assert len(shop_info) >= 2
        assert all(isinstance(info, dict) for info in shop_info)


class TestTravelTime:
    """Test TravelTime class functionality."""

    def test_travel_time_initialization(self):
        """Test creating travel time manager."""
        travel_time = TravelTime()

        assert travel_time.travel_times == {}

    def test_calculate_travel_time_basic(self):
        """Test basic travel time calculation."""
        travel_time = TravelTime()

        time_hours = travel_time.calculate_travel_time("City1", "City2")
        assert isinstance(time_hours, int)
        assert 1 <= time_hours <= 168  # Between 1 hour and 1 week

    def test_calculate_travel_time_with_method(self):
        """Test travel time calculation with different methods."""
        travel_time = TravelTime()

        methods = [TravelMethod.WALK, TravelMethod.HORSE, TravelMethod.CARRIAGE,
                  TravelMethod.SHIP, TravelMethod.TELEPORT]

        times = []
        for method in methods:
            time_hours = travel_time.calculate_travel_time("City1", "City2", method)
            times.append(time_hours)
            assert isinstance(time_hours, int)

        # Teleport should be fastest
        teleport_idx = list(TravelMethod).index(TravelMethod.TELEPORT)
        walk_idx = list(TravelMethod).index(TravelMethod.WALK)
        assert times[teleport_idx] <= times[walk_idx]

    def test_set_and_get_travel_time(self):
        """Test setting and getting specific travel times."""
        travel_time = TravelTime()

        travel_time.set_travel_time("City1", "City2", 12)
        retrieved_time = travel_time.get_travel_time("City1", "City2")

        assert retrieved_time == 12
        assert travel_time.get_travel_time("City2", "City1") == 12  # Should be bidirectional

    def test_travel_time_not_found(self):
        """Test getting travel time for non-existent route."""
        travel_time = TravelTime()

        time = travel_time.get_travel_time("NonExistent1", "NonExistent2")
        assert time is None


class TestWorldMap:
    """Test WorldMap class functionality."""

    def test_world_map_initialization(self):
        """Test creating world map."""
        world_map = WorldMap()

        assert world_map.type == "text_based"
        assert world_map.navigation == True
        assert world_map.travel_time == True
        assert len(world_map.travel_options) == 5  # All travel methods
        assert world_map.cities == {}

    def test_add_city(self):
        """Test adding cities to world map."""
        world_map = WorldMap()
        city = City("Test City", "city_1", GeographyType.COASTAL, CultureType.MERCANTILE)

        world_map.add_city(city)

        assert len(world_map.cities) == 1
        assert "Test City" in world_map.cities
        assert world_map.get_city("Test City") == city

    def test_get_city_not_found(self):
        """Test getting non-existent city."""
        world_map = WorldMap()

        city = world_map.get_city("NonExistent")
        assert city is None

    def test_connect_cities(self):
        """Test connecting cities."""
        world_map = WorldMap()
        city1 = City("City1", "city_1", GeographyType.PLAINS, CultureType.MILITARISTIC)
        city2 = City("City2", "city_2", GeographyType.FOREST, CultureType.SCHOLARLY)

        world_map.add_city(city1)
        world_map.add_city(city2)

        world_map.connect_cities("City1", "City2")

        assert "City2" in city1.connections
        assert "City1" in city2.connections
        assert world_map.can_travel("City1", "City2")
        assert world_map.can_travel("City2", "City1")

    def test_get_connected_cities(self):
        """Test getting connected cities."""
        world_map = WorldMap()
        city1 = City("City1", "city_1", GeographyType.MOUNTAINOUS, CultureType.RELIGIOUS)
        city2 = City("City2", "city_2", GeographyType.DESERT, CultureType.NOMADIC)
        city3 = City("City3", "city_3", GeographyType.ISLAND, CultureType.ARTISTIC)

        world_map.add_city(city1)
        world_map.add_city(city2)
        world_map.add_city(city3)

        world_map.connect_cities("City1", "City2")
        world_map.connect_cities("City1", "City3")

        connected = world_map.get_connected_cities("City1")
        assert len(connected) == 2
        assert "City2" in connected
        assert "City3" in connected

    def test_get_world_map_info(self):
        """Test getting world map information."""
        world_map = WorldMap()
        info = world_map.get_travel_info()

        assert isinstance(info, dict)
        assert info["type"] == "text_based"
        assert info["navigation"] == True
        assert info["travel_time"] == True
        assert len(info["travel_options"]) == 5


class TestWorld:
    """Test World class functionality."""

    def test_world_initialization(self):
        """Test creating world."""
        world = World()

        assert world.current_location is None
        assert world.visited_locations == []
        assert world.game_state == "menu"
        assert world.player_character is None
        assert isinstance(world.world_map, WorldMap)

    def test_generate_world(self):
        """Test world generation."""
        world = World()

        success = world.generate_world()

        assert success == True
        assert len(world.world_map.cities) == 20

        # Check all cities have required elements
        for city in world.world_map.cities.values():
            assert len(city.buildings) >= 8
            assert len(city.shops) >= 2
            assert city.description is not None

        # Check connectivity
        for city in world.world_map.cities.values():
            assert len(city.connections) >= 2

    def test_start_game(self):
        """Test starting the game."""
        world = World()

        success = world.start_game("TestPlayer", "Warrior")

        assert success == True
        assert world.game_state == "playing"
        assert world.current_location is not None
        assert len(world.visited_locations) == 1
        assert world.player_character is not None
        assert world.player_character["name"] == "TestPlayer"
        assert world.player_character["class"] == "Warrior"
        assert world.player_character["level"] == 1

    def test_travel_to_city(self):
        """Test traveling between cities."""
        world = World()
        world.start_game("TestPlayer", "Warrior")

        # Get connected cities
        connected_cities = world.get_travel_options()
        if connected_cities:
            target_city = connected_cities[0]["city_name"]

            success = world.travel_to_city(target_city)

            assert success == True
            assert world.current_location == target_city
            assert target_city in world.visited_locations
            assert world.player_character["location"] == target_city

    def test_travel_to_invalid_city(self):
        """Test traveling to non-connected city."""
        world = World()
        world.start_game("TestPlayer", "Warrior")

        success = world.travel_to_city("NonExistentCity")
        assert success == False

    def test_explore_current_city(self):
        """Test exploring current city."""
        world = World()
        world.start_game("TestPlayer", "Warrior")

        city_info = world.explore_current_city()

        assert isinstance(city_info, dict)
        assert "city_name" in city_info
        assert "city_description" in city_info
        assert "geography" in city_info
        assert "culture" in city_info
        assert "buildings" in city_info
        assert "shops" in city_info
        assert "layout" in city_info

    def test_get_travel_options(self):
        """Test getting travel options."""
        world = World()
        world.start_game("TestPlayer", "Warrior")

        options = world.get_travel_options()

        assert isinstance(options, list)
        # Should have at least some travel options
        for option in options:
            assert "city_name" in option
            assert "geography" in option
            assert "culture" in option
            assert "travel_time" in option

    def test_get_world_info(self):
        """Test getting world information."""
        world = World()
        world.start_game("TestPlayer", "Warrior")

        info = world.get_world_info()

        assert isinstance(info, dict)
        assert "current_location" in info
        assert "visited_cities" in info
        assert "total_cities" in info
        assert "game_state" in info
        assert "world_map" in info
        assert "player" in info

        assert info["game_state"] == "playing"
        assert info["total_cities"] == 20
        assert info["visited_cities"] == 1

    def test_get_city_stats(self):
        """Test getting city statistics."""
        world = World()
        world.generate_world()

        stats = world.get_city_stats()

        assert isinstance(stats, dict)
        assert "total_cities" in stats
        assert "geography_distribution" in stats
        assert "culture_distribution" in stats
        assert "building_distribution" in stats
        assert "shop_distribution" in stats

        assert stats["total_cities"] == 20


class TestUtilityFunctions:
    """Test utility functions."""

    def test_create_world(self):
        """Test creating world through utility function."""
        world = create_world()

        assert isinstance(world, World)
        assert len(world.world_map.cities) == 20

    def test_get_city_balance_stats(self):
        """Test getting city balance statistics."""
        stats = get_city_balance_stats()

        assert isinstance(stats, dict)
        assert "total_cities" in stats
        assert "geography_distribution" in stats
        assert "culture_distribution" in stats

    def test_validate_world_structure(self):
        """Test world structure validation."""
        is_valid = validate_world_structure()
        assert isinstance(is_valid, bool)
        # Should return True for properly generated world

    def test_verify_unique_geography(self):
        """Test geography uniqueness verification."""
        has_unique = verify_unique_geography()
        assert isinstance(has_unique, bool)

    def test_verify_unique_cultures(self):
        """Test culture uniqueness verification."""
        has_unique = verify_unique_cultures()
        assert isinstance(has_unique, bool)


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_world_with_empty_cities(self):
        """Test world operations when no cities exist."""
        world = World()

        # Should not crash when exploring without cities
        city_info = world.explore_current_city()
        assert city_info == {}

        # Should not crash when getting travel options without cities
        options = world.get_travel_options()
        assert options == []

    def test_travel_with_invalid_method(self):
        """Test travel with invalid method."""
        world = World()
        world.start_game("TestPlayer", "Warrior")

        connected_cities = world.get_travel_options()
        if connected_cities:
            target_city = connected_cities[0]["city_name"]

            # Should handle invalid method gracefully
            success = world.travel_to_city(target_city, "invalid_method")
            assert success == True  # Should default to walk

    def test_city_generation_extremes(self):
        """Test city generation with extreme parameters."""
        # Create multiple cities to test variety
        cities = []
        for i in range(10):
            geography = list(GeographyType)[i % len(GeographyType)]
            culture = list(CultureType)[i % len(CultureType)]
            city = City(f"City{i}", f"city_{i}", geography, culture)
            cities.append(city)

        # All cities should have valid data
        for city in cities:
            assert len(city.buildings) >= 8
            assert len(city.buildings) <= 12
            assert len(city.shops) >= 2
            assert len(city.shops) <= 4
            assert len(city.description) > 20

    def test_travel_time_boundary_values(self):
        """Test travel time calculations at boundaries."""
        travel_time = TravelTime()

        # Test minimum and maximum travel times
        min_time = travel_time.calculate_travel_time("City1", "City2", TravelMethod.TELEPORT)
        max_time = travel_time.calculate_travel_time("City1", "City2", TravelMethod.WALK, 10.0)

        assert 1 <= min_time <= 168
        assert 1 <= max_time <= 168

    def test_duplicate_connections(self):
        """Test handling duplicate city connections."""
        world_map = WorldMap()
        city1 = City("City1", "city_1", GeographyType.COASTAL, CultureType.MERCANTILE)
        city2 = City("City2", "city_2", GeographyType.MOUNTAINOUS, CultureType.MILITARISTIC)

        world_map.add_city(city1)
        world_map.add_city(city2)

        # Connect multiple times
        world_map.connect_cities("City1", "City2")
        world_map.connect_cities("City1", "City2")
        world_map.connect_cities("City2", "City1")

        # Should not create duplicate connections
        connected = world_map.get_connected_cities("City1")
        assert len(connected) == 1
        assert "City2" in connected


if __name__ == "__main__":
    pytest.main([__file__, "-v"])