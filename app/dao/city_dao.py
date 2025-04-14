from app.dao.generic_dao import BaseDAO

class CityDAO(BaseDAO):
    """
    DAO class for handling database operations related to the 'city' table.
    """
    def __init__(self):
        super().__init__()
        self.table = "city"
   