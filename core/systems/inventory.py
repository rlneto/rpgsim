"""
Inventory System for RPGSim
Optimized for LLM agents with explicit item management and equipment
"""

from typing import Dict, List, Any, Optional, Union
from core.models import Character, Item, ItemType
from core.validation import ValidationError


def add_item_to_inventory(character: Character, item: Union[Item, str], quantity: int = 1) -> Dict[str, Any]:
    """
    Add an item to character's inventory.

    Args:
        character: Character to add item to
        item: Item object or item name string
        quantity: Quantity of item to add

    Returns:
        Dict with addition results
    """
    if quantity <= 0:
        raise ValidationError("Quantity must be positive")

    # Handle string item names by creating a basic item
    if isinstance(item, str):
        # Determine item type based on name
        if any(weapon_word in item.lower() for weapon_word in ['sword', 'axe', 'hammer', 'dagger']):
            item_type = ItemType.WEAPON
            equippable = True
        elif any(armor_word in item.lower() for armor_word in ['armor', 'helmet', 'shield', 'boots']):
            item_type = ItemType.ARMOR
            equippable = True
        elif any(consumable_word in item.lower() for consumable_word in ['potion', 'elixir', 'scroll']):
            item_type = ItemType.CONSUMABLE
            equippable = False
        else:
            item_type = ItemType.MATERIAL
            equippable = False

        item_obj = Item(
            id=f"item_{item.lower().replace(' ', '_')}",
            name=item,
            type=item_type,
            description=f"A {item.lower()}",
            value=10,
            equippable=equippable,
            consumable=(item_type == ItemType.CONSUMABLE),
            max_stack=1
        )
    else:
        item_obj = item

    # Initialize inventory if character doesn't have one
    if not hasattr(character, 'inventory'):
        character.inventory = []

    # Add item to inventory
    for _ in range(quantity):
        character.inventory.append(item_obj)

    return {
        'success': True,
        'message': f'Added {quantity}x {item_obj.name} to inventory',
        'item_added': item_obj.name,
        'quantity': quantity,
        'total_items': len(character.inventory)
    }


def equip_item(character: Character, item: Union[Item, str]) -> Dict[str, Any]:
    """
    Equip an item from character's inventory.

    Args:
        character: Character to equip item on
        item: Item object or item name to equip

    Returns:
        Dict with equip results
    """
    if not hasattr(character, 'inventory'):
        return {
            'success': False,
            'message': 'Character has no inventory',
            'equipped_item': None
        }

    # Find item in inventory
    item_to_equip = None
    item_index = -1

    for i, inv_item in enumerate(character.inventory):
        if isinstance(item, str):
            # Compare by name if item is string
            if inv_item.name == item:
                item_to_equip = inv_item
                item_index = i
                break
        else:
            # Compare by object if item is Item
            if inv_item.id == item.id:
                item_to_equip = inv_item
                item_index = i
                break

    if not item_to_equip:
        return {
            'success': False,
            'message': f'Item {item if isinstance(item, str) else item.name} not found in inventory',
            'equipped_item': None
        }

    # Initialize equipment if character doesn't have one
    if not hasattr(character, 'equipment'):
        character.equipment = {}

    # Determine equipment slot based on item name/type
    slot = _get_equipment_slot(item_to_equip.name)

    # Move item from inventory to equipment
    if slot in character.equipment:
        # Unequip current item and move back to inventory
        old_item = character.equipment[slot]
        character.inventory.append(old_item)

    character.equipment[slot] = item_to_equip
    character.inventory.pop(item_index)

    return {
        'success': True,
        'message': f'Equipped {item_to_equip.name} in {slot} slot',
        'equipped_item': item_to_equip.name,
        'slot': slot,
        'equipment_slots': len(character.equipment) if hasattr(character, 'equipment') else 0
    }


def remove_item_from_inventory(character: Character, item: Union[Item, str], quantity: int = 1) -> Dict[str, Any]:
    """
    Remove an item from character's inventory.

    Args:
        character: Character to remove item from
        item: Item object or item name to remove
        quantity: Quantity to remove

    Returns:
        Dict with removal results
    """
    if not hasattr(character, 'inventory'):
        return {
            'success': False,
            'message': 'Character has no inventory',
            'removed_quantity': 0
        }

    if quantity <= 0:
        raise ValidationError("Quantity must be positive")

    # Find and remove items
    removed_count = 0
    items_to_remove = []

    for inv_item in character.inventory:
        if isinstance(item, str):
            if inv_item.name == item and removed_count < quantity:
                items_to_remove.append(inv_item)
                removed_count += 1
        else:
            if inv_item.id == item.id and removed_count < quantity:
                items_to_remove.append(inv_item)
                removed_count += 1

        if removed_count >= quantity:
            break

    # Remove items from inventory
    for item_to_remove in items_to_remove:
        character.inventory.remove(item_to_remove)

    return {
        'success': removed_count > 0,
        'message': f'Removed {removed_count}x {item if isinstance(item, str) else item.name} from inventory',
        'removed_quantity': removed_count,
        'requested_quantity': quantity,
        'remaining_items': len(character.inventory)
    }


def get_inventory_summary(character: Character) -> Dict[str, Any]:
    """
    Get summary of character's inventory.

    Args:
        character: Character to get inventory summary for

    Returns:
        Dict with inventory summary
    """
    if not hasattr(character, 'inventory'):
        return {
            'total_items': 0,
            'total_value': 0,
            'item_types': {},
            'has_equipment': False
        }

    inventory = character.inventory
    total_value = sum(getattr(item, 'value', 0) for item in inventory)
    item_types = {}

    for item in inventory:
        item_name = item.name
        if item_name in item_types:
            item_types[item_name] += 1
        else:
            item_types[item_name] = 1

    return {
        'total_items': len(inventory),
        'total_value': total_value,
        'item_types': item_types,
        'has_equipment': hasattr(character, 'equipment') and len(character.equipment) > 0,
        'equipment_slots': len(character.equipment) if hasattr(character, 'equipment') else 0
    }


def get_equipment_summary(character: Character) -> Dict[str, Any]:
    """
    Get summary of character's equipped items.

    Args:
        character: Character to get equipment summary for

    Returns:
        Dict with equipment summary
    """
    if not hasattr(character, 'equipment') or not character.equipment:
        return {
            'equipped_items': {},
            'total_slots': 0,
            'total_value': 0
        }

    equipment = character.equipment
    total_value = sum(getattr(item, 'value', 0) for item in equipment.values())

    return {
        'equipped_items': {slot: item.name for slot, item in equipment.items()},
        'total_slots': len(equipment),
        'total_value': total_value
    }


def _get_equipment_slot(item_name: str) -> str:
    """
    Determine equipment slot based on item name.

    Args:
        item_name: Name of the item

    Returns:
        Equipment slot name
    """
    item_lower = item_name.lower()

    if any(word in item_lower for word in ['sword', 'axe', 'hammer', 'dagger', 'weapon']):
        return 'weapon'
    elif any(word in item_lower for word in ['shield', 'armor', 'helmet', 'chest', 'boots']):
        return 'armor'
    elif any(word in item_lower for word in ['ring', 'amulet', 'necklace', 'bracelet']):
        return 'accessory'
    elif any(word in item_lower for word in ['robe', 'cloak', 'mantle']):
        return 'chest'
    elif any(word in item_lower for word in ['gloves', 'gauntlets']):
        return 'hands'
    elif any(word in item_lower for word in ['boots', 'shoes']):
        return 'feet'
    elif any(word in item_lower for word in ['hat', 'helmet', 'crown']):
        return 'head'
    else:
        return 'misc'


# Export all functions for easy access
__all__ = [
    'add_item_to_inventory',
    'remove_item_from_inventory',
    'equip_item',
    'get_inventory_summary',
    'get_equipment_summary'
]