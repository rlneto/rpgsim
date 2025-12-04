# City System

## `city_management.py`

City Management System for Economic Infrastructure
FOCUS: Living cities with economy, NPCs, and services

### Classes

### class `CityManager`

Manager for city systems and economy

#### `get_all_cities`

Get list of all cities

**Signature:** `get_all_cities(self) -> List[Dict]`

#### `get_city_economy`

Get city economic information

**Signature:** `get_city_economy(self, city_id: str) -> Dict`

#### `get_city_info`

Get comprehensive city information

**Signature:** `get_city_info(self, city_id: str) -> Dict`

#### `get_city_npcs`

Get NPCs in city

**Signature:** `get_city_npcs(self, city_id: str) -> Dict`

#### `get_city_services`

Get available services in city

**Signature:** `get_city_services(self, city_id: str) -> Dict`

#### `simulate_city_day`

Simulate one day of city economic activity

**Signature:** `simulate_city_day(self, city_id: str) -> Dict`

#### `update_city_prosperity`

Update city prosperity

**Signature:** `update_city_prosperity(self, city_id: str, change: float) -> Dict`

### Functions

### `get_all_cities`

Get all cities (BDD compliant)

**Signature:** `get_all_cities() -> List[Dict]`

### `get_city_economy`

Get city economy (BDD compliant)

**Signature:** `get_city_economy(city_id: str) -> Dict`

### `get_city_info`

Get city information (BDD compliant)

**Signature:** `get_city_info(city_id: str) -> Dict`

### `get_city_manager`

Get global city manager

**Signature:** `get_city_manager()`

### `get_city_services`

Get city services (BDD compliant)

**Signature:** `get_city_services(city_id: str) -> Dict`

### `simulate_city_day`

Simulate city day (BDD compliant)

**Signature:** `simulate_city_day(city_id: str) -> Dict`
