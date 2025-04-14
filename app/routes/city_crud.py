from flask.views import MethodView
from flask import jsonify
from flask_smorest import Blueprint
from app.dao.city_dao import CityDAO
from app.models.city_schemas import CitySchema, UpdateCitySchema, PostCitySchema
from app.models.base_schema import SuccessResponseSchema, MessageResponseSchema

# Blueprint
city_bp = Blueprint('city', __name__, description="CRUD operations for cities.")

# DAO
city_dao = CityDAO()

# Operations for the collection (/city)
@city_bp.route('/city')
class CityCollection(MethodView):
    @city_bp.response(200, CitySchema(many=True), description="Cities successfully retrieved.")
    @city_bp.doc(summary="Retrieve all cities", description="Fetch all cities from the database.")
    def get(self):
        """
        GET method: Retrieve all cities.
        """
        data = city_dao.generic_get_all()
        return jsonify(data), 200

    @city_bp.arguments(PostCitySchema)
    @city_bp.response(201, MessageResponseSchema, description="New city successfully inserted.")
    @city_bp.response(503, MessageResponseSchema, description="Error inserting the city.")
    @city_bp.doc(summary="Insert new city", description="Insert a new city into the database.")
    def post(self, new_data):
        """
        POST method: Insert a new city.
        """
        result = city_dao.generic_insert(new_data)
        if result:
            return {"message": "New city inserted"}, 201
        return {"message": "There was a problem inserting the city"}, 503

# Operations for a single resource (/city/<id>)
@city_bp.route('/city/<int:city_id>')
class CityResource(MethodView):
    @city_bp.response(200, CitySchema, description="City successfully retrieved.")
    @city_bp.response(404, MessageResponseSchema, description="City not found.")
    @city_bp.doc(summary="Retrieve a city", description="Fetch a city by its ID.")
    def get(self, city_id):
        """
        GET method: Retrieve a city by ID.
        """
        city = city_dao.generic_get_by_field("id", city_id)
        if city:
            return jsonify(city), 200
        return {"message": "City not found"}, 404

    @city_bp.arguments(UpdateCitySchema)
    @city_bp.response(200, SuccessResponseSchema, description="City successfully updated.")
    @city_bp.response(404, MessageResponseSchema, description="City not found.")
    @city_bp.doc(summary="Update a city", description="Update an existing city by its ID.")
    def patch(self, update_data, city_id):
        """
        PATCH method: Update a city by ID.
        """
        result = city_dao.generic_update("id", {"id": city_id, **update_data})
        if result:
            return {"success": True}, 200
        return {"message": "City not found"}, 404

    @city_bp.response(200, MessageResponseSchema, description="City successfully deleted.")
    @city_bp.response(404, MessageResponseSchema, description="City not found.")
    @city_bp.doc(summary="Delete a city", description="Delete a city by its ID.")
    def delete(self, city_id):
        """
        DELETE method: Delete a city by ID.
        """
        if city_dao.generic_delete("id", city_id):
            return {"message": "City deleted successfully"}, 200
        return {"message": "City not found"}, 404
    