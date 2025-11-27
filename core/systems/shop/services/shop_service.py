"""
Shop business logic services
"""
from typing import Dict, List, Optional, Tuple, Any
from ..domain.shop import (
    Shop, ShopItem, ShopInventory, ShopEconomy, ShopTransaction,
    ShopType, ItemRarity, ItemCondition, ShopQuality, DEFAULT_SHOP_CONFIGS
)
from .item_service import ItemGenerationService, ItemPricingService


class ShopCreationService:
    """Service for shop creation logic"""

    def __init__(self):
        self.item_service = ItemGenerationService()

    def create_shop(self, shop_id: str, name: str, shop_type: str, owner: str,
                   location: str, quality_level: str, gold_reserve: Optional[int] = None,
                   inventory_size: Optional[int] = None) -> Optional[Shop]:
        """Create a new shop with validation"""

        # Convert enum inputs to strings if needed
        shop_type_str = shop_type.value if hasattr(shop_type, 'value') else shop_type
        quality_level_str = quality_level.value if hasattr(quality_level, 'value') else quality_level

        # Validate inputs
        if not self._validate_shop_inputs(shop_id, name, shop_type_str, quality_level_str):
            return None

        # Get configuration
        config = DEFAULT_SHOP_CONFIGS.get(shop_type_str, {
            "quality_level": ShopQuality.STANDARD.value,
            "initial_gold": 1000,
            "inventory_size": 25
        })

        # Set default values
        if gold_reserve is None:
            gold_reserve = config["initial_gold"]

        if inventory_size is None:
            inventory_size = config["inventory_size"]

        # Validate numeric inputs
        if not self._validate_numeric_inputs(gold_reserve, inventory_size):
            return None

        # Create inventory
        inventory = ShopInventory(max_size=inventory_size)
        initial_items = self.item_service.generate_inventory(shop_type_str, inventory_size)
        for item in initial_items:
            inventory.add_item(item)

        # Create economy
        economy = ShopEconomy(
            gold_reserves=gold_reserve,
            quality_modifier=self._get_quality_modifier(quality_level_str)
        )

        # Create shop
        shop = Shop(
            id=shop_id,
            name=name,
            shop_type=shop_type,  # Keep original type (enum or string)
            location=location,
            owner=owner,
            quality_level=quality_level,  # Keep original type (enum or string)
            inventory=inventory,
            economy=economy
        )

        return shop

    def _validate_shop_inputs(self, shop_id: str, name: str, shop_type: str, quality_level: str) -> bool:
        """Validate shop input parameters"""
        # Validate shop_id
        if not shop_id or len(shop_id.strip()) < 3:
            return False

        # Validate name
        if not name or len(name.strip()) < 3 or len(name) > 50:
            return False

        # Handle enum input for shop_type
        shop_type_str = shop_type
        if hasattr(shop_type, 'value'):
            shop_type_str = shop_type.value

        # Validate shop_type
        if not ShopType.is_valid_type(shop_type_str):
            return False

        # Handle enum input for quality_level
        quality_level_str = quality_level
        if hasattr(quality_level, 'value'):
            quality_level_str = quality_level.value

        # Validate quality_level
        if not ShopQuality.is_valid_quality(quality_level_str):
            return False

        return True

    def _validate_numeric_inputs(self, gold_reserve: int, inventory_size: int) -> bool:
        """Validate numeric input parameters"""
        if gold_reserve < 100 or gold_reserve > 10000:
            return False

        if inventory_size < 10 or inventory_size > 50:
            return False

        return True

    def _get_quality_modifier(self, quality_level: str) -> float:
        """Get quality modifier for pricing"""
        modifiers = {
            ShopQuality.BASIC.value: 0.8,
            ShopQuality.STANDARD.value: 1.0,
            ShopQuality.PREMIUM.value: 1.2,
            ShopQuality.LUXURY.value: 1.5
        }
        return modifiers.get(quality_level, 1.0)


class ShopTransactionService:
    """Service for shop transaction logic"""

    def __init__(self):
        self.pricing_service = ItemPricingService()

    def process_buy_transaction(self, shop: Shop, item_id: str, character_gold: int,
                               character_reputation: int = 50) -> Dict[str, Any]:
        """Process buy transaction"""
        # Find item
        item = shop.inventory.find_item(item_id)
        if not item or not item.is_available():
            return {
                "success": False,
                "reason": "Item not available",
                "item": None
            }

        # Calculate price
        final_price = self.pricing_service.calculate_buy_price(
            shop, item, character_reputation
        )

        # Check if character can afford
        if character_gold < final_price:
            return {
                "success": False,
                "reason": "Insufficient gold",
                "required_gold": final_price,
                "available_gold": character_gold,
                "item": None
            }

        # Check if shop can afford
        if not shop.economy.can_afford(final_price):
            return {
                "success": False,
                "reason": "Shop cannot afford to buy this item",
                "item": None
            }

        # Process transaction
        shop.economy.update_gold_reserves(-final_price)
        shop.inventory.remove_item(item_id)

        # Create transaction record
        transaction = ShopTransaction.create_buy_transaction(
            item, 1, final_price, character_reputation
        )
        shop.add_transaction(transaction)

        return {
            "success": True,
            "item": item.get_summary(),
            "price_paid": final_price,
            "gold_spent": final_price,
            "remaining_gold": character_gold - final_price,
            "shop_gold_remaining": shop.economy.gold_reserves
        }

    def process_sell_transaction(self, shop: Shop, item: ShopItem,
                                character_reputation: int = 50) -> Dict[str, Any]:
        """Process sell transaction"""
        # Check if shop can buy this item type
        if not shop.can_buy_item_type(item.item_type):
            return {
                "success": False,
                "reason": f"This shop doesn't buy {item.item_type} items",
                "gold_received": 0,
                "item_sold": None
            }

        # Calculate offer
        final_offer = self.pricing_service.calculate_sell_price(
            shop, item, character_reputation
        )

        # Check if shop can afford
        if not shop.economy.can_afford(final_offer):
            return {
                "success": False,
                "reason": "Shop doesn't have enough gold",
                "gold_received": 0,
                "item_sold": None
            }

        # Process transaction
        shop.economy.update_gold_reserves(-final_offer)

        # Add to inventory if space available
        item_added = shop.inventory.add_item(item)

        # Create transaction record
        transaction = ShopTransaction.create_sell_transaction(
            item, 1, final_offer, character_reputation
        )
        shop.add_transaction(transaction)

        return {
            "success": True,
            "item_sold": item.get_summary(),
            "gold_received": final_offer,
            "market_value": item.value,
            "shop_gold_remaining": shop.economy.gold_reserves,
            "item_added": item_added
        }


class ShopInventoryService:
    """Service for shop inventory management"""

    def __init__(self):
        self.item_service = ItemGenerationService()

    def refresh_inventory(self, shop: Shop, current_day: int) -> Dict[str, Any]:
        """Refresh shop inventory"""
        # Generate new items
        new_items = self.item_service.generate_inventory(
            shop.shop_type, shop.inventory.max_size
        )

        # Refresh inventory
        items_added = shop.inventory.refresh(new_items)
        shop.restock_timer = 0

        return {
            "success": True,
            "items_added": items_added,
            "current_inventory_size": shop.inventory.current_size,
            "max_inventory_size": shop.inventory.max_size,
            "refresh_day": current_day
        }

    def restock_shop(self, shop: Shop, items: Optional[List[ShopItem]] = None) -> Dict[str, Any]:
        """Restock shop with specific items or auto-generate"""
        if items is None:
            # Auto-restock based on shop type
            items = self.item_service.generate_inventory(shop.shop_type, shop.inventory.max_size)

        # Add items to inventory
        added_count = 0
        for item in items:
            if shop.inventory.add_item(item):
                added_count += 1

        # Reset restock timer
        shop.restock_timer = 0

        return {
            "success": True,
            "items_added": added_count,
            "current_inventory_size": shop.inventory.current_size,
            "max_inventory_size": shop.inventory.max_size
        }

    def get_inventory_summary(self, shop: Shop) -> Dict[str, Any]:
        """Get comprehensive inventory summary"""
        return {
            "total_items": shop.inventory.current_size,
            "max_size": shop.inventory.max_size,
            "last_refreshed": shop.inventory.last_refreshed,
            "item_types": shop.inventory.get_summary()["item_types"],
            "rarities": shop.inventory.get_summary()["rarities"],
            "items_by_type": {
                item_type: len(shop.inventory.get_items_by_type(item_type))
                for item_type in shop.inventory.get_summary()["item_types"]
            },
            "items_by_rarity": {
                rarity: len(shop.inventory.get_items_by_rarity(rarity))
                for rarity in shop.inventory.get_summary()["rarities"]
            }
        }


class ShopEconomyService:
    """Service for shop economic management"""

    def update_shop_economy(self, shop: Shop, economic_change: int,
                           location_wealth_change: int = 0) -> Dict[str, Any]:
        """Update shop economy based on transactions"""
        # Validate economic change
        if economic_change < -1000 or economic_change > 1000:
            return {
                "success": False,
                "reason": "Economic change must be between -1000 and 1000"
            }

        old_gold = shop.economy.gold_reserves

        # Update gold reserve
        shop.economy.update_gold_reserves(economic_change)

        # Update price modifier based on location wealth
        if location_wealth_change != 0:
            wealth_factor = 1.0 + (location_wealth_change * 0.05)
            shop.economy.price_modifier = max(
                0.5, min(2.0, shop.economy.price_modifier * wealth_factor)
            )

        # Update restock timer
        shop.restock_timer = max(0, shop.restock_timer - 1)

        return {
            "success": True,
            "old_gold_reserve": old_gold,
            "new_gold_reserve": shop.economy.gold_reserves,
            "economic_change": economic_change,
            "price_modifier": shop.economy.price_modifier,
            "restock_timer": shop.restock_timer
        }

    def get_economic_analysis(self, shop: Shop) -> Dict[str, Any]:
        """Get detailed economic analysis"""
        # Analyze recent transactions
        recent_transactions = shop.customer_history[-20:]  # Last 20 transactions

        buy_count = sum(1 for t in recent_transactions if t.transaction_type == "buy")
        sell_count = sum(1 for t in recent_transactions if t.transaction_type == "sell")

        total_buy_value = sum(t.total_price for t in recent_transactions if t.transaction_type == "buy")
        total_sell_value = sum(t.total_price for t in recent_transactions if t.transaction_type == "sell")

        # Calculate metrics
        transaction_ratio = buy_count / max(1, (buy_count + sell_count))
        profit_margin = (total_buy_value - total_sell_value) / max(1, total_buy_value) if total_buy_value > 0 else 0

        return {
            "current_gold": shop.economy.gold_reserves,
            "price_modifier": shop.economy.price_modifier,
            "recent_transactions": len(recent_transactions),
            "buy_transactions": buy_count,
            "sell_transactions": sell_count,
            "transaction_ratio": transaction_ratio,
            "total_buy_value": total_buy_value,
            "total_sell_value": total_sell_value,
            "profit_margin": profit_margin,
            "economic_health": self._assess_economic_health(shop, profit_margin)
        }

    def _assess_economic_health(self, shop: Shop, profit_margin: float) -> str:
        """Assess shop economic health"""
        if shop.economy.gold_reserves < 500:
            return "critical"
        elif shop.economy.gold_reserves < 1000:
            return "poor"
        elif profit_margin < 0.1:
            return "fair"
        elif profit_margin < 0.3:
            return "good"
        else:
            return "excellent"


class ShopManagementService:
    """Service for comprehensive shop management"""

    def __init__(self):
        self.creation_service = ShopCreationService()
        self.transaction_service = ShopTransactionService()
        self.inventory_service = ShopInventoryService()
        self.economy_service = ShopEconomyService()

    def get_shop_overview(self, shop: Shop) -> Dict[str, Any]:
        """Get complete shop overview"""
        return {
            "shop_info": shop.get_summary(),
            "inventory": self.inventory_service.get_inventory_summary(shop),
            "economy": self.economy_service.get_economic_analysis(shop),
            "recent_transactions": [
                {
                    "type": t.transaction_type,
                    "item": t.item_name,
                    "quantity": t.quantity,
                    "total_price": t.total_price,
                    "timestamp": t.timestamp.isoformat()
                }
                for t in shop.customer_history[-10:]
            ]
        }

    def update_reputation_discounts(self, shop: Shop, discount_config: Dict[str, float]) -> bool:
        """Update reputation discount configuration"""
        try:
            shop.reputation_discounts.update(discount_config)
            return True
        except Exception:
            return False

    def get_shop_statistics(self, shop: Shop) -> Dict[str, Any]:
        """Get comprehensive shop statistics"""
        return {
            "basic_info": {
                "name": shop.name,
                "type": shop.shop_type,
                "location": shop.location,
                "quality": shop.quality_level
            },
            "inventory_stats": self.inventory_service.get_inventory_summary(shop),
            "economic_stats": self.economy_service.get_economic_analysis(shop),
            "transaction_stats": {
                "total_transactions": len(shop.customer_history),
                "buy_transactions": sum(1 for t in shop.customer_history if t.transaction_type == "buy"),
                "sell_transactions": sum(1 for t in shop.customer_history if t.transaction_type == "sell")
            },
            "customer_engagement": {
                "avg_reputation": sum(t.customer_reputation for t in shop.customer_history) / max(1, len(shop.customer_history))
            }
        }
