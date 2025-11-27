"""
World business logic services
"""
from typing import Dict, List, Optional, Tuple
from ..domain.world import World, Location, TravelConnection, TravelRequirement, DEFAULT_WORLD_CONFIG


class WorldService:
    """Service for world management and navigation logic"""

    def __init__(self, world: Optional[World] = None):
        self.world = world or self._create_default_world()

    def _create_default_world(self) -> World:
        """Create default world from configuration"""
        world = World(
            id="default",
            name="RPGSim World",
            description="Default game world"
        )

        # Add locations from config
        for location in DEFAULT_WORLD_CONFIG["locations"].values():
            world.add_location(location)

        # Add connections from config
        for from_loc, connections in DEFAULT_WORLD_CONFIG["connections"].items():
            for connection in connections:
                world.add_connection(connection)

        return world

    def get_world_info(self) -> Dict:
        """Get world information summary"""
        if not self.world:
            return {}

        return self.world.get_summary()

    def get_starting_location(self) -> Optional[Location]:
        """Get starting location for new characters"""
        if not self.world:
            return None

        return self.world.get_start_location()

    def get_accessible_locations(self, character_data: Dict) -> List[Location]:
        """Get all locations accessible to character"""
        if not self.world:
            return []

        return self.world.get_accessible_locations(character_data)

    def get_location_info(self, location_id: str) -> Optional[Dict]:
        """Get detailed information about a location"""
        if not self.world:
            return None

        location = self.world.get_location(location_id)
        if not location:
            return None

        return {
            "location": location.get_summary(),
            "connections": self._get_connection_info(location_id),
            "services": location.available_services,
            "special_features": location.special_features
        }

    def _get_connection_info(self, location_id: str) -> List[Dict]:
        """Get connection information for location"""
        if not self.world:
            return []

        connections = self.world.get_connections_from(location_id)
        return [
            {
                "to_location": conn.to_location_id,
                "to_location_name": self.world.get_location(conn.to_location_id).name if self.world.get_location(conn.to_location_id) else "Unknown",
                "travel_time": conn.travel_time,
                "difficulty": conn.difficulty,
                "requirements": conn.get_total_requirements(),
                "description": conn.description
            }
            for conn in connections
        ]

    def add_location(self, location_data: Dict) -> bool:
        """Add new location to world"""
        if not self.world or not location_data:
            return False

        from ..domain.world import Location, LocationType, Coordinates

        try:
            location = Location(
                id=location_data["id"],
                name=location_data["name"],
                location_type=LocationType(location_data["type"]),
                description=location_data.get("description", ""),
                coordinates=Coordinates(
                    x=location_data.get("x", 0),
                    y=location_data.get("y", 0),
                    z=location_data.get("z", 0)
                ),
                level_requirement=location_data.get("level_requirement", 1),
                size=location_data.get("size", "medium"),
                population=location_data.get("population", 0),
                available_services=location_data.get("services", []),
                special_features=location_data.get("special_features", [])
            )

            return self.world.add_location(location)
        except (KeyError, ValueError):
            return False

    def remove_location(self, location_id: str) -> bool:
        """Remove location from world"""
        if not self.world:
            return False

        return self.world.remove_location(location_id)

    def add_connection(self, connection_data: Dict) -> bool:
        """Add travel connection between locations"""
        if not self.world or not connection_data:
            return False

        try:
            requirements = []
            for req_data in connection_data.get("requirements", []):
                from ..domain.world import TravelRequirement, TravelRequirementType
                requirement = TravelRequirement(
                    requirement_type=TravelRequirementType(req_data["type"]),
                    value=req_data.get("value", 0),
                    description=req_data.get("description", "")
                )
                requirements.append(requirement)

            connection = TravelConnection(
                from_location_id=connection_data["from_location"],
                to_location_id=connection_data["to_location"],
                travel_time=connection_data["travel_time"],
                difficulty=connection_data["difficulty"],
                requirements=requirements,
                description=connection_data.get("description", "")
            )

            return self.world.add_connection(connection)
        except (KeyError, ValueError):
            return False

    def advance_time(self, minutes: int) -> bool:
        """Advance world time"""
        if not self.world or minutes <= 0:
            return False

        self.world.advance_time(minutes)
        return True

    def get_current_time(self) -> str:
        """Get current world time as string"""
        if not self.world:
            return "00:00"

        return self.world.get_time_string()

    def get_locations_by_type(self, location_type: str) -> List[Dict]:
        """Get all locations of specific type"""
        if not self.world:
            return []

        from ..domain.world import LocationType

        try:
            loc_type = LocationType(location_type)
            locations = self.world.get_locations_by_type(loc_type)
            return [loc.get_summary() for loc in locations]
        except ValueError:
            return []

    def validate_world_integrity(self) -> List[str]:
        """Validate world data integrity"""
        if not self.world:
            return ["No world loaded"]

        issues = []

        # Check for orphaned connections
        for from_loc_id, connections in self.world.connections.items():
            if from_loc_id not in self.world.locations:
                issues.append(f"Orphaned connections from unknown location: {from_loc_id}")

            for conn in connections:
                if conn.to_location_id not in self.world.locations:
                    issues.append(f"Connection to unknown location: {conn.to_location_id}")

        # Check for start location
        if not self.world.get_start_location():
            issues.append("No starting location defined")

        # Check for isolated locations
        for loc_id, location in self.world.locations.items():
            if not location.connected_locations and not location.is_start_location:
                issues.append(f"Isolated location: {location.name} ({loc_id})")

        return issues
