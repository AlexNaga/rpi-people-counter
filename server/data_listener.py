from data_handler import DataHandler
from db_handler import DatabaseHandler
import paho.mqtt.client as mqtt
import configparser

config = configparser.ConfigParser()
config.read("config/config.ini")

# The location to receive data from
PHYSICAL_AREA = config.get("DEFAULT", "PHYSICAL_AREA")

MQTT_SERVER = config.get("DEFAULT", "MQTT_SERVER")
MQTT_PORT = config.getint("DEFAULT", "MQTT_PORT")


class DataListener:
    def __init__(self, physical_area):
        self.physical_area = physical_area

        # Config the MQTT client
        self.mqttc = mqtt.Client()

        # Connect to the MQTT broker
        self.mqttc.connect(MQTT_SERVER, MQTT_PORT)

        self.data_handler = DataHandler()
        self.db_handler = DatabaseHandler()

    def start(self):
        """Listens for data from the MQTT broker"""
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_message = self.on_message
        self.mqttc.loop_forever()  # Blocking loop to the broker

    def on_connect(self, client, userdata, flags, rc):
        """Event handler for MQTT connection"""
        print("Connected to the broker with status code "+str(rc))
        client.subscribe(self.physical_area + "/+")

    def on_message(self, client, userdata, msg):
        """Event handler for MQTT message"""
        payload = msg.payload.decode("utf-8")
        data = self.data_handler.from_json(payload)

        devices_count = data["devices_count"]
        devices_found = self.data_handler.is_device_found(devices_count)

        # Only save to db if devices found
        if devices_found:
            self.db_handler.add(data)

        # Send data to client here through Server-sent event


if __name__ == "__main__":
    data_listener = DataListener(PHYSICAL_AREA)
    data_listener.start()
