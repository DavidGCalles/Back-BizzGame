from marshmallow import Schema, fields

class BaseSchema(Schema):
    """
    BaseSchema: Class to manage the schema of the base model.
    """
    def from_array_to_json(self, values):
        keys = self.fields.keys()
        return dict(zip(keys, values))
    
class UpdateItemSchema(BaseSchema):
    """
    UpdateItemSchema: Class to manage the schema of the items to update.
    """
    id = fields.Int(required=True, metadata={"description": "ID of the item to update"})
    name = fields.Str(required=False, metadata={"description": "Updated name"})
    description = fields.Str(required=False, metadata={"description": "Updated description"})

class SearchItemSchema(BaseSchema):
    """
    SearchItemSchema: Class to manage the schema of the items to search.
    """
    name = fields.Str(required=False)
    id = fields.Int(required=False)
    description = fields.Str(required=False, metadata={"description": "Updated description"})


class SuccessResponseSchema(Schema):
    """
    SuccessResponseSchema: Class to manage the schema of the success response.
    """
    success = fields.Bool(metadata={"description": "Indicates whether the operation was successful"})

class MessageResponseSchema(Schema):
    """
    MessageResponseSchema: Class to manage the schema of the message response.
    """
    message = fields.Str(metadata={"description": "Response message"})
    
