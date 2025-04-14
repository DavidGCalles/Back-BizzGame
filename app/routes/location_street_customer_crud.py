from flask.views import MethodView
from flask import jsonify
from flask_smorest import Blueprint
from app.dao.location_street_customer_dao import LocationDAO, StreetDAO, CustomerDAO
from app.models.location_street_customer_schemas import LocationSchema, StreetSchema, CustomerSchema
from app.models.base_schema import MessageResponseSchema
from app.services.city_generation import CityGenerator
import random

# Blueprints
location_bp = Blueprint('location', __name__, description="CRUD operations for locations.")
street_bp = Blueprint('street', __name__, description="CRUD operations for streets.")
customer_bp = Blueprint('customer', __name__, description="CRUD operations for customers.")

# DAOs
location_dao = LocationDAO()
street_dao = StreetDAO()
customer_dao = CustomerDAO()

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

@location_bp.route('/location/generate')
class LocationGenerate(MethodView):
    @location_bp.response(200, MessageResponseSchema, description="Locations successfully generated.")
    def post(self):
        """
        POST method: Generate locations.
        """
        generator = CityGenerator()
        locations = [generator.generate_location(city_id=1) for _ in range(10)]  # Generate 10 locations for city_id=1
        for location in locations:
            location_dao.generic_insert(location)
        return {"message": "Locations generated successfully"}, 200

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

@street_bp.route('/street/generate')
class StreetGenerate(MethodView):
    @street_bp.response(200, MessageResponseSchema, description="Streets successfully generated.")
    def post(self):
        """
        POST method: Generate streets.
        """
        generator = CityGenerator()
        # Assuming city_id=1 and generating 10 streets
        locations = location_dao.generic_get_all()  # Fetch all locations to connect streets
        city_id = 1  # Replace with dynamic city_id if needed
        streets = []

        if len(locations) < 2:
            return {"message": "Not enough locations to generate streets."}, 400

        for _ in range(10):  # Generate 10 streets
            start_location = random.choice(locations)
            end_location = random.choice(locations)
            if start_location["id"] != end_location["id"]:  # Avoid self-loops
                street = generator.generate_street(city_id, start_location["id"], end_location["id"])
                streets.append(street)
                street_dao.generic_insert(street)

        return {"message": "Streets generated successfully"}, 200

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

@customer_bp.route('/customer/generate')
class CustomerGenerate(MethodView):
    @customer_bp.response(200, MessageResponseSchema, description="Customers successfully generated.")
    def post(self):
        """
        POST method: Generate customers.
        """
        generator = CityGenerator()
        city_id = 1  # Replace with dynamic city_id if needed
        customers = [generator.generate_customer(city_id) for _ in range(10)]  # Generate 10 customers

        for customer in customers:
            customer_dao.generic_insert(customer)

        return {"message": "Customers generated successfully"}, 200