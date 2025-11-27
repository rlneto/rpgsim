"""
World domain entities and value objects
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set
from enum import Enum


class LocationType(Enum):
    """Types of locations in the game world"""
    CITY = "city"
    DUNGEON = "dungeon"
    VILLAGE = "village"
    FOREST = "forest"
    MOUNTAIN = "mountain"
    RIVER = "river"
    DESERT = "desert"
    CASTLE = "castle"
    RUINS = "ruins"
    TEMPLE = "temple"


class TravelRequirementType(Enum):
    """Types of travel requirements between locations"""
    NONE = "none"
    LEVEL = "level"
    ITEM = "item"
    QUEST = "quest"
    GOLD = "gold"
    SKILL = "skill"


@dataclass(frozen=True)
class TravelRequirement:
    """Travel requirement between locations"""
    requirement_type: TravelRequirementType
    value: int = 0
    description: str = ""
    
    def is_met(self, character_data: Dict) -> bool:
        """Check if requirement is met by character"""
        if self.requirement_type == TravelRequirementType.NONE:
            return True
        elif self.requirement_type == TravelRequirementType.LEVEL:
            return character_data.get("level", 0) >= self.value
        elif self.requirement_type == TravelRequirementType.GOLD:
            return character_data.get("gold", 0) >= self.value
        elif self.requirement_type == TravelRequirementType.ITEM:
            return self.value in character_data.get("inventory", [])
        
        return False


@dataclass(frozen=True)
class TravelConnection:
    """Connection between two locations"""
    from_location_id: str
    to_location_id: str
    travel_time: int  # in minutes
    difficulty: int  # 1-10 scale
    requirements: List[TravelRequirement] = field(default_factory=list)
    description: str = ""
    
    def can_travel(self, character_data: Dict) -> bool:
        """Check if character can travel via this connection"""
        return all(req.is_met(character_data) for req in self.requirements)
    
    def get_total_requirements(self) -> str:
        """Get human-readable requirements string"""
        if not self.requirements:
            return "None"
        
        req_strings = []
        for req in self.requirements:
            if req.requirement_type == TravelRequirementType.LEVEL:
                req_strings.append(f"Level {req.value}+")
            elif req.requirement_type == TravelRequirementType.GOLD:
                req_strings.append(f"{req.value} Gold")
            elif req.requirement_type == TravelRequirementType.ITEM:
                req_strings.append(f"{req.description}")
        
        return ", ".join(req_strings)


@dataclass(frozen=True)
class Coordinates:
    """Geographic coordinates for location"""
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    
    def distance_to(self, other: 'Coordinates') -> float:
        """Calculate distance to another coordinate"""
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5


@dataclass(frozen=True)
class Location:
    """Location entity in the game world"""
    id: str
    name: str
    location_type: LocationType
    description: str
    coordinates: Coordinates
    level_requirement: int = 1
    size: str = "medium"  # small, medium, large
    population: int = 0
    available_services: List[str] = field(default_factory=list)
    connected_locations: Set[str] = field(default_factory=set)
    is_start_location: bool = False
    weather: str = "clear"
    time_zone: str = "standard"
    special_features: List[str] = field(default_factory=list)
    
    def is_accessible_by_level(self, character_level: int) -> bool:
        """Check if location is accessible by character level"""
        return character_level >= self.level_requirement
    
    def has_service(self, service: str) -> bool:
        """Check if location provides specific service"""
        return service in self.available_services
    
    def get_summary(self) -> Dict[str, any]:
        """Get location summary"""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.location_type.value,
            "level": self.level_requirement,
            "size": self.size,
            "services": self.available_services,
            "connections": list(self.connected_locations),
            "start_location": self.is_start_location
        }


@dataclass
class World:
    """World aggregate root entity"""
    id: str
    name: str
    description: str
    locations: Dict[str, Location] = field(default_factory=dict)
    connections: Dict[str, List[TravelConnection]] = field(default_factory=dict)
    current_time: int = 0  # Game time in minutes
    time_scale: float = 1.0  # Time speed multiplier
    active_characters: Set[str] = field(default_factory=set)
    
    def add_location(self, location: Location) -> bool:
        """Add location to world"""
        if not location or not location.id:
            return False
        
        self.locations[location.id] = location
        return True
    
    def remove_location(self, location_id: str) -> bool:
        """Remove location from world"""
        if location_id in self.locations:
            del self.locations[location_id]
            
            # Remove connections to/from this location
            if location_id in self.connections:
                del self.connections[location_id]
            
            for from_loc_id, connections in self.connections.items():
                self.connections[from_loc_id] = [
                    conn for conn in connections
                    if conn.to_location_id != location_id
                ]
            
            return True
        return False
    
    def add_connection(self, connection: TravelConnection) -> bool:
        """Add travel connection between locations"""
        if not connection or not connection.from_location_id or not connection.to_location_id:
            return False
        
        # Validate locations exist
        if (connection.from_location_id not in self.locations or 
            connection.to_location_id not in self.locations):
            return False
        
        # Add to connections
        if connection.from_location_id not in self.connections:
            self.connections[connection.from_location_id] = []
        
        self.connections[connection.from_location_id].append(connection)
        
        # Update location connections
        if connection.from_location_id in self.locations:
            self.locations[connection.from_location_id].connected_locations.add(connection.to_location_id)
        
        return True
    
    def get_location(self, location_id: str) -> Optional[Location]:
        """Get location by ID"""
        return self.locations.get(location_id)
    
    def get_connections_from(self, location_id: str) -> List[TravelConnection]:
        """Get all connections from a location"""
        return self.connections.get(location_id, [])
    
    def get_start_location(self) -> Optional[Location]:
        """Get the starting location for the world"""
        for location in self.locations.values():
            if location.is_start_location:
                return location
        return None
    
    def get_locations_by_type(self, location_type: LocationType) -> List[Location]:
        """Get all locations of a specific type"""
        return [
            loc for loc in self.locations.values()
            if loc.location_type == location_type
        ]
    
    def get_accessible_locations(self, character_data: Dict) -> List[Location]:
        """Get all locations accessible to character"""
        accessible = []
        
        for location in self.locations.values():
            if location.is_accessible_by_level(character_data.get("level", 0)):
                accessible.append(location)
        
        return accessible
    
    def calculate_travel_time(self, connection: TravelConnection, character_data: Dict) -> int:
        """Calculate actual travel time for character"""
        base_time = connection.travel_time
        
        # Apply character speed modifiers
        character_level = character_data.get("level", 0)
        speed_factor = 1.0 + (character_level * 0.01)
        
        # Apply difficulty modifier
        difficulty_factor = 1.0 + (connection.difficulty * 0.1)
        
        return int(base_time * speed_factor * difficulty_factor)
    
    def can_travel(self, from_location_id: str, to_location_id: str, character_data: Dict) -> bool:
        """Check if character can travel between locations"""
        connections = self.get_connections_from(from_location_id)
        
        for connection in connections:
            if connection.to_location_id == to_location_id:
                return connection.can_travel(character_data)
        
        return False
    
    def advance_time(self, minutes: int) -> None:
        """Advance world time"""
        self.current_time += int(minutes * self.time_scale)
    
    def get_time_string(self) -> str:
        """Get current time as human-readable string"""
        total_minutes = self.current_time
        hours = (total_minutes // 60) % 24
        days = total_minutes // (60 * 24)
        minutes = total_minutes % 60
        
        if days == 0:
            return f"{hours:02d}:{minutes:02d}"
        elif days == 1:
            return f"Tomorrow {hours:02d}:{minutes:02d}"
        else:
            return f"Day {days} {hours:02d}:{minutes:02d}"
    
    def get_summary(self) -> Dict[str, any]:
        """Get world summary"""
        return {
            "id": self.id,
            "name": self.name,
            "locations": len(self.locations),
            "connections": sum(len(conns) for conns in self.connections.values()),
            "current_time": self.get_time_string(),
            "characters": len(self.active_characters)
        }


# Sample world data
DEFAULT_WORLD_CONFIG = {
    "locations": {
        "riverdale": Location(
            id="riverdale",
            name="Riverdale",
            location_type=LocationType.VILLAGE,
            description="A peaceful village nestled by the river",
            coordinates=Coordinates(0, 0, 0),
            level_requirement=1,
            size="small",
            population=500,
            available_services=["inn", "general_store", "blacksmith"],
            is_start_location=True
        ),
        "stonecrest": Location(
            id="stonecrest",
            name="Stonecrest",
            location_type=LocationType.CITY,
            description="A bustling city of trade and adventure",
            coordinates=Coordinates(100, 50, 0),
            level_requirement=3,
            size="large",
            population=5000,
            available_services=["inn", "weapon_shop", "armor_shop", "magic_shop", "bank", "guild"]
        ),
        "dark_forest": Location(
            id="dark_forest",
            name="Dark Forest",
            location_type=LocationType.FOREST,
            description="A mysterious forest shrouded in mist",
            coordinates=Coordinates(50, -100, 0),
            level_requirement=5,
            size="medium",
            available_services=["none"]
        )
    },
    "connections": {
        "riverdale": [
            TravelConnection(
                from_location_id="riverdale",
                to_location_id="stonecrest",
                travel_time=120,
                difficulty=3,
                requirements=[],
                description="Well-maintained road to the city"
            ),
            TravelConnection(
                from_location_id="riverdale",
                to_location_id="dark_forest",
                travel_time=90,
                difficulty=5,
                requirements=[TravelRequirement(
                    requirement_type=TravelRequirementType.LEVEL,
                    value=3,
                    description="Level 3+ required"
                )],
                description="Forest path, requires experience"
            )
        ]
    }
}