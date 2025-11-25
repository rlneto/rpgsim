"""
City Management System for RPGSim
Handles city structure, economy, services, reputation, and player interactions
Comprehensive city simulation with buildings, services, and dynamic systems
"""

import random
from enum import Enum
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field


class BuildingType(Enum):
    """Types of buildings available in cities"""

    TAVERN = "tavern"
    WEAPON_SHOP = "weapon_shop"
    ARMOR_SHOP = "armor_shop"
    MAGIC_SHOP = "magic_shop"
    GENERAL_STORE = "general_store"
    TEMPLE = "temple"
    GUILD_HALL = "guild_hall"
    MARKET = "market"
    INN = "inn"
    BANK = "bank"
    LIBRARY = "library"
    BLACKSMITH = "blacksmith"
    ALCHEMIST = "alchemist"
    TAILOR = "tailor"
    JEWELER = "jeweler"
    BARRACKS = "barracks"


class EconomyType(Enum):
    """City economic specializations"""

    TRADE = "trade"
    AGRICULTURAL = "agricultural"
    INDUSTRIAL = "industrial"
    MAGICAL = "magical"
    MINING = "mining"
    FISHING = "fishing"


class ArchitecturalStyle(Enum):
    """City architectural styles"""

    MEDIEVAL = "medieval"
    GOTHIC = "gothic"
    RENAISSANCE = "renaissance"
    ORIENTAL = "oriental"
    BAROQUE = "baroque"


class ServiceType(Enum):
    """Types of city services"""

    GUARDS = "guards"
    HEALTHCARE = "healthcare"
    EDUCATION = "education"
    INFRASTRUCTURE = "infrastructure"


class ReputationLevel(Enum):
    """Player reputation levels with cities"""

    HATED = -5
    HOSTILE = -4
    SUSPICIOUS = -3
    WARY = -2
    NEUTRAL = -1
    FRIENDLY = 0
    RESPECTED = 1
    HONORED = 2
    REVERED = 3
    LEGENDARY = 4


@dataclass
# pylint: disable=too-many-instance-attributes
class Building:
    """Represents a building in a city"""

    id: str
    type: BuildingType
    name: str
    function: str
    position: Dict[str, Any]
    visitable: bool = True
    services: List[str] = field(default_factory=list)
    quality: float = 1.0
    operating_hours: Dict[str, int] = field(
        default_factory=lambda: {"open": 8, "close": 20}
    )


@dataclass
class CityServices:
    """City services infrastructure"""

    guards: Dict[str, Any] = field(default_factory=dict)
    healthcare: Dict[str, Any] = field(default_factory=dict)
    education: Dict[str, Any] = field(default_factory=dict)
    infrastructure: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CityStats:
    """Statistical information about a city"""

    population: int = 5000
    wealth_level: int = 5
    development_level: int = 3
    prosperity: int = 50
    growth_rate: float = 0.02
    literacy_rate: int = 75
    crime_rate: int = 5


@dataclass
class PlayerReputation:
    """Player reputation with a specific city"""

    city_id: str
    reputation_score: int = 0
    completed_quests: int = 0
    trades_made: int = 0
    time_in_city: int = 0
    major_events: List[Dict[str, Any]] = field(default_factory=list)


# pylint: disable=too-many-instance-attributes
class City:
    """Represents a city with comprehensive management systems"""

    # Building function definitions
    BUILDING_FUNCTIONS = {
        BuildingType.TAVERN: "Social gathering place with food and drinks",
        BuildingType.WEAPON_SHOP: "Sells weapons and combat equipment",
        BuildingType.ARMOR_SHOP: "Sells armor and protective gear",
        BuildingType.MAGIC_SHOP: "Sells magical items and spell components",
        BuildingType.GENERAL_STORE: "Sells basic supplies and everyday items",
        BuildingType.TEMPLE: "Religious services and healing",
        BuildingType.GUILD_HALL: "Professional organization and training",
        BuildingType.MARKET: "Trading hub for various goods",
        BuildingType.INN: "Lodging and rest for travelers",
        BuildingType.BANK: "Financial services and currency exchange",
        BuildingType.LIBRARY: "Knowledge repository and research",
        BuildingType.BLACKSMITH: "Metalworking and equipment repair",
        BuildingType.ALCHEMIST: "Potions and chemical compounds",
        BuildingType.TAILOR: "Clothing and textile goods",
        BuildingType.JEWELER: "Precious items and accessories",
        BuildingType.BARRACKS: "Military training and recruitment",
    }

    # Building service definitions
    BUILDING_SERVICES = {
        BuildingType.TAVERN: ["food", "drinks", "lodging", "rumors"],
        BuildingType.WEAPON_SHOP: [
            "weapon_sales",
            "weapon_repair",
            "weapon_upgrades",
        ],
        BuildingType.ARMOR_SHOP: [
            "armor_sales",
            "armor_repair",
            "custom_fitting",
        ],
        BuildingType.MAGIC_SHOP: [
            "magic_items",
            "spell_components",
            "enchanting",
        ],
        BuildingType.GENERAL_STORE: ["supplies", "tools", "food_items"],
        BuildingType.TEMPLE: [
            "healing",
            "blessings",
            "confession",
            "religious_guidance",
        ],
        BuildingType.GUILD_HALL: [
            "training",
            "quests",
            "professional_services",
        ],
        BuildingType.MARKET: ["trading", "bargaining", "specialty_goods"],
        BuildingType.INN: ["rooms", "food", "stables", "local_information"],
        BuildingType.BANK: [
            "deposits",
            "loans",
            "currency_exchange",
            "safe_storage",
        ],
        BuildingType.LIBRARY: [
            "research",
            "knowledge_sharing",
            "scrolls",
            "maps",
        ],
        BuildingType.BLACKSMITH: ["metal_work", "repairs", "custom_items"],
        BuildingType.ALCHEMIST: ["potions", "ingredients", "transmutations"],
        BuildingType.TAILOR: ["clothing", "repairs", "custom_outfits"],
        BuildingType.JEWELER: ["jewelry", "gems", "enchanted_items"],
        BuildingType.BARRACKS: [
            "training",
            "recruitment",
            "military_services",
        ],
    }

    # Cultural traits by economy type
    CULTURAL_TRAITS = {
        EconomyType.TRADE: [
            "merchant_caravans",
            "diverse_marketplace",
            "foreign_goods",
            "diplomatic_relations",
        ],
        EconomyType.AGRICULTURAL: [
            "farming_communities",
            "seasonal_festivals",
            "food_production",
            "rural_traditions",
        ],
        EconomyType.INDUSTRIAL: [
            "craftsmanship_guilds",
            "innovation_centers",
            "manufacturing_power",
            "technical_expertise",
        ],
        EconomyType.MAGICAL: [
            "arcane_academy",
            "mystical_research",
            "spell_casting",
            "magical_innovation",
        ],
        EconomyType.MINING: [
            "mining_guilds",
            "metal_working",
            "gem_cutting",
            "underground_communities",
        ],
        EconomyType.FISHING: [
            "maritime_traditions",
            "boat_building",
            "seafood_processing",
            "coastal_culture",
        ],
    }

    # Economy modifiers
    ECONOMY_MODIFIERS = {
        EconomyType.TRADE: {
            "shop_availability": 1.3,
            "price_multiplier": 0.9,
            "wealth_bonus": 2,
        },
        EconomyType.AGRICULTURAL: {
            "shop_availability": 0.8,
            "price_multiplier": 1.1,
            "wealth_bonus": -1,
        },
        EconomyType.INDUSTRIAL: {
            "shop_availability": 1.2,
            "price_multiplier": 1.0,
            "wealth_bonus": 1,
        },
        EconomyType.MAGICAL: {
            "shop_availability": 0.9,
            "price_multiplier": 1.3,
            "wealth_bonus": 3,
        },
        EconomyType.MINING: {
            "shop_availability": 1.1,
            "price_multiplier": 1.15,
            "wealth_bonus": 2,
        },
        EconomyType.FISHING: {
            "shop_availability": 1.0,
            "price_multiplier": 1.05,
            "wealth_bonus": 0,
        },
    }

    def __init__(self, city_id: str, name: str):
        """Initialize a new city"""
        self.id = city_id
        self.name = name
        self.buildings: List[Building] = []
        self.economy_type = random.choice(list(EconomyType))
        self.architectural_style = random.choice(list(ArchitecturalStyle))
        self.stats = CityStats()
        self.services = CityServices()
        self.cultural_traits = self.CULTURAL_TRAITS[self.economy_type].copy()
        self.discovered = False
        self.player_reputation: Dict[str, PlayerReputation] = {}

        # Generate city features
        self._generate_buildings()
        self._generate_services()
        self._adjust_stats_by_economy()

    def _generate_buildings(self) -> None:
        """Generate buildings for the city"""
        # Select 8-12 building types
        num_buildings = random.randint(8, 12)
        selected_types = random.sample(list(BuildingType), num_buildings)

        for i, building_type in enumerate(selected_types):
            building = Building(
                id=f"{self.id}_building_{i}",
                type=building_type,
                name=self._generate_building_name(building_type),
                function=self.BUILDING_FUNCTIONS[building_type],
                position=self._generate_building_position(),
                services=self.BUILDING_SERVICES[building_type].copy(),
                quality=random.uniform(0.5, 1.5),
            )
            self.buildings.append(building)

    def _generate_building_name(self, building_type: BuildingType) -> str:
        """Generate a name for a building based on its type"""
        prefixes = {
            BuildingType.TAVERN: [
                "The Prancing Pony",
                "Sleeping Dragon",
                "Golden Mug",
                "Tired Traveler",
            ],
            BuildingType.INN: [
                "Royal Suites",
                "Comfortable Beds",
                "Traveler's Rest",
                "Grand Hotel",
            ],
            BuildingType.WEAPON_SHOP: [
                "Sharp Blades",
                "Warrior's Arsenal",
                "Master Smith",
                "Arms of Legend",
            ],
            BuildingType.ARMOR_SHOP: [
                "Protective Plates",
                "Shield Bearer",
                "Armor Craft",
                "Defense Works",
            ],
            BuildingType.MAGIC_SHOP: [
                "Mystic Wares",
                "Arcane Arts",
                "Spell Components",
                "Magical Essentials",
            ],
            BuildingType.GENERAL_STORE: [
                "General Goods",
                "Market Essentials",
                "Supply Depot",
                "Everyday Needs",
            ],
        }

        if building_type in prefixes:
            return random.choice(prefixes[building_type])
        return building_type.value.replace("_", " ").title()

    def _generate_building_position(self) -> Dict[str, Any]:
        """Generate position data for a building"""
        districts = [
            "market_district",
            "residential",
            "commercial",
            "industrial",
            "temple_district",
        ]
        return {
            "x": random.randint(1, 10),
            "y": random.randint(1, 10),
            "district": random.choice(districts),
        }

    def _generate_services(self) -> None:
        """Generate city services"""
        # Guard services
        self.services.guards = {
            "strength": random.randint(5, 20),
            "response_time": random.randint(1, 5),
            "patrol_coverage": random.randint(50, 100),
            "crime_rate": max(1, 10 - self.stats.wealth_level),
        }

        # Healthcare services
        self.services.healthcare = {
            "hospitals": random.randint(1, 5),
            "healers": random.randint(2, 10),
            "potion_shops": random.randint(3, 8),
            "service_quality": random.randint(60, 100),
        }

        # Educational services
        self.services.education = {
            "schools": random.randint(2, 6),
            "libraries": random.randint(1, 4),
            "academies": random.randint(0, 2),
            "literacy_rate": random.randint(70, 100),
        }

        # Infrastructure services
        self.services.infrastructure = {
            "roads_quality": random.randint(3, 10),
            "water_system": random.randint(5, 10),
            "lighting": random.randint(3, 10),
            "sanitation": random.randint(4, 10),
        }

    def _adjust_stats_by_economy(self) -> None:
        """Adjust city statistics based on economy type"""
        modifiers = self.ECONOMY_MODIFIERS[self.economy_type]
        self.stats.wealth_level = max(
            1, min(10, self.stats.wealth_level + modifiers["wealth_bonus"])
        )
        self.stats.prosperity = max(
            0,
            min(100, self.stats.prosperity + (modifiers["wealth_bonus"] * 10)),
        )

        # Adjust population based on economy
        if self.economy_type == EconomyType.MAGICAL:
            self.stats.population = random.randint(3000, 15000)
        elif self.economy_type == EconomyType.TRADE:
            self.stats.population = random.randint(8000, 50000)
        elif self.economy_type == EconomyType.AGRICULTURAL:
            self.stats.population = random.randint(2000, 10000)
        else:
            self.stats.population = random.randint(4000, 30000)

    def get_building_by_type(
        self, building_type: BuildingType
    ) -> Optional[Building]:
        """Get a building of a specific type"""
        for building in self.buildings:
            if building.type == building_type:
                return building
        return None

    def get_buildings_by_district(self, district: str) -> List[Building]:
        """Get all buildings in a specific district"""
        return [
            b for b in self.buildings if b.position["district"] == district
        ]

    def get_shop_availability(self) -> int:
        """Calculate shop availability percentage"""
        base_availability = 100
        modifier = self.ECONOMY_MODIFIERS[self.economy_type][
            "shop_availability"
        ]
        return int(base_availability * modifier)

    def get_price_multiplier(self) -> float:
        """Get price multiplier for the city"""
        return self.ECONOMY_MODIFIERS[self.economy_type]["price_multiplier"]

    def get_description(self) -> str:
        """Generate a description of the city"""
        population = self.stats.population
        descriptions = {
            # pylint: disable=line-too-long
            EconomyType.TRADE: f"A bustling merchant hub with diverse marketplaces and {population} inhabitants",
            # pylint: disable=line-too-long
            EconomyType.AGRICULTURAL: f"A peaceful farming community with fertile fields and {population} residents",
            # pylint: disable=line-too-long
            EconomyType.INDUSTRIAL: f"A crafty center of innovation and manufacturing with {population} workers",
            # pylint: disable=line-too-long
            EconomyType.MAGICAL: f"An arcane center filled with mystical energy and {population} practitioners",
            # pylint: disable=line-too-long
            EconomyType.MINING: f"A rugged mountain settlement around mineral deposits with {population} miners",
            # pylint: disable=line-too-long
            EconomyType.FISHING: f"A coastal town with thriving fishing industry and {population} fishermen",
        }
        base_desc = descriptions.get(
            self.economy_type,
            f"A growing settlement with {population} inhabitants",
        )

        return f"{self.name}: {base_desc}. Known for {', '.join(self.cultural_traits[:2])}."

    def get_services_summary(self) -> List[str]:
        """Generate a summary of available services"""
        summary = []
        summary.append(
            f"Market: {self.get_building_by_type(BuildingType.MARKET) is not None}"
        )
        summary.append(
            f"Security: {self.services.guards['strength']} guards maintaining order"
        )
        inns = [b for b in self.buildings if b.type == BuildingType.INN]
        summary.append(f"Lodging: {len(inns)} inns available")
        summary.append(
            f"Commerce: {len([b for b in self.buildings if 'shop' in b.type.value])} shops"
        )
        return summary

    def update_reputation(
        self, player_id: str, change: int, reason: str = ""
    ) -> None:
        """Update player reputation with this city"""
        if player_id not in self.player_reputation:
            self.player_reputation[player_id] = PlayerReputation(
                city_id=self.id
            )

        rep = self.player_reputation[player_id]
        rep.reputation_score += change

        if reason:
            rep.major_events.append(
                {"event": reason, "reputation_impact": change}
            )

    # pylint: disable=too-many-return-statements
    def get_player_reputation_level(self, player_id: str) -> ReputationLevel:
        """Get reputation level for a player"""
        if player_id not in self.player_reputation:
            return ReputationLevel.NEUTRAL

        score = self.player_reputation[player_id].reputation_score

        # Define reputation thresholds and levels
        thresholds = [
            (80, ReputationLevel.LEGENDARY),
            (60, ReputationLevel.REVERED),
            (40, ReputationLevel.HONORED),
            (20, ReputationLevel.RESPECTED),
            (5, ReputationLevel.FRIENDLY),
            (-5, ReputationLevel.NEUTRAL),
            (-15, ReputationLevel.WARY),
            (-30, ReputationLevel.SUSPICIOUS),
            (-50, ReputationLevel.HOSTILE),
        ]

        for threshold, level in thresholds:
            if score >= threshold:
                return level
        return ReputationLevel.HATED

    def get_pricing_modifier(self, player_id: str) -> float:
        """Get pricing modifier based on player reputation"""
        level = self.get_player_reputation_level(player_id)

        modifiers = {
            ReputationLevel.LEGENDARY: 0.8,
            ReputationLevel.REVERED: 0.85,
            ReputationLevel.HONORED: 0.9,
            ReputationLevel.RESPECTED: 0.95,
            ReputationLevel.FRIENDLY: 0.98,
            ReputationLevel.NEUTRAL: 1.0,
            ReputationLevel.WARY: 1.05,
            ReputationLevel.SUSPICIOUS: 1.1,
            ReputationLevel.HOSTILE: 1.2,
            ReputationLevel.HATED: 1.3,
        }

        return modifiers[level]

    def get_available_services(self, player_id: str) -> List[str]:
        """Get services available to a player based on reputation"""
        level = self.get_player_reputation_level(player_id)

        basic_services = ["general_store", "tavern"]
        advanced_services = [
            "specialty_shop",
            "guild_membership",
            "elite_training",
        ]
        premium_services = ["noble_favor", "city_council", "royal_commissions"]

        available = basic_services.copy()

        if level.value >= ReputationLevel.FRIENDLY.value:
            available.extend(advanced_services)

        if level.value >= ReputationLevel.HONORED.value:
            available.extend(premium_services)

        return available

    def simulate_growth(self, days: int = 30) -> None:
        """Simulate city growth over time"""
        population_growth = int(
            self.stats.population * self.stats.growth_rate * (days / 30)
        )
        self.stats.population += population_growth

        # Adjust prosperity based on growth
        if population_growth > 0:
            self.stats.prosperity = min(
                100, self.stats.prosperity + random.randint(1, 5)
            )

        # Update development level occasionally
        if random.random() < 0.1:
            self.stats.development_level = min(
                5, self.stats.development_level + 1
            )


class CityManager:
    """Manages multiple cities and city-related operations"""

    def __init__(self):
        """Initialize the city manager"""
        self.cities: Dict[str, City] = {}
        self.player_locations: Dict[str, str] = {}
        self.discovered_cities: Dict[str, List[str]] = {}

    def create_city(self, city_id: str, name: str) -> City:
        """Create a new city"""
        if city_id in self.cities:
            raise ValueError(f"City {city_id} already exists")

        city = City(city_id, name)
        self.cities[city_id] = city
        return city

    def get_city(self, city_id: str) -> Optional[City]:
        """Get a city by ID"""
        return self.cities.get(city_id)

    def get_all_cities(self) -> List[City]:
        """Get all cities"""
        return list(self.cities.values())

    def player_enter_city(self, player_id: str, city_id: str) -> bool:
        """Have a player enter a city"""
        if city_id not in self.cities:
            return False

        self.player_locations[player_id] = city_id

        # Track discovery
        if player_id not in self.discovered_cities:
            self.discovered_cities[player_id] = []

        if city_id not in self.discovered_cities[player_id]:
            self.discovered_cities[player_id].append(city_id)
            self.cities[city_id].discovered = True

        return True

    def get_player_current_city(self, player_id: str) -> Optional[City]:
        """Get the city a player is currently in"""
        city_id = self.player_locations.get(player_id)
        return self.cities.get(city_id) if city_id else None

    def get_discovered_cities(self, player_id: str) -> List[City]:
        """Get cities discovered by a player"""
        city_ids = self.discovered_cities.get(player_id, [])
        return [self.cities[cid] for cid in city_ids if cid in self.cities]

    def get_cities_by_economy(self, economy_type: EconomyType) -> List[City]:
        """Get cities by economy type"""
        return [
            city
            for city in self.cities.values()
            if city.economy_type == economy_type
        ]

    def simulate_all_cities_growth(self, days: int = 30) -> None:
        """Simulate growth for all cities"""
        for city in self.cities.values():
            city.simulate_growth(days)

    def export_city_data(self) -> Dict[str, Any]:
        """Export all city data for saving"""
        return {
            "cities": {
                cid: {
                    "id": city.id,
                    "name": city.name,
                    "economy_type": city.economy_type.value,
                    "architectural_style": city.architectural_style.value,
                    "stats": {
                        "population": city.stats.population,
                        "wealth_level": city.stats.wealth_level,
                        "development_level": city.stats.development_level,
                        "prosperity": city.stats.prosperity,
                        "growth_rate": city.stats.growth_rate,
                        "literacy_rate": city.stats.literacy_rate,
                        "crime_rate": city.stats.crime_rate,
                    },
                    "buildings": [
                        {
                            "id": b.id,
                            "type": b.type.value,
                            "name": b.name,
                            "function": b.function,
                            "position": b.position,
                            "quality": b.quality,
                        }
                        for b in city.buildings
                    ],
                    "services": {
                        "guards": city.services.guards,
                        "healthcare": city.services.healthcare,
                        "education": city.services.education,
                        "infrastructure": city.services.infrastructure,
                    },
                }
                for cid, city in self.cities.items()
            },
            "discovered_cities": self.discovered_cities,
        }


# Utility functions
def get_all_building_types() -> List[str]:
    """Get all available building types as strings"""
    return [bt.value for bt in BuildingType]


def get_all_economy_types() -> List[str]:
    """Get all economy types as strings"""
    return [et.value for et in EconomyType]


def get_all_architectural_styles() -> List[str]:
    """Get all architectural styles as strings"""
    return [as_.value for as_ in ArchitecturalStyle]


def validate_city_balance(cities: List[City]) -> bool:
    """Validate that cities have balanced characteristics"""
    if len(cities) < 2:
        return True

    # Check economy distribution
    economies = [city.economy_type for city in cities]
    unique_economies = len(set(economies))

    # Should have good variety
    return unique_economies >= min(3, len(EconomyType))


def verify_minimum_building_count(
    cities: List[City], min_buildings: int = 8
) -> bool:
    """Verify all cities have minimum building count"""
    return all(len(city.buildings) >= min_buildings for city in cities)
