from flask.views import MethodView
from flask_smorest import Blueprint
from app.services.city_generation import CityGenerator
from app.dao.city_dao import CityDAO
from app.dao.location_street_customer_dao import LocationDAO, StreetDAO, CustomerDAO
from app.models.base_schema import MessageResponseSchema
from app.models.city_schemas import GenerateCitySchema  # Import the schema

# Blueprint
generation_bp = Blueprint('generation', __name__, description="Full city generation operations.")

# DAOs
city_dao = CityDAO()
location_dao = LocationDAO()
street_dao = StreetDAO()
customer_dao = CustomerDAO()

@generation_bp.route('/generate/full-city')
class FullCityGenerate(MethodView):
    @generation_bp.arguments(GenerateCitySchema, location="json")
    @generation_bp.response(200, MessageResponseSchema, description="Full city data successfully generated.")
    def post(self, args):
        """
        POST method: Generate full city data (cities, locations, streets, customers).
        """
        generator = CityGenerator()
        data = generator.generate_city_data(
            num_cities=args.get("num_cities"),
            locations_per_city=args.get("locations_per_city"),
            streets_per_city=args.get("streets_per_city"),
            customers_per_city=args.get("customers_per_city")
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

        return {"message": "Full city data generated successfully"}, 200