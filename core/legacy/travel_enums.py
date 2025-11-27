"""
Travel enums for RPGSim
Travel-related enumerations and constants
"""

from typing import List


class TerrainType:
    """Types of terrain that affect travel"""

    PLAINS = "plains"
    FOREST = "forest"
    MOUNTAINS = "mountains"
    HILLS = "hills"
    SWAMP = "swamp"
    DESERT = "desert"
    COASTAL = "coastal"
    TUNDRA = "tundra"
    JUNGLE = "jungle"
    VOLCANIC = "volcanic"

    @classmethod
    def get_all_terrain_types(cls) -> List[str]:
        """Get all available terrain types."""
        return [
            cls.PLAINS,
            cls.FOREST,
            cls.MOUNTAINS,
            cls.HILLS,
            cls.SWAMP,
            cls.DESERT,
            cls.COASTAL,
            cls.TUNDRA,
            cls.JUNGLE,
            cls.VOLCANIC,
        ]

    @classmethod
    def is_valid_terrain(cls, terrain: str) -> bool:
        """Check if terrain type is valid."""
        return terrain in cls.get_all_terrain_types()


class TravelMethod:
    """Methods of travel available to players"""

    WALK = "walk"
    HORSE = "horse"
    CART = "cart"
    BOAT = "boat"
    SHIP = "ship"
    TELEPORT = "teleport"

    @classmethod
    def get_all_methods(cls) -> List[str]:
        """Get all available travel methods."""
        return [cls.WALK, cls.HORSE, cls.CART, cls.BOAT, cls.SHIP, cls.TELEPORT]

    @classmethod
    def is_valid_method(cls, method: str) -> bool:
        """Check if travel method is valid."""
        return method in cls.get_all_methods()


class TravelEvent:
    """Types of events that can occur during travel"""

    MERCHANT_ENCOUNTER = "merchant_encounter"
    BANDIT_ATTACK = "bandit_attack"
    WEATHER_CHANGE = "weather_change"
    WILD_ANIMAL = "wild_animal"
    LOST_TRAVELER = "lost_traveler"
    ANCIENT_RUINS = "ancient_ruins"
    NATURAL_RESOURCE = "natural_resource"
    ROAD_BLOCKAGE = "road_blockage"
    FRIENDLY_PATROL = "friendly_patrol"
    MYSTERIOUS_STRANGER = "mysterious_stranger"
    TREASURE_MAP = "treasure_map"
    EQUIPMENT_FAILURE = "equipment_failure"

    @classmethod
    def get_all_events(cls) -> List[str]:
        """Get all possible travel events."""
        return [
            cls.MERCHANT_ENCOUNTER,
            cls.BANDIT_ATTACK,
            cls.WEATHER_CHANGE,
            cls.WILD_ANIMAL,
            cls.LOST_TRAVELER,
            cls.ANCIENT_RUINS,
            cls.NATURAL_RESOURCE,
            cls.ROAD_BLOCKAGE,
        ]

    @classmethod
    def is_valid_event(cls, event: str) -> bool:
        """Check if travel event is valid."""
        return event in cls.get_all_events()


class TravelEquipment:
    """Special equipment that aids travel"""

    MOUNT = "mount"
    CART = "cart"
    BOAT = "boat"
    CLIMBING_GEAR = "climbing_gear"
    COMPASS = "compass"
    LANTERN = "lantern"
    CLOAK = "cloak"
    SURVIVAL_KIT = "survival_kit"

    @classmethod
    def get_all_equipment(cls) -> List[str]:
        """Get all available travel equipment."""
        return [
            cls.MOUNT,
            cls.CART,
            cls.BOAT,
            cls.CLIMBING_GEAR,
            cls.COMPASS,
            cls.LANTERN,
            cls.CLOAK,
            cls.SURVIVAL_KIT,
        ]

    @classmethod
    def is_valid_equipment(cls, equipment: str) -> bool:
        """Check if equipment type is valid."""
        return equipment in cls.get_all_equipment()


class EncounterDifficulty:
    """Difficulty levels for encounters"""

    TRIVIAL = 1
    EASY = 2
    MODERATE = 3
    HARD = 4
    DEADLY = 5

    @classmethod
    def get_all_difficulties(cls) -> List[int]:
        """Get all difficulty levels."""
        return [cls.TRIVIAL, cls.EASY, cls.MODERATE, cls.HARD, cls.DEADLY]

    @classmethod
    def is_valid_difficulty(cls, difficulty: int) -> bool:
        """Check if difficulty level is valid."""
        return difficulty in cls.get_all_difficulties()


class TravelStatus:
    """Status of ongoing travel"""

    PLANNING = "planning"
    IN_PROGRESS = "in_progress"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    INTERRUPTED = "interrupted"

    @classmethod
    def get_all_statuses(cls) -> List[str]:
        """Get all travel statuses."""
        return [
            cls.PLANNING,
            cls.IN_PROGRESS,
            cls.PAUSED,
            cls.COMPLETED,
            cls.FAILED,
            cls.INTERRUPTED,
        ]

    @classmethod
    def is_valid_status(cls, status: str) -> bool:
        """Check if status is valid."""
        return status in cls.get_all_statuses()
