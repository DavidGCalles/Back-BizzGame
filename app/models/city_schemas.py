from marshmallow import fields
from app.models.base_schema import BaseSchema

class CitySchema(BaseSchema):
    """
    CitySchema: Class to manage the schema of the cities.
    """
    id = fields.Int(required=False, metadata={"description": "ID of the city"})
    name = fields.Str(required=True, metadata={"description": "Name of the city"})
    population = fields.Int(required=True, metadata={"description": "Population of the city"})
    region = fields.Str(required=False, metadata={"description": "Region of the city"})

class UpdateCitySchema(BaseSchema):
    """
    UpdateCitySchema: Class to manage the schema of the cities to update.
    """
    name = fields.Str(required=False, metadata={"description": "Updated name of the city"})
    population = fields.Int(required=False, metadata={"description": "Updated population of the city"})
    region = fields.Str(required=False, metadata={"description": "Updated region of the city"})

class PostCitySchema(BaseSchema):
    """
    PostCitySchema: Class to manage the schema of the cities to insert.
    """
    name = fields.Str(required=True, metadata={"description": "Name of the city"})
    population = fields.Int(required=True, metadata={"description": "Population of the city"})
    region = fields.Str(required=False, metadata={"description": "Region of the city"})