import json
import paho.mqtt.client as mqtt


class DataHandler:
    def __init__(self, physical_area, device_id, mqtt_server, mqtt_port):
        self.physical_area = physical_area

        # Config the MQTT client
        self.mqttc = mqtt.Client(client_id=device_id)

        # Connect to the MQTT broker
        self.mqttc.connect(mqtt_server, mqtt_port)

    def send_data(self, data):
        """Sends the data to the MQTT broker"""
        print(data)
        self.mqttc.publish(self.physical_area, data)

    def to_json(self, devices):
        """Encodes the data to JSON"""
        data = {}

        # Loop through the devices
        for count, mac_address in enumerate(devices):
            data[count] = mac_address

        json_data = json.dumps(data)  # Encode to JSON
        return json_data
