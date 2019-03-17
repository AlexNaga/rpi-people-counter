from datetime import datetime
from time import sleep
import bluetooth
import json
# import paho.mqtt.client as mqtt

physical_area = "room0"

# Config the MQTT client
# device_id = "rpi0w_0"
# mqttc = mqtt.Client(device_id)
# mqtt_server = "test.mosquitto.org"
# mqtt_port = 1883
# mqttc.connect(mqtt_server, mqtt_port)


def find_devices():
    """Scan for nearby Bluetooth devices"""
    return bluetooth.discover_devices(duration=2)


def to_json(data):
    json_data = {}

    # Loop through the MAC addresses
    for count, mac_address in enumerate(data):
        json_data[count] = mac_address

    return json_data


def send_data(data):
    data_out = json.dumps(data)  # encode to JSON
    # client.publish("topic/" + physical_area, "Hello world!");


while True:
    nearby_devices = find_devices()
    is_empty = len(nearby_devices) < 1

    time = datetime.now().strftime("%H:%M")
    print("Found %d devices - %s" % (len(nearby_devices), time))

    # If no devices found, don't send the data
    if is_empty:
        continue

    data = to_json(nearby_devices)

    print(data)
    send_data(data)

