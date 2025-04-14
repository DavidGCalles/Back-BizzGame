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

class GenerateCitySchema(BaseSchema):
    """
    GenerateCitySchema: Class to validate city generation input.
    """
    max_population = fields.Int(required=True, 
                            validate=lambda x: x > 0,
                            metadata={"description": "Maximum population allowed in the city."})
    max_locations = fields.Int(required=True, 
                            validate=lambda x: x > 0,
                            metadata={"description": "Maximum number of locations allowed in the city."})
    residential_rate = fields.Float(required=True, 
                            validate=lambda x: 0 <= x <= 1,
                            metadata={"description": "Rate of residential locations."})
    commercial_rate = fields.Float(required=True, 
                            validate=lambda x: 0 <= x <= 1,
                            metadata={"description": "Rate of commercial locations."})
    difficulty_level = fields.Str(required=True, 
                            validate=lambda x: x in ["easy", "medium", "hard"],
                            metadata={"description": "Difficulty level for city generation."})

class RandomCitySchema(BaseSchema):
    """
    """
    num_cities = fields.Int(required=True, 
                            validate=lambda x: x > 0,
                            metadata={"description": "Number of cities to generate."})

class GenerateBoundedCitySchema(BaseSchema):
    """
    GenerateBoundedCitySchema: Class to validate bounded city generation input.
    """
    difficulty_level = fields.Str(required=True,
                            validate=lambda x: x in ["easy", "medium", "hard"],
                            metadata={"description": "Difficulty level for city generation."})
    