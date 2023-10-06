import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import logging
from src.resources.vehicles import blp as VehiclesBlueprint
from src.resources.login import blp as LoginBlueprint
from src.resources.parkingspace import blp as ParkingSpaceBlueprint
from src.resources.slot import blp as SlotsBlueprint
from flask_jwt_extended import JWTManager
from flask_smorest import Api
from flask import Flask
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename=os.getenv('LOG_FILE_NAME'),)
logger = logging.getLogger(__name__)


def create_app():
    app = Flask(__name__)

    app.config["PROPOGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = os.getenv("API_TITLE")
    app.config["API_VERSION"] = os.getenv("API_VERSION") 
    app.config["OPENAPI_VERSION"] = os.getenv("OPENAPI_VERSION")
    app.config["OPENAPI_URL_PREFIX"] = os.getenv("OPENAPI_URL_PREFIX") 
    app.config["OPENAPI_SWAGGER_UI_PATH"] = os.getenv("OPENAPI_SWAGGER_UI_PATH") 
    app.config["OPENAPI_SWAGGER_UI_URL"] = os.getenv("OPENAPI_SWAGGER_UI_URL") 

    api = Api(app)

    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    jwt = JWTManager(app)

    api.register_blueprint(SlotsBlueprint)
    api.register_blueprint(LoginBlueprint)
    api.register_blueprint(ParkingSpaceBlueprint)
    api.register_blueprint(VehiclesBlueprint)

    return app
