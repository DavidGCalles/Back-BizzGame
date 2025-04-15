from flask.views import MethodView
from flask import jsonify
from flask_smorest import Blueprint
from app.dao.customer_dao import CustomerDAO
from app.models.customer_schemas import CustomerSchema
from app.models.base_schema import MessageResponseSchema

# Blueprints
customer_bp = Blueprint('customer', __name__, description="CRUD operations for customers.")

# DAOs
customer_dao = CustomerDAO()

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
