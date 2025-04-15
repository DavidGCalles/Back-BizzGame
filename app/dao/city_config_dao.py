from app.dao.generic_dao import BaseDAO
from app.models.city_config_schemas import CityConfigSchema

class CityConfigDAO(BaseDAO):
    """
    DAO class for handling database operations related to the 'city_configs' table.
    """
    def __init__(self):
        super().__init__()
        self.table = "city_configs"

    def get_single_city_config_by_difficulty(self,difficulty_level):
        """
        Get a single city configuration by difficulty level.
        """
        return CityConfigSchema().from_array_to_json(self.generic_get_by_field("difficulty_level", difficulty_level))
   