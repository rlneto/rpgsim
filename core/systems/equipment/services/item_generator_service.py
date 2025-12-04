"""
Item Generator Service
"""
import random
import uuid
from typing import Dict, List
from core.models import Item, ItemType, ItemRarity
from ..domain.equipment import LootGenerationResult


class ItemGeneratorService:
    """Service for generating items"""

    def __init__(self):
        self.generated_items: Dict[str, Item] = {}
        self.adjectives = ["Burning", "Frozen", "Swift", "Heavy", "Ancient", "Cursed", "Blessed", "Shiny", "Rusty", "Sharp"]
        self.nouns = ["Might", "Wisdom", "Agility", "Protection", "Shadows", "Light", "Kings", "Dragons", "Doom", "Hope"]

    def generate_unique_item(self, item_id: str, item_type: ItemType, rarity: ItemRarity = None) -> Item:
        """Generate a unique item"""
        if rarity is None:
            rarity = random.choice(list(ItemRarity))

        name_prefix = rarity.value.title()
        type_name = item_type.value.title()

        adj = random.choice(self.adjectives)
        noun = random.choice(self.nouns)

        short_id = item_id[-4:] if len(item_id) >= 4 else item_id
        name = f"{name_prefix} {type_name} of {adj} {noun} {short_id}"

        stats = self._generate_stats(item_type, rarity)
        value = self._calculate_value(rarity, stats)

        item = Item(
            id=item_id,
            name=name,
            type=item_type,
            rarity=rarity,
            value=value,
            stats_mod=stats,
            equippable=True,
            description=f"A {rarity.value} {item_type.value}."
        )

        self.generated_items[item_id] = item
        return item

    def generate_loot(self, difficulty: str) -> LootGenerationResult:
        """Generate loot based on difficulty"""
        item_count = 1
        gold_base = 20
        rarity_weights = {ItemRarity.COMMON: 0.8, ItemRarity.UNCOMMON: 0.2}

        if difficulty == "medium":
            gold_base = 50
            rarity_weights = {ItemRarity.COMMON: 0.5, ItemRarity.UNCOMMON: 0.4, ItemRarity.RARE: 0.1}
        elif difficulty == "hard":
            gold_base = 100
            rarity_weights = {ItemRarity.UNCOMMON: 0.5, ItemRarity.RARE: 0.4, ItemRarity.EPIC: 0.1}

        items = []
        rarity_dist = {r.value: 0 for r in ItemRarity}

        for _ in range(item_count):
            rarity = random.choices(list(rarity_weights.keys()), weights=list(rarity_weights.values()), k=1)[0]
            item_type = random.choice([ItemType.WEAPON, ItemType.ARMOR, ItemType.ACCESSORY])
            item = self.generate_unique_item(f"loot_{uuid.uuid4()}", item_type, rarity)
            items.append(item)
            rarity_dist[rarity.value] += 1

        gold = random.randint(gold_base, gold_base * 2)

        return LootGenerationResult(items, gold, rarity_dist)

    def generate_all_unique_items(self) -> List[Item]:
        """Generate a full set of unique items"""
        items = []
        types = [ItemType.WEAPON, ItemType.ARMOR, ItemType.ACCESSORY]

        for i in range(200):
            item_type = types[i % 3]
            item = self.generate_unique_item(f"unique_{i:03d}", item_type)
            items.append(item)

        return items

    def _generate_stats(self, item_type: ItemType, rarity: ItemRarity) -> Dict[str, int]:
        """Generate stats for item"""
        multiplier = {
            ItemRarity.COMMON: 1,
            ItemRarity.UNCOMMON: 2,
            ItemRarity.RARE: 3,
            ItemRarity.EPIC: 5,
            ItemRarity.LEGENDARY: 10
        }.get(rarity, 1)

        stats = {}
        if item_type == ItemType.WEAPON:
            stats["strength"] = 2 * multiplier
            stats["dexterity"] = 1 * multiplier
            stats["critical_chance"] = 1 * multiplier
        elif item_type == ItemType.ARMOR:
            stats["constitution"] = 2 * multiplier
            stats["defense"] = 5 * multiplier
        elif item_type == ItemType.ACCESSORY:
            stats["wisdom"] = 2 * multiplier
            stats["intelligence"] = 2 * multiplier

        return stats

    def _calculate_value(self, rarity: ItemRarity, stats: Dict[str, int]) -> int:
        """Calculate gold value"""
        base = sum(stats.values()) * 10
        mult = {
            ItemRarity.COMMON: 1,
            ItemRarity.UNCOMMON: 2,
            ItemRarity.RARE: 5,
            ItemRarity.EPIC: 10,
            ItemRarity.LEGENDARY: 50
        }.get(rarity, 1)
        return max(10, base * mult)
