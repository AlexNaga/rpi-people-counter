from .data_handler import DataHandler
from .db_handler import DatabaseHandler
from app import mqtt
import configparser

config = configparser.ConfigParser()
config.read("config/config.ini")

# The location to receive data from
PHYSICAL_AREA = config.get("DEFAULT", "PHYSICAL_AREA")

data_handler = DataHandler()
db_handler = DatabaseHandler()


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    """Event handler for MQTT connection"""
    print("Connected to the broker with status code " + str(rc))
    mqtt.subscribe(PHYSICAL_AREA + "/+")


@mqtt.on_message()
def handle_mqtt_message(client, userdata, msg):
    """Event handler for MQTT message"""
    data = dict(
        topic=msg.topic,
        payload=msg.payload.decode()
    )

    print(data)

    # payload = msg.payload.decode("utf-8")
    # data = data_handler.from_json(payload)

    # Publish the data to the Redis database
    # red.publish("event", payload)

    # Send the data to client as Server-sent event
    print("a")
    sse.publish({"message": "Hello!3"}, type='greeting')
    print("b")

    devices_count = data["devices_count"]
    devices_found = data_handler.is_device_found(devices_count)

    # Only save to db if devices found
    if devices_found:
        db_handler.add(data)
