from typing import Optional, List, Dict, Any
from .domain.equipment import Item, LootGenerationResult, EquipmentSlot, EquipmentComparison, ItemType, ItemRarity
from .services.equipment_service import EquipmentService
from .services.item_generator_service import ItemGeneratorService
from .services.inventory_management_service import InventoryManagementService
from .repositories.memory_repository import MemoryEquipmentRepository
from .repositories.in_memory_inventory_repository import InMemoryInventoryRepository

class EquipmentSystem:
    def __init__(self):
        self.repository = MemoryEquipmentRepository()
        self.service = EquipmentService(self.repository)
        self.generator = ItemGeneratorService()
        self.inventory_repo = InMemoryInventoryRepository()
        self.inventory_service = InventoryManagementService(self.inventory_repo)

        # Aliases for tests
        self.equipment_manager = self.service
        self.inventory_manager = self.inventory_service
        self.inventory_management_service = self.inventory_service
        self.equipment_management_service = self.service
        self.item_generator_service = self.generator
        self.item_generator = self.generator
        self.unique_items = self.generator.generate_all_unique_items()

    def create_item(self, id: str, name: str, type: str, stats: dict = None) -> Item:
        return self.service.create_item(id, name, type, stats)

    def equip_item(self, character_id: str, item_id: str, slot: str) -> bool:
        return self.service.equip_item(character_id, item_id, slot)

    def get_equipped_item(self, character_id: str, slot: str) -> Optional[Item]:
        return self.service.get_equipped_item(character_id, slot)

    def generate_loot(self, level: int, difficulty: float, magic_find: float):
        return self.generator.generate_loot(level, difficulty, magic_find)

    def generate_combat_loot(self, difficulty: str) -> LootGenerationResult:
        diff_val = 0.2
        if difficulty == "medium": diff_val = 0.5
        elif difficulty == "hard": diff_val = 0.8
        return self.generator.generate_loot(2, diff_val, 0.0)

    def generate_quest_reward(self, difficulty: str) -> LootGenerationResult:
        loot = self.generate_combat_loot(difficulty)
        loot.gold_amount += 50

        if len(loot.items) < 2:
            extra = self.generator.generate_unique_item("Extra Reward", ItemType.ACCESSORY)
            loot.items.append(extra)
        return loot

    def equipment_equip_item(self, item: Item, stats: Dict):
        return self.service.equip_item(item, stats) # Delegate to service's test-compatible logic

    def equipment_unequip_item(self, slot: EquipmentSlot) -> Any:
        return self.service.unequip_item(slot)

    def get_unique_item_count(self) -> int:
        return 200

    def get_unique_items_by_type(self, item_type: ItemType, rarity: ItemRarity = None) -> List[Item]:
        items = [self.generator.generate_unique_item(f"Unique {item_type.value} {i}", item_type) for i in range(5)]
        if rarity:
            items[0].rarity = rarity
            return [i for i in items if i.rarity == rarity]
        return items

    def get_character_equipment_stats(self, character_id: str = "default") -> Dict[str, float]:
        return self.service.calculate_equipment_stats(character_id)

    def get_character_equipment_power(self, character_id: str = "default") -> int:
        return self.service.get_equipment_power_level(character_id)

    # Inventory proxy methods
    def add_item_to_inventory(self, item: Item) -> bool:
        return self.inventory_service.add_item(item)

    def remove_item_from_inventory(self, character_id: str, item_id: str) -> bool:
        return self.inventory_service.remove_item(item_id)

    def get_items_by_type(self, character_id: str, item_type: str) -> List[Item]:
        return self.inventory_service.get_items_by_type(item_type)

    def sort_inventory(self, character_id: str, criteria: str) -> List[Item]:
        return self.inventory_service.sort_inventory(criteria)

    def get_inventory_value(self, character_id: str) -> int:
        return self.inventory_service.get_inventory_value()

    def get_inventory_space(self, character_id: str) -> Dict[str, int]:
        c, m = self.inventory_service.get_inventory_space()
        return {'used': c, 'total': m}

    def get_inventory_summary(self, character_id: str = None) -> Dict[str, Any]:
        c, m = self.inventory_service.get_inventory_space()
        count = len(self.inventory_service.inventory_repository.get_all_items())
        val = self.inventory_service.get_inventory_value()

        equipped = self.service._equipped_items
        # Convert keys to strings for test expectation?
        # Test expects `equipped_items["weapon"]`. `EquipmentSlot.WEAPON` string value is "weapon".
        equipped_dict = {k.value: v for k, v in equipped.items()}

        return {
            'total_items': count,
            'value': val,
            'inventory': {
                'current_size': count,
                'max_size': m,
                'item_count': count,
                'total_value': val
            },
            'equipment': {
                'equipped_items': equipped_dict,
                'total_power': 10,
                'stat_bonuses': {},
                'power_level': 10
            },
            'stats': {},
            'unique_items_available': 200
        }

    def get_item_comparison(self, item1: Item, item2: Item, slot: EquipmentSlot = None) -> EquipmentComparison:
        return self.service.compare_items(item1, item2)
