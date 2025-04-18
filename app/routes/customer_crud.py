from flask.views import MethodView
from flask import jsonify
from flask_smorest import Blueprint
from app.dao.customer_dao import CustomerDAO
from app.models.customer_schemas import CustomerSchema, PostCustomerSchema, UpdateCustomerSchema, SearchCustomerSchema
from app.models.base_schema import SuccessResponseSchema, MessageResponseSchema

# Blueprint
customer_bp = Blueprint('customer', __name__, description="CRUD operations for customers.")

# DAO
customer_dao = CustomerDAO()

# Operations for the collection (/customer)
@customer_bp.route('/customer')
class CustomerCollection(MethodView):
    @customer_bp.response(200, CustomerSchema(many=True), description="Customers successfully retrieved.")
    @customer_bp.doc(summary="Retrieve all customers", description="Fetch all customers from the database.")
    def get(self):
        """
        GET method: Retrieve all customers.
        """
        data = customer_dao.get_all_customers()
        return jsonify(data), 200

    @customer_bp.arguments(PostCustomerSchema)
    @customer_bp.response(201, MessageResponseSchema, description="New customer successfully inserted.")
    @customer_bp.response(503, MessageResponseSchema, description="Error inserting the customer.")
    @customer_bp.doc(summary="Insert new customer", description="Insert a new customer into the database.")
    def post(self, new_data):
        """
        POST method: Insert a new customer.
        """
        result = customer_dao.generic_insert(new_data)
        if result:
            return {"message": "New customer inserted"}, 201
        return {"message": "There was a problem inserting the customer"}, 503

# Operations for a single resource (/customer/<id>)
@customer_bp.route('/customer/<int:customer_id>')
class CustomerResource(MethodView):
    @customer_bp.response(200, CustomerSchema, description="Customer successfully retrieved.")
    @customer_bp.response(404, MessageResponseSchema, description="Customer not found.")
    @customer_bp.doc(summary="Retrieve a customer", description="Fetch a customer by its ID.")
    def get(self, customer_id):
        """
        GET method: Retrieve a customer by ID.
        """
        customer = customer_dao.generic_get_by_field("id", customer_id)
        if customer:
            return jsonify(customer), 200
        return {"message": "Customer not found"}, 404

    @customer_bp.arguments(UpdateCustomerSchema)
    @customer_bp.response(200, SuccessResponseSchema, description="Customer successfully updated.")
    @customer_bp.response(404, MessageResponseSchema, description="Customer not found.")
    @customer_bp.doc(summary="Update a customer", description="Update an existing customer by its ID.")
    def patch(self, update_data, customer_id):
        """
        PATCH method: Update a customer by ID.
        """
        result = customer_dao.generic_update("id", {"id": customer_id, **update_data})
        if result:
            return {"success": True}, 200
        return {"message": "Customer not found"}, 404

    @customer_bp.response(200, MessageResponseSchema, description="Customer successfully deleted.")
    @customer_bp.response(404, MessageResponseSchema, description="Customer not found.")
    @customer_bp.doc(summary="Delete a customer", description="Delete a customer by its ID.")
    def delete(self, customer_id):
        """
        DELETE method: Delete a customer by ID.
        """
        if customer_dao.generic_delete("id", customer_id):
            return {"message": "Customer deleted successfully"}, 200
        return {"message": "Customer not found"}, 404

@customer_bp.route('/customer/search')
class CustomerSearch(MethodView):
    @customer_bp.arguments(SearchCustomerSchema, location="query")
    @customer_bp.response(200, CustomerSchema(many=True), description="Customers successfully retrieved.")
    @customer_bp.response(400, MessageResponseSchema, description="Invalid search parameters.")
    @customer_bp.doc(summary="Search customers", description="Search customers by specific fields.")
    def get(self, args):
        """
        GET method: Search customers by fields.

        Query parameters:
        - name: Name of the customer (optional)
        - email: Email of the customer (optional)
        - phone: Phone number of the customer (optional)
        - city_id: ID of the city the customer belongs to (optional)
        """
        query_params = {key: value for key, value in args.items() if value is not None}

        if not query_params:
            return {"message": "No search parameters provided"}, 400

        results = customer_dao.generic_search(query_params, True)
        if not results:
            return {"message": "No customers found matching the criteria"}, 404
        # Iterate over the array to get CustomerSchema jsons
        for i in range(len(results)):
            results[i] = CustomerSchema().from_array_to_json(results[i])
        return jsonify(results), 200

