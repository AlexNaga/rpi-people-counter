import json
from data_sender import DataSender
from datetime import datetime
from easydict import EasyDict as edict
import configparser

config = configparser.ConfigParser()
config.read("config/config.ini")

# The location for this device
PHYSICAL_AREA = config.get("DEFAULT", "PHYSICAL_AREA")


class DataHandler:
    def __init__(self):
        self.data_sender = DataSender()

    def send_data(self, devices_count, sensor_type):
        """Sends the data to the MQTT broker"""
        json_data = self.to_json(devices_count, sensor_type)
        self.data_sender.send_data(json_data)

    def to_json(self, devices_count, sensor_type):
        """Encodes the data to JSON"""
        timestamp = str(datetime.now())

        data = edict({"devices_count": devices_count,
                      "timestamp": timestamp, "area": PHYSICAL_AREA, "sensor_type": sensor_type})

        json_data = json.dumps(data)  # Encode to JSON
        return json_data
