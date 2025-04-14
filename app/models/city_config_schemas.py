from marshmallow import fields, validate
from app.models.base_schema import BaseSchema

class CityConfigSchema(BaseSchema):
    """
    CityConfigSchema: Class to manage the schema of city configurations.
    """
    id = fields.Int(required=False, metadata={"description": "ID of the city configuration"})
    difficulty_level = fields.Str(
        required=True,
        validate=validate.OneOf(["easy", "medium", "hard"]),
        metadata={"description": "Difficulty level for city generation"}
    )
    residential_rate = fields.Float(
        required=True,
        validate=lambda x: 0 <= x <= 1,
        metadata={"description": "Rate of residential locations"}
    )
    commercial_rate = fields.Float(
        required=True,
        validate=lambda x: 0 <= x <= 1,
        metadata={"description": "Rate of commercial locations"}
    )
    max_population = fields.Int(
        required=True,
        validate=lambda x: x > 0,
        metadata={"description": "Maximum population allowed in the city"}
    )
    max_companies = fields.Int(
        required=True,
        validate=lambda x: x > 0,
        metadata={"description": "Maximum number of companies allowed in the city"}
    )
    description = fields.Str(
        required=False,
        metadata={"description": "Additional details about the configuration"}
    )