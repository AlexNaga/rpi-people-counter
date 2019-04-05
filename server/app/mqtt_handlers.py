from app import mqtt
import configparser

config = configparser.ConfigParser()
config.read("config/config.ini")

# The location to receive data from
PHYSICAL_AREA = config.get("DEFAULT", "PHYSICAL_AREA")


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe(PHYSICAL_AREA + "/+")


@mqtt.on_message()
def handle_mqtt_message(client, userdata, msg):
    data = dict(
        topic=msg.topic,
        payload=msg.payload.decode()
    )

    print(data)
