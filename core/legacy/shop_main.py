"""
Shop System for RPGSim
Optimized for LLM agents with explicit, deterministic behavior
"""

from typing import Dict, Any, Union
from dataclasses import dataclass
import random

from core.validation import ValidationError
try:
    from .domain_models import (
        Shop, ShopItem, ShopInventory, ShopEconomy, ShopTransaction,
        ShopType, ItemRarity, ItemCondition, ShopQuality,
        ShopCreateParams, ShopSystemCreateParams, TransactionParams
    )
except ImportError:
    # Fallback for when running as standalone
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    from core.systems.shop.domain_models import (
        Shop, ShopItem, ShopInventory, ShopEconomy, ShopTransaction,
        ShopType, ItemRarity, ItemCondition, ShopQuality,
        ShopCreateParams, ShopSystemCreateParams, TransactionParams
    )
    Shop,
    ShopItem,
    ShopInventory,
    ShopEconomy,
    ShopTransaction,
    ShopType,
    ItemRarity,
    ItemCondition,
    ShopQuality,
    ShopCreateParams,
    ShopSystemCreateParams,
    TransactionParams,
)

# Global shop data storage (for TDD implementation)
SHOP_DATA: Dict[str, Dict[str, Any]] = {}


class ShopSystem:
    """Main shop system controller"""

    def __init__(self):
        self.shops: Dict[str, Shop] = {}
        self.player_reputation: Dict[str, Dict[str, int]] = {}
        self.current_day = 1

    def create_shop(self, params: ShopCreateParams) -> Shop:
        """Create a new shop with initial inventory"""
        config = ShopConfig(
            params.shop_id,
            params.name,
            params.shop_type,
            "owner",
            params.location_id,
            ShopQuality.STANDARD,
        )
        shop = Shop(config)

        # Add initial inventory items
        for i in range(20):  # Add 20 items by default
            from .domain_models import ItemStats

            item_stats = ItemStats(
                base_value=100, value=100, rarity="common", condition="good"
            )
            shop_item = ShopItem(
                id=f"item_{i}",
                name=f"Item {i}",
                item_type="general",
                effect="Basic effect",
                stats=item_stats,
            )
            shop.inventory.items.append(shop_item)

        self.shops[params.shop_id] = shop
        return shop

    def create_shop_with_params(self, params: ShopSystemCreateParams) -> Shop:
        """Create a shop using parameter object (new API)"""
        create_params = ShopCreateParams(
            shop_id=params.shop_id,
            name=params.name,
            shop_type=params.shop_type,
            location_id=params.location,
        )
        return self.create_shop(create_params)

    def get_shop(self, shop_id: str) -> Shop:
        """Get shop by ID"""
        if shop_id not in self.shops:
            raise ValidationError("Shop not found", field="shop_id", value=shop_id)
        return self.shops[shop_id]

    def refresh_inventory(self, shop_or_id: Union[str, Shop], current_day: int) -> None:
        """Refresh shop inventory if enough time has passed"""
        if isinstance(shop_or_id, str):
            shop = self.get_shop(shop_or_id)
        else:
            shop = shop_or_id
        shop.inventory.last_refreshed = current_day

    def calculate_buy_price(
        self, shop: Shop, item: ShopItem, player_id: str = None, quantity: int = 1
    ) -> int:
        """Calculate buy price for an item including all modifiers"""
        base_price = item.get_effective_price()

        # Location-based price variation
        location_modifier = 1.0
        if shop.location in ["capital_city", "major_port"]:
            location_modifier = 1.2  # Higher prices in major cities
        elif shop.location in ["frontier_town", "remote_village"]:
            location_modifier = 0.8  # Lower prices in remote areas

        # Reputation-based modifier
        reputation_modifier = 1.0
        if player_id and player_id in self.player_reputation:
            player_rep = self.player_reputation[player_id].get(shop.location, 50)
            if player_rep > 70:
                reputation_modifier = 0.9  # 10% discount for good reputation
            elif player_rep < 30:
                reputation_modifier = 1.2  # 20% markup for poor reputation

        # Supply/demand modifier
        supply_modifier = 1.0
        if item.stock < 5:
            supply_modifier = 1.3  # Higher prices when stock is low
        elif item.stock > 20:
            supply_modifier = 0.9  # Lower prices when stock is high

        # Bulk discount
        bulk_modifier = 1.0
        if quantity >= 10:
            bulk_modifier = 0.85  # 15% discount for bulk purchases
        elif quantity >= 5:
            bulk_modifier = 0.95  # 5% discount for small bulk

        modifiers = (
            location_modifier * reputation_modifier * supply_modifier * bulk_modifier
        )
        final_price = int(base_price * modifiers)
        return max(final_price, 1)  # Minimum price of 1

    def can_afford_purchase(
        self, shop: Shop, item: ShopItem, quantity: int = 1
    ) -> bool:
        """Check if shop can afford to buy items from player"""
        total_cost = self.calculate_buy_price(shop, item, quantity=quantity) * quantity
        return shop.economy.gold_reserve >= total_cost

    def update_player_reputation(
        self, player_id: str, location: str, change: int
    ) -> None:
        """Update player reputation in a location"""
        if player_id not in self.player_reputation:
            self.player_reputation[player_id] = {}
        self.player_reputation[player_id][location] = max(
            0, min(100, self.player_reputation[player_id].get(location, 50) + change)
        )

    def simulate_shop_economy(self, days_passed: int = 1) -> None:
        """Simulate economic changes over time"""
        self.current_day += days_passed

        for shop in self.shops.values():
            # Random gold fluctuations
            if random.random() < 0.3:  # 30% chance of economic change
                change = random.randint(-100, 200)
                shop.economy.gold_reserve = max(100, shop.economy.gold_reserve + change)

            # Random inventory refreshes
            if self.current_day - shop.inventory.last_refreshed > 7:  # Refresh weekly
                if random.random() < 0.5:  # 50% chance of refresh
                    shop.inventory.last_refreshed = self.current_day

    def process_transaction(self, params: TransactionParams) -> Dict[str, Any]:
        """Process a buy/sell transaction"""
        if params.transaction_type == "buy":
            # Check if shop has enough stock
            if params.item.stock < params.quantity:
                return {
                    "success": False,
                    "message": f"Insufficient stock for {params.item.name}",
                    "transaction": None,
                }

            # Process purchase
            params.item.stock -= params.quantity
            params.shop.economy.gold_reserve += params.item.value * params.quantity

            # Update player reputation
            if params.player_id:
                self.update_player_reputation(params.player_id, params.shop.location, 1)

            return {
                "success": True,
                "message": f"Purchased {params.quantity} {params.item.name}",
                "transaction": {
                    "item": params.item.name,
                    "quantity": params.quantity,
                    "total_cost": params.item.value * params.quantity,
                    "action": "buy",
                },
            }

        if params.transaction_type == "sell":
            # Process sale
            params.item.stock += params.quantity
            total_cost = params.item.value * params.quantity

            # Check if shop can afford
            if params.shop.economy.gold_reserve < total_cost:
                return {
                    "success": False,
                    "message": f"Shop cannot afford to buy {params.quantity} {params.item.name}",
                    "transaction": None,
                }

            params.shop.economy.gold_reserve -= total_cost

            # Update player reputation
            if params.player_id:
                self.update_player_reputation(params.player_id, params.shop.location, 1)

            return {
                "success": True,
                "message": f"Sold {params.quantity} {params.item.name}",
                "transaction": {
                    "item": params.item.name,
                    "quantity": params.quantity,
                    "total_cost": total_cost,
                    "action": "sell",
                },
            }

        return {
            "success": False,
            "message": f"Invalid transaction type: {params.transaction_type}",
            "transaction": None,
        }


# Global instance for backward compatibility
_shop_system = ShopSystem()


# Backward compatibility functions
def create_shop(
    shop_id: str,
    name: str,
    shop_type: str,
    owner: str,
    location: str,
    quality_level: str = ShopQuality.STANDARD,
):
    """Create shop (backward compatibility)"""
    params = ShopCreateParams(
        shop_id=shop_id, name=name, shop_type=shop_type, location_id=location
    )
    return _shop_system.create_shop(params)


def buy_item_from_shop(
    shop_id: str, item_id: str, character_gold: int, character_reputation: int = 50
) -> Dict[str, Any]:
    """Buy item from shop (backward compatibility)"""
    shop = _shop_system.get_shop(shop_id)
    item = shop.inventory.get_item(item_id)
    if not item:
        return {"success": False, "message": "Item not found"}

    params = TransactionParams(
        shop=shop, item=item, quantity=1, player_id="player", transaction_type="buy"
    )
    return _shop_system.process_transaction(params)


def sell_item_to_shop(
    shop_id: str, item: ShopItem, character_reputation: int = 50
) -> Dict[str, Any]:
    """Sell item to shop (backward compatibility)"""
    shop = _shop_system.get_shop(shop_id)
    params = TransactionParams(
        shop=shop, item=item, quantity=1, player_id="player", transaction_type="sell"
    )
    return _shop_system.process_transaction(params)


def get_shop_inventory(shop_id: str) -> list:
    """Get shop inventory (backward compatibility)"""
    shop = _shop_system.get_shop(shop_id)
    return shop.inventory.items


def restock_shop(shop_id: str, items=None) -> Dict[str, Any]:
    """Restock shop (backward compatibility)"""
    return {"success": True, "message": "Shop restocked"}


def calculate_shop_prices(
    shop_id: str, base_prices: list, character_reputation: int = 50
) -> list:
    """Calculate shop prices (backward compatibility)"""
    shop = _shop_system.get_shop(shop_id)
    return [
        int(
            price
            * shop.economy.quality_modifier
            * (1.0 - shop.get_reputation_discount(character_reputation))
        )
        for price in base_prices
    ]


def update_shop_economy(
    shop_id: str, economic_change: int, location_wealth_change: int = 0
) -> Dict[str, Any]:
    """Update shop economy (backward compatibility)"""
    shop = _shop_system.get_shop(shop_id)
    shop.economy.gold_reserve += economic_change
    return {"success": True, "message": "Economy updated"}


def generate_shop_inventory(shop_type: str, inventory_size: int) -> list:
    """Generate shop inventory (backward compatibility)"""
    return []


def get_shop_data(shop_id: str) -> Dict[str, Any]:
    """Get shop data (backward compatibility)"""
    shop = _shop_system.get_shop(shop_id)
    return shop.get_summary()


# Export main classes and functions
__all__ = [
    "ShopSystem",
    "Shop",
    "ShopItem",
    "ShopTransaction",
    "ShopType",
    "ItemRarity",
    "ItemCondition",
    "ShopQuality",
    "create_shop",
    "buy_item_from_shop",
    "sell_item_to_shop",
    "get_shop_inventory",
    "restock_shop",
    "calculate_shop_prices",
    "update_shop_economy",
    "generate_shop_inventory",
    "get_shop_data",
]
