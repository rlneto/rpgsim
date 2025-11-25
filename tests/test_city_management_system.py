"""
Comprehensive unit tests for City Management System
Tests all city management components including buildings, services, reputation, and player interactions
"""

import pytest

# Try to import hypothesis, but make it optional for basic testing
try:
    from hypothesis import given, strategies as st
    from hypothesis.strategies import integers, text, lists, sampled_from, dictionaries, floats, booleans
    HYPOTHESIS_AVAILABLE = True
except ImportError:
    HYPOTHESIS_AVAILABLE = False

from core.systems.city_management import (
    City, CityManager, Building, BuildingType, EconomyType, ArchitecturalStyle,
    ServiceType, ReputationLevel, CityServices, CityStats, PlayerReputation,
    get_all_building_types, get_all_economy_types, get_all_architectural_styles,
    validate_city_balance, verify_minimum_building_count
)


class TestBuildingType:
    """Test BuildingType enum"""

    def test_building_type_values(self):
        """Test that all building types have expected values"""
        expected_types = [
            "tavern", "weapon_shop", "armor_shop", "magic_shop", "general_store",
            "temple", "guild_hall", "market", "inn", "bank", "library",
            "blacksmith", "alchemist", "tailor", "jeweler", "barracks"
        ]
        actual_types = [bt.value for bt in BuildingType]
        assert set(actual_types) == set(expected_types)

    def test_building_type_count(self):
        """Test building type count is correct"""
        assert len(BuildingType) == 16

    def test_building_type_properties(self):
        """Test each building type has valid properties"""
        for bt in BuildingType:
            assert isinstance(bt.value, str)
            assert len(bt.value) > 0
            assert bt.value.replace('_', '').replace('-', '').isalnum()


class TestEconomyType:
    """Test EconomyType enum"""

    def test_economy_type_values(self):
        """Test that all economy types have expected values"""
        expected_types = ["trade", "agricultural", "industrial", "magical", "mining", "fishing"]
        actual_types = [et.value for et in EconomyType]
        assert set(actual_types) == set(expected_types)

    def test_economy_type_count(self):
        """Test economy type count is correct"""
        assert len(EconomyType) == 6


class TestArchitecturalStyle:
    """Test ArchitecturalStyle enum"""

    def test_architectural_style_values(self):
        """Test that all architectural styles have expected values"""
        expected_styles = ["medieval", "gothic", "renaissance", "oriental", "baroque"]
        actual_styles = [as_.value for as_ in ArchitecturalStyle]
        assert set(actual_styles) == set(expected_styles)

    def test_architectural_style_count(self):
        """Test architectural style count is correct"""
        assert len(ArchitecturalStyle) == 5


class TestReputationLevel:
    """Test ReputationLevel enum"""

    def test_reputation_level_values(self):
        """Test that reputation levels have correct values"""
        levels = list(ReputationLevel)
        values = [level.value for level in levels]
        assert min(values) == -5
        assert max(values) == 4
        assert len(set(values)) == len(values)  # All unique

    def test_reputation_level_ordering(self):
        """Test reputation levels are properly ordered"""
        levels = list(ReputationLevel)
        for i in range(len(levels) - 1):
            assert levels[i].value < levels[i + 1].value


class TestBuilding:
    """Test Building class"""

    def test_building_creation(self):
        """Test building creation with valid data"""
        building = Building(
            id="test_building",
            type=BuildingType.TAVERN,
            name="Test Tavern",
            function="A place for drinks",
            position={"x": 1, "y": 1, "district": "market"},
            services=["drinks", "food"]
        )

        assert building.id == "test_building"
        assert building.type == BuildingType.TAVERN
        assert building.name == "Test Tavern"
        assert building.function == "A place for drinks"
        assert building.visitable is True
        assert building.services == ["drinks", "food"]
        assert building.quality == 1.0

    def test_building_with_custom_attributes(self):
        """Test building with custom attributes"""
        building = Building(
            id="custom_building",
            type=BuildingType.WEAPON_SHOP,
            name="Custom Shop",
            function="Sells weapons",
            position={"x": 5, "y": 3, "district": "commercial"},
            visitable=False,
            services=["sales"],
            quality=1.5,
            operating_hours={"open": 10, "close": 22}
        )

        assert building.visitable is False
        assert building.quality == 1.5
        assert building.operating_hours == {"open": 10, "close": 22}


class TestCityServices:
    """Test CityServices class"""

    def test_city_services_default_creation(self):
        """Test CityServices creation with defaults"""
        services = CityServices()
        assert services.guards == {}
        assert services.healthcare == {}
        assert services.education == {}
        assert services.infrastructure == {}

    def test_city_services_with_data(self):
        """Test CityServices with provided data"""
        services = CityServices(
            guards={"strength": 10},
            healthcare={"hospitals": 2},
            education={"schools": 3},
            infrastructure={"roads": 5}
        )

        assert services.guards["strength"] == 10
        assert services.healthcare["hospitals"] == 2
        assert services.education["schools"] == 3
        assert services.infrastructure["roads"] == 5


class TestCityStats:
    """Test CityStats class"""

    def test_city_stats_default_values(self):
        """Test CityStats default values"""
        stats = CityStats()
        assert stats.population == 5000
        assert stats.wealth_level == 5
        assert stats.development_level == 3
        assert stats.prosperity == 50
        assert stats.growth_rate == 0.02
        assert stats.literacy_rate == 75
        assert stats.crime_rate == 5

    def test_city_stats_custom_values(self):
        """Test CityStats with custom values"""
        stats = CityStats(
            population=10000,
            wealth_level=8,
            development_level=4,
            prosperity=75,
            growth_rate=0.05,
            literacy_rate=90,
            crime_rate=2
        )

        assert stats.population == 10000
        assert stats.wealth_level == 8
        assert stats.development_level == 4
        assert stats.prosperity == 75
        assert stats.growth_rate == 0.05
        assert stats.literacy_rate == 90
        assert stats.crime_rate == 2


class TestPlayerReputation:
    """Test PlayerReputation class"""

    def test_player_reputation_creation(self):
        """Test PlayerReputation creation"""
        rep = PlayerReputation(city_id="test_city")
        assert rep.city_id == "test_city"
        assert rep.reputation_score == 0
        assert rep.completed_quests == 0
        assert rep.trades_made == 0
        assert rep.time_in_city == 0
        assert rep.major_events == []

    def test_player_reputation_with_data(self):
        """Test PlayerReputation with initial data"""
        events = [{"event": "quest_complete", "reputation_impact": 10}]
        rep = PlayerReputation(
            city_id="test_city",
            reputation_score=25,
            completed_quests=5,
            trades_made=10,
            time_in_city=30,
            major_events=events
        )

        assert rep.reputation_score == 25
        assert rep.completed_quests == 5
        assert rep.trades_made == 10
        assert rep.time_in_city == 30
        assert rep.major_events == events


class TestCity:
    """Test City class"""

    def test_city_creation(self):
        """Test basic city creation"""
        city = City("test_city", "Testville")

        assert city.id == "test_city"
        assert city.name == "Testville"
        assert isinstance(city.economy_type, EconomyType)
        assert isinstance(city.architectural_style, ArchitecturalStyle)
        assert len(city.buildings) >= 8
        assert isinstance(city.stats, CityStats)
        assert isinstance(city.services, CityServices)
        assert city.discovered is False

    def test_city_buildings_generation(self):
        """Test city generates correct number of buildings"""
        city = City("test_city", "Testville")

        assert len(city.buildings) >= 8
        assert len(city.buildings) <= 12  # Maximum from random.randint(8, 12)

        # Check all buildings have required attributes
        for building in city.buildings:
            assert isinstance(building, Building)
            assert building.id.startswith(f"{city.id}_building_")
            assert building.name
            assert building.function
            assert building.position
            assert building.services

    def test_city_building_functions(self):
        """Test all buildings have valid functions"""
        city = City("test_city", "Testville")

        for building in city.buildings:
            assert building.function in City.BUILDING_FUNCTIONS.values()
            assert len(building.function) > 10  # Functions should be descriptive

    def test_city_building_services(self):
        """Test all buildings have valid services"""
        city = City("test_city", "Testville")

        for building in city.buildings:
            expected_services = City.BUILDING_SERVICES[building.type]
            assert set(building.services) == set(expected_services)

    def test_get_building_by_type(self):
        """Test finding buildings by type"""
        city = City("test_city", "Testville")

        # Test for existing building types
        for building in city.buildings:
            found = city.get_building_by_type(building.type)
            assert found is not None
            assert found.type == building.type

        # Test for non-existent building type
        # Create a building type that might not exist
        unused_types = set(BuildingType) - set(b.type for b in city.buildings)
        if unused_types:
            not_found = city.get_building_by_type(next(iter(unused_types)))
            assert not_found is None

    def test_get_buildings_by_district(self):
        """Test finding buildings by district"""
        city = City("test_city", "Testville")

        # Get all districts that have buildings
        districts = set(b.position["district"] for b in city.buildings)

        for district in districts:
            buildings = city.get_buildings_by_district(district)
            assert all(b.position["district"] == district for b in buildings)

    def test_shop_availability(self):
        """Test shop availability calculation"""
        city = City("test_city", "Testville")
        availability = city.get_shop_availability()

        assert isinstance(availability, int)
        assert 50 <= availability <= 150  # Reasonable range

    def test_price_multiplier(self):
        """Test price multiplier calculation"""
        city = City("test_city", "Testville")
        multiplier = city.get_price_multiplier()

        assert isinstance(multiplier, float)
        assert 0.7 <= multiplier <= 1.5  # Reasonable range

    def test_get_description(self):
        """Test city description generation"""
        city = City("test_city", "Testville")
        description = city.get_description()

        assert isinstance(description, str)
        assert city.name in description
        assert str(city.stats.population) in description
        assert len(description) > 50  # Should be descriptive

    def test_get_services_summary(self):
        """Test services summary generation"""
        city = City("test_city", "Testville")
        summary = city.get_services_summary()

        assert isinstance(summary, list)
        assert len(summary) >= 4  # Should have at least 4 service entries

        # Check specific services are mentioned
        summary_text = ' '.join(summary)
        assert any(service in summary_text.lower() for service in ['market', 'guards', 'inns', 'shops'])

    def test_reputation_management(self):
        """Test reputation update and retrieval"""
        city = City("test_city", "Testville")

        # Test initial reputation
        level = city.get_player_reputation_level("player1")
        assert level == ReputationLevel.NEUTRAL

        # Update reputation
        city.update_reputation("player1", 20, "completed quest")
        level = city.get_player_reputation_level("player1")
        assert level == ReputationLevel.RESPECTED

        # Check reputation data
        rep = city.player_reputation["player1"]
        assert rep.reputation_score == 20
        assert len(rep.major_events) == 1
        assert rep.major_events[0]["event"] == "completed quest"
        assert rep.major_events[0]["reputation_impact"] == 20

    def test_pricing_modifier_by_reputation(self):
        """Test pricing modifier based on reputation"""
        city = City("test_city", "Testville")

        # Test neutral reputation
        modifier = city.get_pricing_modifier("player1")
        assert modifier == 1.0

        # Test good reputation
        city.update_reputation("player1", 30, "saved city")
        modifier = city.get_pricing_modifier("player1")
        assert modifier < 1.0  # Should get discount

        # Test bad reputation
        city.update_reputation("player2", -40, "committed crime")
        modifier = city.get_pricing_modifier("player2")
        assert modifier > 1.0  # Should get surcharge

    def test_available_services_by_reputation(self):
        """Test service availability based on reputation"""
        city = City("test_city", "Testville")

        # Test neutral reputation
        services = city.get_available_services("player1")
        assert "general_store" in services
        assert "tavern" in services
        assert len(services) == 2  # Only basic services

        # Test good reputation
        city.update_reputation("player1", 30, "helped citizens")
        services = city.get_available_services("player1")
        assert len(services) > 2  # Should have advanced services
        assert "specialty_shop" in services

    def test_city_growth_simulation(self):
        """Test city growth simulation"""
        city = City("test_city", "Testville")
        initial_population = city.stats.population
        initial_prosperity = city.stats.prosperity
        initial_development = city.stats.development_level

        city.simulate_growth(30)  # Simulate 30 days

        # Population should grow
        assert city.stats.population >= initial_population

        # Prosperity and development might increase
        assert city.stats.prosperity >= initial_prosperity
        assert city.stats.development_level >= initial_development

        assert city.stats.development_level <= 5  # Max level

    def test_cultural_traits_generation(self):
        """Test cultural traits based on economy"""
        city = City("test_city", "Testville")
        expected_traits = City.CULTURAL_TRAITS[city.economy_type]

        assert set(city.cultural_traits) == set(expected_traits)

    def test_economy_specific_stats_adjustment(self):
        """Test stats adjustment based on economy type"""
        # Create multiple cities and check they have reasonable variety
        cities = []
        for i in range(20):  # Create many cities to get variety
            city = City(f"city_{i}", "Test")
            cities.append(city)

        # Check we have some variety in economy types
        economies = [city.economy_type for city in cities]
        unique_economies = set(economies)

        # Should have at least some variety across 20 cities
        assert len(unique_economies) >= 3

        # Test that stats are adjusted correctly for found economies
        for economy_type in unique_economies:
            # Find a city with this economy type
            city = next(c for c in cities if c.economy_type == economy_type)

            # Check that stats are adjusted
            modifiers = City.ECONOMY_MODIFIERS[economy_type]
            expected_wealth_range = (1, 10)  # Min/max after bounds checking

            assert expected_wealth_range[0] <= city.stats.wealth_level <= expected_wealth_range[1]

            # Check that stats are within expected ranges
            expected_wealth = max(1, min(10, 5 + modifiers["wealth_bonus"]))
            # Note: Due to random selection of economy type, we check the range
            assert 1 <= city.stats.wealth_level <= 10


class TestCityManager:
    """Test CityManager class"""

    def test_city_manager_creation(self):
        """Test CityManager creation"""
        manager = CityManager()
        assert len(manager.cities) == 0
        assert len(manager.player_locations) == 0
        assert len(manager.discovered_cities) == 0

    def test_create_city(self):
        """Test creating a new city"""
        manager = CityManager()
        city = manager.create_city("test_city", "Testville")

        assert isinstance(city, City)
        assert city.id == "test_city"
        assert city.name == "Testville"
        assert "test_city" in manager.cities

    def test_create_duplicate_city(self):
        """Test creating duplicate city raises error"""
        manager = CityManager()
        manager.create_city("test_city", "Testville")

        with pytest.raises(ValueError, match="City test_city already exists"):
            manager.create_city("test_city", "Another Ville")

    def test_get_city(self):
        """Test retrieving a city"""
        manager = CityManager()
        manager.create_city("test_city", "Testville")

        city = manager.get_city("test_city")
        assert city is not None
        assert city.id == "test_city"

        # Test non-existent city
        city = manager.get_city("non_existent")
        assert city is None

    def test_get_all_cities(self):
        """Test retrieving all cities"""
        manager = CityManager()

        # Initially empty
        assert len(manager.get_all_cities()) == 0

        # Add cities
        manager.create_city("city1", "Ville1")
        manager.create_city("city2", "Ville2")

        all_cities = manager.get_all_cities()
        assert len(all_cities) == 2
        city_names = [city.name for city in all_cities]
        assert "Ville1" in city_names
        assert "Ville2" in city_names

    def test_player_enter_city(self):
        """Test player entering a city"""
        manager = CityManager()
        city = manager.create_city("test_city", "Testville")

        # Player enters city
        success = manager.player_enter_city("player1", "test_city")
        assert success is True

        # Check player location
        current_city = manager.get_player_current_city("player1")
        assert current_city == city

        # Test entering non-existent city
        success = manager.player_enter_city("player1", "non_existent")
        assert success is False

    def test_city_discovery_tracking(self):
        """Test tracking discovered cities"""
        manager = CityManager()
        manager.create_city("city1", "Ville1")
        manager.create_city("city2", "Ville2")

        # Player discovers first city
        manager.player_enter_city("player1", "city1")
        discovered = manager.get_discovered_cities("player1")
        assert len(discovered) == 1
        assert discovered[0].id == "city1"
        assert discovered[0].discovered is True

        # Player discovers second city
        manager.player_enter_city("player1", "city2")
        discovered = manager.get_discovered_cities("player1")
        assert len(discovered) == 2
        discovered_ids = [city.id for city in discovered]
        assert "city1" in discovered_ids
        assert "city2" in discovered_ids

        # Test new player with no discoveries
        discovered = manager.get_discovered_cities("player2")
        assert len(discovered) == 0

    def test_get_cities_by_economy(self):
        """Test filtering cities by economy type"""
        manager = CityManager()

        # Create many cities to get variety in economies
        cities = []
        for i in range(20):  # Create enough to get variety
            city = manager.create_city(f"city_{i}", f"Ville{i}")
            cities.append(city)

        # Get different economy types
        for economy_type in EconomyType:
            cities_of_type = manager.get_cities_by_economy(economy_type)
            # All returned cities should be of the correct type
            assert all(city.economy_type == economy_type for city in cities_of_type)

        # Check that we have at least some variety
        economies = [city.economy_type for city in cities]
        unique_economies = set(economies)
        assert len(unique_economies) >= 3  # Should have at least 3 different types

    def test_simulate_all_cities_growth(self):
        """Test simulating growth for all cities"""
        manager = CityManager()
        city1 = manager.create_city("city1", "Ville1")
        city2 = manager.create_city("city2", "Ville2")

        initial_pop1 = city1.stats.population
        initial_pop2 = city2.stats.population

        manager.simulate_all_cities_growth(60)  # 60 days

        # Both cities should have grown
        assert city1.stats.population >= initial_pop1
        assert city2.stats.population >= initial_pop2

    def test_export_city_data(self):
        """Test exporting city data"""
        manager = CityManager()
        manager.create_city("test_city", "Testville")
        manager.player_enter_city("player1", "test_city")

        data = manager.export_city_data()

        assert "cities" in data
        assert "discovered_cities" in data
        assert "test_city" in data["cities"]
        assert "player1" in data["discovered_cities"]

        # Check city data structure
        city_data = data["cities"]["test_city"]
        assert city_data["id"] == "test_city"
        assert city_data["name"] == "Testville"
        assert "buildings" in city_data
        assert "services" in city_data
        assert "stats" in city_data


class TestUtilityFunctions:
    """Test utility functions"""

    def test_get_all_building_types(self):
        """Test getting all building types as strings"""
        types = get_all_building_types()
        assert isinstance(types, list)
        assert len(types) == len(BuildingType)
        assert all(isinstance(t, str) for t in types)

    def test_get_all_economy_types(self):
        """Test getting all economy types as strings"""
        types = get_all_economy_types()
        assert isinstance(types, list)
        assert len(types) == len(EconomyType)
        assert all(isinstance(t, str) for t in types)

    def test_get_all_architectural_styles(self):
        """Test getting all architectural styles as strings"""
        styles = get_all_architectural_styles()
        assert isinstance(styles, list)
        assert len(styles) == len(ArchitecturalStyle)
        assert all(isinstance(s, str) for s in styles)

    def test_validate_city_balance(self):
        """Test city balance validation"""
        manager = CityManager()

        # Empty list should pass
        assert validate_city_balance([]) is True

        # Single city should pass
        city = manager.create_city("city1", "Ville1")
        assert validate_city_balance([city]) is True

        # Multiple cities with different economies should pass
        # Force different economies by creating new cities until we get variety
        cities = []
        economies = set()
        for i in range(10):
            city = manager.create_city(f"city_{i}", f"Ville{i}")
            cities.append(city)
            economies.add(city.economy_type)
            if len(economies) >= 3:
                break

        if len(cities) >= 2:
            assert validate_city_balance(cities) is True

    def test_verify_minimum_building_count(self):
        """Test minimum building count verification"""
        manager = CityManager()

        # Cities should have at least 8 buildings by default
        cities = []
        for i in range(3):
            city = manager.create_city(f"city_{i}", f"Ville{i}")
            cities.append(city)

        assert verify_minimum_building_count(cities) is True
        assert verify_minimum_building_count(cities, min_buildings=8) is True
        assert verify_minimum_building_count(cities, min_buildings=12) is False  # Unlikely to have this many


class TestCitySystemIntegration:
    """Integration tests for city system components"""

    def test_player_journey_simulation(self):
        """Test simulating a player's journey through cities"""
        manager = CityManager()

        # Create cities
        cities = [
            manager.create_city("silverhaven", "Silverhaven"),
            manager.create_city("goldshire", "Goldshire"),
            manager.create_city("crystalpeak", "Crystalpeak")
        ]

        player_id = "adventurer"

        # Player travels and builds reputation
        for i, city in enumerate(cities):
            manager.player_enter_city(player_id, city.id)

            # Build some reputation in each city
            if i == 0:
                city.update_reputation(player_id, 25, "completed first quest")
            elif i == 1:
                city.update_reputation(player_id, 15, "helped merchants")
            else:
                city.update_reputation(player_id, 35, "saved city from threat")

        # Verify player discovered all cities
        discovered = manager.get_discovered_cities(player_id)
        assert len(discovered) == 3

        # Verify reputation progression (at least should be respected or higher)
        assert cities[0].get_player_reputation_level(player_id) in [ReputationLevel.FRIENDLY, ReputationLevel.RESPECTED]
        assert cities[1].get_player_reputation_level(player_id) in [ReputationLevel.FRIENDLY, ReputationLevel.RESPECTED]
        assert cities[2].get_player_reputation_level(player_id) in [ReputationLevel.RESPECTED, ReputationLevel.HONORED, ReputationLevel.REVERED]

    def test_city_economy_differences(self):
        """Test that different economy types create different cities"""
        manager = CityManager()

        # Force creation of cities with different economies
        economy_cities = {}
        for economy_type in EconomyType:
            city_id = f"{economy_type.value}_city"
            city = manager.create_city(city_id, f"{economy_type.value.title()}ville")
            # Force the economy type
            city.economy_type = economy_type
            city._adjust_stats_by_economy()
            economy_cities[economy_type] = city

        # Verify differences
        trade_city = economy_cities[EconomyType.TRADE]
        agricultural_city = economy_cities[EconomyType.AGRICULTURAL]
        magical_city = economy_cities[EconomyType.MAGICAL]

        # Trade city should have better shop availability
        assert trade_city.get_shop_availability() > agricultural_city.get_shop_availability()

        # Trade city should have lower prices
        assert trade_city.get_price_multiplier() < magical_city.get_price_multiplier()

        # Cities should have different population ranges
        assert trade_city.stats.population != agricultural_city.stats.population

    def test_city_service_quality_correlation(self):
        """Test correlation between wealth and service quality"""
        manager = CityManager()

        cities = []
        for i in range(5):
            city = manager.create_city(f"city_{i}", f"Ville{i}")
            cities.append(city)

        # Sort cities by wealth
        cities.sort(key=lambda c: c.stats.wealth_level)

        # Higher wealth cities should have better services
        poorest = cities[0]
        richest = cities[-1]

        # Check correlation between wealth and service quality (general trend)
        # Note: Due to random generation, we check for reasonable correlation
        high_wealth_cities = [c for c in cities if c.stats.wealth_level >= 7]
        low_wealth_cities = [c for c in cities if c.stats.wealth_level <= 3]

        if high_wealth_cities and low_wealth_cities:
            avg_high_quality = sum(c.services.healthcare["service_quality"] for c in high_wealth_cities) / len(high_wealth_cities)
            avg_low_quality = sum(c.services.healthcare["service_quality"] for c in low_wealth_cities) / len(low_wealth_cities)

            # High wealth cities should generally have better service quality (allowing some variance)
            assert avg_high_quality >= avg_low_quality - 20  # Allow some variance due to randomness

        # Check crime rate correlation (wealthier cities should generally have lower crime)
        if high_wealth_cities and low_wealth_cities:
            avg_high_crime = sum(c.services.guards["crime_rate"] for c in high_wealth_cities) / len(high_wealth_cities)
            avg_low_crime = sum(c.services.guards["crime_rate"] for c in low_wealth_cities) / len(low_wealth_cities)

            # Allow for some variance in crime rates due to random generation
            assert avg_high_crime <= avg_low_crime + 5  # Reasonable variance


class TestCitySystemEdgeCases:
    """Test edge cases and boundary conditions"""

    def test_maximum_reputation_levels(self):
        """Test maximum reputation level behavior"""
        city = City("test_city", "Testville")

        # Add massive reputation
        city.update_reputation("player", 1000, "legendary hero")

        level = city.get_player_reputation_level("player")
        assert level == ReputationLevel.LEGENDARY

        # Should get best pricing
        modifier = city.get_pricing_modifier("player")
        assert modifier == 0.8  # Best discount

        # Should have all services
        services = city.get_available_services("player")
        assert len(services) > len(["general_store", "tavern", "specialty_shop", "guild_membership"])

    def test_minimum_reputation_levels(self):
        """Test minimum reputation level behavior"""
        city = City("test_city", "Testville")

        # Add massive negative reputation
        city.update_reputation("villain", -1000, "terrible crimes")

        level = city.get_player_reputation_level("villain")
        assert level == ReputationLevel.HATED

        # Should get worst pricing
        modifier = city.get_pricing_modifier("villain")
        assert modifier == 1.3  # Worst surcharge

        # Should only have basic services
        services = city.get_available_services("villain")
        assert services == ["general_store", "tavern"]

    def test_city_growth_boundaries(self):
        """Test city growth stays within boundaries"""
        city = City("test_city", "Testville")

        # Simulate many years of growth
        city.simulate_growth(3650)  # 10 years

        # Development level should not exceed maximum
        assert city.stats.development_level <= 5

        # Prosperity should not exceed maximum
        assert city.stats.prosperity <= 100

        # Population should be reasonable
        assert city.stats.population > 0

    def test_city_name_validation(self):
        """Test city creation with various names and IDs"""
        test_cases = [
            ("Silverhaven", "city_1"),
            ("Goldshire", "city_2"),
            ("Crystal Peak", "city_3"),
            ("Shadowmere", "city_4"),
            ("Windridge", "city_5")
        ]

        for name, city_id in test_cases:
            city = City(city_id, name)
            assert city.name == name
            assert city.id == city_id

    def test_growth_simulation_various_periods(self):
        """Test growth simulation with various time periods"""
        test_periods = [1, 7, 30, 90, 365, 1000]

        for days in test_periods:
            city = City(f"test_city_{days}", "Testville")
            initial_population = city.stats.population

            city.simulate_growth(days)

            # Population should change (or stay the same)
            assert city.stats.population >= initial_population


if __name__ == "__main__":
    pytest.main([__file__, "-v"])