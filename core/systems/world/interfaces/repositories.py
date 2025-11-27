"""
World data repository interfaces
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from ..domain.world import World, Location, TravelConnection


class WorldRepository(ABC):
    """Repository interface for world data access"""

    @abstractmethod
    def save_world(self, world: World) -> bool:
        """Save world to storage"""
        pass

    @abstractmethod
    def load_world(self, world_id: str) -> Optional[World]:
        """Load world by ID"""
        pass

    @abstractmethod
    def delete_world(self, world_id: str) -> bool:
        """Delete world by ID"""
        pass

    @abstractmethod
    def list_worlds(self) -> List[Dict]:
        """List all worlds"""
        pass


class LocationRepository(ABC):
    """Repository interface for location data access"""

    @abstractmethod
    def save_location(self, world_id: str, location: Location) -> bool:
        """Save location to world storage"""
        pass

    @abstractmethod
    def load_location(self, world_id: str, location_id: str) -> Optional[Location]:
        """Load location by ID"""
        pass

    @abstractmethod
    def delete_location(self, world_id: str, location_id: str) -> bool:
        """Delete location by ID"""
        pass

    @abstractmethod
    def list_locations(self, world_id: str) -> List[Location]:
        """List all locations in world"""
        pass

    @abstractmethod
    def search_locations(self, world_id: str, query: str) -> List[Location]:
        """Search locations by query"""
        pass


class TravelConnectionRepository(ABC):
    """Repository interface for travel connection data access"""

    @abstractmethod
    def save_connection(self, world_id: str, connection: TravelConnection) -> bool:
        """Save travel connection to world storage"""
        pass

    @abstractmethod
    def load_connections_from(self, world_id: str, from_location_id: str) -> List[TravelConnection]:
        """Load all connections from a location"""
        pass

    @abstractmethod
    def delete_connection(self, world_id: str, from_location_id: str, to_location_id: str) -> bool:
        """Delete connection between locations"""
        pass

    @abstractmethod
    def list_connections(self, world_id: str) -> List[TravelConnection]:
        """List all connections in world"""
        pass
