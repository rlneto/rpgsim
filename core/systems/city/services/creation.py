from ..domain.city import City, Building
from ..interfaces.repositories import CityRepository

class CityCreationService:
    def __init__(self, repository: CityRepository):
        self.repository = repository

    def create_city(self, id: str, name: str, population: int) -> City:
        city = City(id=id, name=name, population=population)
        self.repository.add(city)
        return city
