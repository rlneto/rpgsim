"""
Memory repository implementations for world data
"""
from typing import List, Dict, Optional
from ..interfaces.repositories import WorldRepository, LocationRepository, TravelConnectionRepository
from ..domain.world import World, Location, TravelConnection


class MemoryWorldRepository(WorldRepository):
    """In-memory world repository"""
    
    def __init__(self):
        self._worlds: Dict[str, World] = {}
    
    def save_world(self, world: World) -> bool:
        """Save world to memory storage"""
        if not world.id:
            return False
        
        self._worlds[world.id] = world
        return True
    
    def load_world(self, world_id: str) -> Optional[World]:
        """Load world by ID"""
        return self._worlds.get(world_id)
    
    def delete_world(self, world_id: str) -> bool:
        """Delete world by ID"""
        if world_id in self._worlds:
            del self._worlds[world_id]
            return True
        return False
    
    def list_worlds(self) -> List[Dict]:
        """List all worlds"""
        return [world.get_summary() for world in self._worlds.values()]


class MemoryLocationRepository(LocationRepository):
    """In-memory location repository"""
    
    def __init__(self, world_repository: WorldRepository):
        self.world_repository = world_repository
    
    def save_location(self, world_id: str, location: Location) -> bool:
        """Save location to world storage"""
        world = self.world_repository.load_world(world_id)
        if not world:
            return False
        
        success = world.add_location(location)
        if success:
            self.world_repository.save_world(world)
        
        return success
    
    def load_location(self, world_id: str, location_id: str) -> Optional[Location]:
        """Load location by ID"""
        world = self.world_repository.load_world(world_id)
        if not world:
            return None
        
        return world.get_location(location_id)
    
    def delete_location(self, world_id: str, location_id: str) -> bool:
        """Delete location by ID"""
        world = self.world_repository.load_world(world_id)
        if not world:
            return False
        
        success = world.remove_location(location_id)
        if success:
            self.world_repository.save_world(world)
        
        return success
    
    def list_locations(self, world_id: str) -> List[Location]:
        """List all locations in world"""
        world = self.world_repository.load_world(world_id)
        if not world:
            return []
        
        return list(world.locations.values())
    
    def search_locations(self, world_id: str, query: str) -> List[Location]:
        """Search locations by query"""
        world = self.world_repository.load_world(world_id)
        if not world:
            return []
        
        query = query.lower()
        results = []
        
        for location in world.locations.values():
            if (query in location.name.lower() or 
                query in location.description.lower() or
                query in location.location_type.value):
                results.append(location)
        
        return results


class MemoryTravelConnectionRepository(TravelConnectionRepository):
    """In-memory travel connection repository"""
    
    def __init__(self, world_repository: WorldRepository):
        self.world_repository = world_repository
    
    def save_connection(self, world_id: str, connection: TravelConnection) -> bool:
        """Save travel connection to world storage"""
        world = self.world_repository.load_world(world_id)
        if not world:
            return False
        
        success = world.add_connection(connection)
        if success:
            self.world_repository.save_world(world)
        
        return success
    
    def load_connections_from(self, world_id: str, from_location_id: str) -> List[TravelConnection]:
        """Load all connections from a location"""
        world = self.world_repository.load_world(world_id)
        if not world:
            return []
        
        return world.get_connections_from(from_location_id)
    
    def delete_connection(self, world_id: str, from_location_id: str, to_location_id: str) -> bool:
        """Delete connection between locations"""
        world = self.world_repository.load_world(world_id)
        if not world:
            return False
        
        # Find and remove the connection
        if from_location_id in world.connections:
            connections = world.connections[from_location_id]
            for i, conn in enumerate(connections):
                if conn.to_location_id == to_location_id:
                    connections.pop(i)
                    self.world_repository.save_world(world)
                    return True
        
        return False
    
    def list_connections(self, world_id: str) -> List[TravelConnection]:
        """List all connections in world"""
        world = self.world_repository.load_world(world_id)
        if not world:
            return []
        
        all_connections = []
        for connections in world.connections.values():
            all_connections.extend(connections)
        
        return all_connections