from data_handler import DataHandler
from scanner import Scanner
from datetime import datetime
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

PHYSICAL_AREA = config.get("DEFAULT", "PHYSICAL_AREA") # The location for this device
DEVICE_ID = config.get("DEFAULT", "DEVICE_ID")
MQTT_SERVER = config.get("DEFAULT", "MQTT_SERVER")
MQTT_PORT = config.getint("DEFAULT", "MQTT_PORT")

data_handler = DataHandler(
    PHYSICAL_AREA, DEVICE_ID, MQTT_SERVER, MQTT_PORT)


def send_data(devices):
    """Sends the data to the MQTT broker"""
    json_data = data_handler.to_json(devices)
    data_handler.send_data(json_data)


def is_device_found(devices):
    """Checks if any device found"""
    return len(devices) > 0


def main():
    while True:
        scanner = Scanner()
        bt_devices = scanner.find_bt_devices()
        device_not_found = is_device_found(bt_devices) == False

        time = datetime.now().strftime("%H:%M:%S")
        print("%s - %d devices found" % (time, len(bt_devices)))

        if device_not_found:
            continue  # Don't send the data

        send_data(bt_devices)


if __name__ == "__main__":
    main()
