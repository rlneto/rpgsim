# Equipment System

## `facade.py`

Equipment System Facade

### Classes

### class `EquipmentSystem`

Facade for Equipment System

#### `add_item_to_inventory`

Add item to inventory

**Signature:** `add_item_to_inventory(self, item: core.models.Item) -> bool`

#### `equipment_equip_item`

Equip an item

**Signature:** `equipment_equip_item(self, item: core.models.Item, character_stats: Dict[str, int]) -> Tuple[bool, str, Optional[core.models.Item]]`

#### `equipment_unequip_item`

Unequip item

**Signature:** `equipment_unequip_item(self, slot: core.systems.equipment.domain.equipment.EquipmentSlot) -> Tuple[bool, str, Optional[core.models.Item]]`

#### `generate_combat_loot`

Generate loot from combat

**Signature:** `generate_combat_loot(self, difficulty: str) -> core.systems.equipment.domain.equipment.LootGenerationResult`

#### `generate_quest_reward`

Generate quest reward

**Signature:** `generate_quest_reward(self, difficulty: str) -> core.systems.equipment.domain.equipment.LootGenerationResult`

#### `get_character_equipment_power`

Get power level

**Signature:** `get_character_equipment_power(self) -> int`

#### `get_character_equipment_stats`

Get stats from equipment

**Signature:** `get_character_equipment_stats(self) -> Dict[str, int]`

#### `get_inventory_summary`

Get summary of inventory and equipment

**Signature:** `get_inventory_summary(self) -> Dict[str, Any]`

#### `get_item_comparison`

Compare items

**Signature:** `get_item_comparison(self, current_item: Optional[core.models.Item], new_item: core.models.Item, slot: core.systems.equipment.domain.equipment.EquipmentSlot) -> core.systems.equipment.domain.equipment.EquipmentComparison`

#### `get_unique_item_count`

Get count of unique items

**Signature:** `get_unique_item_count(self) -> int`

#### `get_unique_items_by_type`

Get unique items filtered

**Signature:** `get_unique_items_by_type(self, item_type: core.models.ItemType, rarity: core.models.ItemRarity = None) -> List[core.models.Item]`

### Functions

## `equipment_service.py`

Equipment services

### Classes

### class `EquipmentManager`

Service for managing equipment

#### `calculate_equipment_stats`

Calculate total stats from equipment

**Signature:** `calculate_equipment_stats(self) -> Dict[str, int]`

#### `compare_items`

Compare two items

**Signature:** `compare_items(self, current_item: Optional[core.models.Item], new_item: core.models.Item, slot: core.systems.equipment.domain.equipment.EquipmentSlot) -> core.systems.equipment.domain.equipment.EquipmentComparison`

#### `equip_item`

Equip an item

**Signature:** `equip_item(self, item: core.models.Item, character_stats: Dict[str, int]) -> Tuple[bool, str, Optional[core.models.Item]]`

#### `get_equipment_power_level`

Calculate total equipment power level

**Signature:** `get_equipment_power_level(self) -> int`

#### `get_equipped_item`

Get item in slot

**Signature:** `get_equipped_item(self, slot: core.systems.equipment.domain.equipment.EquipmentSlot) -> Optional[core.models.Item]`

#### `unequip_item`

Unequip item from slot

**Signature:** `unequip_item(self, slot: core.systems.equipment.domain.equipment.EquipmentSlot) -> Tuple[bool, str, Optional[core.models.Item]]`

### class `InventoryManager`

Service for managing inventory

#### `add_item`

Add item to inventory

**Signature:** `add_item(self, item: core.models.Item) -> bool`

#### `get_inventory_space`

Get space usage

**Signature:** `get_inventory_space(self) -> Tuple[int, int]`

#### `get_inventory_value`

Get total value

**Signature:** `get_inventory_value(self) -> int`

#### `get_item`

Get item by ID

**Signature:** `get_item(self, item_id: str) -> Optional[core.models.Item]`

#### `get_items_by_type`

Get items by type

**Signature:** `get_items_by_type(self, item_type: core.models.ItemType) -> List[core.models.Item]`

#### `remove_item`

Remove item from inventory

**Signature:** `remove_item(self, item_id: str) -> bool`

#### `sort_inventory`

Sort inventory

**Signature:** `sort_inventory(self, key: str) -> None`

### class `ItemGenerator`

Service for generating items

#### `generate_all_unique_items`

Generate a full set of unique items

**Signature:** `generate_all_unique_items(self) -> List[core.models.Item]`

#### `generate_loot`

Generate loot based on difficulty

**Signature:** `generate_loot(self, difficulty: str) -> core.systems.equipment.domain.equipment.LootGenerationResult`

#### `generate_unique_item`

Generate a unique item

**Signature:** `generate_unique_item(self, item_id: str, item_type: core.models.ItemType, rarity: core.models.ItemRarity = None) -> core.models.Item`

### Functions

## `equipment.py`

Equipment system domain entities and value objects

### Classes

### class `EquipmentComparison`

Result of comparing two items

### class `EquipmentSlot`

Equipment slots

### class `EquipmentSlotInfo`

Information about an equipment slot

### class `EquipmentStat`

Represents a stat bonus from equipment

### class `ItemEffect`

Item effects

### class `LootGenerationResult`

Result of loot generation

### Functions
