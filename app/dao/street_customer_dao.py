from app.dao.generic_dao import BaseDAO
from app.models.street_customer_schemas import StreetSchema

class StreetDAO(BaseDAO):
    """
    DAO class for handling database operations related to the 'street' table.
    """
    def __init__(self):
        super().__init__()
        self.table = "street"
    def get_all_streets(self):
        """
        Retrieve all streets from the database.
        """
        result = self.generic_get_all()
        return [StreetSchema().from_array_to_json(row) for row in result]

class CustomerDAO(BaseDAO):
    """
    DAO class for handling database operations related to the 'customer' table.
    """
    def __init__(self):
        super().__init__()
        self.table = "customer"