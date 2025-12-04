# Travel System

## `travel_system.py`

Travel System for Economic Infrastructure
FOCUS: Travel between cities with costs and routes

### Classes

### class `TravelManager`

Manager for travel between cities

#### `calculate_travel_cost`

Calculate travel cost with character discounts

**Signature:** `calculate_travel_cost(self, from_city: str, to_city: str, character_level: int = 1) -> Dict`

#### `get_all_routes`

Get all available travel routes

**Signature:** `get_all_routes(self) -> Dict`

#### `get_available_destinations`

Get available travel destinations from city

**Signature:** `get_available_destinations(self, from_city: str) -> Dict`

#### `get_travel_history`

Get travel history

**Signature:** `get_travel_history(self, character_id: Optional[str] = None) -> Dict`

#### `get_travel_route`

Get specific travel route information

**Signature:** `get_travel_route(self, from_city: str, to_city: str) -> Dict`

#### `initiate_travel`

Initiate travel between cities

**Signature:** `initiate_travel(self, character_id: str, from_city: str, to_city: str, character_gold: int, character_level: int = 1) -> Dict`

### Functions

### `calculate_travel_cost`

Calculate travel cost (BDD compliant)

**Signature:** `calculate_travel_cost(from_city: str, to_city: str, character_level: int = 1) -> Dict`

### `get_all_travel_routes`

Get all travel routes (BDD compliant)

**Signature:** `get_all_travel_routes() -> Dict`

### `get_available_destinations`

Get available travel destinations (BDD compliant)

**Signature:** `get_available_destinations(from_city: str) -> Dict`

### `get_travel_manager`

Get global travel manager

**Signature:** `get_travel_manager()`

### `get_travel_route`

Get travel route information (BDD compliant)

**Signature:** `get_travel_route(from_city: str, to_city: str) -> Dict`

### `initiate_travel`

Initiate travel (BDD compliant)

**Signature:** `initiate_travel(character_id: str, from_city: str, to_city: str, character_gold: int, character_level: int = 1) -> Dict`
