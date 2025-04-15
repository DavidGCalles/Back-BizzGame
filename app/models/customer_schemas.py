from marshmallow import fields
from app.models.base_schema import BaseSchema

class CustomerSchema(BaseSchema):
    """
    CustomerSchema: Class to manage the schema of customers.
    """
    id = fields.Int(required=False, metadata={"description": "ID of the customer"})
    name = fields.Str(required=True, metadata={"description": "Name of the customer"})
    email = fields.Email(required=True, metadata={"description": "Email of the customer"})
    phone = fields.Str(required=True, metadata={"description": "Phone number of the customer"})
    city_id = fields.Int(required=True, metadata={"description": "ID of the city the customer belongs to"})