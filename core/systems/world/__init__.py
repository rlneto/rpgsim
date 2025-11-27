"""
World system module - provides modular world management
"""

from .domain.world import (
    World, Location, TravelConnection, TravelRequirement, 
    LocationType, TravelRequirementType, Coordinates, DEFAULT_WORLD_CONFIG
)

from .services.world_service import WorldService
from .services.travel_service import TravelService, TravelRoute
from .services.location_service import LocationService

from .repositories.memory_repository import (
    MemoryWorldRepository, MemoryLocationRepository, MemoryTravelConnectionRepository
)

from .interfaces.repositories import (
    WorldRepository, LocationRepository, TravelConnectionRepository
)

from .facade import WorldSystem

__all__ = [
    # Domain entities
    'World', 'Location', 'TravelConnection', 'TravelRequirement',
    'LocationType', 'TravelRequirementType', 'Coordinates', 'DEFAULT_WORLD_CONFIG',
    
    # Services
    'WorldService', 'TravelService', 'TravelRoute', 'LocationService',
    
    # Repositories
    'MemoryWorldRepository', 'MemoryLocationRepository', 'MemoryTravelConnectionRepository',
    
    # Interfaces
    'WorldRepository', 'LocationRepository', 'TravelConnectionRepository',
    
    # Facade
    'WorldSystem'
]