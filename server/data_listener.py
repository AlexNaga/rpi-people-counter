import json
import paho.mqtt.client as mqtt
from datetime import datetime

class DataListener:
    def __init__(self, physical_area, mqtt_server, mqtt_port):
        self.physical_area = physical_area

        # Config the MQTT client
        self.mqttc = mqtt.Client()

        # Connect to the MQTT broker
        self.mqttc.connect(mqtt_server, mqtt_port)

    def start(self):
        """Listens for data from the MQTT broker"""
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_message = self.on_message
        self.mqttc.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        """Event handler for MQTT connection"""
        print("Connected to the broker with status code "+str(rc))
        client.subscribe(self.physical_area + "/+")

    def on_message(self, client, userdata, msg):
        """Event handler for MQTT message"""
        time = datetime.now().strftime("%H:%M:%S")
        print("%s %s %s" % (time, msg.topic, msg.payload))

    def from_json(self, json_data):
        """Decode the data from JSON"""
        data = json.loads(json_data) # Decode JSON data
        return data
