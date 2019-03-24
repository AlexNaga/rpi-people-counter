from data_handler import DataHandler
from scanner import Scanner
from datetime import datetime
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

# The location for this device
PHYSICAL_AREA = config.get("DEFAULT", "PHYSICAL_AREA")
DEVICE_ID = config.get("DEFAULT", "DEVICE_ID")

data_handler = DataHandler(PHYSICAL_AREA, DEVICE_ID)


def send_data(devices):
    """Sends the data to the MQTT broker"""
    json_data = data_handler.to_json(devices)
    data_handler.send_data(json_data)


def is_device_found(devices):
    """Checks if any device found"""
    return len(devices) > 0


def main():
    scanner = Scanner()
    scanner.start_bt()

    while True:
        bt_devices = scanner.find_bt_devices()

        time = datetime.now().strftime("%H:%M:%S")
        print("%s - %d devices found" % (time, len(bt_devices)))

        if not is_device_found(bt_devices):
            continue  # If no devices found, don't send the data

        send_data(bt_devices)


if __name__ == "__main__":
    main()
