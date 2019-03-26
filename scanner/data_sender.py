import paho.mqtt.client as mqtt
import configparser

config = configparser.ConfigParser()
config.read("config/config.ini")

PHYSICAL_AREA = config.get("DEFAULT", "PHYSICAL_AREA")
SENSOR_ID = config.get("DEFAULT", "SENSOR_ID")

MQTT_SERVER = config.get("DEFAULT", "MQTT_SERVER")
MQTT_PORT = config.getint("DEFAULT", "MQTT_PORT")


class DataSender:
    def __init__(self):
        self.physical_area = PHYSICAL_AREA

        # Config the MQTT client
        self.mqttc = mqtt.Client(client_id=SENSOR_ID)

        # Connect to the MQTT broker
        self.mqttc.connect(MQTT_SERVER, MQTT_PORT)

    def send_data(self, data):
        """Sends the data to the MQTT broker"""
        self.mqttc.publish(self.physical_area, data)
