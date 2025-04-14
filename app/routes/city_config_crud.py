from flask.views import MethodView
from flask import jsonify
from flask_smorest import Blueprint
from app.dao.city_config_dao import CityConfigDAO
from app.models.city_config_schemas import CityConfigSchema
from app.models.base_schema import SuccessResponseSchema, MessageResponseSchema

# Blueprint
city_config_bp = Blueprint('city_config', __name__, description="CRUD operations for city configurations.")

# DAO
city_config_dao = CityConfigDAO()

# Operations for the collection (/city-config)
@city_config_bp.route('/city-config')
class CityConfigCollection(MethodView):
    @city_config_bp.response(200, CityConfigSchema(many=True), description="City configurations successfully retrieved.")
    @city_config_bp.doc(summary="Retrieve all city configurations", description="Fetch all city configurations from the database.")
    def get(self):
        """
        GET method: Retrieve all city configurations.
        """
        data = city_config_dao.generic_get_all()
        return jsonify(data), 200

    @city_config_bp.arguments(CityConfigSchema)
    @city_config_bp.response(201, MessageResponseSchema, description="New city configuration successfully inserted.")
    @city_config_bp.response(503, MessageResponseSchema, description="Error inserting the city configuration.")
    @city_config_bp.doc(summary="Insert new city configuration", description="Insert a new city configuration into the database.")
    def post(self, new_data):
        """
        POST method: Insert a new city configuration.
        """
        result = city_config_dao.generic_insert(new_data)
        if result:
            return {"message": "New city configuration inserted"}, 201
        return {"message": "There was a problem inserting the city configuration"}, 503

# Operations for a single resource (/city-config/<id>)
@city_config_bp.route('/city-config/<int:config_id>')
class CityConfigResource(MethodView):
    @city_config_bp.response(200, CityConfigSchema, description="City configuration successfully retrieved.")
    @city_config_bp.response(404, MessageResponseSchema, description="City configuration not found.")
    @city_config_bp.doc(summary="Retrieve a city configuration", description="Fetch a city configuration by its ID.")
    def get(self, config_id):
        """
        GET method: Retrieve a city configuration by ID.
        """
        config = city_config_dao.generic_get_by_field("id", config_id)
        if config:
            return jsonify(config), 200
        return {"message": "City configuration not found"}, 404

    @city_config_bp.arguments(CityConfigSchema)
    @city_config_bp.response(200, SuccessResponseSchema, description="City configuration successfully updated.")
    @city_config_bp.response(404, MessageResponseSchema, description="City configuration not found.")
    @city_config_bp.doc(summary="Update a city configuration", description="Update an existing city configuration by its ID.")
    def patch(self, update_data, config_id):
        """
        PATCH method: Update a city configuration by ID.
        """
        result = city_config_dao.generic_update("id", {"id": config_id, **update_data})
        if result:
            return {"success": True}, 200
        return {"message": "City configuration not found"}, 404

    @city_config_bp.response(200, MessageResponseSchema, description="City configuration successfully deleted.")
    @city_config_bp.response(404, MessageResponseSchema, description="City configuration not found.")
    @city_config_bp.doc(summary="Delete a city configuration", description="Delete a city configuration by its ID.")
    def delete(self, config_id):
        """
        DELETE method: Delete a city configuration by ID.
        """
        if city_config_dao.generic_delete("id", config_id):
            return {"message": "City configuration deleted successfully"}, 200
        return {"message": "City configuration not found"}, 404