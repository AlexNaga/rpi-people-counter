import json
from datetime import datetime
import paho.mqtt.client as mqtt
from easydict import EasyDict as edict

class DataHandler:
    def __init__(self, physical_area, device_id, mqtt_server, mqtt_port):
        self.physical_area = physical_area

        # Config the MQTT client
        self.mqttc = mqtt.Client(client_id=device_id)

        # Connect to the MQTT broker
        self.mqttc.connect(mqtt_server, mqtt_port)


    def send_data(self, data):
        """Sends the data to the MQTT broker"""
        self.mqttc.publish(self.physical_area, data)

    def to_json(self, devices):
        """Encodes the data to JSON"""
        data = []

        for device_id in devices:
            timestamp = str(datetime.now())
            obj = edict({"device_id":device_id, "time":timestamp})
            data.append(obj)

        json_data = json.dumps(data)  # Encode to JSON
        return json_data
