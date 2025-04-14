from flask.views import MethodView
from flask import jsonify
from flask_smorest import Blueprint
from app.dao.street_customer_dao import StreetDAO, CustomerDAO
from app.models.street_customer_schemas import StreetSchema, CustomerSchema
from app.models.base_schema import MessageResponseSchema

# Blueprints
street_bp = Blueprint('street', __name__, description="CRUD operations for streets.")
customer_bp = Blueprint('customer', __name__, description="CRUD operations for customers.")

# DAOs
street_dao = StreetDAO()
customer_dao = CustomerDAO()

# Street CRUD
@street_bp.route('/street')
class StreetCollection(MethodView):
    @street_bp.response(200, StreetSchema(many=True), description="Streets successfully retrieved.")
    def get(self):
        data = street_dao.generic_get_all()
        return jsonify(data), 200

    @street_bp.arguments(StreetSchema)
    @street_bp.response(201, MessageResponseSchema, description="New street successfully inserted.")
    def post(self, new_data):
        result = street_dao.generic_insert(new_data)
        if result:
            return {"message": "New street inserted"}, 201
        return {"message": "Error inserting street"}, 503

# Customer CRUD
@customer_bp.route('/customer')
class CustomerCollection(MethodView):
    @customer_bp.response(200, CustomerSchema(many=True), description="Customers successfully retrieved.")
    def get(self):
        data = customer_dao.generic_get_all()
        return jsonify(data), 200

    @customer_bp.arguments(CustomerSchema)
    @customer_bp.response(201, MessageResponseSchema, description="New customer successfully inserted.")
    def post(self, new_data):
        result = customer_dao.generic_insert(new_data)
        if result:
            return {"message": "New customer inserted"}, 201
        return {"message": "Error inserting customer"}, 503
