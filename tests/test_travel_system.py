"""
Comprehensive unit tests for Travel System
Tests travel mechanics, events, costs, fast travel, and all travel-related functionality
"""

import pytest
import random
from unittest.mock import patch, MagicMock

from core.systems.travel import (
    TravelSystem, TerrainType, TravelMethod, TravelEvent, TravelEquipment,
    EncounterDifficulty, TravelStatus, Position, TravelRoute, TravelCost,
    TravelPlan, ActiveTravel, TravelStatus, get_all_terrain_types,
    get_all_travel_methods, get_all_travel_equipment, calculate_route_difficulty,
    validate_travel_requirements
)


class TestPosition:
    """Test Position class"""

    def test_position_creation(self):
        """Test position creation with coordinates"""
        pos = Position(10, 5)
        assert pos.x == 10
        assert pos.y == 5
        assert pos.z == 0  # Default value

    def test_position_with_z(self):
        """Test position with elevation"""
        pos = Position(3, 7, 2)
        assert pos.x == 3
        assert pos.y == 7
        assert pos.z == 2

    def test_distance_calculation(self):
        """Test Manhattan distance calculation"""
        pos1 = Position(0, 0)
        pos2 = Position(3, 4)
        assert pos1.distance_to(pos2) == 7.0  # 3 + 4

    def test_distance_with_elevation(self):
        """Test distance calculation with elevation"""
        pos1 = Position(0, 0, 0)
        pos2 = Position(3, 4, 2)
        assert pos1.distance_to(pos2) == 9.0  # 3 + 4 + 2

    def test_same_position_distance(self):
        """Test distance between same positions"""
        pos = Position(5, 5)
        assert pos.distance_to(pos) == 0.0


class TestTravelRoute:
    """Test TravelRoute class"""

    def test_route_creation(self):
        """Test route creation"""
        route = TravelRoute(
            from_location="city_a",
            to_location="city_b",
            distance=5.0,
            terrain=TerrainType.PLAINS,
            danger_level=2
        )

        assert route.from_location == "city_a"
        assert route.to_location == "city_b"
        assert route.distance == 5.0
        assert route.terrain == TerrainType.PLAINS
        assert route.danger_level == 2
        assert route.safe_route_available is False
        assert route.level_requirement == 1
        assert route.restricted is False

    def test_route_with_optional_params(self):
        """Test route creation with optional parameters"""
        route = TravelRoute(
            from_location="city_a",
            to_location="city_b",
            distance=10.0,
            terrain=TerrainType.MOUNTAINS,
            danger_level=4,
            safe_route_available=True,
            level_requirement=10,
            restricted=True
        )

        assert route.safe_route_available is True
        assert route.level_requirement == 10
        assert route.restricted is True


class TestTravelPlan:
    """Test TravelPlan class"""

    def test_plan_creation_minimal(self):
        """Test plan creation with minimal parameters"""
        route = TravelRoute("city_a", "city_b", 5, TerrainType.PLAINS, 2)
        plan = TravelPlan(route=route)

        assert plan.route == route
        assert plan.method == TravelMethod.WALK
        assert plan.party_size == 1
        assert plan.equipment == []
        assert plan.departure_time == "morning"
        assert plan.fast_travel is False
        assert plan.planned_events == []

    def test_plan_with_all_params(self):
        """Test plan creation with all parameters"""
        route = TravelRoute("city_a", "city_b", 5, TerrainType.PLAINS, 2)
        plan = TravelPlan(
            route=route,
            method=TravelMethod.HORSE,
            party_size=3,
            equipment=[TravelEquipment.MOUNT],
            departure_time="evening",
            fast_travel=True,
            planned_events=["stop_at_inn"]
        )

        assert plan.method == TravelMethod.HORSE
        assert plan.party_size == 3
        assert plan.equipment == [TravelEquipment.MOUNT]
        assert plan.departure_time == "evening"
        assert plan.fast_travel is True
        assert plan.planned_events == ["stop_at_inn"]


class TestTravelCost:
    """Test TravelCost class"""

    def test_cost_creation_default(self):
        """Test cost creation with defaults"""
        cost = TravelCost()
        assert cost.gold_cost == 0
        assert cost.time_cost == 0
        assert cost.energy_cost == 0
        assert cost.food_cost == 0
        assert cost.water_cost == 0
        assert cost.stamina_cost == 0

    def test_cost_creation_with_values(self):
        """Test cost creation with specific values"""
        cost = TravelCost(
            gold_cost=100,
            time_cost=8,
            energy_cost=20,
            food_cost=10,
            water_cost=10,
            stamina_cost=30
        )

        assert cost.gold_cost == 100
        assert cost.time_cost == 8
        assert cost.energy_cost == 20
        assert cost.food_cost == 10
        assert cost.water_cost == 10
        assert cost.stamina_cost == 30


class TestActiveTravel:
    """Test ActiveTravel class"""

    def test_active_travel_creation(self):
        """Test active travel creation"""
        route = TravelRoute("city_a", "city_b", 5, TerrainType.PLAINS, 2)
        plan = TravelPlan(route=route)
        costs = TravelCost(gold_cost=50, time_cost=10)

        active_travel = ActiveTravel(
            plan=plan,
            status=TravelStatus.IN_PROGRESS,
            progress=25.0,
            time_elapsed=2,
            events_occurred=[],
            resources_consumed=costs,
            completion_time=10
        )

        assert active_travel.plan == plan
        assert active_travel.status == TravelStatus.IN_PROGRESS
        assert active_travel.progress == 25.0
        assert active_travel.time_elapsed == 2
        assert active_travel.events_occurred == []
        assert active_travel.resources_consumed == costs
        assert active_travel.completion_time == 10


class TestTravelSystem:
    """Test TravelSystem class"""

    def test_system_initialization(self):
        """Test travel system initialization"""
        system = TravelSystem()
        assert system.active_travels == {}
        assert system.discovered_routes == {}
        assert system.fast_travel_unlocks == {}

    def test_calculate_distance(self):
        """Test distance calculation"""
        system = TravelSystem()
        pos1 = Position(0, 0)
        pos2 = Position(3, 4)

        distance = system.calculate_distance(pos1, pos2)
        assert distance == 7.0

    def test_calculate_travel_cost_basic(self):
        """Test basic travel cost calculation"""
        system = TravelSystem()
        route = TravelRoute("city_a", "city_b", 5, TerrainType.PLAINS, 2)
        plan = TravelPlan(route=route)

        cost = system.calculate_travel_cost(route, plan)

        assert cost.gold_cost > 0
        assert cost.time_cost > 0
        assert cost.energy_cost > 0
        assert cost.food_cost > 0
        assert cost.water_cost > 0
        assert cost.stamina_cost > 0

    def test_calculate_travel_cost_with_party_size(self):
        """Test travel cost with different party sizes"""
        system = TravelSystem()
        route = TravelRoute("city_a", "city_b", 3, TerrainType.PLAINS, 2)

        plan_small = TravelPlan(route=route, party_size=1)
        plan_large = TravelPlan(route=route, party_size=4)

        cost_small = system.calculate_travel_cost(route, plan_small)
        cost_large = system.calculate_travel_cost(route, plan_large)

        # Larger party should cost more resources
        assert cost_large.energy_cost > cost_small.energy_cost
        assert cost_large.food_cost > cost_small.food_cost
        assert cost_large.water_cost > cost_small.water_cost
        assert cost_large.stamina_cost > cost_small.stamina_cost

    def test_calculate_travel_cost_terrain_effects(self):
        """Test travel cost with different terrain types"""
        system = TravelSystem()
        plains_route = TravelRoute("city_a", "city_b", 3, TerrainType.PLAINS, 1)
        mountains_route = TravelRoute("city_a", "city_b", 3, TerrainType.MOUNTAINS, 1)

        plan = TravelPlan(route=plains_route)
        plains_cost = system.calculate_travel_cost(plains_route, plan)

        plan.route = mountains_route
        mountains_cost = system.calculate_travel_cost(mountains_route, plan)

        # Mountains should be more expensive and take longer
        assert mountains_cost.time_cost > plains_cost.time_cost
        assert mountains_cost.gold_cost > plains_cost.gold_cost

    def test_calculate_travel_cost_fast_travel(self):
        """Test fast travel cost calculation"""
        system = TravelSystem()
        route = TravelRoute("city_a", "city_b", 5, TerrainType.PLAINS, 2)

        normal_plan = TravelPlan(route=route, fast_travel=False)
        fast_plan = TravelPlan(route=route, fast_travel=True)

        normal_cost = system.calculate_travel_cost(route, normal_plan)
        fast_cost = system.calculate_travel_cost(route, fast_plan)

        # Fast travel should cost more gold but less time
        assert fast_cost.gold_cost > normal_cost.gold_cost
        assert fast_cost.time_cost < normal_cost.time_cost

    def test_calculate_travel_cost_equipment_bonuses(self):
        """Test equipment bonuses on travel cost"""
        system = TravelSystem()
        route = TravelRoute("city_a", "city_b", 5, TerrainType.PLAINS, 2)

        plan_no_equip = TravelPlan(route=route, equipment=[])
        plan_with_equip = TravelPlan(route=route, equipment=[TravelEquipment.MOUNT])

        cost_no_equip = system.calculate_travel_cost(route, plan_no_equip)
        cost_with_equip = system.calculate_travel_cost(route, plan_with_equip)

        # Equipment should reduce time and cost
        assert cost_with_equip.time_cost < cost_no_equip.time_cost
        assert cost_with_equip.gold_cost <= cost_no_equip.gold_cost

    def test_calculate_encounter_chance_basic(self):
        """Test basic encounter chance calculation"""
        system = TravelSystem()
        route = TravelRoute("city_a", "city_b", 3, TerrainType.PLAINS, 2)
        plan = TravelPlan(route=route, party_size=1)

        # Test with different character levels
        chance_low_level = system.calculate_encounter_chance(route, plan, character_level=1)
        chance_high_level = system.calculate_encounter_chance(route, plan, character_level=10)

        # Higher level should have lower encounter chance
        assert 0 <= chance_low_level <= 0.9
        assert 0 <= chance_high_level <= 0.9
        assert chance_high_level <= chance_low_level

    def test_calculate_encounter_chance_party_size(self):
        """Test encounter chance with different party sizes"""
        system = TravelSystem()
        route = TravelRoute("city_a", "city_b", 5, TerrainType.PLAINS, 3)

        solo_plan = TravelPlan(route=route, party_size=1)
        group_plan = TravelPlan(route=route, party_size=4)

        solo_chance = system.calculate_encounter_chance(route, solo_plan, character_level=5)
        group_chance = system.calculate_encounter_chance(route, group_plan, character_level=5)

        # Group should have lower encounter chance
        assert 0 <= solo_chance <= 0.9
        assert 0 <= group_chance <= 0.9
        assert group_chance <= solo_chance

    def test_calculate_encounter_chance_terrain_effects(self):
        """Test encounter chance with different terrain types"""
        system = TravelSystem()
        safe_route = TravelRoute("city_a", "city_b", 3, TerrainType.PLAINS, 1)
        dangerous_route = TravelRoute("city_a", "city_b", 3, TerrainType.MOUNTAINS, 4)

        plan = TravelPlan(route=safe_route, party_size=2)

        safe_chance = system.calculate_encounter_chance(safe_route, plan, character_level=5)
        dangerous_chance = system.calculate_encounter_chance(dangerous_route, plan, character_level=5)

        # Dangerous terrain should have higher encounter chance
        assert 0 <= safe_chance <= 0.9
        assert 0 <= dangerous_chance <= 0.9
        assert dangerous_chance >= safe_chance

    def test_generate_travel_events(self):
        """Test travel event generation"""
        system = TravelSystem()
        route = TravelRoute("city_a", "city_b", 5, TerrainType.PLAINS, 2)
        plan = TravelPlan(route=route)

        events = system.generate_travel_events(route, plan, character_level=5)

        assert isinstance(events, list)
        # Should have reasonable number of events
        assert len(events) <= 5

        # Events should be sorted by time occurred
        if len(events) > 1:
            for i in range(1, len(events)):
                assert events[i-1].time_occurred <= events[i].time_occurred

    def test_generate_travel_events_structure(self):
        """Test travel event structure"""
        system = TravelSystem()
        route = TravelRoute("city_a", "city_b", 3, TerrainType.FOREST, 2)
        plan = TravelPlan(route=route)

        with patch('random.random', return_value=0.5):  # Force event generation
            events = system.generate_travel_events(route, plan, character_level=5)

            if events:  # If any events were generated
                for event in events:
                    assert isinstance(event.event_type, str)
                    valid_events = [TravelEvent.MERCHANT_ENCOUNTER, TravelEvent.BANDIT_ATTACK, TravelEvent.WEATHER_CHANGE,
                                   TravelEvent.WILD_ANIMAL, TravelEvent.LOST_TRAVELER, TravelEvent.ANCIENT_RUINS,
                                   TravelEvent.NATURAL_RESOURCE, TravelEvent.ROAD_BLOCKAGE, TravelEvent.FRIENDLY_PATROL,
                                   TravelEvent.MYSTERIOUS_STRANGER, TravelEvent.TREASURE_MAP, TravelEvent.EQUIPMENT_FAILURE]
                    assert event.event_type in valid_events
                    assert event.time_occurred > 0
                    assert event.outcome in ["positive", "negative", "neutral"]
                    assert isinstance(event.details, dict)
                    assert isinstance(event.choices, list)

    def test_can_fast_travel_unlocked(self):
        """Test fast travel when unlocked"""
        system = TravelSystem()
        system.unlock_fast_travel("player1")
        system.discover_route("player1", TravelRoute("city_a", "city_b", 3, TerrainType.PLAINS, 1))

        can_travel, reason = system.can_fast_travel("player1", "city_a", "city_b", character_level=5)

        assert can_travel is True
        assert reason == "Fast travel available"

    def test_cannot_fast_travel_locked(self):
        """Test fast travel when not unlocked"""
        system = TravelSystem()

        can_travel, reason = system.can_fast_travel("player1", "city_a", "city_b", character_level=5)

        assert can_travel is False
        assert reason == "Fast travel not unlocked"

    def test_cannot_fast_travel_low_level(self):
        """Test fast travel with low level character"""
        system = TravelSystem()
        system.unlock_fast_travel("player1")

        can_travel, reason = system.can_fast_travel("player1", "city_a", "city_b", character_level=1)

        assert can_travel is False
        assert reason == "Must be at least level 3"

    def test_cannot_fast_travel_not_discovered(self):
        """Test fast travel to undiscovered location"""
        system = TravelSystem()
        system.unlock_fast_travel("player1")

        can_travel, reason = system.can_fast_travel("player1", "city_a", "city_b", character_level=5)

        assert can_travel is False
        assert reason == "Destination not discovered"

    def test_cannot_fast_travel_restricted(self):
        """Test fast travel to restricted location"""
        system = TravelSystem()
        system.unlock_fast_travel("player1")
        restricted_route = TravelRoute("city_a", "city_b", 3, TerrainType.PLAINS, 1, restricted=True)
        system.discover_route("player1", restricted_route)

        can_travel, reason = system.can_fast_travel("player1", "city_a", "city_b", character_level=5)

        assert can_travel is False
        assert reason == "Route is restricted"

    def test_cannot_fast_travel_level_requirement(self):
        """Test fast travel with insufficient level"""
        system = TravelSystem()
        system.unlock_fast_travel("player1")
        level_route = TravelRoute("city_a", "city_b", 3, TerrainType.PLAINS, 1, level_requirement=10)
        system.discover_route("player1", level_route)

        can_travel, reason = system.can_fast_travel("player1", "city_a", "city_b", character_level=5)

        assert can_travel is False
        assert reason == "Requires level 10"

    def test_initiate_travel(self):
        """Test initiating travel"""
        system = TravelSystem()
        route = TravelRoute("city_a", "city_b", 3, TerrainType.PLAINS, 2)
        plan = TravelPlan(route=route)

        active_travel = system.initiate_travel("player1", plan, character_level=5)

        assert isinstance(active_travel, ActiveTravel)
        assert active_travel.status == TravelStatus.IN_PROGRESS
        assert active_travel.progress == 0.0
        assert active_travel.time_elapsed == 0
        assert "player1" in system.active_travels

    def test_update_travel_progress(self):
        """Test updating travel progress"""
        system = TravelSystem()
        route = TravelRoute("city_a", "city_b", 4, TerrainType.PLAINS, 2)
        plan = TravelPlan(route=route)

        active_travel = system.initiate_travel("player1", plan, character_level=5)

        # Update after 2 hours
        updated = system.update_travel("player1", hours_passed=2)

        assert updated == active_travel
        assert updated.time_elapsed == 2
        assert updated.progress > 0

        # Check not complete yet
        assert updated.status == TravelStatus.IN_PROGRESS

    def test_update_travel_completion(self):
        """Test updating travel to completion"""
        system = TravelSystem()
        route = TravelRoute("city_a", "city_b", 2, TerrainType.PLAINS, 1)
        plan = TravelPlan(route=route)

        active_travel = system.initiate_travel("player1", plan, character_level=5)
        completion_time = active_travel.completion_time

        # Update past completion time
        updated = system.update_travel("player1", hours_passed=completion_time + 1)

        assert updated.status == TravelStatus.COMPLETED
        assert updated.progress == 100.0

    def test_complete_travel(self):
        """Test completing travel"""
        system = TravelSystem()
        route = TravelRoute("city_a", "city_b", 3, TerrainType.PLAINS, 2)
        plan = TravelPlan(route=route)

        active_travel = system.initiate_travel("player1", plan, character_level=5)

        success = system.complete_travel("player1")

        assert success is True
        assert active_travel.status == TravelStatus.COMPLETED
        assert "player1" in system.discovered_routes

    def test_cancel_travel(self):
        """Test canceling travel"""
        system = TravelSystem()
        route = TravelRoute("city_a", "city_b", 3, TerrainType.PLAINS, 2)
        plan = TravelPlan(route=route)

        active_travel = system.initiate_travel("player1", plan, character_level=5)

        success = system.cancel_travel("player1")

        assert success is True
        assert "player1" not in system.active_travels

    def test_get_travel_status(self):
        """Test getting travel status"""
        system = TravelSystem()
        route = TravelRoute("city_a", "city_b", 3, TerrainType.PLAINS, 2)
        plan = TravelPlan(route=route)

        # Status before travel
        status = system.get_travel_status("player1")
        assert status is None

        # Status after initiating travel
        active_travel = system.initiate_travel("player1", plan, character_level=5)
        status = system.get_travel_status("player1")

        assert status == active_travel
        assert status.status == TravelStatus.IN_PROGRESS

    def test_discover_route(self):
        """Test discovering routes"""
        system = TravelSystem()
        route = TravelRoute("city_a", "city_b", 3, TerrainType.PLAINS, 2)

        system.discover_route("player1", route)

        assert "player1" in system.discovered_routes
        assert route in system.discovered_routes["player1"]

    def test_discover_route_duplicate(self):
        """Test discovering duplicate routes"""
        system = TravelSystem()
        route = TravelRoute("city_a", "city_b", 3, TerrainType.PLAINS, 2)

        system.discover_route("player1", route)
        system.discover_route("player1", route)  # Same route again

        # Should only have one instance
        routes = system.discovered_routes["player1"]
        assert len(routes) == 1
        assert routes[0] == route

    def test_unlock_fast_travel(self):
        """Test unlocking fast travel"""
        system = TravelSystem()

        assert system.fast_travel_unlocks.get("player1", False) is False

        system.unlock_fast_travel("player1")

        assert system.fast_travel_unlocks["player1"] is True

    def test_get_available_destinations(self):
        """Test getting available fast travel destinations"""
        system = TravelSystem()
        system.unlock_fast_travel("player1")

        # Add some discovered routes
        route1 = TravelRoute("city_a", "city_b", 3, TerrainType.PLAINS, 1)
        route2 = TravelRoute("city_a", "city_c", 5, TerrainType.MOUNTAINS, 3)
        restricted_route = TravelRoute("city_a", "city_d", 4, TerrainType.PLAINS, 2, restricted=True)

        system.discover_route("player1", route1)
        system.discover_route("player1", route2)
        system.discover_route("player1", restricted_route)

        destinations = system.get_available_destinations("player1", "city_a", character_level=5)

        # Should include non-restricted routes
        assert route1 in destinations
        assert route2 in destinations
        # Should not include restricted route
        assert restricted_route not in destinations

    def test_calculate_fast_travel_cost(self):
        """Test fast travel cost calculation"""
        system = TravelSystem()
        route = TravelRoute("city_a", "city_b", 5, TerrainType.PLAINS, 2)

        fast_cost = system.calculate_fast_travel_cost(route, character_level=5)

        # Fast travel should have specific characteristics
        assert fast_cost.gold_cost > 0
        assert fast_cost.time_cost > 0
        assert fast_cost.time_cost <= 1  # Should be very fast

    def test_generate_event_details_merchant(self):
        """Test generating merchant encounter details"""
        system = TravelSystem()

        details = system._generate_event_details(TravelEvent.MERCHANT_ENCOUNTER, TerrainType.PLAINS, 5)

        assert "merchant_type" in details
        assert "prices" in details
        assert "special_items" in details
        assert "reputation" in details
        assert details["special_items"] >= 0
        assert details["merchant_type"] in ["weapons", "potions", "general_goods", "luxury_items"]

    def test_generate_event_details_bandit(self):
        """Test generating bandit attack details"""
        system = TravelSystem()

        details = system._generate_event_details(TravelEvent.BANDIT_ATTACK, TerrainType.FOREST, 5)

        assert "bandit_count" in details
        assert "difficulty" in details
        assert "demand_type" in details
        assert "negotiation_possible" in details
        assert 2 <= details["bandit_count"] <= 8
        assert 1 <= details["difficulty"] <= 5

    def test_generate_event_details_weather(self):
        """Test generating weather change details"""
        system = TravelSystem()

        details = system._generate_event_details(TravelEvent.WEATHER_CHANGE, TerrainType.MOUNTAINS, 5)

        assert "weather_type" in details
        assert "duration" in details
        assert "visibility" in details
        assert "movement_impact" in details
        assert 1 <= details["duration"] <= 8

    def test_generate_event_choices(self):
        """Test generating event choices"""
        system = TravelSystem()

        # Test event types that should have choices
        choice_events = [
            TravelEvent.LOST_TRAVELER,
            TravelEvent.ANCIENT_RUINS,
            TravelEvent.ROAD_BLOCKAGE,
            TravelEvent.MYSTERIOUS_STRANGER
        ]

        for event_type in choice_events:
            choices = system._generate_event_choices(event_type)
            assert isinstance(choices, list)
            if choices:  # If choices were generated
                assert len(choices) >= 2
                assert all(isinstance(choice, str) for choice in choices)

        # Test event types that should not have choices
        non_choice_events = [TravelEvent.MERCHANT_ENCOUNTER, TravelEvent.WEATHER_CHANGE]

        for event_type in non_choice_events:
            choices = system._generate_event_choices(event_type)
            assert choices == []


class TestTravelSystemIntegration:
    """Integration tests for travel system"""

    def test_complete_travel_journey(self):
        """Test a complete travel journey from start to finish"""
        system = TravelSystem()
        route = TravelRoute("home_city", "destination_city", 4, TerrainType.PLAINS, 2)
        plan = TravelPlan(route=route, party_size=2, equipment=[TravelEquipment.MOUNT])

        # Start travel
        active_travel = system.initiate_travel("player1", plan, character_level=5)
        assert active_travel.status == TravelStatus.IN_PROGRESS

        # Update progress over time
        hours_per_update = 2
        updates_needed = (active_travel.completion_time // hours_per_update) + 1

        for i in range(updates_needed):
            updated = system.update_travel("player1", hours_passed=hours_per_update)
            if updated.status == TravelStatus.COMPLETED:
                break

        # Complete the journey
        success = system.complete_travel("player1")
        assert success is True

        # Verify destination is discovered
        discovered_routes = system.discovered_routes.get("player1", [])
        destination_routes = [r for r in discovered_routes if r.to_location == "destination_city"]
        assert len(destination_routes) > 0

    def test_multiple_travelers(self):
        """Test system handling multiple simultaneous travelers"""
        system = TravelSystem()

        route1 = TravelRoute("city_a", "city_b", 3, TerrainType.PLAINS, 1)
        route2 = TravelRoute("city_c", "city_d", 5, TerrainType.FOREST, 3)

        plan1 = TravelPlan(route=route1)
        plan2 = TravelPlan(route=route2, party_size=3)

        # Start multiple travels
        travel1 = system.initiate_travel("player1", plan1, character_level=5)
        travel2 = system.initiate_travel("player2", plan2, character_level=8)

        # Verify both are tracked separately
        assert len(system.active_travels) == 2
        assert system.get_travel_status("player1") == travel1
        assert system.get_travel_status("player2") == travel2

        # Update one traveler
        system.update_travel("player1", hours_passed=1)

        # Verify only the updated traveler changed
        assert system.get_travel_status("player1").time_elapsed == 1
        assert system.get_travel_status("player2").time_elapsed == 0

    def test_fast_travel_workflow(self):
        """Test complete fast travel workflow"""
        system = TravelSystem()

        # Initial state - cannot fast travel
        can_travel, reason = system.can_fast_travel("player1", "city_a", "city_b", 5)
        assert can_travel is False

        # Discover route through normal travel
        route = TravelRoute("city_a", "city_b", 3, TerrainType.PLAINS, 1)
        plan = TravelPlan(route=route)

        system.initiate_travel("player1", plan, character_level=5)
        system.complete_travel("player1")

        # Still cannot fast travel (not unlocked)
        can_travel, reason = system.can_fast_travel("player1", "city_a", "city_b", 5)
        assert can_travel is False

        # Unlock fast travel
        system.unlock_fast_travel("player1")

        # Now can fast travel
        can_travel, reason = system.can_fast_travel("player1", "city_a", "city_b", 5)
        assert can_travel is True

        # Get destinations
        destinations = system.get_available_destinations("player1", "city_a", 5)
        assert len(destinations) >= 1

    def test_terrain_specific_equipment(self):
        """Test terrain-specific equipment requirements"""
        system = TravelSystem()

        # Mountain route without climbing gear
        mountain_route = TravelRoute("city_a", "city_b", 3, TerrainType.MOUNTAINS, 4)
        plan_without_gear = TravelPlan(route=mountain_route, equipment=[])

        cost_without_gear = system.calculate_travel_cost(mountain_route, plan_without_gear)

        # Mountain route with climbing gear
        plan_with_gear = TravelPlan(route=mountain_route, equipment=[TravelEquipment.CLIMBING_GEAR])

        cost_with_gear = system.calculate_travel_cost(mountain_route, plan_with_gear)

        # Climbing gear should help in mountains
        assert cost_with_gear.time_cost < cost_without_gear.time_cost

        # Coastal route with boat
        coastal_route = TravelRoute("city_a", "city_b", 5, TerrainType.COASTAL, 2)
        plan_with_boat = TravelPlan(route=coastal_route, equipment=[TravelEquipment.BOAT])

        coastal_cost = system.calculate_travel_cost(coastal_route, plan_with_boat)
        plan_without_boat = TravelPlan(route=coastal_route, equipment=[])
        coastal_cost_without = system.calculate_travel_cost(coastal_route, plan_without_boat)

        # Boat should help in coastal terrain
        assert coastal_cost.time_cost < coastal_cost_without.time_cost

    def test_encounter_probability_progression(self):
        """Test that encounter probability scales correctly"""
        system = TravelSystem()

        # Test different distances
        short_route = TravelRoute("city_a", "city_b", 2, TerrainType.PLAINS, 2)
        long_route = TravelRoute("city_a", "city_c", 8, TerrainType.PLAINS, 2)

        plan = TravelPlan(route=short_route, party_size=2)

        short_chance = system.calculate_encounter_chance(short_route, plan, character_level=5)
        long_chance = system.calculate_encounter_chance(long_route, plan, character_level=5)

        # Longer route should have higher encounter chance
        assert long_chance >= short_chance

        # Test different danger levels
        safe_route = TravelRoute("city_a", "city_b", 4, TerrainType.PLAINS, 1)
        dangerous_route = TravelRoute("city_a", "city_b", 4, TerrainType.PLAINS, 5)

        safe_chance = system.calculate_encounter_chance(safe_route, plan, character_level=5)
        dangerous_chance = system.calculate_encounter_chance(dangerous_route, plan, character_level=5)

        # More dangerous route should have higher encounter chance
        assert dangerous_chance >= safe_chance


class TestUtilityFunctions:
    """Test utility functions"""

    def test_get_all_terrain_types(self):
        """Test getting all terrain types"""
        types = get_all_terrain_types()
        assert isinstance(types, list)
        assert len(types) == 10  # 10 terrain types defined
        assert all(isinstance(t, str) for t in types)

    def test_get_all_travel_methods(self):
        """Test getting all travel methods"""
        methods = get_all_travel_methods()
        assert isinstance(methods, list)
        assert len(methods) == 6  # 6 travel methods defined
        assert all(isinstance(m, str) for m in methods)

    def test_get_all_travel_equipment(self):
        """Test getting all travel equipment"""
        equipment = get_all_travel_equipment()
        assert isinstance(equipment, list)
        assert len(equipment) == 8  # 8 equipment types defined
        assert all(isinstance(e, str) for e in equipment)

    def test_calculate_route_difficulty(self):
        """Test route difficulty calculation"""
        easy_route = TravelRoute("city_a", "city_b", 3, TerrainType.PLAINS, 1)
        hard_route = TravelRoute("city_a", "city_b", 5, TerrainType.MOUNTAINS, 5)

        # Test with appropriate level
        easy_difficulty = calculate_route_difficulty(easy_route, character_level=5)
        hard_difficulty = calculate_route_difficulty(hard_route, character_level=5)

        assert easy_difficulty == "EASY" or easy_difficulty == "MODERATE"
        assert hard_difficulty == "HARD" or hard_difficulty == "VERY HARD"

        # Test with insufficient level
        impossible_difficulty = calculate_route_difficulty(
            TravelRoute("city_a", "city_b", 3, TerrainType.PLAINS, 1, level_requirement=10),
            character_level=5
        )
        assert impossible_difficulty == "IMPOSSIBLE"

    def test_validate_travel_requirements(self):
        """Test travel requirement validation"""
        normal_route = TravelRoute("city_a", "city_b", 3, TerrainType.PLAINS, 1)
        level_route = TravelRoute("city_a", "city_b", 3, TerrainType.PLAINS, 1, level_requirement=10)
        restricted_route = TravelRoute("city_a", "city_b", 3, TerrainType.PLAINS, 1, restricted=True)

        # Normal route should pass
        assert validate_travel_requirements(normal_route, character_level=5, equipment=[]) is True

        # Level requirement should fail
        assert validate_travel_requirements(level_route, character_level=5, equipment=[]) is False

        # Level requirement should pass with sufficient level
        assert validate_travel_requirements(level_route, character_level=10, equipment=[]) is True

        # Restricted route should fail for low level
        assert validate_travel_requirements(restricted_route, character_level=5, equipment=[]) is False

        # Restricted route should pass for high level
        assert validate_travel_requirements(restricted_route, character_level=15, equipment=[]) is True

        # Mountain route should require climbing gear
        mountain_route = TravelRoute("city_a", "city_b", 3, TerrainType.MOUNTAINS, 4)
        assert validate_travel_requirements(mountain_route, character_level=10, equipment=[]) is False
        assert validate_travel_requirements(mountain_route, character_level=10, equipment=[TravelEquipment.CLIMBING_GEAR]) is True


class TestEdgeCases:
    """Test edge cases and boundary conditions"""

    def test_zero_distance_travel(self):
        """Test travel with zero distance"""
        system = TravelSystem()
        route = TravelRoute("city_a", "city_a", 0, TerrainType.PLAINS, 1)
        plan = TravelPlan(route=route)

        cost = system.calculate_travel_cost(route, plan)

        # Even zero distance should have minimum costs
        assert cost.time_cost >= 0
        assert cost.gold_cost >= 0

    def test_maximum_distance_travel(self):
        """Test travel with very long distance"""
        system = TravelSystem()
        route = TravelRoute("city_a", "city_z", 50, TerrainType.PLAINS, 2)
        plan = TravelPlan(route=route)

        cost = system.calculate_travel_cost(route, plan)

        # Long distance should have high costs
        assert cost.time_cost > 0
        assert cost.gold_cost > 0

    def test_maximum_character_level(self):
        """Test encounter chance with maximum character level"""
        system = TravelSystem()
        route = TravelRoute("city_a", "city_b", 5, TerrainType.MOUNTAINS, 5)
        plan = TravelPlan(route=route, party_size=1)

        # Level 50 (way above normal range)
        chance = system.calculate_encounter_chance(route, plan, character_level=50)

        # Should have significant reduction
        assert 0 <= chance <= 0.5

    def test_minimum_character_level(self):
        """Test encounter chance with minimum character level"""
        system = TravelSystem()
        route = TravelRoute("city_a", "city_b", 5, TerrainType.MOUNTAINS, 5)
        plan = TravelPlan(route=route, party_size=1)

        # Level 1 (minimum)
        chance = system.calculate_encounter_chance(route, plan, character_level=1)

        # Should have no level reduction
        assert 0 <= chance <= 0.9

    def test_maximum_party_size(self):
        """Test travel with very large party"""
        system = TravelSystem()
        route = TravelRoute("city_a", "city_b", 3, TerrainType.PLAINS, 2)
        plan = TravelPlan(route=route, party_size=10)

        cost = system.calculate_travel_cost(route, plan)

        # Large party should significantly increase resource costs
        assert cost.food_cost >= 10  # At least 10 food units
        assert cost.water_cost >= 10  # At least 10 water units
        assert cost.energy_cost >= 20  # At least 20 energy units

    def test_all_equipment_combinations(self):
        """Test travel with all possible equipment"""
        system = TravelSystem()
        route = TravelRoute("city_a", "city_b", 5, TerrainType.PLAINS, 2)
        all_equipment = [TravelEquipment.MOUNT, TravelEquipment.CART, TravelEquipment.BOAT, TravelEquipment.CLIMBING_GEAR, TravelEquipment.COMPASS, TravelEquipment.LANTERN, TravelEquipment.CLOAK, TravelEquipment.SURVIVAL_KIT]
        plan = TravelPlan(route=route, equipment=all_equipment)

        cost = system.calculate_travel_cost(route, plan)

        # Having all equipment should provide significant benefits
        assert cost.gold_cost >= 0
        assert cost.time_cost >= 0

        # Equipment should be capped at 50% reduction
        # Time should be reduced but not eliminated
        assert cost.time_cost > 0

    def test_extremely_dangerous_route(self):
        """Test travel on maximum danger route"""
        system = TravelSystem()
        route = TravelRoute("city_a", "city_b", 5, TerrainType.VOLCANIC, 5)  # Most dangerous
        plan = TravelPlan(route=route, party_size=1)

        cost = system.calculate_travel_cost(route, plan)
        chance = system.calculate_encounter_chance(route, plan, character_level=5)

        # Should be very expensive and dangerous
        assert cost.time_cost > 0
        assert cost.gold_cost > 0
        assert chance >= 0.15  # At least 15% encounter chance (actual: ~0.19)

    def test_update_nonexistent_travel(self):
        """Test updating travel for non-existent traveler"""
        system = TravelSystem()

        result = system.update_travel("nonexistent", hours_passed=5)

        assert result is None

    def test_complete_nonexistent_travel(self):
        """Test completing travel for non-existent traveler"""
        system = TravelSystem()

        success = system.complete_travel("nonexistent")

        assert success is False

    def test_cancel_nonexistent_travel(self):
        """Test canceling travel for non-existent traveler"""
        system = TravelSystem()

        success = system.cancel_travel("nonexistent")

        assert success is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])