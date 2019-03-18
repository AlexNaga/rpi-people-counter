from datetime import datetime
from time import sleep
import bluetooth
import json
import paho.mqtt.client as mqtt

# Config the location for this device
physical_area = "lnu/campus/classroom_0"

# Config the MQTT client
device_id = "rpi0w_0"
mqttc = mqtt.Client(client_id=device_id)

# Connect to the MQTT broker
mqtt_server = "192.168.10.235"
mqtt_port = 1883
mqttc.connect(mqtt_server, mqtt_port)


def find_devices():
    """Scans for nearby Bluetooth devices"""
    return bluetooth.discover_devices(duration=2)


def to_json(devices):
    """Encodes the data to JSON"""
    data = {}

    # Loop through the devices
    for count, mac_address in enumerate(devices):
        data[count] = mac_address

    json_data = json.dumps(data)  # Encode to JSON
    return json_data


def send_data(data):
    """Sends the data to the MQTT broker"""
    print(data)
    mqttc.publish(physical_area, data)


while True:
    nearby_devices = find_devices()
    print(nearby_devices)
    is_empty = len(nearby_devices) < 1

    time = datetime.now().strftime("%H:%M")
    print("Found %d devices - %s" % (len(nearby_devices), time))

    # If no devices found, don't send the data
    if is_empty:
        continue

    json_data = to_json(nearby_devices)
    send_data(json_data)
