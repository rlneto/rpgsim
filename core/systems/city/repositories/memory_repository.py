from typing import List, Optional
from ..domain.city import City, Building
from ..interfaces.repositories import CityRepository

class MemoryCityRepository(CityRepository):
    def __init__(self):
        self._cities: dict[str, City] = {}

    def get(self, city_id: str) -> Optional[City]:
        return self._cities.get(city_id)

    def add(self, city: City) -> None:
        self._cities[city.id] = city

    def update(self, city: City) -> None:
        if city.id in self._cities:
            self._cities[city.id] = city

    def delete(self, city_id: str) -> None:
        if city_id in self._cities:
            del self._cities[city_id]

    def list_all(self) -> List[City]:
        return list(self._cities.values())
