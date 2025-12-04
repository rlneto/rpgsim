# Inventory System

## `facade.py`

Facade for inventory system

### Classes

### class `InventorySystem`

Facade for inventory operations

#### `add_item`

Add item to character inventory

**Signature:** `add_item(self, character_id: str, item: core.models.Item, quantity: int = 1) -> bool`

#### `create_inventory`

Create inventory for character

**Signature:** `create_inventory(self, character_id: str, max_slots: int = 30) -> bool`

#### `get_inventory_summary`

Get inventory summary

**Signature:** `get_inventory_summary(self, character_id: str) -> Optional[Dict[str, Any]]`

#### `get_item_count`

Get count of specific item

**Signature:** `get_item_count(self, character_id: str, item_id: str) -> int`

#### `remove_item`

Remove item from character inventory

**Signature:** `remove_item(self, character_id: str, item_id: str, quantity: int = 1) -> Optional[core.models.Item]`

### Functions

## `memory_repository.py`

Memory repository for inventory

### Classes

### class `MemoryInventoryRepository`

In-memory implementation of inventory repository

#### `delete`

Delete inventory from memory

**Signature:** `delete(self, character_id: str) -> bool`

#### `exists`

Check if inventory exists

**Signature:** `exists(self, character_id: str) -> bool`

#### `load`

Load inventory from memory

**Signature:** `load(self, character_id: str) -> Optional[core.systems.inventory.domain.inventory.Inventory]`

#### `save`

Save inventory to memory

**Signature:** `save(self, character_id: str, inventory: core.systems.inventory.domain.inventory.Inventory) -> bool`

### Functions

## `inventory_service.py`

Inventory service for RPGSim
Handles inventory business logic

### Classes

### class `InventoryService`

Service for managing inventory operations

#### `add_item`

Add item to character inventory

**Signature:** `add_item(self, character_id: str, item: core.models.Item, quantity: int = 1) -> bool`

#### `can_add_item`

Check if item can be added to inventory

**Signature:** `can_add_item(self, character_id: str, item: core.models.Item, quantity: int = 1) -> bool`

#### `create_inventory`

Create new inventory for character

**Signature:** `create_inventory(self, character_id: str, max_slots: int = 30, max_weight: float = 100.0) -> core.systems.inventory.domain.inventory.Inventory`

#### `delete_inventory`

Delete character inventory

**Signature:** `delete_inventory(self, character_id: str) -> bool`

#### `equip_item`

Equip item from specific slot

**Signature:** `equip_item(self, character_id: str, slot_index: int) -> bool`

#### `get_equipped_items`

Get all equipped items

**Signature:** `get_equipped_items(self, character_id: str) -> Dict[str, Any]`

#### `get_inventory`

Get inventory by character ID

**Signature:** `get_inventory(self, character_id: str) -> Optional[core.systems.inventory.domain.inventory.Inventory]`

#### `get_inventory_summary`

Get inventory summary

**Signature:** `get_inventory_summary(self, character_id: str) -> Optional[Dict[str, Any]]`

#### `get_item_count`

Get count of specific item in inventory

**Signature:** `get_item_count(self, character_id: str, item_id: str) -> int`

#### `remove_item`

Remove item from character inventory

**Signature:** `remove_item(self, character_id: str, item_id: str, quantity: int = 1) -> Optional[core.models.Item]`

#### `transfer_item`

Transfer item between characters

**Signature:** `transfer_item(self, from_character_id: str, to_character_id: str, item_id: str, quantity: int = 1) -> bool`

#### `unequip_item`

Unequip item from slot type

**Signature:** `unequip_item(self, character_id: str, slot_type: str) -> Optional[core.models.Item]`

### Functions

## `inventory.py`

Inventory domain models for RPGSim

### Classes

### class `Inventory`

Main inventory class

#### `add_item`

Add item to inventory

**Signature:** `add_item(self, item: core.models.Item, quantity: int = 1) -> bool`

#### `can_add_item`

Check if item can be added to inventory

**Signature:** `can_add_item(self, item: core.models.Item, quantity: int = 1) -> bool`

#### `equip_item`

Equip item from slot

**Signature:** `equip_item(self, slot: core.systems.inventory.domain.inventory.InventorySlot) -> bool`

#### `get_empty_slots`

Get all empty slots

**Signature:** `get_empty_slots(self) -> List[core.systems.inventory.domain.inventory.InventorySlot]`

#### `get_equipped_items`

Get all equipped items

**Signature:** `get_equipped_items(self) -> Dict[core.systems.inventory.domain.inventory.InventorySlotType, Optional[core.models.Item]]`

#### `get_item_count`

Get total count of specific item

**Signature:** `get_item_count(self, item_id: str) -> int`

#### `get_slots_with_item`

Get all slots containing specific item

**Signature:** `get_slots_with_item(self, item_id: str) -> List[core.systems.inventory.domain.inventory.InventorySlot]`

#### `get_summary`

Get inventory summary

**Signature:** `get_summary(self) -> Dict[str, Any]`

#### `get_total_value`

Get total value of all items

**Signature:** `get_total_value(self) -> int`

#### `get_total_weight`

Get total weight of all items

**Signature:** `get_total_weight(self) -> float`

#### `remove_item`

Remove item from inventory

**Signature:** `remove_item(self, item_id: str, quantity: int = 1) -> Optional[core.models.Item]`

#### `unequip_item`

Unequip item from slot type

**Signature:** `unequip_item(self, slot_type: core.systems.inventory.domain.inventory.InventorySlotType) -> Optional[core.models.Item]`

### class `InventorySlot`

Represents a single inventory slot

#### `add_item`

Add item to slot

**Signature:** `add_item(self, item: core.models.Item, quantity: int = 1) -> bool`

#### `can_add_item`

Check if item can be added to this slot

**Signature:** `can_add_item(self, item: core.models.Item, quantity: int = 1) -> bool`

#### `get_total_weight`

Get total weight of items in slot

**Signature:** `get_total_weight(self) -> float`

#### `is_empty`

Check if slot is empty

**Signature:** `is_empty(self) -> bool`

#### `remove_item`

Remove item from slot

**Signature:** `remove_item(self, quantity: int = 1) -> Optional[core.models.Item]`

### class `InventorySlotType`

Types of inventory slots

### Functions

## `repositories.py`

Inventory repository interface

### Classes

### class `InventoryRepository`

Abstract repository for inventory persistence

#### `delete`

Delete inventory from repository

**Signature:** `delete(self, character_id: str) -> bool`

#### `exists`

Check if inventory exists

**Signature:** `exists(self, character_id: str) -> bool`

#### `load`

Load inventory from repository

**Signature:** `load(self, character_id: str) -> Optional[core.systems.inventory.domain.inventory.Inventory]`

#### `save`

Save inventory to repository

**Signature:** `save(self, character_id: str, inventory: core.systems.inventory.domain.inventory.Inventory) -> bool`

### Functions
