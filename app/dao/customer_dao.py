from app.dao.generic_dao import BaseDAO
from app.models.customer_schemas import CustomerSchema

class CustomerDAO(BaseDAO):
    """
    DAO class for handling database operations related to the 'customer' table.
    """
    def __init__(self):
        super().__init__()
        self.table = "customer"
    def get_all_customers(self):
        """
        Get all customers from the database.
        """
        data = self.generic_get_all()
        if not data:
            return []
        customers = []
        for customer in data:
            customer_object = CustomerSchema().from_array_to_json(customer)
            customers.append(customer_object)
        return customers