"""
Location System for RPGSim
Optimized for LLM agents with explicit, deterministic behavior
"""

from typing import List, Dict, Any, Optional, Tuple
import random
import time

from core.models import Location, LocationType
from core.validation import ValidationError


def create_location(
    id: str,
    name: str,
    type: LocationType,
    level: int,
    description: str = "",
    enemies: Optional[List[Any]] = None,
    npcs: Optional[List[Any]] = None,
    items: Optional[List[Any]] = None,
    quests: Optional[List[Any]] = None,
    connections: Optional[List[str]] = None,
) -> Location:
    """
    Create new location with explicit contract.

    Args:
        id: Location identifier (1-50 chars, unique)
        name: Location name (1-100 chars)
        type: Location type from LocationType enum
        level: Recommended level (1-100)
        description: Location description (0-500 chars)
        enemies: List of enemies at location
        npcs: List of NPCs at location
        items: List of items at location
        quests: List of quests at location
        connections: List of connected location IDs

    Returns:
        Location: Created location with valid properties

    Raises:
        ValidationError: If parameters are invalid
    """
    try:
        location = Location(
            id=id,
            name=name,
            type=type,
            level=level,
            description=description,
            enemies=enemies or [],
            npcs=npcs or [],
            items=items or [],
            quests=quests or [],
            connections=connections or [],
        )
        return location
    except Exception as e:
        raise ValidationError(f"Failed to create location: {str(e)}")


def get_location_by_id(
    location_id: str, locations: Dict[str, Location]
) -> Optional[Location]:
    """
    Get location by ID from location dictionary.

    Args:
        location_id: Location identifier to find
        locations: Dictionary of locations to search

    Returns:
        Optional[Location]: Location if found, None otherwise

    Raises:
        ValidationError: If parameters are invalid
    """
    if not location_id or not location_id.strip():
        raise ValidationError("Location ID cannot be empty")

    if not isinstance(locations, dict):
        raise ValidationError("Locations must be a dictionary")

    return locations.get(location_id)


def get_locations_by_type(
    location_type: LocationType, locations: Dict[str, Location]
) -> List[Location]:
    """
    Get all locations of specific type.

    Args:
        location_type: Type of locations to find
        locations: Dictionary of locations to search

    Returns:
        List[Location]: List of locations of specified type

    Raises:
        ValidationError: If parameters are invalid
    """
    if not isinstance(locations, dict):
        raise ValidationError("Locations must be a dictionary")

    return [
        location for location in locations.values() if location.type == location_type
    ]


def calculate_travel_time(
    from_location: Location,
    to_location: Location,
    character_level: int = 1,
    travel_method: str = "walking",
) -> int:
    """
    Calculate travel time between locations.

    Args:
        from_location: Starting location
        to_location: Destination location
        character_level: Character level affecting travel speed
        travel_method: Method of travel (walking, horse, cart)

    Returns:
        int: Travel time in minutes

    Raises:
        ValidationError: If parameters are invalid
    """
    if not isinstance(from_location, Location):
        raise ValidationError("From location must be a Location object")

    if not isinstance(to_location, Location):
        raise ValidationError("To location must be a Location object")

    if character_level < 1 or character_level > 100:
        raise ValidationError("Character level must be between 1 and 100")

    # Base travel time calculation (simplified for TDD)
    base_time = 30  # 30 minutes base time

    # Distance factor (using level difference as proxy for distance)
    level_difference = abs(to_location.level - from_location.level)
    distance_factor = 1 + (level_difference * 0.1)

    # Character speed factor
    speed_factor = 1.0 + (character_level * 0.01)  # Higher level = faster travel

    # Travel method modifier
    method_modifiers = {"walking": 1.0, "horse": 0.7, "cart": 0.8, "fast": 0.5}
    method_modifier = method_modifiers.get(travel_method, 1.0)

    # Final calculation
    travel_time = int(base_time * distance_factor / speed_factor * method_modifier)

    # Ensure minimum travel time
    return max(travel_time, 5)


def get_adjacent_locations(
    location: Location, locations: Dict[str, Location]
) -> List[Location]:
    """
    Get all locations connected to given location.

    Args:
        location: Location to get adjacents for
        locations: Dictionary of all locations

    Returns:
        List[Location]: List of adjacent locations

    Raises:
        ValidationError: If parameters are invalid
    """
    if not isinstance(location, Location):
        raise ValidationError("Location must be a Location object")

    if not isinstance(locations, dict):
        raise ValidationError("Locations must be a dictionary")

    adjacent_locations = []

    for connection_id in location.connections:
        connected_location = locations.get(connection_id)
        if connected_location:
            adjacent_locations.append(connected_location)

    return adjacent_locations


def validate_travel_requirements(
    character_level: int,
    target_location: Location,
    current_gold: int = 0,
    required_items: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Validate if character can travel to location.

    Args:
        character_level: Character level
        target_location: Destination location
        current_gold: Current gold amount
        required_items: List of required items

    Returns:
        Dict[str, Any]: Validation result with can_travel flag

    Raises:
        ValidationError: If parameters are invalid
    """
    if character_level < 1 or character_level > 100:
        raise ValidationError("Character level must be between 1 and 100")

    if not isinstance(target_location, Location):
        raise ValidationError("Target location must be a Location object")

    if current_gold < 0:
        raise ValidationError("Current gold cannot be negative")

    # Level requirement check
    level_requirement = target_location.level
    meets_level_requirement = character_level >= level_requirement

    # Gold requirement check (base cost)
    gold_requirement = max(0, target_location.level * 10)  # 10 gold per level
    meets_gold_requirement = current_gold >= gold_requirement

    # Item requirement check
    meets_item_requirement = True
    if required_items:
        # For now, assume character has required items
        # This will be expanded when inventory system is implemented
        meets_item_requirement = True

    can_travel = (
        meets_level_requirement and meets_gold_requirement and meets_item_requirement
    )

    return {
        "can_travel": can_travel,
        "level_requirement": level_requirement,
        "meets_level_requirement": meets_level_requirement,
        "gold_requirement": gold_requirement,
        "meets_gold_requirement": meets_gold_requirement,
        "item_requirements": required_items or [],
        "meets_item_requirement": meets_item_requirement,
        "reasons": [],
    }


def update_location_state(
    location: Location,
    character_visits: bool = True,
    enemies_defeated: Optional[List[Any]] = None,
    items_taken: Optional[List[Any]] = None,
    quests_completed: Optional[List[Any]] = None,
) -> Location:
    """
    Update location state after character interaction.

    Args:
        location: Location to update
        character_visits: Whether character visited location
        enemies_defeated: List of defeated enemies
        items_taken: List of taken items
        quests_completed: List of completed quests

    Returns:
        Location: Updated location

    Raises:
        ValidationError: If parameters are invalid
    """
    if not isinstance(location, Location):
        raise ValidationError("Location must be a Location object")

    # Update visit status
    if character_visits:
        location.mark_visited()

    # Update enemies (remove defeated ones)
    if enemies_defeated:
        for enemy in enemies_defeated:
            if enemy in location.enemies:
                location.enemies.remove(enemy)

    # Update items (remove taken ones)
    if items_taken:
        for item in items_taken:
            if item in location.items:
                location.items.remove(item)

    # Update quests (remove completed ones)
    if quests_completed:
        for quest in quests_completed:
            if quest in location.quests:
                location.quests.remove(quest)

    return location


def get_location_description(
    location: Location, character_level: int = 1, include_secrets: bool = False
) -> str:
    """
    Get formatted location description for character.

    Args:
        location: Location to describe
        character_level: Character level affecting description detail
        include_secrets: Whether to include secret information

    Returns:
        str: Formatted location description

    Raises:
        ValidationError: If parameters are invalid
    """
    if not isinstance(location, Location):
        raise ValidationError("Location must be a Location object")

    if character_level < 1 or character_level > 100:
        raise ValidationError("Character level must be between 1 and 100")

    # Base description
    description_parts = [f"{location.name}"]

    if location.description:
        description_parts.append(location.description)

    # Level information
    difficulty = location.get_difficulty_rating()
    description_parts.append(f"Difficulty: {difficulty}")

    # Location type information
    type_descriptions = {
        LocationType.TOWN: "A peaceful settlement",
        LocationType.DUNGEON: "A dangerous underground complex",
        LocationType.FOREST: "A dense woodland area",
        LocationType.MOUNTAIN: "A towering mountain range",
        LocationType.DESERT: "An arid desert wasteland",
        LocationType.CASTLE: "A fortified stronghold",
        LocationType.TEMPLE: "An ancient place of worship",
        LocationType.CAVE: "A dark natural cavern",
        LocationType.RUINS: "Remnants of an ancient civilization",
        LocationType.CAMP: "A temporary encampment",
    }

    type_desc = type_descriptions.get(location.type, "An unknown location type")
    description_parts.append(f"Type: {type_desc}")

    # Dynamic information based on character level and location state
    if location.level > character_level + 10:
        description_parts.append("⚠️ This location seems too dangerous for you.")

    if location.enemies and len(location.enemies) > 0:
        enemy_count = len(location.enemies)
        description_parts.append(f"Enemies present: {enemy_count}")

    if location.npcs and len(location.npcs) > 0:
        npc_count = len(location.npcs)
        description_parts.append(f"NPCs present: {npc_count}")

    if location.items and len(location.items) > 0:
        item_count = len(location.items)
        description_parts.append(f"Items available: {item_count}")

    # Secret information (only if high enough level or location visited)
    if include_secrets and (character_level >= location.level or location.visited):
        if location.quests and len(location.quests) > 0:
            quest_count = len(location.quests)
            description_parts.append(f"📜 Special quests available: {quest_count}")

    return " | ".join(description_parts)
