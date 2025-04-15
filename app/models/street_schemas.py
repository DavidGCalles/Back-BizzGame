from marshmallow import fields
from app.models.base_schema import BaseSchema

class StreetSchema(BaseSchema):
    """
    StreetSchema: Class to manage the schema of streets.
    """
    id = fields.Int(required=False, metadata={"description": "ID of the street"})
    name = fields.Str(required=True, metadata={"description": "Name of the street"})
    city_id = fields.Int(required=True, metadata={"description": "ID of the city the street belongs to"})
    start_location_id = fields.Int(required=True, metadata={"description": "ID of the starting location"})
    end_location_id = fields.Int(required=True, metadata={"description": "ID of the ending location"})
    length = fields.Float(required=True, metadata={"description": "Length of the street"})

class SearchStreetSchema(BaseSchema):
    """
    SearchStreetSchema: Class to manage the schema of the streets to search.
    """
    name = fields.Str(required=False, metadata={"description": "Name of the street"})
    id = fields.Int(required=False, metadata={"description": "ID of the street"})
    city_id = fields.Int(required=False, metadata={"description": "ID of the city the street belongs to"})
    start_location_id = fields.Int(required=False, metadata={"description": "ID of the starting location"})
    end_location_id = fields.Int(required=False, metadata={"description": "ID of the ending location"})

class UpdateStreetSchema(BaseSchema):
    """
    UpdateStreetSchema: Class to manage the schema of the streets to update.
    """
    name = fields.Str(required=False, metadata={"description": "Updated name of the street"})
    city_id = fields.Int(required=False, metadata={"description": "ID of the city the street belongs to"})
    start_location_id = fields.Int(required=False, metadata={"description": "ID of the starting location"})
    end_location_id = fields.Int(required=False, metadata={"description": "ID of the ending location"})
    length = fields.Float(required=False, metadata={"description": "Length of the street"})

class PostStreetSchema(BaseSchema):
    """
    PostStreetSchema: Class to manage the schema of the streets to insert.
    """
    name = fields.Str(required=True, metadata={"description": "Name of the street"})
    city_id = fields.Int(required=True, metadata={"description": "ID of the city the street belongs to"})
    start_location_id = fields.Int(required=True, metadata={"description": "ID of the starting location"})
    end_location_id = fields.Int(required=True, metadata={"description": "ID of the ending location"})
    length = fields.Float(required=True, metadata={"description": "Length of the street"})