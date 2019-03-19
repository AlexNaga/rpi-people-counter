import paho.mqtt.client as mqtt
from datetime import datetime
from data_handler import DataHandler
from db_handler import DatabaseHandler
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

MQTT_SERVER = config.get("DEFAULT", "MQTT_SERVER")
MQTT_PORT = config.getint("DEFAULT", "MQTT_PORT")


class DataListener:
    def __init__(self, physical_area):
        self.physical_area = physical_area

        # Config the MQTT client
        self.mqttc = mqtt.Client()

        # Connect to the MQTT broker
        self.mqttc.connect(MQTT_SERVER, MQTT_PORT)


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

        payload = msg.payload.decode("utf-8")

        data_handler = DataHandler()
        obj = data_handler.from_json(payload)
        devices = data_handler.add_area_to_data(obj, msg.topic)

        db_handler = DatabaseHandler()
        db_handler.add_to_db(devices)

        # TODO: Create a post (a nice formatted JSON) and add this post to the db
