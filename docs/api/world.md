# World System

## `dungeon_locations.py`

World System Update for Dungeon Locations
FOCUS: Add dungeon entrances to existing world

### Classes

### Functions

### `add_dungeon_locations_to_world`

Add dungeon locations to world system

**Signature:** `add_dungeon_locations_to_world()`

### `get_dungeon_entrance`

Get dungeon entrance information (BDD compliant)

**Signature:** `get_dungeon_entrance(dungeon_name: str) -> Dict`

### `get_dungeon_locations`

Get all dungeon locations

**Signature:** `get_dungeon_locations()`

## `facade.py`

Facade for world system operations

### Classes

### class `WorldSystem`

Facade for all world system operations

#### `add_connection`

Add travel connection between locations

**Signature:** `add_connection(self, connection_data: Dict) -> bool`

#### `add_location`

Add new location to world

**Signature:** `add_location(self, location_data: Dict) -> bool`

#### `advance_time`

Advance world time

**Signature:** `advance_time(self, minutes: int) -> bool`

#### `calculate_distance`

Calculate distance between two locations

**Signature:** `calculate_distance(self, from_location_id: str, to_location_id: str) -> Optional[float]`

#### `discover_location`

Discover a location for character

**Signature:** `discover_location(self, location_id: str, character_data: Dict) -> Dict`

#### `find_route`

Find best route between two locations

**Signature:** `find_route(self, from_location_id: str, to_location_id: str, character_data: Dict) -> Optional[Dict]`

#### `get_accessible_locations`

Get all locations accessible to character

**Signature:** `get_accessible_locations(self, character_data: Dict) -> List[Dict]`

#### `get_available_destinations`

Get all available destinations from a location

**Signature:** `get_available_destinations(self, from_location_id: str, character_data: Dict) -> List[Dict]`

#### `get_character_context`

Get complete world context for character

**Signature:** `get_character_context(self, character_data: Dict) -> Dict`

#### `get_current_time`

Get current world time

**Signature:** `get_current_time(self) -> str`

#### `get_location_details`

Get detailed information about a location

**Signature:** `get_location_details(self, location_id: str) -> Optional[Dict]`

#### `get_location_statistics`

Get statistics for a location

**Signature:** `get_location_statistics(self, location_id: str) -> Optional[Dict]`

#### `get_locations_by_service`

Get locations that provide specific service

**Signature:** `get_locations_by_service(self, service: str, character_data: Dict) -> List[Dict]`

#### `get_locations_in_range`

Get locations within range of a center location

**Signature:** `get_locations_in_range(self, center_location_id: str, max_distance: float, character_data: Dict) -> List[Dict]`

#### `get_starting_location`

Get starting location for new characters

**Signature:** `get_starting_location(self) -> Optional[Dict]`

#### `get_travel_statistics`

Get travel statistics for character

**Signature:** `get_travel_statistics(self, character_data: Dict) -> Dict`

#### `get_world_info`

Get world information summary

**Signature:** `get_world_info(self) -> Dict`

#### `get_world_overview`

Get overview of all locations in world

**Signature:** `get_world_overview(self, character_data: Dict) -> Dict`

#### `remove_location`

Remove location from world

**Signature:** `remove_location(self, location_id: str) -> bool`

#### `search_locations`

Search locations by name or type

**Signature:** `search_locations(self, query: str, character_data: Dict) -> List[Dict]`

#### `simulate_travel`

Simulate travel along a route

**Signature:** `simulate_travel(self, route_data: Dict, character_data: Dict) -> Dict`

#### `validate_world_integrity`

Validate world data integrity

**Signature:** `validate_world_integrity(self) -> List[str]`

### Functions

### `advance_time`

Advance world time (backward compatibility)

**Signature:** `advance_time(minutes: int) -> bool`

### `find_route`

Find route between locations (backward compatibility)

**Signature:** `find_route(from_location_id: str, to_location_id: str, character_data: Dict) -> Optional[Dict]`

### `get_current_time`

Get current world time (backward compatibility)

**Signature:** `get_current_time() -> str`

### `get_location_details`

Get location details (backward compatibility)

**Signature:** `get_location_details(location_id: str) -> Optional[Dict]`

### `get_starting_location`

Get starting location (backward compatibility)

**Signature:** `get_starting_location() -> Optional[Dict]`

### `get_world_info`

Get world information (backward compatibility)

**Signature:** `get_world_info() -> Dict`

## `memory_repository.py`

Memory repository implementations for world data

### Classes

### class `MemoryLocationRepository`

In-memory location repository

#### `delete_location`

Delete location by ID

**Signature:** `delete_location(self, world_id: str, location_id: str) -> bool`

#### `list_locations`

List all locations in world

**Signature:** `list_locations(self, world_id: str) -> List[core.systems.world.domain.world.Location]`

#### `load_location`

Load location by ID

**Signature:** `load_location(self, world_id: str, location_id: str) -> Optional[core.systems.world.domain.world.Location]`

#### `save_location`

Save location to world storage

**Signature:** `save_location(self, world_id: str, location: core.systems.world.domain.world.Location) -> bool`

#### `search_locations`

Search locations by query

**Signature:** `search_locations(self, world_id: str, query: str) -> List[core.systems.world.domain.world.Location]`

### class `MemoryTravelConnectionRepository`

In-memory travel connection repository

#### `delete_connection`

Delete connection between locations

**Signature:** `delete_connection(self, world_id: str, from_location_id: str, to_location_id: str) -> bool`

#### `list_connections`

List all connections in world

**Signature:** `list_connections(self, world_id: str) -> List[core.systems.world.domain.world.TravelConnection]`

#### `load_connections_from`

Load all connections from a location

**Signature:** `load_connections_from(self, world_id: str, from_location_id: str) -> List[core.systems.world.domain.world.TravelConnection]`

#### `save_connection`

Save travel connection to world storage

**Signature:** `save_connection(self, world_id: str, connection: core.systems.world.domain.world.TravelConnection) -> bool`

### class `MemoryWorldRepository`

In-memory world repository

#### `delete_world`

Delete world by ID

**Signature:** `delete_world(self, world_id: str) -> bool`

#### `list_worlds`

List all worlds

**Signature:** `list_worlds(self) -> List[Dict]`

#### `load_world`

Load world by ID

**Signature:** `load_world(self, world_id: str) -> Optional[core.systems.world.domain.world.World]`

#### `save_world`

Save world to memory storage

**Signature:** `save_world(self, world: core.systems.world.domain.world.World) -> bool`

### Functions

## `world_service.py`

World business logic services

### Classes

### class `WorldService`

Service for world management and navigation logic

#### `add_connection`

Add travel connection between locations

**Signature:** `add_connection(self, connection_data: Dict) -> bool`

#### `add_location`

Add new location to world

**Signature:** `add_location(self, location_data: Dict) -> bool`

#### `advance_time`

Advance world time

**Signature:** `advance_time(self, minutes: int) -> bool`

#### `get_accessible_locations`

Get all locations accessible to character

**Signature:** `get_accessible_locations(self, character_data: Dict) -> List[core.systems.world.domain.world.Location]`

#### `get_current_time`

Get current world time as string

**Signature:** `get_current_time(self) -> str`

#### `get_location_info`

Get detailed information about a location

**Signature:** `get_location_info(self, location_id: str) -> Optional[Dict]`

#### `get_locations_by_type`

Get all locations of specific type

**Signature:** `get_locations_by_type(self, location_type: str) -> List[Dict]`

#### `get_starting_location`

Get starting location for new characters

**Signature:** `get_starting_location(self) -> Optional[core.systems.world.domain.world.Location]`

#### `get_world_info`

Get world information summary

**Signature:** `get_world_info(self) -> Dict`

#### `remove_location`

Remove location from world

**Signature:** `remove_location(self, location_id: str) -> bool`

#### `validate_world_integrity`

Validate world data integrity

**Signature:** `validate_world_integrity(self) -> List[str]`

### Functions

## `travel_service.py`

Travel logic and route calculation services

### Classes

### class `ActiveTravel`

Represents currently active travel

### class `PathedRoute`

Travel route with multiple steps (from existing TravelRoute)

#### `get_summary`

Get route summary

**Signature:** `get_summary(self) -> Dict`

### class `Position`

Position coordinates for locations

#### `distance_to`

Calculate Manhattan distance to another position

**Signature:** `distance_to(self, other: 'Position') -> float`

### class `TerrainType`

Types of terrain that affect travel

### class `TravelCost`

Represents the costs associated with travel

### class `TravelEquipment`

Special equipment that aids travel

### class `TravelEvent`

Types of events that can occur during travel

### class `TravelEventData`

Represents an event that occurs during travel

### class `TravelMethod`

Methods of travel available to players

### class `TravelPlan`

Represents a planned travel journey

### class `TravelRouteInfo`

Represents a travel route between locations (from legacy TravelRoute)

### class `TravelService`

Service for travel logic, route calculation, and simulation

#### `calculate_distance`

Calculate travel distance between two locations using world data.

**Signature:** `calculate_distance(self, from_location_id: str, to_location_id: str) -> float`

#### `calculate_encounter_chance`

Calculate encounter probability

**Signature:** `calculate_encounter_chance(self, route: core.systems.world.services.travel_service.TravelRouteInfo, plan: core.systems.world.services.travel_service.TravelPlan, character_level: int) -> float`

#### `calculate_travel_cost`

Calculate comprehensive travel costs

**Signature:** `calculate_travel_cost(self, route: core.systems.world.services.travel_service.TravelRouteInfo, plan: core.systems.world.services.travel_service.TravelPlan) -> core.systems.world.services.travel_service.TravelCost`

#### `find_route`

Find best route between two locations using pathfinding

**Signature:** `find_route(self, from_location_id: str, to_location_id: str, character_data: Dict) -> Optional[core.systems.world.services.travel_service.PathedRoute]`

#### `generate_travel_events`

Generate random events for a journey

**Signature:** `generate_travel_events(self, route: core.systems.world.services.travel_service.TravelRouteInfo, plan: core.systems.world.services.travel_service.TravelPlan, character_level: int) -> List[core.systems.world.services.travel_service.TravelEventData]`

#### `get_available_destinations`

Get all available destinations from a location

**Signature:** `get_available_destinations(self, from_location_id: str, character_data: Dict) -> List[Dict]`

#### `get_travel_status`

Get current travel status

**Signature:** `get_travel_status(self, player_id: str) -> Optional[core.systems.world.services.travel_service.ActiveTravel]`

#### `initiate_travel`

Start a new travel journey

**Signature:** `initiate_travel(self, player_id: str, plan: core.systems.world.services.travel_service.TravelPlan, character_level: int) -> core.systems.world.services.travel_service.ActiveTravel`

#### `update_travel`

Update travel progress

**Signature:** `update_travel(self, player_id: str, hours_passed: int) -> Optional[core.systems.world.services.travel_service.ActiveTravel]`

### class `TravelStatus`

Status of ongoing travel

### Functions

## `location_service.py`

Location management and operations services

### Classes

### class `LocationService`

Service for location management and operations

#### `calculate_distance`

Calculate distance between two locations

**Signature:** `calculate_distance(self, from_location_id: str, to_location_id: str) -> Optional[float]`

#### `discover_location`

Discover a location for character

**Signature:** `discover_location(self, location_id: str, character_data: Dict) -> Dict`

#### `get_location_details`

Get detailed information about a location

**Signature:** `get_location_details(self, location_id: str) -> Optional[Dict]`

#### `get_location_statistics`

Get statistics for a location

**Signature:** `get_location_statistics(self, location_id: str) -> Optional[Dict]`

#### `get_locations_by_service`

Get locations that provide specific service

**Signature:** `get_locations_by_service(self, service: str, character_data: Dict) -> List[Dict]`

#### `get_locations_in_range`

Get locations within range of a center location

**Signature:** `get_locations_in_range(self, center_location_id: str, max_distance: float, character_data: Dict) -> List[Dict]`

#### `get_world_overview`

Get overview of all locations in world

**Signature:** `get_world_overview(self, character_data: Dict) -> Dict`

#### `search_locations`

Search locations by name or type

**Signature:** `search_locations(self, query: str, character_data: Dict) -> List[Dict]`

#### `update_location_status`

Update location status (weather, events, etc.)

**Signature:** `update_location_status(self, location_id: str, updates: Dict) -> bool`

### Functions

## `world.py`

World domain entities and value objects

### Classes

### class `Coordinates`

Geographic coordinates for location

#### `distance_to`

Calculate distance to another coordinate

**Signature:** `distance_to(self, other: 'Coordinates') -> float`

### class `GeographyType`

Types of geography for BDD testing

### class `Location`

Location entity in the game world

#### `get_summary`

Get location summary

**Signature:** `get_summary(self) -> Dict[str, <built-in function any>]`

#### `has_service`

Check if location provides specific service

**Signature:** `has_service(self, service: str) -> bool`

#### `is_accessible_by_level`

Check if location is accessible by character level

**Signature:** `is_accessible_by_level(self, character_level: int) -> bool`

### class `LocationType`

Types of locations in the game world

### class `TravelConnection`

Connection between two locations

#### `can_travel`

Check if character can travel via this connection

**Signature:** `can_travel(self, character_data: Dict) -> bool`

#### `get_total_requirements`

Get human-readable requirements string

**Signature:** `get_total_requirements(self) -> str`

### class `TravelRequirement`

Travel requirement between locations

#### `is_met`

Check if requirement is met by character

**Signature:** `is_met(self, character_data: Dict) -> bool`

### class `TravelRequirementType`

Types of travel requirements between locations

### class `World`

World aggregate root entity

#### `add_connection`

Add travel connection between locations

**Signature:** `add_connection(self, connection: core.systems.world.domain.world.TravelConnection) -> bool`

#### `add_location`

Add location to world

**Signature:** `add_location(self, location: core.systems.world.domain.world.Location) -> bool`

#### `advance_time`

Advance world time

**Signature:** `advance_time(self, minutes: int) -> None`

#### `calculate_travel_time`

Calculate actual travel time for character

**Signature:** `calculate_travel_time(self, connection: core.systems.world.domain.world.TravelConnection, character_data: Dict) -> int`

#### `can_travel`

Check if character can travel between locations

**Signature:** `can_travel(self, from_location_id: str, to_location_id: str, character_data: Dict) -> bool`

#### `get_accessible_locations`

Get all locations accessible to character

**Signature:** `get_accessible_locations(self, character_data: Dict) -> List[core.systems.world.domain.world.Location]`

#### `get_connections_from`

Get all connections from a location

**Signature:** `get_connections_from(self, location_id: str) -> List[core.systems.world.domain.world.TravelConnection]`

#### `get_location`

Get location by ID

**Signature:** `get_location(self, location_id: str) -> Optional[core.systems.world.domain.world.Location]`

#### `get_locations_by_type`

Get all locations of a specific type

**Signature:** `get_locations_by_type(self, location_type: core.systems.world.domain.world.LocationType) -> List[core.systems.world.domain.world.Location]`

#### `get_start_location`

Get the starting location for the world

**Signature:** `get_start_location(self) -> Optional[core.systems.world.domain.world.Location]`

#### `get_summary`

Get world summary

**Signature:** `get_summary(self) -> Dict[str, <built-in function any>]`

#### `get_time_string`

Get current time as human-readable string

**Signature:** `get_time_string(self) -> str`

#### `remove_location`

Remove location from world

**Signature:** `remove_location(self, location_id: str) -> bool`

### Functions

## `repositories.py`

World data repository interfaces

### Classes

### class `LocationRepository`

Repository interface for location data access

#### `delete_location`

Delete location by ID

**Signature:** `delete_location(self, world_id: str, location_id: str) -> bool`

#### `list_locations`

List all locations in world

**Signature:** `list_locations(self, world_id: str) -> List[core.systems.world.domain.world.Location]`

#### `load_location`

Load location by ID

**Signature:** `load_location(self, world_id: str, location_id: str) -> Optional[core.systems.world.domain.world.Location]`

#### `save_location`

Save location to world storage

**Signature:** `save_location(self, world_id: str, location: core.systems.world.domain.world.Location) -> bool`

#### `search_locations`

Search locations by query

**Signature:** `search_locations(self, world_id: str, query: str) -> List[core.systems.world.domain.world.Location]`

### class `TravelConnectionRepository`

Repository interface for travel connection data access

#### `delete_connection`

Delete connection between locations

**Signature:** `delete_connection(self, world_id: str, from_location_id: str, to_location_id: str) -> bool`

#### `list_connections`

List all connections in world

**Signature:** `list_connections(self, world_id: str) -> List[core.systems.world.domain.world.TravelConnection]`

#### `load_connections_from`

Load all connections from a location

**Signature:** `load_connections_from(self, world_id: str, from_location_id: str) -> List[core.systems.world.domain.world.TravelConnection]`

#### `save_connection`

Save travel connection to world storage

**Signature:** `save_connection(self, world_id: str, connection: core.systems.world.domain.world.TravelConnection) -> bool`

### class `WorldRepository`

Repository interface for world data access

#### `delete_world`

Delete world by ID

**Signature:** `delete_world(self, world_id: str) -> bool`

#### `list_worlds`

List all worlds

**Signature:** `list_worlds(self) -> List[Dict]`

#### `load_world`

Load world by ID

**Signature:** `load_world(self, world_id: str) -> Optional[core.systems.world.domain.world.World]`

#### `save_world`

Save world to storage

**Signature:** `save_world(self, world: core.systems.world.domain.world.World) -> bool`

### Functions
