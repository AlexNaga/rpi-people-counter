from data_sender import DataSender
from datetime import datetime
from easydict import EasyDict as edict
import configparser
import csv
import json

config = configparser.ConfigParser()
config.read("config/config.ini")

# The location for this device
PHYSICAL_AREA = config.get("DEFAULT", "PHYSICAL_AREA")


class DataHandler:
    # def __init__(self):
        # self.data_sender = DataSender()

    # def send_data(self, devices_count, sensor_type):
    #     """Sends the data to the MQTT broker"""
    #     json_data = self.to_json(devices_count, sensor_type)
    #     self.data_sender.send_data(json_data)

    def save_data(self, devices_count, sensor_type):
        """Saves the data locally"""
        dateFormat = "%Y-%m-%d %H:%M:%S"  # 2019-04-01 16:17:26
        timestamp = str(datetime.now().strftime(dateFormat))
        fields = [timestamp, sensor_type, devices_count, PHYSICAL_AREA]

        # Append to CSV file
        with open(r"./data/local_data.csv", "a") as f:
            writer = csv.writer(f)
            writer.writerow(fields)

    def to_json(self, devices_count, sensor_type):
        """Encodes the data to JSON"""
        dateFormat = "%Y-%m-%d %H:%M:%S"  # 2019-04-01 16:17:26
        timestamp = str(datetime.now().strftime(dateFormat))

        data = edict({"devices_count": devices_count,
                      "timestamp": timestamp, "area": PHYSICAL_AREA, "sensor_type": sensor_type})

        json_data = json.dumps(data)  # Encode to JSON
        return json_data
