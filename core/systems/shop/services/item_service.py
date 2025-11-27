"""
Shop item generation and pricing services
"""
from typing import Dict, List, Any
from ..domain.shop import (
    ShopItem, Shop, ShopType, ItemRarity, ItemCondition, ShopQuality
)


class ItemGenerationService:
    """Service for generating shop items"""
    
    def __init__(self):
        self.item_pools = self._initialize_item_pools()
    
    def _initialize_item_pools(self) -> Dict[str, List[Dict[str, Any]]]:
        """Initialize item pools for different shop types"""
        return {
            ShopType.WEAPONS.value: [
                {
                    "name": "Iron Sword",
                    "item_type": "weapon",
                    "rarity": ItemRarity.COMMON.value,
                    "price": 100,
                    "value": 80,
                    "effect": "Standard damage"
                },
                {
                    "name": "Steel Axe",
                    "item_type": "weapon",
                    "rarity": ItemRarity.COMMON.value,
                    "price": 150,
                    "value": 120,
                    "effect": "High damage"
                },
                {
                    "name": "Silver Dagger",
                    "item_type": "weapon",
                    "rarity": ItemRarity.UNCOMMON.value,
                    "price": 300,
                    "value": 250,
                    "effect": "Swift strikes"
                },
                {
                    "name": "Enchanted Blade",
                    "item_type": "weapon",
                    "rarity": ItemRarity.RARE.value,
                    "price": 800,
                    "value": 600,
                    "effect": "Magic damage"
                }
            ],
            ShopType.ARMOR.value: [
                {
                    "name": "Leather Armor",
                    "item_type": "armor",
                    "rarity": ItemRarity.COMMON.value,
                    "price": 120,
                    "value": 100,
                    "effect": "Basic protection"
                },
                {
                    "name": "Chain Mail",
                    "item_type": "armor",
                    "rarity": ItemRarity.COMMON.value,
                    "price": 200,
                    "value": 180,
                    "effect": "Good protection"
                },
                {
                    "name": "Iron Shield",
                    "item_type": "shield",
                    "rarity": ItemRarity.COMMON.value,
                    "price": 80,
                    "value": 70,
                    "effect": "Defense boost"
                },
                {
                    "name": "Enchanted Plate",
                    "item_type": "armor",
                    "rarity": ItemRarity.RARE.value,
                    "price": 1200,
                    "value": 900,
                    "effect": "Magic resistance"
                }
            ],
            ShopType.POTIONS.value: [
                {
                    "name": "Health Potion",
                    "item_type": "potion",
                    "rarity": ItemRarity.COMMON.value,
                    "price": 50,
                    "value": 40,
                    "effect": "Restores health"
                },
                {
                    "name": "Mana Potion",
                    "item_type": "potion",
                    "rarity": ItemRarity.COMMON.value,
                    "price": 60,
                    "value": 50,
                    "effect": "Restores mana"
                },
                {
                    "name": "Stamina Potion",
                    "item_type": "potion",
                    "rarity": ItemRarity.UNCOMMON.value,
                    "price": 75,
                    "value": 60,
                    "effect": "Increases stamina"
                },
                {
                    "name": "Elixir of Life",
                    "item_type": "potion",
                    "rarity": ItemRarity.LEGENDARY.value,
                    "price": 2000,
                    "value": 1500,
                    "effect": "Full restoration"
                }
            ],
            ShopType.MAGIC_ITEMS.value: [
                {
                    "name": "Fire Scroll",
                    "item_type": "scroll",
                    "rarity": ItemRarity.UNCOMMON.value,
                    "price": 200,
                    "value": 180,
                    "effect": "Fire damage spell"
                },
                {
                    "name": "Healing Scroll",
                    "item_type": "scroll",
                    "rarity": ItemRarity.UNCOMMON.value,
                    "price": 250,
                    "value": 200,
                    "effect": "Healing spell"
                },
                {
                    "name": "Magic Ring",
                    "item_type": "magic",
                    "rarity": ItemRarity.RARE.value,
                    "price": 600,
                    "value": 450,
                    "effect": "Magic boost"
                },
                {
                    "name": "Staff of Power",
                    "item_type": "magic",
                    "rarity": ItemRarity.EPIC.value,
                    "price": 1500,
                    "value": 1200,
                    "effect": "Amplifies spells"
                }
            ],
            ShopType.GENERAL_GOODS.value: [
                {
                    "name": "Torch",
                    "item_type": "general",
                    "rarity": ItemRarity.COMMON.value,
                    "price": 5,
                    "value": 4,
                    "effect": "Light source"
                },
                {
                    "name": "Rope",
                    "item_type": "general",
                    "rarity": ItemRarity.COMMON.value,
                    "price": 10,
                    "value": 8,
                    "effect": "Climbing tool"
                },
                {
                    "name": "Rations",
                    "item_type": "general",
                    "rarity": ItemRarity.COMMON.value,
                    "price": 15,
                    "value": 12,
                    "effect": "Food supply"
                },
                {
                    "name": "Map Kit",
                    "item_type": "general",
                    "rarity": ItemRarity.UNCOMMON.value,
                    "price": 100,
                    "value": 80,
                    "effect": "Navigation aid"
                }
            ]
        }
    
    def generate_inventory(self, shop_type: str, inventory_size: int) -> List[ShopItem]:
        """Generate inventory for shop based on type and quality"""
        inventory = []
        
        # Get appropriate item pool
        item_pool = self.item_pools.get(shop_type, self.item_pools[ShopType.GENERAL_GOODS.value])
        
        # Generate items based on shop type rarity distribution
        rarity_distribution = self._get_rarity_distribution(shop_type)
        
        import random
        for i in range(inventory_size):
            # Select item template
            item_template = random.choice(item_pool).copy()
            
            # Select rarity based on distribution
            rarity = random.choices(
                list(rarity_distribution.keys()),
                weights=list(rarity_distribution.values()),
                k=1
            )[0]
            
            # Adjust value and price based on rarity
            rarity_multiplier = self._get_rarity_multiplier(rarity)
            adjusted_value = int(item_template["value"] * rarity_multiplier)
            adjusted_price = int(item_template["price"] * rarity_multiplier)
            
            # Create ShopItem
            item = ShopItem(
                id=f"{shop_type}_{i:03d}_{rarity}",
                name=item_template["name"],
                item_type=item_template["item_type"],
                effect=item_template["effect"],
                base_value=item_template["value"],
                value=adjusted_value,
                rarity=rarity,
                condition=random.choice([ItemCondition.GOOD.value, ItemCondition.EXCELLENT.value]),
                quantity=random.randint(1, 3)
            )
            
            inventory.append(item)
        
        return inventory[:inventory_size]
    
    def _get_rarity_distribution(self, shop_type: str) -> Dict[str, float]:
        """Get rarity distribution for shop type"""
        if shop_type in [ShopType.RARE_DEALER.value, ShopType.ARTIFACTS.value]:
            # Rare dealers have more rare items
            return {
                ItemRarity.COMMON.value: 0.1,
                ItemRarity.UNCOMMON.value: 0.3,
                ItemRarity.RARE.value: 0.4,
                ItemRarity.EPIC.value: 0.15,
                ItemRarity.LEGENDARY.value: 0.05
            }
        elif shop_type in [ShopType.BLACKSMITHING.value, ShopType.WEAPONS.value]:
            # Premium shops have better items
            return {
                ItemRarity.COMMON.value: 0.3,
                ItemRarity.UNCOMMON.value: 0.4,
                ItemRarity.RARE.value: 0.2,
                ItemRarity.EPIC.value: 0.08,
                ItemRarity.LEGENDARY.value: 0.02
            }
        else:
            # Standard distribution
            return {
                ItemRarity.COMMON.value: 0.6,
                ItemRarity.UNCOMMON.value: 0.25,
                ItemRarity.RARE.value: 0.1,
                ItemRarity.EPIC.value: 0.04,
                ItemRarity.LEGENDARY.value: 0.01
            }
    
    def _get_rarity_multiplier(self, rarity: str) -> float:
        """Get value multiplier for rarity"""
        multipliers = {
            ItemRarity.COMMON.value: 1.0,
            ItemRarity.UNCOMMON.value: 1.5,
            ItemRarity.RARE.value: 2.5,
            ItemRarity.EPIC.value: 5.0,
            ItemRarity.LEGENDARY.value: 10.0
        }
        return multipliers.get(rarity, 1.0)
    
    def generate_custom_item(self, name: str, item_type: str, base_value: int,
                             rarity: str = ItemRarity.COMMON.value,
                             condition: str = ItemCondition.GOOD.value,
                             effect: str = "Standard effect") -> ShopItem:
        """Generate custom shop item"""
        import uuid
        rarity_multiplier = self._get_rarity_multiplier(rarity)
        adjusted_value = int(base_value * rarity_multiplier)
        
        return ShopItem(
            id=str(uuid.uuid4())[:8],
            name=name,
            item_type=item_type,
            effect=effect,
            base_value=base_value,
            value=adjusted_value,
            rarity=rarity,
            condition=condition,
            quantity=1
        )


class ItemPricingService:
    """Service for item pricing calculations"""
    
    def calculate_buy_price(self, shop: Shop, item: ShopItem, 
                           character_reputation: int = 50) -> int:
        """Calculate final buy price for character"""
        # Get reputation discount
        reputation_discount = shop.get_reputation_discount(character_reputation)
        
        # Calculate base price
        base_price = item.get_effective_price()
        
        # Apply modifiers
        final_price = int(
            base_price * shop.economy.price_modifier * (1.0 - reputation_discount)
        )
        
        # Apply bulk discount for multiple items
        if item.quantity > 1:
            bulk_discount = min(0.2, item.quantity * 0.05)  # Up to 20% discount
            final_price = int(final_price * (1.0 - bulk_discount))
        
        return final_price
    
    def calculate_sell_price(self, shop: Shop, item: ShopItem,
                             character_reputation: int = 50) -> int:
        """Calculate final sell offer for character's item"""
        # Calculate market value
        market_value = item.value
        
        # Apply rarity multiplier
        rarity_multiplier = self._get_rarity_sell_multiplier(item.rarity)
        adjusted_market_value = int(market_value * rarity_multiplier)
        
        # Apply reputation modifier
        reputation_modifier = self._get_reputation_sell_modifier(character_reputation)
        
        # Calculate final offer
        final_offer = int(
            adjusted_market_value * shop.economy.price_modifier * reputation_modifier
        )
        
        # Apply shop gold reserve limitation
        max_offer = min(final_offer, shop.economy.gold_reserves)
        
        return max_offer
    
    def calculate_dynamic_price(self, shop: Shop, item: ShopItem,
                                supply_factor: float = 1.0, demand_factor: float = 1.0,
                                location_wealth: float = 1.0) -> int:
        """Calculate dynamic price based on market conditions"""
        base_price = item.get_effective_price()
        
        # Apply market factors
        supply_adjustment = 1.0 + (1.0 - supply_factor) * 0.3  # Low supply = higher price
        demand_adjustment = 1.0 + (demand_factor - 1.0) * 0.5   # High demand = higher price
        wealth_adjustment = 1.0 + (location_wealth - 1.0) * 0.2
        
        # Apply shop quality modifier
        quality_modifier = self._get_quality_price_modifier(shop.quality_level)
        
        # Calculate final dynamic price
        dynamic_price = int(
            base_price * supply_adjustment * demand_adjustment * 
            wealth_adjustment * quality_modifier
        )
        
        # Apply reasonable bounds
        min_price = int(base_price * 0.5)
        max_price = int(base_price * 2.0)
        
        return max(min_price, min(dynamic_price, max_price))
    
    def calculate_bulk_purchase_price(self, shop: Shop, items: List[ShopItem],
                                     character_reputation: int = 50) -> Dict[str, Any]:
        """Calculate price for bulk purchase with discount"""
        total_base_price = sum(item.get_effective_price() for item in items)
        
        # Get reputation discount
        reputation_discount = shop.get_reputation_discount(character_reputation)
        
        # Calculate bulk discount based on quantity
        total_quantity = sum(item.quantity for item in items)
        bulk_discount = min(0.3, total_quantity * 0.02)  # Up to 30% discount
        
        # Apply all modifiers
        final_total = int(
            total_base_price * shop.economy.price_modifier * 
            (1.0 - reputation_discount) * (1.0 - bulk_discount)
        )
        
        return {
            "total_base_price": total_base_price,
            "reputation_discount": reputation_discount,
            "bulk_discount": bulk_discount,
            "shop_modifier": shop.economy.price_modifier,
            "final_total": final_total,
            "items_purchased": len(items),
            "total_quantity": total_quantity
        }
    
    def _get_rarity_sell_multiplier(self, rarity: str) -> float:
        """Get sell price multiplier for rarity"""
        multipliers = {
            ItemRarity.COMMON.value: 1.0,
            ItemRarity.UNCOMMON.value: 1.5,
            ItemRarity.RARE.value: 2.5,
            ItemRarity.EPIC.value: 5.0,
            ItemRarity.LEGENDARY.value: 10.0
        }
        return multipliers.get(rarity, 1.0)
    
    def _get_reputation_sell_modifier(self, reputation: int) -> float:
        """Get reputation modifier for selling"""
        if reputation >= 80:
            return 1.2  # 20% bonus for high reputation
        elif reputation >= 60:
            return 1.1  # 10% bonus for good reputation
        elif reputation >= 40:
            return 1.0  # No bonus for neutral
        else:
            return 0.9  # 10% penalty for low reputation
    
    def _get_quality_price_modifier(self, quality: str) -> float:
        """Get price modifier for shop quality"""
        modifiers = {
            ShopQuality.BASIC.value: 0.8,
            ShopQuality.STANDARD.value: 1.0,
            ShopQuality.PREMIUM.value: 1.3,
            ShopQuality.LUXURY.value: 1.6
        }
        return modifiers.get(quality, 1.0)
