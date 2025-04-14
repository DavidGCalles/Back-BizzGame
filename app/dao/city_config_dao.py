from app.dao.generic_dao import BaseDAO

class CityConfigDAO(BaseDAO):
    """
    DAO class for handling database operations related to the 'city_configs' table.
    """
    def __init__(self):
        super().__init__()
        self.table = "city_configs"
   