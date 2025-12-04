"""
Unit Tests for the refactored Travel System, accessed through the WorldSystem facade.
"""

import pytest
from unittest.mock import MagicMock, patch
from core.systems.world.facade import WorldSystem
from core.systems.world.services.travel_service import (
    TravelService,
    PathedRoute,
    TravelPlan,
    TravelRouteInfo,
    TravelStatus,
    TerrainType,
)
from core.systems.world.domain.world import World, Location, Coordinates, LocationType

@pytest.fixture
def mock_world():
    """Fixture to create a mock World object for testing."""
    world = MagicMock(spec=World)
    world.get_connection = MagicMock()
    
    # Mock locations
    locations = {
        "startville": Location(id="startville", name="Startville", coordinates=Coordinates(x=0, y=0), location_type=LocationType.VILLAGE, description="A starting town.", available_services=[]),
        "endburg": Location(id="endburg", name="Endburg", coordinates=Coordinates(x=10, y=20), location_type=LocationType.CITY, description="A large city.", available_services=[]),
    }
    world.get_location.side_effect = lambda loc_id: locations.get(loc_id)
    world.locations = locations
    
    # Mock connections
    connection = MagicMock(to_location_id="endburg", can_travel=MagicMock(return_value=True), difficulty=0.2, travel_time=10)
    connections = {
        "startville": [connection]
    }
    world.get_connections_from.side_effect = lambda loc_id: connections.get(loc_id, [])
    world.get_connection.return_value = connection
    
    world.calculate_travel_time.return_value = 10
    
    return world

@pytest.fixture
def world_system(mock_world):
    """Fixture to create a WorldSystem with a mocked TravelService."""
    with patch('core.systems.world.facade.WorldService'), \
         patch('core.systems.world.facade.LocationService'):
        system = WorldSystem()
        # Directly replace the travel_service with one using the mock_world
        system.travel_service = TravelService(mock_world)
        return system

def test_find_route(world_system):
    """Test finding a route between two locations."""
    route = world_system.travel_service.find_route("startville", "endburg", {})
    assert route is not None
    assert isinstance(route, PathedRoute)
    assert route.from_location == "startville"
    assert route.to_location == "endburg"
    assert len(route.steps) > 0

def test_initiate_travel(world_system):
    """Test initiating a travel plan."""
    route_info = TravelRouteInfo(
        from_location="startville",
        to_location="endburg",
        distance=30,
        terrain=TerrainType.PLAINS,
        danger_level=1,
    )
    plan = TravelPlan(route=route_info)
    
    active_travel = world_system.travel_service.initiate_travel("player1", plan, character_level=1)
    
    assert active_travel is not None
    assert active_travel.status == TravelStatus.IN_PROGRESS
    assert world_system.travel_service.get_travel_status("player1") == active_travel

def test_update_travel(world_system):
    """Test updating travel progress."""
    route_info = TravelRouteInfo(
        from_location="startville",
        to_location="endburg",
        distance=30,
        terrain=TerrainType.PLAINS,
        danger_level=1,
    )
    plan = TravelPlan(route=route_info)
    
    active_travel = world_system.travel_service.initiate_travel("player1", plan, character_level=1)
    
    # Simulate time passing
    completion_time = active_travel.completion_time
    world_system.travel_service.update_travel("player1", completion_time // 2)
    
    updated_travel = world_system.travel_service.get_travel_status("player1")
    assert updated_travel.progress > 0
    assert updated_travel.progress < 100
    
    # Simulate more time passing to complete the travel
    world_system.travel_service.update_travel("player1", completion_time)
    updated_travel = world_system.travel_service.get_travel_status("player1")
    assert updated_travel.status == TravelStatus.COMPLETED
    assert updated_travel.progress == 100.0

def test_get_available_destinations(world_system):
    """Test getting available destinations from a location."""
    destinations = world_system.travel_service.get_available_destinations("startville", {})
    assert destinations is not None
    assert len(destinations) > 0
    assert destinations[0]['name'] == 'Endburg'
