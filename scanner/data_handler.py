import json
from datetime import datetime
import paho.mqtt.client as mqtt
from easydict import EasyDict as edict
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

MQTT_SERVER = config.get("DEFAULT", "MQTT_SERVER")
MQTT_PORT = config.getint("DEFAULT", "MQTT_PORT")


class DataHandler:
    def __init__(self, physical_area, device_id):
        self.physical_area = physical_area

        # Config the MQTT client
        self.mqttc = mqtt.Client(client_id=device_id)

        # Connect to the MQTT broker
        self.mqttc.connect(MQTT_SERVER, MQTT_PORT)

    def send_data(self, data):
        """Sends the data to the MQTT broker"""
        self.mqttc.publish(self.physical_area, data)

    def to_json(self, devices):
        """Encodes the data to JSON"""
        data = []

        for device_id in devices:
            timestamp = str(datetime.now())
            obj = edict({"device_id": device_id,
                         "timestamp": timestamp, "area": self.physical_area})
            data.append(obj)

        json_data = json.dumps(data)  # Encode to JSON
        return json_data
