from marshmallow import fields
from app.models.base_schema import BaseSchema

class LocationSchema(BaseSchema):
    """
    LocationSchema: Class to manage the schema of locations.
    """
    id = fields.Int(required=False, metadata={"description": "ID of the location"})
    name = fields.Str(required=True, metadata={"description": "Name of the location"})
    city_id = fields.Int(required=True, metadata={"description": "ID of the city the location belongs to"})
    location_type_id = fields.Str(required=True, metadata={"description": "Type of the location (e.g., junction, residential)"})

class LocationTypeSchema(BaseSchema):
    """
    LocationTypeSchema: Class to manage the schema of location types.
    """
    id = fields.Int(required=False, metadata={"description": "ID of the location type"})
    name = fields.Str(required=True, metadata={"description": "Name of the location type"})
    description = fields.Str(required=True, metadata={"description": "Description of the location type"})
    max_capacity = fields.Int(required=True, metadata={"description": "Maximum capacity of the location type"})
    used_capacity = fields.Int(required=True, metadata={"description": "Used capacity of the location type"})
    rent = fields.Float(required=True, metadata={"description": "Rent of the location type"})
    maintenance_cost = fields.Float(required=True, metadata={"description": "Maintenance cost of the location type"})
