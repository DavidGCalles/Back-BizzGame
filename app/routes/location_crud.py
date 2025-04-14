from flask.views import MethodView
from flask import jsonify
from flask_smorest import Blueprint
from app.dao.location_dao import LocationDAO, LocationTypeDAO
from app.models.location_schemas import LocationSchema, LocationTypeSchema
from app.models.base_schema import MessageResponseSchema

# Blueprints
location_bp = Blueprint('location', __name__, description="CRUD operations for locations.")
location_type_bp = Blueprint('location_type', __name__, description="CRUD operations for location types.")

# DAOs
location_dao = LocationDAO()
location_type_dao = LocationTypeDAO()


# Location CRUD
@location_bp.route('/location')
class LocationCollection(MethodView):
    @location_bp.response(200, LocationSchema(many=True), description="Locations successfully retrieved.")
    def get(self):
        data = location_dao.generic_get_all()
        return jsonify(data), 200

    @location_bp.arguments(LocationSchema)
    @location_bp.response(201, MessageResponseSchema, description="New location successfully inserted.")
    def post(self, new_data):
        result = location_dao.generic_insert(new_data)
        if result:
            return {"message": "New location inserted"}, 201
        return {"message": "Error inserting location"}, 503

@location_type_bp.route('/location_type')
class LocationTypeCollection(MethodView):
    @location_type_bp.response(200, LocationTypeSchema(many=True), description="Location types successfully retrieved.")
    def get(self):
        data = location_type_dao.generic_get_all()
        return jsonify(data), 200

    @location_type_bp.arguments(LocationTypeSchema)
    @location_type_bp.response(201, MessageResponseSchema, description="New location type successfully inserted.")
    def post(self, new_data):
        result = location_type_dao.generic_insert(new_data)
        if result:
            return {"message": "New location type inserted"}, 201
        return {"message": "Error inserting location type"}, 503