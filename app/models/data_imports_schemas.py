from marshmallow import fields
from app.models.base_schema import BaseSchema

class CityImportSchema(BaseSchema):
    """
    CityImportSchema: Class to manage the schema of the cities for data import.
    """
    name = fields.Str(required=True, metadata={"description": "Name of the city"})
    region = fields.Str(required=False, metadata={"description": "Region of the city"})