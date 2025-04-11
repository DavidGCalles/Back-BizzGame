from flask.views import MethodView
from flask_smorest import Blueprint
from app.dao.city_dao import CityDAO
from app.models.data_imports_schemas import CityImportSchema
from app.models.city_schemas import CitySchema
from app.models.base_schema import MessageResponseSchema
from app.services.osm import OSMService
from time import sleep
from config import LOGGER

# Blueprint
data_imports_bp = Blueprint('data_imports', __name__, description="Data import operations.")

# DAO
city_dao = CityDAO()

# Operations for data imports (/data-imports/cities)
@data_imports_bp.route('/data-imports/cities')
class CityDataImport(MethodView):
    @data_imports_bp.arguments(CityImportSchema(many=True))
    @data_imports_bp.response(201, MessageResponseSchema, description="Cities successfully auto-populated.")
    @data_imports_bp.response(503, MessageResponseSchema, description="Error auto-populating cities.")
    @data_imports_bp.doc(summary="Auto-populate cities", description="Auto-populate the database with multiple cities.")
    def post(self, cities_data):
        """
        POST method: Auto-populate the database with multiple cities.
        """
        osm_service = OSMService()
        city_schema = CitySchema()
        for city_obj in cities_data:
            country = city_obj.get("region")
            LOGGER.info("%s city data being proccesed. Remember that OSM API has a API rate limit of 1/10s.", city_obj["name"])
            city_dict = osm_service.get_city_data(city_obj["name"], country)
            LOGGER.info("%s city data being proccesed. Remember that OSM API has a API rate limit of 1/10s.", city_dict["name"])
            streets = city_dict.pop("streets")
            LOGGER.info("Streets found: %s", len(streets))
            errors = city_schema.validate(city_dict)
            if errors:
                return {"message": "There was a problem with the data"}, 503
            city_dao.generic_insert(city_dict)
            sleep(30)
        return {"message": "Cities auto-populated successfully"}, 201