# from data_listener import events_api, DataListener
from .routes import data_api
# from .data_listener import DataListener
from flask_sse import sse
from flask_cors import CORS
from flask import Flask
from flask_mqtt import Mqtt
import configparser

config = configparser.ConfigParser()
config.read("config/config.ini")

# The location to receive data from
PHYSICAL_AREA = config.get("DEFAULT", "PHYSICAL_AREA")
REDIS_SERVER = config.get("DEFAULT", "REDIS_SERVER")

MQTT_SERVER = config.get("DEFAULT", "MQTT_SERVER")
MQTT_PORT = config.getint("DEFAULT", "MQTT_PORT")

mqtt = Mqtt()


def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config["REDIS_URL"] = "redis://" + REDIS_SERVER
    app.config["MQTT_BROKER_URL"] = MQTT_SERVER
    app.config["MQTT_BROKER_PORT"] = MQTT_PORT
    app.config["MQTT_REFRESH_TIME"] = 1.0  # Refresh time in seconds

    app.register_blueprint(data_api)
    # app.register_blueprint(events_api)
    # app.register_blueprint(sse, url_prefix="/data/events")

    mqtt.init_app(app)
    from app import mqtt_handlers

    # data_listener = DataListener(PHYSICAL_AREA)
    # data_listener.start()
    return app
