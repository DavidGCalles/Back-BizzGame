"""
This module initializes the Flask application, configures the API and CORS settings, 
registers the blueprints, and checks the database coherence.
"""
import os
from flask import Flask
from flask_smorest import Api
from flask_cors import CORS
from app.routes.main import main_bp
from app.routes.data_imports import data_imports_bp
from app.routes.city_crud import city_bp
from app.routes.city_config_crud import city_config_bp
from app.routes.location_crud import location_bp, location_type_bp
from app.routes.street_customer_crud import street_bp, customer_bp
from app.routes.generation_crud import generation_bp
from app.services.db import DBManager
from config import Config


def create_app():
    """Initializes the Flask application, configures the API and CORS settings,
    registers the blueprints, and checks the database coherence."""
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config["API_TITLE"] = "Flask API"
    app.config["API_VERSION"] = "1.0"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_JSON_PATH"] = "swagger.json"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    if os.getenv("SWAGGER_HOST"):
        app.config['SWAGGER_UI_HOST'] = os.getenv("SWAGGER_HOST")
    origins_allowed = []
    if Config.FLASK_ENV is None or Config.FLASK_ENV == "development":
        origins_allowed.append("http://localhost:8080")
    else:
        origins_allowed.append("https://front-arquetipo-856517455627.europe-southwest1.run.app")
    CORS(app, origins=origins_allowed,
         expose_headers=['Content-Type'],
         supports_credentials=True)
    api = Api(app)

    api.register_blueprint(main_bp)
    api.register_blueprint(city_bp)
    api.register_blueprint(city_config_bp)
    api.register_blueprint(location_bp)
    api.register_blueprint(location_type_bp)
    api.register_blueprint(street_bp)
    api.register_blueprint(customer_bp)
    api.register_blueprint(generation_bp)
    api.register_blueprint(data_imports_bp)
    DBManager().check_coherence()
    return app
