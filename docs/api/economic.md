# Economic System

## `economic_integration.py`

Economic System Integration for WP-002
FOCUS: Connect all economic systems (city, travel, shop)

### Classes

### class `EconomicIntegration`

Integration manager for all economic systems

#### `get_character_economic_options`

Get all economic options available to character

**Signature:** `get_character_economic_options(self, character_id: str, current_city: str, character_gold: int, character_level: int) -> Dict`

#### `get_city_economic_profile`

Get complete economic profile for a city

**Signature:** `get_city_economic_profile(self, city_id: str) -> Dict`

#### `get_economic_overview`

Get complete economic overview

**Signature:** `get_economic_overview(self) -> Dict`

#### `process_character_action`

Process character economic action

**Signature:** `process_character_action(self, action_type: str, action_data: Dict) -> Dict`

#### `simulate_economic_day`

Simulate one day of economic activity

**Signature:** `simulate_economic_day(self) -> Dict`

### Functions

### `get_character_economic_options`

Get character economic options (BDD compliant)

**Signature:** `get_character_economic_options(character_id: str, current_city: str, character_gold: int, character_level: int) -> Dict`

### `get_city_economic_profile`

Get city economic profile (BDD compliant)

**Signature:** `get_city_economic_profile(city_id: str) -> Dict`

### `get_economic_integration`

Get global economic integration

**Signature:** `get_economic_integration()`

### `get_economic_overview`

Get economic overview (BDD compliant)

**Signature:** `get_economic_overview() -> Dict`
