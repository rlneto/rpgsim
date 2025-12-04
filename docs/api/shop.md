# Shop System

## `domain_models.py`

Shop domain models for RPGSim

### Classes

### class `ItemCondition`

Condition levels for items

### class `ItemRarity`

Rarity levels for items

### class `ItemStats`

Item statistics and properties

### class `Shop`

Complete shop representation

#### `can_afford_item`

Check if player can afford an item from this shop

**Signature:** `can_afford_item(self, item_value: int, player_gold: int) -> bool`

#### `get_final_price`

Get final price after shop modifiers

**Signature:** `get_final_price(self, base_price: int) -> int`

#### `get_reputation_discount`

Get discount based on reputation

**Signature:** `get_reputation_discount(self, reputation: int) -> float`

#### `get_shop_summary`

Get shop summary information

**Signature:** `get_shop_summary(self) -> Dict[str, Any]`

#### `get_summary`

Get complete shop summary

**Signature:** `get_summary(self) -> Dict[str, Any]`

#### `is_premium_quality`

Check if shop has premium quality

**Signature:** `is_premium_quality(self) -> bool`

### class `ShopConfig`

Shop configuration data

### class `ShopCreateParams`

Parameters for shop creation to reduce argument count

### class `ShopEconomy`

Shop economic data

#### `get_economic_status`

Get economic status information

**Signature:** `get_economic_status(self) -> Dict[str, Any]`

### class `ShopInfo`

Shop basic information

### class `ShopInventory`

Shop inventory management

#### `add_item`

Add item to inventory

**Signature:** `add_item(self, item: core.systems.shop.domain_models.ShopItem) -> None`

#### `get_item`

Get item by ID

**Signature:** `get_item(self, item_id: str) -> Optional[core.systems.shop.domain_models.ShopItem]`

#### `get_total_items`

Get total number of items

**Signature:** `get_total_items(self) -> int`

#### `get_total_value`

Get total value of all items

**Signature:** `get_total_value(self) -> int`

#### `remove_item`

Remove item from inventory

**Signature:** `remove_item(self, item_id: str) -> bool`

### class `ShopItem`

Represents an item in shop inventory

#### `get_effective_price`

Get price adjusted by condition and rarity

**Signature:** `get_effective_price(self) -> int`

#### `get_total_value`

Get total value of all items in stock

**Signature:** `get_total_value(self) -> int`

#### `is_available`

Check if item is available for purchase

**Signature:** `is_available(self) -> bool`

### class `ShopQuality`

Quality levels for shops

### class `ShopSystemCreateParams`

Parameters for ShopSystem.create_shop to reduce argument count

### class `ShopTransaction`

Represents a shop transaction

#### `get_transaction_summary`

Get transaction summary

**Signature:** `get_transaction_summary(self) -> Dict[str, Any]`

### class `ShopType`

Types of shops with different specializations

### class `TransactionParams`

Parameters for transactions to reduce argument count

### Functions

## `shop_system.py`

Shop System for Economic Infrastructure
FOCUS: Dynamic shopping with inventory management and pricing

### Classes

### class `ShopManager`

Manager for shops and economic transactions

#### `calculate_purchase_cost`

Calculate purchase cost with discounts

**Signature:** `calculate_purchase_cost(self, shop_id: str, item_id: str, quantity: int, customer_spent_total: int = 0) -> Dict`

#### `get_all_shops`

Get all shops in all cities

**Signature:** `get_all_shops(self) -> Dict`

#### `get_shop_info`

Get comprehensive shop information

**Signature:** `get_shop_info(self, shop_id: str) -> Dict`

#### `get_shop_inventory`

Get shop inventory with pricing

**Signature:** `get_shop_inventory(self, shop_id: str) -> Dict`

#### `get_shops_in_city`

Get all shops in a city

**Signature:** `get_shops_in_city(self, city_id: str) -> Dict`

#### `purchase_item`

Purchase item from shop

**Signature:** `purchase_item(self, shop_id: str, item_id: str, quantity: int, character_gold: int, customer_spent_total: int = 0) -> Dict`

#### `update_shop_prices`

Update shop prices (economic simulation)

**Signature:** `update_shop_prices(self, shop_id: str, price_change_factor: float) -> Dict`

### Functions

### `get_all_shops`

Get all shops (BDD compliant)

**Signature:** `get_all_shops() -> Dict`

### `get_shop_info`

Get shop information (BDD compliant)

**Signature:** `get_shop_info(shop_id: str) -> Dict`

### `get_shop_inventory`

Get shop inventory (BDD compliant)

**Signature:** `get_shop_inventory(shop_id: str) -> Dict`

### `get_shop_manager`

Get global shop manager

**Signature:** `get_shop_manager()`

### `get_shops_in_city`

Get shops in city (BDD compliant)

**Signature:** `get_shops_in_city(city_id: str) -> Dict`

### `purchase_item`

Purchase item (BDD compliant)

**Signature:** `purchase_item(shop_id: str, item_id: str, quantity: int, character_gold: int, customer_spent_total: int = 0) -> Dict`

## `modularize.py`

Shop modularization utility

### Classes

### Functions

### `modularize_shop_system`

Placeholder for shop system modularization

**Signature:** `modularize_shop_system()`

## `facade.py`

Facade for shop system operations

### Classes

### class `ItemConfig`

Configuration for item generation

### class `MockPrice`

Mock price object for tests

### class `PriceConfig`

Configuration for dynamic price calculation

### class `ShopConfig`

Configuration for shop creation

### class `ShopSystem`

Facade for all shop system operations

#### `add_item_to_inventory`

Add item to shop inventory

**Signature:** `add_item_to_inventory(self, shop_id: str, item: core.systems.shop.domain.shop.ShopItem) -> bool`

#### `calculate_bulk_purchase_price`

Calculate price for bulk purchase with discount

**Signature:** `calculate_bulk_purchase_price(self, shop_id: str, item_ids: List[str], character_reputation: int = 50) -> Optional[Dict[str, Any]]`

#### `calculate_buy_price`

Calculate buy price for item

Returns object with final_price attribute to match tests

**Signature:** `calculate_buy_price(self, shop: Union[str, core.systems.shop.domain.shop.Shop], item: Union[str, core.systems.shop.domain.shop.ShopItem], character_id: str = None, **kwargs) -> Any`

#### `calculate_dynamic_price`

Calculate dynamic price based on market conditions

**Signature:** `calculate_dynamic_price(self, config: core.systems.shop.facade.PriceConfig) -> Optional[int]`

#### `calculate_sell_price`

Calculate sell price for item

Returns object with final_price attribute to match tests

**Signature:** `calculate_sell_price(self, shop: Union[str, core.systems.shop.domain.shop.Shop], item: core.systems.shop.domain.shop.ShopItem, character_id: str = None) -> Any`

#### `create_shop`

Create a new shop

Args:
    config: ShopConfig object or dictionary of parameters
    **kwargs: Individual parameters if config is not provided

**Signature:** `create_shop(self, config: Union[core.systems.shop.facade.ShopConfig, Dict[str, Any]] = None, **kwargs) -> Optional[core.systems.shop.domain.shop.Shop]`

#### `delete_shop`

Delete shop by ID

**Signature:** `delete_shop(self, shop_id: str) -> bool`

#### `find_shops_by_location`

Find shops by location

**Signature:** `find_shops_by_location(self, location: str) -> List[core.systems.shop.domain.shop.Shop]`

#### `find_shops_by_type`

Find shops by type

**Signature:** `find_shops_by_type(self, shop_type: str) -> List[core.systems.shop.domain.shop.Shop]`

#### `generate_custom_item`

Generate custom shop item

**Signature:** `generate_custom_item(self, config: core.systems.shop.facade.ItemConfig) -> core.systems.shop.domain.shop.ShopItem`

#### `get_economic_analysis`

Get detailed economic analysis

**Signature:** `get_economic_analysis(self, shop_id: str) -> Optional[Dict[str, Any]]`

#### `get_shop`

Get shop by ID

**Signature:** `get_shop(self, shop_id: str) -> Optional[core.systems.shop.domain.shop.Shop]`

#### `get_shop_economy`

Get shop economic information

**Signature:** `get_shop_economy(self, shop_id: str) -> Optional[Dict[str, Any]]`

#### `get_shop_inventory`

Get shop inventory

**Signature:** `get_shop_inventory(self, shop_id: str) -> List[core.systems.shop.domain.shop.ShopItem]`

#### `get_shop_overview`

Get complete shop overview

**Signature:** `get_shop_overview(self, shop_id: str) -> Optional[Dict[str, Any]]`

#### `get_shop_statistics`

Get comprehensive shop statistics

**Signature:** `get_shop_statistics(self, shop_id: str) -> Optional[Dict[str, Any]]`

#### `get_transaction_history`

Get shop transaction history

**Signature:** `get_transaction_history(self, shop_id: str, limit: int = 100) -> List[core.systems.shop.domain.shop.ShopTransaction]`

#### `get_transaction_summary`

Get transaction summary for recent period

**Signature:** `get_transaction_summary(self, shop_id: str, days: int = 7) -> Dict[str, Any]`

#### `list_shops`

List all shops

**Signature:** `list_shops(self) -> List[core.systems.shop.domain.shop.Shop]`

#### `process_transaction`

Process shop transaction (buy or sell)

**Signature:** `process_transaction(self, config: Union[core.systems.shop.facade.TransactionConfig, Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]`

#### `refresh_inventory`

Refresh shop inventory

**Signature:** `refresh_inventory(self, shop: Union[str, core.systems.shop.domain.shop.Shop], current_day: int = 1) -> Dict[str, Any]`

#### `refresh_shop_inventory`

Refresh shop inventory (backward compatibility)

**Signature:** `refresh_shop_inventory(self, shop_id: str, current_day: int = 1) -> Dict[str, Any]`

#### `remove_item_from_inventory`

Remove item from shop inventory

**Signature:** `remove_item_from_inventory(self, shop_id: str, item_id: str) -> bool`

#### `restock_shop`

Restock shop inventory

**Signature:** `restock_shop(self, shop_id: str, items: Optional[List[core.systems.shop.domain.shop.ShopItem]] = None) -> Dict[str, Any]`

#### `simulate_customer_traffic`

Simulate customer traffic for testing

**Signature:** `simulate_customer_traffic(self, shop: core.systems.shop.domain.shop.Shop)`

#### `update_reputation`

Update player reputation (helper for tests)

**Signature:** `update_reputation(self, player_id: str, location: str, value: int)`

#### `update_shop_economy`

Update shop economy

**Signature:** `update_shop_economy(self, shop_id: str, economic_change: int, location_wealth_change: int = 0) -> Dict[str, Any]`

### class `TransactionConfig`

Configuration for transaction processing

### Functions

### `buy_item_from_shop`

Buy item from shop (backward compatibility)

**Signature:** `buy_item_from_shop(shop_id: str, item_id: str, character_gold: int, character_reputation: int = 50) -> Dict[str, Any]`

### `calculate_shop_prices`

Calculate shop prices (backward compatibility)

**Signature:** `calculate_shop_prices(shop_id: str, base_prices: List[int], character_reputation: int = 50) -> List[int]`

### `create_shop`

Create shop (backward compatibility)

**Signature:** `create_shop(shop_id: str, name: str, shop_type: str, owner: str, location: str, quality_level: str = 'standard') -> Optional[core.systems.shop.domain.shop.Shop]`

### `generate_shop_inventory`

Generate shop inventory (backward compatibility)

**Signature:** `generate_shop_inventory(shop_type: str, inventory_size: int) -> List[core.systems.shop.domain.shop.ShopItem]`

### `get_shop_data`

Get shop data (backward compatibility)

**Signature:** `get_shop_data(shop_id: str) -> Optional[Dict[str, Any]]`

### `get_shop_inventory`

Get shop inventory (backward compatibility)

**Signature:** `get_shop_inventory(shop_id: str) -> List[core.systems.shop.domain.shop.ShopItem]`

### `restock_shop`

Restock shop (backward compatibility)

**Signature:** `restock_shop(shop_id: str, items: Optional[List[core.systems.shop.domain.shop.ShopItem]] = None) -> Dict[str, Any]`

### `sell_item_to_shop`

Sell item to shop (backward compatibility)

**Signature:** `sell_item_to_shop(shop_id: str, item: core.systems.shop.domain.shop.ShopItem, character_reputation: int = 50) -> Dict[str, Any]`

### `update_shop_economy`

Update shop economy (backward compatibility)

**Signature:** `update_shop_economy(shop_id: str, economic_change: int, location_wealth_change: int = 0) -> Dict[str, Any]`

## `memory_repository.py`

Memory repository implementations for shop data

### Classes

### class `MemoryShopItemRepository`

In-memory shop item repository

#### `delete_item`

Delete item from shop inventory

**Signature:** `delete_item(self, shop_id: str, item_id: str) -> bool`

#### `find_items_by_type`

Find items by type in shop inventory

**Signature:** `find_items_by_type(self, shop_id: str, item_type: str) -> List[core.systems.shop.domain.shop.ShopItem]`

#### `list_items`

List all items in shop inventory

**Signature:** `list_items(self, shop_id: str) -> List[core.systems.shop.domain.shop.ShopItem]`

#### `load_item`

Load item by ID

**Signature:** `load_item(self, shop_id: str, item_id: str) -> Optional[core.systems.shop.domain.shop.ShopItem]`

#### `save_item`

Save item to shop inventory

**Signature:** `save_item(self, shop_id: str, item: core.systems.shop.domain.shop.ShopItem) -> bool`

### class `MemoryShopRepository`

In-memory shop repository

#### `delete_shop`

Delete shop by ID

**Signature:** `delete_shop(self, shop_id: str) -> bool`

#### `find_shops_by_location`

Find shops by location

**Signature:** `find_shops_by_location(self, location: str) -> List[core.systems.shop.domain.shop.Shop]`

#### `find_shops_by_type`

Find shops by type

**Signature:** `find_shops_by_type(self, shop_type: str) -> List[core.systems.shop.domain.shop.Shop]`

#### `list_shops`

List all shops

**Signature:** `list_shops(self) -> List[core.systems.shop.domain.shop.Shop]`

#### `load_shop`

Load shop by ID

**Signature:** `load_shop(self, shop_id: str) -> Optional[core.systems.shop.domain.shop.Shop]`

#### `save_shop`

Save shop to memory storage

**Signature:** `save_shop(self, shop: core.systems.shop.domain.shop.Shop) -> bool`

### class `MemoryShopTransactionRepository`

In-memory shop transaction repository

#### `get_transaction_summary`

Get transaction summary for recent period

**Signature:** `get_transaction_summary(self, shop_id: str, days: int = 7) -> Dict[str, <built-in function any>]`

#### `load_transactions`

Load recent transactions from shop history

**Signature:** `load_transactions(self, shop_id: str, limit: int = 100) -> List[core.systems.shop.domain.shop.ShopTransaction]`

#### `load_transactions_by_type`

Load transactions by type from shop history

**Signature:** `load_transactions_by_type(self, shop_id: str, transaction_type: str, limit: int = 100) -> List[core.systems.shop.domain.shop.ShopTransaction]`

#### `save_transaction`

Save transaction to shop history

**Signature:** `save_transaction(self, shop_id: str, transaction: core.systems.shop.domain.shop.ShopTransaction) -> bool`

### Functions

## `shop_service.py`

Shop business logic services

### Classes

### class `ShopCreationService`

Service for shop creation logic

#### `create_shop`

Create a new shop with validation

**Signature:** `create_shop(self, shop_id: str, name: str, shop_type: str, owner: str, location: str, quality_level: str, gold_reserve: Optional[int] = None, inventory_size: Optional[int] = None) -> Optional[core.systems.shop.domain.shop.Shop]`

### class `ShopEconomyService`

Service for shop economic management

#### `get_economic_analysis`

Get detailed economic analysis

**Signature:** `get_economic_analysis(self, shop: core.systems.shop.domain.shop.Shop) -> Dict[str, Any]`

#### `update_shop_economy`

Update shop economy based on transactions

**Signature:** `update_shop_economy(self, shop: core.systems.shop.domain.shop.Shop, economic_change: int, location_wealth_change: int = 0) -> Dict[str, Any]`

### class `ShopInventoryService`

Service for shop inventory management

#### `get_inventory_summary`

Get comprehensive inventory summary

**Signature:** `get_inventory_summary(self, shop: core.systems.shop.domain.shop.Shop) -> Dict[str, Any]`

#### `refresh_inventory`

Refresh shop inventory

**Signature:** `refresh_inventory(self, shop: core.systems.shop.domain.shop.Shop, current_day: int) -> Dict[str, Any]`

#### `restock_shop`

Restock shop with specific items or auto-generate

**Signature:** `restock_shop(self, shop: core.systems.shop.domain.shop.Shop, items: Optional[List[core.systems.shop.domain.shop.ShopItem]] = None) -> Dict[str, Any]`

### class `ShopManagementService`

Service for comprehensive shop management

#### `get_shop_overview`

Get complete shop overview

**Signature:** `get_shop_overview(self, shop: core.systems.shop.domain.shop.Shop) -> Dict[str, Any]`

#### `get_shop_statistics`

Get comprehensive shop statistics

**Signature:** `get_shop_statistics(self, shop: core.systems.shop.domain.shop.Shop) -> Dict[str, Any]`

#### `update_reputation_discounts`

Update reputation discount configuration

**Signature:** `update_reputation_discounts(self, shop: core.systems.shop.domain.shop.Shop, discount_config: Dict[str, float]) -> bool`

### class `ShopTransactionService`

Service for shop transaction logic

#### `process_buy_transaction`

Process buy transaction

**Signature:** `process_buy_transaction(self, shop: core.systems.shop.domain.shop.Shop, item_id: str, character_gold: int, character_reputation: int = 50) -> Dict[str, Any]`

#### `process_sell_transaction`

Process sell transaction

**Signature:** `process_sell_transaction(self, shop: core.systems.shop.domain.shop.Shop, item: core.systems.shop.domain.shop.ShopItem, character_reputation: int = 50) -> Dict[str, Any]`

### Functions

## `item_service.py`

Shop item generation and pricing services

### Classes

### class `ItemGenerationService`

Service for generating shop items

#### `generate_custom_item`

Generate custom shop item

**Signature:** `generate_custom_item(self, name: str, item_type: str, base_value: int, rarity: str = 'common', condition: str = 'good', effect: str = 'Standard effect') -> core.systems.shop.domain.shop.ShopItem`

#### `generate_inventory`

Generate inventory for shop based on type and quality

**Signature:** `generate_inventory(self, shop_type: str, inventory_size: int) -> List[core.systems.shop.domain.shop.ShopItem]`

### class `ItemPricingService`

Service for item pricing calculations

#### `calculate_bulk_purchase_price`

Calculate price for bulk purchase with discount

**Signature:** `calculate_bulk_purchase_price(self, shop: core.systems.shop.domain.shop.Shop, items: List[core.systems.shop.domain.shop.ShopItem], character_reputation: int = 50) -> Dict[str, Any]`

#### `calculate_buy_price`

Calculate final buy price for character

**Signature:** `calculate_buy_price(self, shop: core.systems.shop.domain.shop.Shop, item: core.systems.shop.domain.shop.ShopItem, character_reputation: int = 50) -> int`

#### `calculate_dynamic_price`

Calculate dynamic price based on market conditions

**Signature:** `calculate_dynamic_price(self, shop: core.systems.shop.domain.shop.Shop, item: core.systems.shop.domain.shop.ShopItem, supply_factor: float = 1.0, demand_factor: float = 1.0, location_wealth: float = 1.0) -> int`

#### `calculate_sell_price`

Calculate final sell offer for character's item

**Signature:** `calculate_sell_price(self, shop: core.systems.shop.domain.shop.Shop, item: core.systems.shop.domain.shop.ShopItem, character_reputation: int = 50) -> int`

### Functions

## `shop.py`

Shop domain entities and value objects

### Classes

### class `ItemCondition`

Condition levels for items

### class `ItemRarity`

Rarity levels for items

### class `Shop`

Shop aggregate root entity

#### `add_transaction`

Add transaction to history

**Signature:** `add_transaction(self, transaction: core.systems.shop.domain.shop.ShopTransaction) -> None`

#### `can_buy_item_type`

Check if shop can buy this item type

**Signature:** `can_buy_item_type(self, item_type: str) -> bool`

#### `get_reputation_discount`

Get discount based on reputation

**Signature:** `get_reputation_discount(self, reputation: int) -> float`

#### `get_summary`

Get shop summary

**Signature:** `get_summary(self) -> Dict[str, Any]`

### class `ShopEconomy`

Shop economic data

#### `can_afford`

Check if shop can afford purchase

**Signature:** `can_afford(self, amount: int) -> bool`

#### `get_economic_status`

Get economic status summary

**Signature:** `get_economic_status(self) -> Dict[str, Any]`

#### `update_gold_reserves`

Update gold reserves

**Signature:** `update_gold_reserves(self, amount: int) -> None`

### class `ShopInventory`

Shop inventory management

#### `add_item`

Add item to inventory

**Signature:** `add_item(self, item: core.systems.shop.domain.shop.ShopItem) -> bool`

#### `find_item`

Find item in inventory

**Signature:** `find_item(self, item_id: str) -> Optional[core.systems.shop.domain.shop.ShopItem]`

#### `get_items_by_rarity`

Get items by rarity

**Signature:** `get_items_by_rarity(self, rarity: str) -> List[core.systems.shop.domain.shop.ShopItem]`

#### `get_items_by_type`

Get items by type

**Signature:** `get_items_by_type(self, item_type: str) -> List[core.systems.shop.domain.shop.ShopItem]`

#### `get_summary`

Get inventory summary

**Signature:** `get_summary(self) -> Dict[str, Any]`

#### `refresh`

Refresh inventory with new items

**Signature:** `refresh(self, new_items: List[core.systems.shop.domain.shop.ShopItem]) -> int`

#### `remove_item`

Remove item from inventory

**Signature:** `remove_item(self, item_id: str) -> Optional[core.systems.shop.domain.shop.ShopItem]`

### class `ShopItem`

Item in shop inventory

#### `add_enchantment`

Add enchantment to item

**Signature:** `add_enchantment(self, enchantment: str) -> None`

#### `get_effective_price`

Get price adjusted for condition and rarity

**Signature:** `get_effective_price(self) -> int`

#### `get_summary`

Get item summary

**Signature:** `get_summary(self) -> Dict[str, Any]`

#### `is_available`

Check if item is available for purchase

**Signature:** `is_available(self) -> bool`

#### `is_rare`

Check if item is rare or better

**Signature:** `is_rare(self) -> bool`

### class `ShopQuality`

Quality levels for shops

### class `ShopTransaction`

Shop transaction record

### class `ShopType`

Types of shops with different specializations

### Functions

## `repositories.py`

Shop data repository interfaces

### Classes

### class `ShopItemRepository`

Repository interface for shop item data access

#### `delete_item`

Delete item from shop inventory

**Signature:** `delete_item(self, shop_id: str, item_id: str) -> bool`

#### `find_items_by_type`

Find items by type in shop inventory

**Signature:** `find_items_by_type(self, shop_id: str, item_type: str) -> List[core.systems.shop.domain.shop.ShopItem]`

#### `list_items`

List all items in shop inventory

**Signature:** `list_items(self, shop_id: str) -> List[core.systems.shop.domain.shop.ShopItem]`

#### `load_item`

Load item by ID

**Signature:** `load_item(self, shop_id: str, item_id: str) -> Optional[core.systems.shop.domain.shop.ShopItem]`

#### `save_item`

Save item to shop inventory

**Signature:** `save_item(self, shop_id: str, item: core.systems.shop.domain.shop.ShopItem) -> bool`

### class `ShopRepository`

Repository interface for shop data access

#### `delete_shop`

Delete shop by ID

**Signature:** `delete_shop(self, shop_id: str) -> bool`

#### `find_shops_by_location`

Find shops by location

**Signature:** `find_shops_by_location(self, location: str) -> List[core.systems.shop.domain.shop.Shop]`

#### `find_shops_by_type`

Find shops by type

**Signature:** `find_shops_by_type(self, shop_type: str) -> List[core.systems.shop.domain.shop.Shop]`

#### `list_shops`

List all shops

**Signature:** `list_shops(self) -> List[core.systems.shop.domain.shop.Shop]`

#### `load_shop`

Load shop by ID

**Signature:** `load_shop(self, shop_id: str) -> Optional[core.systems.shop.domain.shop.Shop]`

#### `save_shop`

Save shop to storage

**Signature:** `save_shop(self, shop: core.systems.shop.domain.shop.Shop) -> bool`

### class `ShopTransactionRepository`

Repository interface for shop transaction data access

#### `get_transaction_summary`

Get transaction summary for recent period

**Signature:** `get_transaction_summary(self, shop_id: str, days: int = 7) -> Dict[str, Any]`

#### `load_transactions`

Load recent transactions from shop history

**Signature:** `load_transactions(self, shop_id: str, limit: int = 100) -> List[core.systems.shop.domain.shop.ShopTransaction]`

#### `load_transactions_by_type`

Load transactions by type from shop history

**Signature:** `load_transactions_by_type(self, shop_id: str, transaction_type: str, limit: int = 100) -> List[core.systems.shop.domain.shop.ShopTransaction]`

#### `save_transaction`

Save transaction to shop history

**Signature:** `save_transaction(self, shop_id: str, transaction: core.systems.shop.domain.shop.ShopTransaction) -> bool`

### Functions
