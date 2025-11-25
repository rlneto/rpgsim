"""
Navigation System for RPGSim
Optimized for LLM agents with explicit, deterministic behavior
"""

from typing import List, Dict, Any, Optional, Tuple
import random

from core.models import Location, LocationType, Character
from core.validation import ValidationError


# Global travel data storage (for TDD implementation)
TRAVEL_DATA: Dict[str, Dict[str, Any]] = {}


def travel_to_location(
    character: Character,
    from_location_id: str,
    to_location_id: str,
    locations: Dict[str, Location],
    travel_method: str = "walking",
) -> Dict[str, Any]:
    """
    Travel to a location with explicit contract.

    Args:
        character: Character traveling
        from_location_id: Starting location ID
        to_location_id: Destination location ID
        locations: Dictionary of all locations
        travel_method: Method of travel (walking, horse, cart, fast)

    Returns:
        Dict[str, Any]: Travel result with status and details

    Raises:
        ValidationError: If parameters are invalid
    """
    # Validate inputs
    if not isinstance(character, Character):
        raise ValidationError("Character must be a Character object")

    if not from_location_id or not to_location_id:
        raise ValidationError("Location IDs cannot be empty")

    if not isinstance(locations, dict):
        raise ValidationError("Locations must be a dictionary")

    # Get locations
    from_location = get_location_by_id(from_location_id, locations)
    to_location = get_location_by_id(to_location_id, locations)

    if not from_location or not to_location:
        raise ValidationError("Invalid location IDs")

    # Validate travel requirements
    travel_validation = validate_travel_requirements(
        character.level, to_location, character.gold, []
    )

    if not travel_validation["can_travel"]:
        return {
            "success": False,
            "reason": travel_validation["reasons"][0]
            if travel_validation["reasons"]
            else "Cannot travel",
            "travel_time": 0,
            "events": [],
        }

    # Calculate travel time
    travel_time = calculate_travel_time(
        from_location, to_location, character.level, travel_method
    )

    # Process travel (consume resources, update character)
    gold_cost = max(0, travel_time // 10)  # 1 gold per 10 minutes

    # Store travel data
    travel_id = (
        f"travel_{character.id}_{from_location_id}_{to_location_id}_{len(TRAVEL_DATA)}"
    )

    TRAVEL_DATA[travel_id] = {
        "character_id": character.id,
        "from_location_id": from_location_id,
        "to_location_id": to_location_id,
        "travel_method": travel_method,
        "travel_time": travel_time,
        "gold_cost": gold_cost,
        "start_time": 0,  # Would be actual time in real implementation
        "events": [],
        "status": "in_progress",
    }

    return {
        "success": True,
        "travel_id": travel_id,
        "from_location": from_location.name,
        "to_location": to_location.name,
        "travel_method": travel_method,
        "travel_time": travel_time,
        "gold_cost": gold_cost,
        "events": [],
    }


def get_available_destinations(
    current_location_id: str, locations: Dict[str, Location], character_level: int = 1
) -> List[Dict[str, Any]]:
    """
    Get available destinations from current location.

    Args:
        current_location_id: Current location ID
        locations: Dictionary of all locations
        character_level: Character level affecting available destinations

    Returns:
        List[Dict[str, Any]]: List of available destinations

    Raises:
        ValidationError: If parameters are invalid
    """
    if not current_location_id:
        raise ValidationError("Current location ID cannot be empty")

    if not isinstance(locations, dict):
        raise ValidationError("Locations must be a dictionary")

    current_location = get_location_by_id(current_location_id, locations)
    if not current_location:
        raise ValidationError("Invalid current location ID")

    # Get connected locations
    adjacent_locations = []
    for connection_id in current_location.connections:
        connected_location = get_location_by_id(connection_id, locations)
        if connected_location:
            # Check if character can travel there (level requirement)
            if (
                connected_location.level <= character_level + 5
            ):  # Can travel to slightly higher levels
                adjacent_locations.append(
                    {
                        "location_id": connection_id,
                        "name": connected_location.name,
                        "level": connected_location.level,
                        "type": connected_location.type.value,
                        "distance": abs(
                            connected_location.level - current_location.level
                        ),
                        "travel_time": calculate_travel_time(
                            current_location, connected_location, character_level
                        ),
                        "can_travel": True,
                        "requirements": {
                            "level": connected_location.level,
                            "gold": max(0, connected_location.level * 10),
                        },
                    }
                )

    return adjacent_locations


def calculate_travel_cost(
    from_location: Location,
    to_location: Location,
    character_level: int = 1,
    travel_method: str = "walking",
    equipment_bonus: float = 1.0,
) -> Dict[str, Any]:
    """
    Calculate travel cost with explicit formula.

    Args:
        from_location: Starting location
        to_location: Destination location
        character_level: Character level affecting cost
        travel_method: Method of travel
        equipment_bonus: Equipment bonus multiplier

    Returns:
        Dict[str, Any]: Cost breakdown

    Raises:
        ValidationError: If parameters are invalid
    """
    if not isinstance(from_location, Location):
        raise ValidationError("From location must be a Location object")

    if not isinstance(to_location, Location):
        raise ValidationError("To location must be a Location object")

    # Base cost calculation
    level_difference = abs(to_location.level - from_location.level)
    distance_factor = 1 + (level_difference * 0.1)

    # Character speed factor
    speed_factor = 1.0 + (character_level * 0.01)

    # Travel method modifier
    method_modifiers = {"walking": 1.0, "horse": 0.7, "cart": 0.8, "fast": 0.5}
    method_modifier = method_modifiers.get(travel_method, 1.0)

    # Terrain modifier (simplified - would use location type in real implementation)
    terrain_modifiers = {
        LocationType.TOWN: 1.0,
        LocationType.DUNGEON: 1.5,
        LocationType.FOREST: 1.2,
        LocationType.MOUNTAIN: 1.8,
        LocationType.DESERT: 1.6,
        LocationType.CASTLE: 1.1,
        LocationType.TEMPLE: 1.0,
        LocationType.CAVE: 1.4,
        LocationType.RUINS: 1.3,
        LocationType.CAMP: 1.0,
    }

    terrain_modifier = terrain_modifiers.get(to_location.type, 1.0)

    # Final cost calculation
    base_cost = 10  # Base cost in gold
    final_cost = int(
        base_cost
        * distance_factor
        / speed_factor
        * method_modifier
        * terrain_modifier
        * equipment_bonus
    )

    # Ensure minimum cost
    final_cost = max(final_cost, 5)

    return {
        "base_cost": base_cost,
        "distance_factor": distance_factor,
        "speed_factor": speed_factor,
        "method_modifier": method_modifier,
        "terrain_modifier": terrain_modifier,
        "equipment_bonus": equipment_bonus,
        "final_cost": final_cost,
        "gold_cost": final_cost,
        "time_cost": final_cost,  # 1 gold = 1 minute
    }


def validate_travel_conditions(
    character: Character, target_location: Location, travel_method: str = "walking"
) -> Dict[str, Any]:
    """
    Validate if character can travel under current conditions.

    Args:
        character: Character attempting to travel
        target_location: Destination location
        travel_method: Method of travel

    Returns:
        Dict[str, Any]: Validation result

    Raises:
        ValidationError: If parameters are invalid
    """
    if not isinstance(character, Character):
        raise ValidationError("Character must be a Character object")

    if not isinstance(target_location, Location):
        raise ValidationError("Target location must be a Location object")

    # Check character status
    if character.hp <= 0:
        return {
            "can_travel": False,
            "reason": "Character is defeated",
            "character_status": "defeated",
        }

    # Check location requirements
    if target_location.level > character.level + 10:
        return {
            "can_travel": False,
            "reason": f"Location too dangerous (level {target_location.level} vs character level {character.level})",
            "level_gap": target_location.level - character.level,
        }

    # Check travel method requirements
    if travel_method == "fast" and character.level < 10:
        return {
            "can_travel": False,
            "reason": f"Fast travel requires level 10+ (character level {character.level})",
            "required_level": 10,
        }

    # Check gold requirement
    gold_required = max(0, target_location.level * 10)
    if character.gold < gold_required:
        return {
            "can_travel": False,
            "reason": f"Insufficient gold (need {gold_required}, have {character.gold})",
            "gold_required": gold_required,
            "gold_have": character.gold,
        }

    return {
        "can_travel": True,
        "reason": "Travel conditions met",
        "character_status": "healthy",
        "level_requirement": target_location.level,
        "gold_requirement": gold_required,
    }


def process_travel_event(
    travel_id: str, event_type: str, event_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Process a travel event.

    Args:
        travel_id: Travel session ID
        event_type: Type of event (encounter, merchant, treasure, etc.)
        event_data: Event-specific data

    Returns:
        Dict[str, Any]: Event processing result

    Raises:
        ValidationError: If parameters are invalid
    """
    if not travel_id or travel_id not in TRAVEL_DATA:
        raise ValidationError("Invalid travel ID")

    if not event_type:
        raise ValidationError("Event type cannot be empty")

    travel_session = TRAVEL_DATA[travel_id]
    if not travel_session:
        raise ValidationError("Travel session not found")

    # Add event to travel session
    event = {
        "type": event_type,
        "data": event_data,
        "timestamp": len(travel_session["events"]),  # Simplified timestamp
    }

    travel_session["events"].append(event)

    # Process event based on type
    if event_type == "encounter":
        return process_encounter_event(travel_id, event_data)
    elif event_type == "merchant":
        return process_merchant_event(travel_id, event_data)
    elif event_type == "treasure":
        return process_treasure_event(travel_id, event_data)
    else:
        return {
            "success": True,
            "event_type": event_type,
            "message": f"Processed {event_type} event",
        }


def process_encounter_event(
    travel_id: str, encounter_data: Dict[str, Any]
) -> Dict[str, Any]:
    """Process combat encounter during travel."""
    # Simplified implementation for TDD
    enemy_type = encounter_data.get("enemy_type", "bandit")
    enemy_level = encounter_data.get("enemy_level", 1)

    outcomes = [
        {"type": "fight", "message": "You fight the enemy"},
        {"type": "flee", "message": "You flee from combat"},
        {"type": "negotiate", "message": "You negotiate with the enemy"},
    ]

    outcome = random.choice(outcomes)

    return {
        "success": True,
        "event_type": "encounter",
        "enemy_type": enemy_type,
        "enemy_level": enemy_level,
        "outcome": outcome["type"],
        "message": outcome["message"],
    }


def process_merchant_event(
    travel_id: str, merchant_data: Dict[str, Any]
) -> Dict[str, Any]:
    """Process merchant encounter during travel."""
    # Simplified implementation for TDD
    merchant_type = merchant_data.get("merchant_type", "trader")
    goods_offered = merchant_data.get("goods", ["rations", "potions"])

    return {
        "success": True,
        "event_type": "merchant",
        "merchant_type": merchant_type,
        "goods_offered": goods_offered,
        "message": f"You encounter a {merchant_type} with {goods_offered[0] if goods_offered else 'various goods'}",
    }


def process_treasure_event(
    travel_id: str, treasure_data: Dict[str, Any]
) -> Dict[str, Any]:
    """Process treasure discovery during travel."""
    # Simplified implementation for TDD
    treasure_type = treasure_data.get("treasure_type", "coins")
    treasure_value = treasure_data.get("value", 50)

    return {
        "success": True,
        "event_type": "treasure",
        "treasure_type": treasure_type,
        "treasure_value": treasure_value,
        "message": f"You found {treasure_type} worth {treasure_value} gold!",
    }


def complete_travel(travel_id: str, locations: Dict[str, Location]) -> Dict[str, Any]:
    """
    Complete travel and update location states.

    Args:
        travel_id: Travel session ID
        locations: Dictionary of all locations

    Returns:
        Dict[str, Any]: Travel completion result

    Raises:
        ValidationError: If parameters are invalid
    """
    if not travel_id or travel_id not in TRAVEL_DATA:
        raise ValidationError("Invalid travel ID")

    travel_session = TRAVEL_DATA[travel_id]
    if not travel_session:
        raise ValidationError("Travel session not found")

    # Update travel session status
    travel_session["status"] = "completed"

    # Update location visited status
    to_location = get_location_by_id(travel_session["to_location_id"], locations)
    if to_location:
        to_location.mark_visited()

    return {
        "success": True,
        "travel_id": travel_id,
        "status": "completed",
        "destination": to_location.name if to_location else "Unknown",
        "events_count": len(travel_session["events"]),
        "total_travel_time": travel_session["travel_time"],
    }


def get_travel_history(character_id: str) -> List[Dict[str, Any]]:
    """
    Get travel history for a character.

    Args:
        character_id: Character ID

    Returns:
        List[Dict[str, Any]]: List of past travels

    Raises:
        ValidationError: If parameters are invalid
    """
    if not character_id:
        raise ValidationError("Character ID cannot be empty")

    # Get all travel sessions for this character
    character_travels = []
    for travel_id, travel_data in TRAVEL_DATA.items():
        if travel_data["character_id"] == character_id:
            character_travels.append(
                {
                    "travel_id": travel_id,
                    "from_location": travel_data["from_location_id"],
                    "to_location": travel_data["to_location_id"],
                    "travel_method": travel_data["travel_method"],
                    "travel_time": travel_data["travel_time"],
                    "gold_cost": travel_data["gold_cost"],
                    "status": travel_data["status"],
                    "events_count": len(travel_data["events"]),
                }
            )

    return character_travels
