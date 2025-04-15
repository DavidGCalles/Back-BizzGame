from flask.views import MethodView
from flask import jsonify
from flask_smorest import Blueprint
from app.dao.street_dao import StreetDAO
from app.models.base_schema import MessageResponseSchema
from app.models.street_schemas import UpdateStreetSchema, PostStreetSchema, StreetSchema, SearchStreetSchema

# Blueprints
street_bp = Blueprint('street', __name__, description="CRUD operations for streets.")

# DAOs
street_dao = StreetDAO()

# Street CRUD
@street_bp.route('/street')
class StreetCollection(MethodView):
    @street_bp.response(200, StreetSchema(many=True), description="Streets successfully retrieved.")
    def get(self):
        data = street_dao.get_all_streets()
        return jsonify(data), 200

    @street_bp.arguments(PostStreetSchema)
    @street_bp.response(201, MessageResponseSchema, description="New street successfully inserted.")
    def post(self, new_data):
        result = street_dao.generic_insert(new_data)
        if result:
            return {"message": "New street inserted"}, 201
        return {"message": "Error inserting street"}, 503

@street_bp.route('/street/search')
class StreetSearch(MethodView):
    @street_bp.arguments(SearchStreetSchema, location="query")
    @street_bp.response(200, StreetSchema(many=True), description="Streets successfully retrieved.")
    @street_bp.response(400, MessageResponseSchema, description="Invalid search parameters.")
    @street_bp.doc(summary="Search streets", description="Search streets by specific fields.")
    def get(self, args):
        """
        GET method: Search items based on query parameters.

        Query parameters:
        - name: Name of the item to search for (optional)
        - category: Category of the item (optional)
        - price_min: Minimum price of the item (optional)
        - price_max: Maximum price of the item (optional)
        """
        print(f"hey: {args}")  # Debugging line to check the received arguments
        query_params = {key: value for key, value in args.items() if value is not None}

        if not query_params:
            return {"message": "No search parameters provided"}, 400

        results = street_dao.generic_search(query_params, True)
        if results:
            results = [StreetSchema().from_array_to_json(item) for item in results]
        return jsonify(results), 200

@street_bp.route('/street/<int:street_id>')
class StreetSingle(MethodView):
    @street_bp.response(200, StreetSchema, description="Street successfully retrieved.")
    @street_bp.response(404, MessageResponseSchema, description="Street not found.")
    @street_bp.doc(summary="Retrieve a street", description="Fetch a street by its ID.")
    def get(self, street_id):
        """
        GET method: Retrieve a street by ID.
        """
        street = street_dao.generic_get_by_field("id", street_id)
        if street:
            return jsonify(street), 200
        return {"message": "Street not found"}, 404

    @street_bp.response(200, MessageResponseSchema, description="Street successfully deleted.")
    @street_bp.response(404, MessageResponseSchema, description="Street not found.")
    @street_bp.doc(summary="Delete a street", description="Delete a street by its ID.")
    def delete(self, street_id):
        """
        DELETE method: Delete a street by ID.
        """
        if street_dao.generic_delete("id", street_id):
            return {"message": "Street deleted successfully"}, 200
        return {"message": "Street not found"}, 404
    @street_bp.arguments(UpdateStreetSchema)
    @street_bp.response(200, MessageResponseSchema, description="Street successfully updated.")
    @street_bp.response(404, MessageResponseSchema, description="Street not found.")
    @street_bp.doc(summary="Update a street", description="Update an existing street by its ID.")
    def patch(self, update_data, street_id):
        """
        PATCH method: Update a street by ID.
        """
        result = street_dao.generic_update("id", {"id": street_id, **update_data})
        if result:
            return {"success": True}, 200
        return {"message": "Street not found"}, 404
