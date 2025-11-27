"""
City System for RPGSim
Optimized for LLM agents with explicit, deterministic behavior
"""

from typing import List, Dict, Any, Optional, Tuple
import random

from core.models import Location, LocationType
from core.validation import ValidationError


# Global city data storage (for TDD implementation)
CITY_DATA: Dict[str, Dict[str, Any]] = {}


def create_city(
    name: str,
    city_type: str = "commercial",
    population: int = 1000,
    wealth_level: int = 5,
    architectural_style: str = "medieval",
    cultural_elements: Optional[List[str]] = None,
) -> Location:
    """
    Create new city with explicit contract.

    Args:
        name: City name (3-50 chars)
        city_type: Type of city (commercial, military, religious, etc.)
        population: City population (10-100000)
        wealth_level: City wealth level (1-10)
        architectural_style: Style of architecture
        cultural_elements: List of cultural elements

    Returns:
        Location: Created city as Location object

    Raises:
        ValidationError: If parameters are invalid
    """
    if not name or len(name.strip()) < 3:
        raise ValidationError("City name must be at least 3 characters")

    if len(name) > 50:
        raise ValidationError("City name cannot exceed 50 characters")

    if population < 10 or population > 100000:
        raise ValidationError("Population must be between 10 and 100000")

    if wealth_level < 1 or wealth_level > 10:
        raise ValidationError("Wealth level must be between 1 and 10")

    # Generate city description based on parameters
    description = f"A {city_type} city with {population:,} inhabitants. "
    description += f"Wealth level: {wealth_level}/10. "
    description += f"Architecture: {architectural_style} style."

    # Determine location level based on wealth and population
    base_level = max(1, wealth_level)
    population_modifier = min(5, population // 10000)  # Large cities are higher level
    city_level = base_level + population_modifier

    # Create city as Location
    city_id = f"city_{name.lower().replace(' ', '_')}"

    city = Location(
        id=city_id,
        name=name,
        type=LocationType.TOWN,
        level=min(city_level, 100),
        description=description,
        enemies=[],
        npcs=[],
        items=[],
        quests=[],
        connections=[],
    )

    # Store city-specific data in global storage
    CITY_DATA[city_id] = {
        "city_type": city_type,
        "population": population,
        "wealth_level": wealth_level,
        "architectural_style": architectural_style,
        "cultural_elements": cultural_elements or [],
        "buildings": [],
        "shops": [],
        "reputation_modifiers": {},
    }

    return city


def get_city_buildings(city: Location) -> List[Dict[str, Any]]:
    """
    Get buildings available in city.

    Args:
        city: City location to get buildings for

    Returns:
        List[Dict[str, Any]]: List of buildings with their functions

    Raises:
        ValidationError: If parameters are invalid
    """
    if not isinstance(city, Location):
        raise ValidationError("City must be a Location object")

    city_id = city.id
    if city_id not in CITY_DATA:
        # Initialize city data if not present
        CITY_DATA[city_id] = {"buildings": [], "shops": [], "reputation_modifiers": {}}

    # Check if buildings already generated
    if CITY_DATA[city_id]["buildings"]:
        return CITY_DATA[city_id]["buildings"]

    # Generate buildings based on city type and wealth
    buildings = []

    # Core buildings (all cities have at least 8 types)
    core_buildings = [
        {"type": "inn", "name": "Local Inn", "function": "rest", "quality": "basic"},
        {
            "type": "training_grounds",
            "name": "Training Grounds",
            "function": "training",
            "quality": "standard",
        },
        {
            "type": "quest_board",
            "name": "Quest Board",
            "function": "quests",
            "quality": "active",
        },
        {
            "type": "crafting_station",
            "name": "Crafting Station",
            "function": "crafting",
            "quality": "equipped",
        },
        {
            "type": "market",
            "name": "Marketplace",
            "function": "trading",
            "quality": "busy",
        },
        {
            "type": "temple",
            "name": "Local Temple",
            "function": "healing",
            "quality": "peaceful",
        },
        {
            "type": "blacksmith",
            "name": "Blacksmith",
            "function": "equipment",
            "quality": "skilled",
        },
        {
            "type": "alchemist",
            "name": "Alchemist Shop",
            "function": "potions",
            "quality": "mysterious",
        },
    ]

    # Add buildings based on wealth level
    wealth_level = CITY_DATA[city_id].get("wealth_level", 5)

    if wealth_level >= 3:
        core_buildings.append(
            {
                "type": "library",
                "name": "City Library",
                "function": "knowledge",
                "quality": "extensive",
            }
        )

    if wealth_level >= 5:
        core_buildings.append(
            {
                "type": "arena",
                "name": "Combat Arena",
                "function": "entertainment",
                "quality": "exciting",
            }
        )

    if wealth_level >= 7:
        core_buildings.append(
            {
                "type": "mage_guild",
                "name": "Mages Guild",
                "function": "magic_training",
                "quality": "arcane",
            }
        )

    if wealth_level >= 9:
        core_buildings.append(
            {
                "type": "palace",
                "name": "Noble Palace",
                "function": "government",
                "quality": "grand",
            }
        )

    # Add city-specific buildings
    city_type = CITY_DATA[city_id].get("city_type", "commercial")

    if city_type == "military":
        core_buildings.extend(
            [
                {
                    "type": "barracks",
                    "name": "Military Barracks",
                    "function": "training",
                    "quality": "disciplined",
                },
                {
                    "type": "armory",
                    "name": "Armory",
                    "function": "equipment",
                    "quality": "military",
                },
            ]
        )
    elif city_type == "religious":
        core_buildings.extend(
            [
                {
                    "type": "grand_temple",
                    "name": "Grand Temple",
                    "function": "worship",
                    "quality": "divine",
                },
                {
                    "type": "monastery",
                    "name": "Monastery",
                    "function": "training",
                    "quality": "spiritual",
                },
            ]
        )
    elif city_type == "commercial":
        core_buildings.extend(
            [
                {
                    "type": "merchant_guild",
                    "name": "Merchants Guild",
                    "function": "trading",
                    "quality": "prosperous",
                },
                {
                    "type": "bank",
                    "name": "City Bank",
                    "function": "finance",
                    "quality": "secure",
                },
            ]
        )

    CITY_DATA[city_id]["buildings"] = buildings
    return buildings


def get_city_shops(city: Location) -> List[Dict[str, Any]]:
    """
    Get shops available in city.

    Args:
        city: City location to get shops for

    Returns:
        List[Dict[str, Any]]: List of shops with their inventories

    Raises:
        ValidationError: If parameters are invalid
    """
    if not isinstance(city, Location):
        raise ValidationError("City must be a Location object")

    city_id = city.id
    if city_id not in CITY_DATA:
        CITY_DATA[city_id] = {"buildings": [], "shops": [], "reputation_modifiers": {}}

    # Check if shops already generated
    if CITY_DATA[city_id]["shops"]:
        return CITY_DATA[city_id]["shops"]

    shops = []
    wealth_level = CITY_DATA[city_id].get("wealth_level", 5)
    city_type = CITY_DATA[city_id].get("city_type", "commercial")

    # Generate shops based on city type and wealth
    shop_types = [
        {
            "type": "weapon_smith",
            "name": "Weapon Smith",
            "specialty": "weapons",
            "inventory_size": 15,
        },
        {
            "type": "armor_merchant",
            "name": "Armor Merchant",
            "specialty": "armor",
            "inventory_size": 12,
        },
        {
            "type": "general_store",
            "name": "General Store",
            "specialty": "general",
            "inventory_size": 25,
        },
    ]

    # Add specialized shops based on wealth and type
    if wealth_level >= 4:
        shop_types.append(
            {
                "type": "magic_shop",
                "name": "Magic Shop",
                "specialty": "magic_items",
                "inventory_size": 10,
            }
        )

    if wealth_level >= 6:
        shop_types.append(
            {
                "type": "rare_dealer",
                "name": "Rare Items Dealer",
                "specialty": "rare",
                "inventory_size": 8,
            }
        )

    if city_type == "commercial":
        shop_types.append(
            {
                "type": "trading_post",
                "name": "Trading Post",
                "specialty": "trade_goods",
                "inventory_size": 20,
            }
        )

    # Generate inventory for each shop
    for shop in shop_types:
        shop["gold_reserve"] = wealth_level * 200  # Gold based on city wealth
        shop["inventory"] = []  # Will be populated when item system is integrated
        shop["price_modifier"] = (
            1.0 + (10 - wealth_level) * 0.05
        )  # Poorer cities = higher prices
        shops.append(shop)

    CITY_DATA[city_id]["shops"] = shops
    return shops


def get_city_description(city: Location) -> str:
    """
    Get detailed city description.

    Args:
        city: City location to describe

    Returns:
        str: Detailed city description

    Raises:
        ValidationError: If parameters are invalid
    """
    if not isinstance(city, Location):
        raise ValidationError("City must be a Location object")

    city_id = city.id
    if city_id not in CITY_DATA:
        # Generate basic city data if not present
        CITY_DATA[city_id] = {
            "city_type": "commercial",
            "population": 1000,
            "wealth_level": 5,
            "architectural_style": "medieval",
            "cultural_elements": [],
            "buildings": [],
            "shops": [],
            "reputation_modifiers": {},
        }

    city_data = CITY_DATA[city_id]

    description_parts = [f"🏰 {city.name}"]

    # Basic information
    description_parts.append(f"Type: {city_data['city_type'].title()} City")
    description_parts.append(f"Population: {city_data['population']:,}")
    description_parts.append(f"Wealth: {city_data['wealth_level']}/10")
    description_parts.append(
        f"Architecture: {city_data['architectural_style'].title()}"
    )

    # Buildings
    buildings = get_city_buildings(city)
    if buildings:
        description_parts.append(f"Buildings: {len(buildings)} available")

    # Shops
    shops = get_city_shops(city)
    if shops:
        description_parts.append(f"Shops: {len(shops)} establishments")

    # Cultural elements
    if city_data["cultural_elements"]:
        cultural_desc = ", ".join(city_data["cultural_elements"][:3])  # Show first 3
        description_parts.append(f"Culture: {cultural_desc}")

    return " | ".join(description_parts)


def add_building_to_city(city: Location, building: Dict[str, Any]) -> bool:
    """
    Add building to city.

    Args:
        city: City location to add building to
        building: Building data to add

    Returns:
        bool: True if building added successfully

    Raises:
        ValidationError: If parameters are invalid
    """
    if not isinstance(city, Location):
        raise ValidationError("City must be a Location object")

    if not isinstance(building, dict):
        raise ValidationError("Building must be a dictionary")

    city_id = city.id
    if city_id not in CITY_DATA:
        CITY_DATA[city_id] = {"buildings": [], "shops": [], "reputation_modifiers": {}}

    # Check if building already exists
    existing_buildings = [b["type"] for b in CITY_DATA[city_id]["buildings"]]
    if building["type"] in existing_buildings:
        return False

    CITY_DATA[city_id]["buildings"].append(building)
    return True


def remove_building_from_city(city: Location, building_type: str) -> bool:
    """
    Remove building from city.

    Args:
        city: City location to remove building from
        building_type: Type of building to remove

    Returns:
        bool: True if building removed successfully

    Raises:
        ValidationError: If parameters are invalid
    """
    if not isinstance(city, Location):
        raise ValidationError("City must be a Location object")

    city_id = city.id
    if city_id not in CITY_DATA:
        return False

    # Find and remove building
    for i, building in enumerate(CITY_DATA[city_id]["buildings"]):
        if building["type"] == building_type:
            del CITY_DATA[city_id]["buildings"][i]
            return True

    return False


def update_city_economy(city: Location, economic_change: int) -> Dict[str, Any]:
    """
    Update city economy based on player actions.

    Args:
        city: City location to update
        economic_change: Economic change amount (-100 to +100)

    Returns:
        Dict[str, Any]: Updated economic information

    Raises:
        ValidationError: If parameters are invalid
    """
    if not isinstance(city, Location):
        raise ValidationError("City must be a Location object")

    if economic_change < -100 or economic_change > 100:
        raise ValidationError("Economic change must be between -100 and 100")

    city_id = city.id
    if city_id not in CITY_DATA:
        CITY_DATA[city_id] = {"buildings": [], "shops": [], "reputation_modifiers": {}}

    # Update wealth level
    current_wealth = CITY_DATA[city_id].get("wealth_level", 5)
    new_wealth = max(1, min(10, current_wealth + (economic_change // 20)))
    CITY_DATA[city_id]["wealth_level"] = new_wealth

    # Update shop gold reserves
    for shop in CITY_DATA[city_id].get("shops", []):
        shop["gold_reserve"] = max(100, shop["gold_reserve"] + economic_change)
        # Update price modifiers based on new wealth
        shop["price_modifier"] = 1.0 + (10 - new_wealth) * 0.05

    return {
        "old_wealth_level": current_wealth,
        "new_wealth_level": new_wealth,
        "economic_change": economic_change,
        "affected_shops": len(CITY_DATA[city_id].get("shops", [])),
    }


def get_city_data(city: Location) -> Dict[str, Any]:
    """
    Get city data for a location.

    Args:
        city: City location to get data for

    Returns:
        Dict[str, Any]: City-specific data

    Raises:
        ValidationError: If parameters are invalid
    """
    if not isinstance(city, Location):
        raise ValidationError("City must be a Location object")

    return CITY_DATA.get(
        city.id,
        {
            "city_type": "commercial",
            "population": 1000,
            "wealth_level": 5,
            "architectural_style": "medieval",
            "cultural_elements": [],
            "buildings": [],
            "shops": [],
            "reputation_modifiers": {},
        },
    )
