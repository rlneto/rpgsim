from typing import Dict, Optional, List
from ..domain.equipment import Equipment, Item
from ..interfaces.repositories import EquipmentRepository

class MemoryEquipmentRepository(EquipmentRepository):
    def __init__(self):
        self._items: Dict[str, Item] = {}
        self._equipment: Dict[str, Equipment] = {}

    def add_item(self, item: Item) -> None:
        self._items[item.id] = item

    def get_item(self, item_id: str) -> Optional[Item]:
        return self._items.get(item_id)

    def list_items(self) -> List[Item]:
        return list(self._items.values())

    def get_equipment(self, character_id: str) -> Optional[Equipment]:
        return self._equipment.get(character_id)

    def save_equipment(self, equipment: Equipment) -> None:
        self._equipment[equipment.character_id] = equipment
