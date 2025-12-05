from typing import Dict, List, Optional
from ..domain.equipment import Item

class InMemoryInventoryRepository:
    def __init__(self, max_size: int = 100):
        self._items: Dict[str, Item] = {}
        self.max_size = max_size

    def add_item(self, item: Item) -> None:
        self._items[item.id] = item

    def remove_item(self, item_id: str) -> None:
        if item_id in self._items:
            del self._items[item_id]

    def get_item(self, item_id: str) -> Optional[Item]:
        return self._items.get(item_id)

    def get_all_items(self) -> List[Item]:
        return list(self._items.values())

    def is_full(self) -> bool:
        return len(self._items) >= self.max_size
