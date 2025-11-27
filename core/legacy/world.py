"""
World System for RPGSim
Implements world exploration, cities, geography, and travel system
"""

# pylint: disable=unused-variable

import random
from typing import Dict, List, Optional
from enum import Enum


class GeographyType(Enum):
    """Types of geography for world locations"""

    COASTAL = "coastal"
    MOUNTAINOUS = "mountainous"
    PLAINS = "plains"
    FOREST = "forest"
    DESERT = "desert"
    SWAMP = "swamp"
    ISLAND = "island"
    VOLCANIC = "volcanic"
    ARCTIC = "arctic"
    TROPICAL = "tropical"
    CAVE = "cave"
    FLOATING = "floating"


class BuildingType(Enum):
    """Types of buildings available in cities"""

    INN = "Inn"
    SHOP = "Shop"
    TEMPLE = "Temple"
    BLACKSMITH = "Blacksmith"
    TAVERN = "Tavern"
    GUILD = "Guild"
    LIBRARY = "Library"
    MARKET = "Market"
    ARENA = "Arena"
    BANK = "Bank"
    GUARD_TOWER = "Guard Tower"
    CASTLE = "Castle"
    FARM = "Farm"
    STABLE = "Stable"
    DOCKS = "Docks"
    ALCHEMY_LAB = "Alchemy Lab"


class TravelMethod(Enum):
    """Available travel methods between cities"""

    WALK = "walk"
    HORSE = "horse"
    CARRIAGE = "carriage"
    SHIP = "ship"
    TELEPORT = "teleport"


class CultureType(Enum):
    """Cultural types for cities"""

    MILITARISTIC = "militaristic"
    SCHOLARLY = "scholarly"
    MERCANTILE = "mercantile"
    RELIGIOUS = "religious"
    AGRICULTURAL = "agricultural"
    ARTISTIC = "artistic"
    INDUSTRIAL = "industrial"
    MYSTERIOUS = "mysterious"
    NOMADIC = "nomadic"
    HIERARCHICAL = "hierarchical"


class ShopType(Enum):
    """Types of shops in cities"""

    WEAPONS = "weapons"
    ARMOR = "armor"
    MAGIC = "magic"
    GENERAL = "general"


class Building:  # pylint: disable=too-few-public-methods
    """Represents a building in a city"""

    def __init__(
        self, building_type: BuildingType, name: str, function_desc: str
    ):
        self.building_type = building_type
        self.name = name
        self.function_desc = function_desc
        self.description = self._generate_description()

    def _generate_description(self) -> str:
        """Generate a description based on building type"""
        descriptions = {
            BuildingType.INN: "A cozy place for travelers to rest and recover",
            BuildingType.SHOP: "A general store selling various goods and supplies",
            BuildingType.TEMPLE: "A sacred place for worship and healing",
            BuildingType.BLACKSMITH: "A forge for crafting and repairing weapons",
            BuildingType.TAVERN: "A lively establishment for food, drink, and news",
            BuildingType.GUILD: "A headquarters for professional training",
            BuildingType.LIBRARY: "A repository of knowledge and ancient texts",
            BuildingType.MARKET: "A bustling center for trade and commerce",
            BuildingType.ARENA: "A venue for combat challenges and tournaments",
            BuildingType.BANK: "A secure institution for currency and valuables",
            BuildingType.GUARD_TOWER: "A defensive structure maintaining city safety",
            BuildingType.CASTLE: "The residence of nobility and seat of power",
            BuildingType.FARM: "Agricultural land producing food and resources",
            BuildingType.STABLE: "A facility for housing and caring for animals",
            BuildingType.DOCKS: "A harbor for ships and sea travel",
            BuildingType.ALCHEMY_LAB: "A laboratory for creating potions and elixirs",
        }
        return descriptions.get(
            self.building_type, "A unique building with special purpose"
        )

    def get_info(self) -> Dict:
        """Get building information"""
        return {
            "type": self.building_type.value,
            "name": self.name,
            "function": self.function_desc,
            "description": self.description,
        }


class Shop:  # pylint: disable=too-few-public-methods
    """Represents a shop in a city"""

    def __init__(self, name: str, shop_type: ShopType, city_name: str):
        self.name = name
        self.shop_type = shop_type
        self.city_name = city_name
        self.inventory = self._generate_inventory()
        self.prices = self._generate_prices()

    def _generate_inventory(self) -> List[str]:
        """Generate shop inventory based on type"""
        inventory_options = {
            ShopType.WEAPONS: [
                "swords",
                "axes",
                "spears",
                "bows",
                "daggers",
                "hammers",
            ],
            ShopType.ARMOR: [
                "helmet",
                "chestplate",
                "gauntlets",
                "boots",
                "shield",
            ],
            ShopType.MAGIC: [
                "potions",
                "scrolls",
                "mana crystals",
                "spell books",
                "talismans",
            ],
            ShopType.GENERAL: [
                "food",
                "clothing",
                "tools",
                "rope",
                "torches",
                "backpacks",
            ],
        }
        base_items = inventory_options.get(
            self.shop_type, inventory_options[ShopType.GENERAL]
        )
        num_items = min(random.randint(3, 6), len(base_items))
        return random.sample(base_items, num_items)

    def _generate_prices(self) -> Dict[str, int]:
        """Generate prices for items"""
        prices = {}
        for item in self.inventory:
            base_price = random.randint(5, 500)
            # Adjust price based on shop type
            if self.shop_type == ShopType.WEAPONS:
                base_price *= 1.5
            elif self.shop_type == ShopType.ARMOR:
                base_price *= 1.3
            elif self.shop_type == ShopType.MAGIC:
                base_price *= 2.0
            prices[item] = int(base_price)
        return prices

    def get_info(self) -> Dict:
        """Get shop information"""
        return {
            "name": self.name,
            "type": self.shop_type.value,
            "inventory": self.inventory.copy(),
            "prices": self.prices.copy(),
        }


class City:  # pylint: disable=too-many-instance-attributes
    """Represents a city in the game world"""

    def __init__(
        self,
        name: str,
        city_id: str,
        geography: GeographyType,
        culture: CultureType,
    ):
        self.name = name
        self.city_id = city_id
        self.geography = geography
        self.culture = culture
        self.buildings = self._generate_buildings()
        self.shops = self._generate_shops()
        self.connections = []
        self.description = self._generate_description()
        self.layout = self._generate_layout()

    def _generate_buildings(self) -> List[Building]:
        """Generate buildings for the city"""
        building_types = list(BuildingType)
        num_buildings = min(random.randint(8, 12), len(building_types))
        selected_types = random.sample(building_types, num_buildings)
        buildings = []
        for building_type in selected_types:
            name = f"{self.name} {building_type.value}"
            function_desc = self._get_building_function(building_type)
            building = Building(building_type, name, function_desc)
            buildings.append(building)
        return buildings

    def _get_building_function(self, building_type: BuildingType) -> str:
        """Get function description for building type"""
        functions = {
            BuildingType.INN: "Rest and recovery",
            BuildingType.SHOP: "Buy general goods",
            BuildingType.TEMPLE: "Healing and blessings",
            BuildingType.BLACKSMITH: "Weapon and armor repair",
            BuildingType.TAVERN: "Information and gossip",
            BuildingType.GUILD: "Quests and training",
            BuildingType.LIBRARY: "Knowledge and lore",
            BuildingType.MARKET: "Trade and commerce",
            BuildingType.ARENA: "Combat challenges",
            BuildingType.BANK: "Currency storage",
            BuildingType.GUARD_TOWER: "Safety and quests",
            BuildingType.CASTLE: "Noble interaction",
            BuildingType.FARM: "Food production",
            BuildingType.STABLE: "Animal services",
            BuildingType.DOCKS: "Sea travel",
            BuildingType.ALCHEMY_LAB: "Potion creation",
        }
        return functions.get(building_type, "Specialized services")

    def _generate_shops(self) -> List[Shop]:
        """Generate shops for the city"""
        shop_types = list(ShopType)
        num_shops = min(random.randint(2, 4), len(shop_types))
        selected_types = random.sample(shop_types, num_shops)
        shops = []
        for i, shop_type in enumerate(selected_types):
            shop_name = f"{self.name} Shop {i+1}"
            shop = Shop(shop_name, shop_type, self.name)
            shops.append(shop)
        return shops

    def _generate_description(self) -> str:
        """Generate city description based on culture"""
        culture_desc = {
            CultureType.MILITARISTIC: "strong army and strict discipline",
            CultureType.SCHOLARLY: "great library and learned scholars",
            CultureType.MERCANTILE: "bustling markets and wealthy merchants",
            CultureType.RELIGIOUS: "grand temples and devout followers",
            CultureType.AGRICULTURAL: "fertile fields and hardworking farmers",
            CultureType.ARTISTIC: "beautiful art and talented performers",
            CultureType.INDUSTRIAL: "busy factories and skilled craftsmen",
            CultureType.MYSTERIOUS: "ancient secrets and hidden knowledge",
            CultureType.NOMADIC: "traveling people and diverse traditions",
            CultureType.HIERARCHICAL: "strict social order and noble leadership",
        }
        culture_desc_text = culture_desc.get(
            self.culture, "unique characteristics"
        )
        base_desc = f"{self.name} is a {self.culture.value} city known for its {culture_desc_text}"
        geography_desc = f" Located in {self.geography.value} terrain"
        return base_desc + geography_desc + "."

    def _generate_layout(self) -> Dict:
        """Generate city layout information"""
        num_districts = random.randint(3, 8)
        num_landmarks = random.randint(2, 5)
        districts = [f"District {i+1}" for i in range(num_districts)]
        landmarks = [f"Landmark {i+1}" for i in range(num_landmarks)]
        return {
            "description": f"Unique layout for {self.name} with {num_districts} districts",
            "districts": districts,
            "landmarks": landmarks,
        }

    def add_connection(self, city_name: str):
        """Add a connection to another city"""
        if city_name not in self.connections:
            self.connections.append(city_name)

    def get_building_types(self) -> List[str]:
        """Get list of building types in city"""
        return [building.building_type.value for building in self.buildings]

    def get_building_info(self) -> List[Dict]:
        """Get information about all buildings"""
        return [building.get_info() for building in self.buildings]

    def get_shop_info(self) -> List[Dict]:
        """Get information about all shops"""
        return [shop.get_info() for shop in self.shops]


class TravelTime:
    """Manages travel time calculations between cities"""

    # Base travel times in hours for different methods
    BASE_TRAVEL_TIMES = {
        TravelMethod.WALK: 1.0,
        TravelMethod.HORSE: 0.7,
        TravelMethod.CARRIAGE: 0.5,
        TravelMethod.SHIP: 0.3,
        TravelMethod.TELEPORT: 0.1,
    }

    def __init__(self):
        self.travel_times = {}

    def calculate_travel_time(
        self,
        _from_city: str,  # pylint: disable=unused-argument
        _to_city: str,  # pylint: disable=unused-argument
        method: TravelMethod = TravelMethod.WALK,
        distance_factor: float = 1.0,
    ) -> int:
        """Calculate travel time between cities"""
        # Generate base time (4-72 hours)
        base_time = random.randint(4, 72)
        # Apply method modifier
        modifier = self.BASE_TRAVEL_TIMES.get(method, 1.0)
        # Apply distance factor and geography modifier
        final_time = int(base_time * modifier * distance_factor)
        # Ensure reasonable bounds
        return max(1, min(final_time, 168))  # Max 1 week

    def set_travel_time(self, from_city: str, to_city: str, hours: int):
        """Set specific travel time between cities"""
        self.travel_times[(from_city, to_city)] = hours
        self.travel_times[(to_city, from_city)] = hours

    def get_travel_time(self, from_city: str, to_city: str) -> Optional[int]:
        """Get travel time between cities"""
        return self.travel_times.get((from_city, to_city))


class WorldMap:
    """Manages the world map and navigation system"""

    def __init__(self):
        self.type = "text_based"
        self.navigation = True
        self.travel_time = True
        self.travel_options = [method.value for method in TravelMethod]
        self.cities = {}
        self.travel_calculator = TravelTime()

    def add_city(self, city: City):
        """Add a city to the world map"""
        self.cities[city.name] = city

    def get_city(self, name: str) -> Optional[City]:
        """Get a city by name"""
        return self.cities.get(name)

    def connect_cities(
        self, city1_name: str, city2_name: str, distance_factor: float = 1.0
    ):
        """Create a bidirectional connection between cities"""
        city1 = self.get_city(city1_name)
        city2 = self.get_city(city2_name)
        if city1 and city2:
            city1.add_connection(city2_name)
            city2.add_connection(city1_name)
            # Calculate and set travel times for all methods
            for method in TravelMethod:
                travel_time = self.travel_calculator.calculate_travel_time(
                    city1_name, city2_name, method, distance_factor
                )
                self.travel_calculator.set_travel_time(
                    city1_name, city2_name, travel_time
                )

    def get_connected_cities(self, city_name: str) -> List[str]:
        """Get list of cities connected to the specified city"""
        city = self.get_city(city_name)
        return city.connections if city else []

    def can_travel(self, from_city: str, to_city: str) -> bool:
        """Check if travel is possible between cities"""
        return to_city in self.get_connected_cities(from_city)

    def get_travel_info(self) -> Dict:
        """Get world map information"""
        return {
            "type": self.type,
            "navigation": self.navigation,
            "travel_time": self.travel_time,
            "travel_options": self.travel_options.copy(),
        }


class World:
    """Main world system managing cities, geography, and travel"""

    def __init__(self):
        self.world_map = WorldMap()
        self.current_location = None
        self.visited_locations = []
        self.game_state = "menu"
        self.player_character = None

    def generate_world(self) -> bool:
        """Generate the complete game world"""
        try:
            # Generate 20 distinct cities
            city_names = [
                "Stormhaven",
                "Ironforge",
                "Silvermoon",
                "Goldshire",
                "Ravenholdt",
                "Whisperwind",
                "Shadowglen",
                "Dawnshire",
                "Twilight Vale",
                "Dragon's Peak",
                "Eldoria",
                "Mysthaven",
                "Winterfell",
                "Summerwind",
                "Autumnreach",
                "Springvale",
                "Crystal Depths",
                "Obsidian Spire",
                "Verdant Grove",
                "Azure Bay",
            ]
            geography_types = list(GeographyType)
            culture_types = list(CultureType)
            # Create cities with unique geography and culture
            for i, name in enumerate(
                city_names
            ):  # pylint: disable=unused-variable
                geography = random.choice(geography_types)
                culture = random.choice(culture_types)
                city_id = f"city_{i}"
                city = City(name, city_id, geography, culture)
                self.world_map.add_city(city)
            # Connect cities with travel routes
            self._connect_all_cities()
            return True
        except (ValueError, TypeError, KeyError):
            return False

    def _connect_all_cities(self):
        """Create travel connections between cities"""
        cities = list(self.world_map.cities.values())
        # Create a network of connections
        for i, city in enumerate(cities):
            # Connect to 2-5 other cities
            num_connections = random.randint(2, min(5, len(cities) - 1))
            # Choose random cities to connect to
            available_cities = [c for c in cities if c.name != city.name]
            connected_cities = random.sample(available_cities, num_connections)
            for connected_city in connected_cities:
                # Calculate distance factor based on geography
                distance_factor = self._calculate_distance_factor(
                    city, connected_city
                )
                self.world_map.connect_cities(
                    city.name, connected_city.name, distance_factor
                )

    def _calculate_distance_factor(self, city1: City, city2: City) -> float:
        """Calculate distance factor between cities based on geography"""
        # Simple distance factor based on geography compatibility
        geography_pairs = {
            (GeographyType.COASTAL, GeographyType.ISLAND): 0.5,
            (GeographyType.MOUNTAINOUS, GeographyType.VOLCANIC): 0.7,
            (GeographyType.PLAINS, GeographyType.PLAINS): 0.8,
            (GeographyType.FOREST, GeographyType.TROPICAL): 0.9,
        }
        # Check for special pairs
        valid_pairs = [
            (city1.geography, city2.geography),
            (city2.geography, city1.geography),
        ]
        for pair, factor in geography_pairs.items():
            if pair in valid_pairs:
                return factor
        # Default random factor
        return random.uniform(0.8, 1.5)

    def start_game(self, character_name: str, character_class: str) -> bool:
        """Start the game with a character"""
        try:
            if not self.world_map.cities:
                self.generate_world()
            # Set current location to first city
            first_city = list(self.world_map.cities.keys())[0]
            self.current_location = first_city
            self.visited_locations = [first_city]
            self.game_state = "playing"
            # Store player info (simplified)
            self.player_character = {
                "name": character_name,
                "class": character_class,
                "level": 1,
                "location": first_city,
                "visited_buildings": [],
            }
            return True
        except (ValueError, TypeError, KeyError):
            return False

    def travel_to_city(self, city_name: str, method: str = "walk") -> bool:
        """Travel to a specified city"""
        if not self.world_map.can_travel(self.current_location, city_name):
            return False
        try:
            TravelMethod(method)  # Validate travel method
        except ValueError:
            pass  # Default to walk
        # Update location
        self.current_location = city_name
        if city_name not in self.visited_locations:
            self.visited_locations.append(city_name)
        # Update player location
        if self.player_character:
            self.player_character["location"] = city_name
        return True

    def explore_current_city(self) -> Dict:
        """Explore the current city and return building information"""
        city = self.world_map.get_city(self.current_location)
        if not city:
            return {}
        # Mark buildings as visited
        if self.player_character:
            building_types = city.get_building_types()
            self.player_character["visited_buildings"] = building_types
        return {
            "city_name": city.name,
            "city_description": city.description,
            "geography": city.geography.value,
            "culture": city.culture.value,
            "buildings": city.get_building_info(),
            "shops": city.get_shop_info(),
            "layout": city.layout,
        }

    def get_travel_options(self) -> List[Dict]:
        """Get available travel options from current location"""
        if not self.current_location:
            return []
        connected_cities = self.world_map.get_connected_cities(
            self.current_location
        )
        options = []
        for city_name in connected_cities:
            city = self.world_map.get_city(city_name)
            if city:
                travel_time = self.world_map.travel_calculator.get_travel_time(
                    self.current_location, city_name
                )
                options.append(
                    {
                        "city_name": city_name,
                        "geography": city.geography.value,
                        "culture": city.culture.value,
                        "travel_time": travel_time or 24,  # Default 24 hours
                    }
                )
        return options

    def get_world_info(self) -> Dict:
        """Get comprehensive world information"""
        return {
            "current_location": self.current_location,
            "visited_cities": len(self.visited_locations),
            "total_cities": len(self.world_map.cities),
            "game_state": self.game_state,
            "world_map": self.world_map.get_travel_info(),
            "player": self.player_character,
        }

    def get_city_stats(self) -> Dict:
        """Get statistics about cities in the world"""
        cities = list(self.world_map.cities.values())
        geography_count = {}
        culture_count = {}
        building_count = {}
        shop_count = {}
        for city in cities:
            # Count geography types
            geo = city.geography.value
            geography_count[geo] = geography_count.get(geo, 0) + 1
            # Count culture types
            cult = city.culture.value
            culture_count[cult] = culture_count.get(cult, 0) + 1
            # Count building types
            for building in city.buildings:
                btype = building.building_type.value
                building_count[btype] = building_count.get(btype, 0) + 1
            # Count shop types
            for shop in city.shops:
                stype = shop.shop_type.value
                shop_count[stype] = shop_count.get(stype, 0) + 1
        return {
            "total_cities": len(cities),
            "geography_distribution": geography_count,
            "culture_distribution": culture_count,
            "building_distribution": building_count,
            "shop_distribution": shop_count,
        }


# Utility functions for external access
def create_world() -> World:
    """Create a new world instance"""
    world = World()
    world.generate_world()
    return world


def get_city_balance_stats() -> Dict[str, int]:
    """Get balance statistics for all cities"""
    world = create_world()
    return world.get_city_stats()


def validate_world_structure() -> bool:
    """Validate that world structure meets requirements"""
    world = create_world()
    # Check city count
    if len(world.world_map.cities) != 20:
        return False
    # Check each city has required elements
    for city in world.world_map.cities.values():
        if len(city.buildings) < 8:
            return False
        if len(city.shops) < 2:
            return False
        if not city.description:
            return False
    # Check connectivity
    for city in world.world_map.cities.values():
        if len(city.connections) < 2:
            return False
    return True


def verify_unique_geography() -> bool:
    """Verify cities have diverse geography"""
    world = create_world()
    geographies = [city.geography for city in world.world_map.cities.values()]
    # Should have at least 15 unique geographies among 20 cities
    unique_geographies = len(set(geographies))
    return unique_geographies >= 15


def verify_unique_cultures() -> bool:
    """Verify cities have diverse cultures"""
    world = create_world()
    cultures = [city.culture for city in world.world_map.cities.values()]
    # Should have good cultural diversity
    unique_cultures = len(set(cultures))
    return unique_cultures >= 8
