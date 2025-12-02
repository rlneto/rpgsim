"""
Facade for world system operations
"""

from typing import List, Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .domain.world import World
else:
    from .domain.world import World
from .services.world_service import WorldService
from .services.travel_service import TravelService, TravelRoute
from .services.location_service import LocationService
from .repositories.memory_repository import (
    MemoryWorldRepository,
    MemoryLocationRepository,
    MemoryTravelConnectionRepository,
)


class WorldSystem:
    """Facade for all world system operations"""

    def __init__(self, world_id: str = "default"):
        # Initialize repositories
        self.world_repo = MemoryWorldRepository()
        self.location_repo = MemoryLocationRepository(self.world_repo)
        self.connection_repo = MemoryTravelConnectionRepository(self.world_repo)

        # Initialize services
        self.world_service = WorldService()
        self.travel_service = TravelService(self.world_service.world)
        self.location_service = LocationService(self.world_service.world)

        # Load or create world
        self.world_id = world_id
        self.world = self._load_or_create_world()

    def _load_or_create_world(self):
        """Load or create world - helper method to reduce attribute count"""

        world = self.world_repo.load_world(self.world_id)
        if not world:
            world = self.world_service.world
            self.world_repo.save_world(world)
        return world

    # World Management Methods
    def get_world_info(self) -> Dict:
        """Get world information summary"""
        return self.world_service.get_world_info()

    def get_starting_location(self) -> Optional[Dict]:
        """Get starting location for new characters"""
        start_location = self.world_service.get_starting_location()
        if start_location:
            return self.location_service.get_location_details(start_location.id)
        return None

    def advance_time(self, minutes: int) -> bool:
        """Advance world time"""
        success = self.world_service.advance_time(minutes)
        if success:
            self.world_repo.save_world(self.world)
        return success

    def get_current_time(self) -> str:
        """Get current world time"""
        return self.world_service.get_current_time()

    def validate_world_integrity(self) -> List[str]:
        """Validate world data integrity"""
        return self.world_service.validate_world_integrity()

    # Location Management Methods
    def get_location_details(self, location_id: str) -> Optional[Dict]:
        """Get detailed information about a location"""
        return self.location_service.get_location_details(location_id)

    def search_locations(self, query: str, character_data: Dict) -> List[Dict]:
        """Search locations by name or type"""
        return self.location_service.search_locations(query, character_data)

    def get_locations_by_service(
        self, service: str, character_data: Dict
    ) -> List[Dict]:
        """Get locations that provide specific service"""
        return self.location_service.get_locations_by_service(service, character_data)

    def get_locations_in_range(
        self, center_location_id: str, max_distance: float, character_data: Dict
    ) -> List[Dict]:
        """Get locations within range of a center location"""
        return self.location_service.get_locations_in_range(
            center_location_id, max_distance, character_data
        )

    def discover_location(self, location_id: str, character_data: Dict) -> Dict:
        """Discover a location for character"""
        return self.location_service.discover_location(location_id, character_data)

    def get_location_statistics(self, location_id: str) -> Optional[Dict]:
        """Get statistics for a location"""
        return self.location_service.get_location_statistics(location_id)

    def get_world_overview(self, character_data: Dict) -> Dict:
        """Get overview of all locations in world"""
        return self.location_service.get_world_overview(character_data)

    def add_location(self, location_data: Dict) -> bool:
        """Add new location to world"""
        success = self.world_service.add_location(location_data)
        if success:
            self.world_repo.save_world(self.world)
        return success

    def remove_location(self, location_id: str) -> bool:
        """Remove location from world"""
        success = self.world_service.remove_location(location_id)
        if success:
            self.world_repo.save_world(self.world)
        return success

    # Travel Management Methods
    def can_travel(
        self, from_location_id: str, to_location_id: str, character_data: Dict
    ) -> bool:
        """Check if character can travel directly between locations"""
        return self.travel_service.can_travel(
            from_location_id, to_location_id, character_data
        )

    def calculate_travel_time(
        self, from_location_id: str, to_location_id: str, character_data: Dict
    ) -> int:
        """Calculate travel time for direct travel"""
        return self.travel_service.calculate_travel_time(
            from_location_id, to_location_id, character_data
        )

    def find_route(
        self, from_location_id: str, to_location_id: str, character_data: Dict
    ) -> Optional[Dict]:
        """Find best route between two locations"""
        route = self.travel_service.find_route(
            from_location_id, to_location_id, character_data
        )
        return route.get_summary() if route else None

    def get_available_destinations(
        self, from_location_id: str, character_data: Dict
    ) -> List[Dict]:
        """Get all available destinations from a location"""
        return self.travel_service.get_available_destinations(
            from_location_id, character_data
        )

    def simulate_travel(self, route_data: Dict, character_data: Dict) -> Dict:
        """Simulate travel along a route"""
        # Convert route data back to TravelRoute object
        if not route_data:
            return {"success": False, "reason": "No route provided"}

        # Reconstruct route (simplified - in production you'd have proper serialization)
        route = TravelRoute(
            from_location=route_data["from"],
            to_location=route_data["to"],
            steps=route_data.get("steps", []),
            total_time=route_data.get("total_time", 0),
            total_difficulty=route_data.get("total_difficulty", 0),
            requirements=[],  # Would need proper reconstruction
            is_valid=route_data.get("valid", True),
        )

        return self.travel_service.simulate_travel(route, character_data)

    def get_travel_statistics(self, character_data: Dict) -> Dict:
        """Get travel statistics for character"""
        return self.travel_service.get_travel_statistics(character_data)

    def add_connection(self, connection_data: Dict) -> bool:
        """Add travel connection between locations"""
        success = self.world_service.add_connection(connection_data)
        if success:
            self.world_repo.save_world(self.world)
        return success

    # Character-Specific Methods
    def get_accessible_locations(self, character_data: Dict) -> List[Dict]:
        """Get all locations accessible to character"""
        locations = self.world_service.get_accessible_locations(character_data)
        # type: ignore[return-value] - pylint confused about return type
        return [self.location_service.get_location_details(loc.id) for loc in locations]

    def calculate_distance(
        self, from_location_id: str, to_location_id: str
    ) -> Optional[float]:
        """Calculate distance between two locations"""
        return self.location_service.calculate_distance(
            from_location_id, to_location_id
        )

    def get_character_context(self, character_data: Dict) -> Dict:
        """Get complete world context for character"""
        return {
            "world_info": self.get_world_info(),
            "current_time": self.get_current_time(),
            "accessible_locations": self.get_accessible_locations(character_data),
            "starting_location": self.get_starting_location(),
            "travel_statistics": self.get_travel_statistics(character_data),
            "world_overview": self.get_world_overview(character_data),
        }


# Global facade instance for backward compatibility
_world_system = WorldSystem()


# Backward compatibility functions
def get_world_info() -> Dict:
    """Get world information (backward compatibility)"""
    return _world_system.get_world_info()


def get_starting_location() -> Optional[Dict]:
    """Get starting location (backward compatibility)"""
    return _world_system.get_starting_location()


def get_location_details(location_id: str) -> Optional[Dict]:
    """Get location details (backward compatibility)"""
    return _world_system.get_location_details(location_id)


def can_travel(
    from_location_id: str, to_location_id: str, character_data: Dict
) -> bool:
    """Check travel possibility (backward compatibility)"""
    return _world_system.can_travel(from_location_id, to_location_id, character_data)


def find_route(
    from_location_id: str, to_location_id: str, character_data: Dict
) -> Optional[Dict]:
    """Find route between locations (backward compatibility)"""
    return _world_system.find_route(from_location_id, to_location_id, character_data)


def advance_time(minutes: int) -> bool:
    """Advance world time (backward compatibility)"""
    return _world_system.advance_time(minutes)


def get_current_time() -> str:
    """Get current world time (backward compatibility)"""
    return _world_system.get_current_time()


# Export main class and compatibility functions
__all__ = [
    "WorldSystem",
    "get_world_info",
    "get_starting_location",
    "get_location_details",
    "can_travel",
    "find_route",
    "advance_time",
    "get_current_time",
]
