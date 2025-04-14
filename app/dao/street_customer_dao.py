from app.dao.generic_dao import BaseDAO

class LocationDAO(BaseDAO):
    """
    DAO class for handling database operations related to the 'location' table.
    """
    def __init__(self):
        super().__init__()
        self.table = "location"

class StreetDAO(BaseDAO):
    """
    DAO class for handling database operations related to the 'street' table.
    """
    def __init__(self):
        super().__init__()
        self.table = "street"

class CustomerDAO(BaseDAO):
    """
    DAO class for handling database operations related to the 'customer' table.
    """
    def __init__(self):
        super().__init__()
        self.table = "customer"