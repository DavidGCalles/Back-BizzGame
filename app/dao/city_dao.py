from app.dao.generic_dao import BaseDAO
from app.models.city_schemas import CitySchema

class CityDAO(BaseDAO):
    """
    DAO class for handling database operations related to the 'city' table.
    """
    def __init__(self):
        super().__init__()
        self.table = "city"

    def get_all_cities(self):
        """
        Get all cities from the database.
        """
        data = self.generic_get_all()
        if not data:
            return []
        cities = []
        for city in data:
            city_object = CitySchema().from_array_to_json(city)
            cities.append(city_object)
        return cities

   