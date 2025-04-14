from app.dao.generic_dao import BaseDAO

class LocationDAO(BaseDAO):
    """
    DAO class for handling database operations related to the 'location' table.
    """
    def __init__(self):
        super().__init__()
        self.table = "location"

class LocationTypeDAO(BaseDAO):
    """
    DAO class for handling database operations related to the 'location_type' table.
    """
    def __init__(self):
        super().__init__()
        self.table = "location_types"