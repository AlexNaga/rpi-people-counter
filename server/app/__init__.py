from .routes import data_api
from flask import Flask
from flask_cors import CORS
from flask_mqtt import Mqtt
import configparser

config = configparser.ConfigParser()
config.read("config/config.ini")

MQTT_SERVER = config.get("DEFAULT", "MQTT_SERVER")
MQTT_PORT = config.getint("DEFAULT", "MQTT_PORT")

mqtt = Mqtt()


def create_app():
    app = Flask(__name__)
    CORS(app)

    time_in_seconds = 1
    app.config["MQTT_REFRESH_TIME"] = time_in_seconds
    app.config["MQTT_BROKER_URL"] = MQTT_SERVER
    app.config["MQTT_BROKER_PORT"] = MQTT_PORT

    app.register_blueprint(data_api)
    mqtt.init_app(app)

    from .data_listener import events_api
    app.register_blueprint(events_api)

    return app
