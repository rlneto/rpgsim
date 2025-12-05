from typing import Optional, List
from .domain.city import City
from .services.creation import CityCreationService
from .repositories.memory_repository import MemoryCityRepository

class CitySystem:
    def __init__(self):
        self.repository = MemoryCityRepository()
        self.creation_service = CityCreationService(self.repository)

    def create_city(self, id: str, name: str, population: int) -> City:
        return self.creation_service.create_city(id, name, population)

    def get_city(self, id: str) -> Optional[City]:
        return self.repository.get(id)

    def list_cities(self) -> List[City]:
        return self.repository.list_all()
