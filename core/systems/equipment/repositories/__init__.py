from .memory_repository import MemoryEquipmentRepository
from .in_memory_inventory_repository import InMemoryInventoryRepository

# Test expects InMemoryEquipmentRepository to be available
class InMemoryEquipmentRepository(MemoryEquipmentRepository):
    def get_all_slots(self):
        # Implementation for test `test_equipment_slots_initialization`
        from ..domain.equipment import EquipmentSlot, EquipmentSlotInfo
        # Return dict of slot_info
        return {slot: EquipmentSlotInfo(slot) for slot in EquipmentSlot}

__all__ = ["MemoryEquipmentRepository", "InMemoryInventoryRepository", "InMemoryEquipmentRepository"]
