from app.dao.generic_dao import BaseDAO
from app.models.location_schemas import LocationSchema, LocationTypeSchema

class LocationDAO(BaseDAO):
    """
    DAO class for handling database operations related to the 'location' table.
    """
    def __init__(self):
        super().__init__()
        self.table = "location"

class LocationTypeDAO(BaseDAO):
    """
    DAO class for handling database operations related to the 'location_type' table.
    """
    def __init__(self):
        super().__init__()
        self.table = "location_types"
    def get_all_by_basic_type(self):
        """
        Get a location type by its basic type.
        """
        data = self.generic_get_all()
        if not data:
            raise ValueError(f"No location type found.")
        basic_type_grouping = {"Business": [], "Residential": []}
        keys = basic_type_grouping.keys()
        for key in keys:
            for item in data:
                if key in item[1]:
                    model_object = LocationTypeSchema().from_array_to_json(item)
                    basic_type_grouping[key].append(model_object)
        return basic_type_grouping