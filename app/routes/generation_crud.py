from flask.views import MethodView
from flask_smorest import Blueprint
from app.services.city_generation import CityGenerator
from app.dao.city_dao import CityDAO
from app.dao.street_customer_dao import StreetDAO, CustomerDAO
from app.dao.location_dao import LocationDAO
from app.models.base_schema import MessageResponseSchema
from app.models.city_schemas import RandomCitySchema, GenerateCitySchema, GenerateBoundedCitySchema  # Import the schema

# Blueprint
generation_bp = Blueprint('generation', __name__, description="Full city generation operations.")

# DAOs
city_dao = CityDAO()
location_dao = LocationDAO()
street_dao = StreetDAO()
customer_dao = CustomerDAO()

@generation_bp.route('/generate/city')
class CityGenerate(MethodView):
    @generation_bp.arguments(GenerateCitySchema, location="json")
    @generation_bp.response(200, MessageResponseSchema, description="City data successfully generated.")
    def post(self, args):
        """
        POST method: Generate city with random data (cities, locations, streets, customers).
        """
        generator = CityGenerator()
        print(args)
        city = generator.generate_city_data(args)
        city_dao.generic_insert(city["cities"][0])
        for location in city["locations"]:
            location_dao.generic_insert(location)
        for street in city["streets"]:
            street_dao.generic_insert(street)
        for customer in city["customers"]:
            customer_dao.generic_insert(customer)

        return {"message": "City data generated successfully"}, 200


@generation_bp.route('/generate/random-city')
class RandomCityGenerate(MethodView):
    @generation_bp.arguments(RandomCitySchema, location="json")
    @generation_bp.response(200, MessageResponseSchema, description="Full city data successfully generated.")
    def post(self, args):
        """
        POST method: Generate full city with random data (cities, locations, streets, customers).
        """
        generator = CityGenerator()
        for _ in range(args.get("num_cities")):
            city = generator.generate_city_data()
            city_dao.generic_insert(city["cities"][0])
            for location in city["locations"]:
                location_dao.generic_insert(location)
            for street in city["streets"]:
                street_dao.generic_insert(street)
            for customer in city["customers"]:
                customer_dao.generic_insert(customer)

        return {"message": "Full city data generated successfully"}, 200

@generation_bp.route('/generate/bounded-city')
class BoundedCityGenerate(MethodView):
    @generation_bp.arguments(GenerateBoundedCitySchema, location="json")
    @generation_bp.response(200, MessageResponseSchema, description="Bounded city data successfully generated.")
    def post(self, args):
        """
        POST method: Generate bounded city data (cities, locations, streets, customers).
        """
        generator = CityGenerator()
        data = generator.generate_bounded_city_data(
            difficulty_level=args.get("difficulty_level")
        )
        print(data)
        for city in data["cities"]:
            city_dao.generic_insert(city)
        for location in data["locations"]:
            location_dao.generic_insert(location)
        for street in data["streets"]:
            street_dao.generic_insert(street)
        for customer in data["customers"]:
            customer_dao.generic_insert(customer)

        return {"message": "Bounded city data generated successfully"}, 200