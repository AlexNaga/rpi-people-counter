from data_handler import DataHandler
from scanner import Scanner
from datetime import datetime

# Config
PHYSICAL_AREA = "lnu/campus/classroom_0"  # The location for this device
DEVICE_ID = "rpi0w_0"
MQTT_SERVER = "192.168.10.235"
MQTT_PORT = 1883

data_handler = DataHandler(
    PHYSICAL_AREA, DEVICE_ID, MQTT_SERVER, MQTT_PORT)


def send_data(devices):
    json_data = data_handler.to_json(devices)
    data_handler.send_data(json_data)


def is_no_device_found(devices):
    """Checks if any Bluetooth device found"""
    return len(devices) < 1


def main():
    while True:
        scanner = Scanner()
        bt_devices = scanner.find_bt_devices()

        time = datetime.now().strftime("%H:%M:%S")
        print("Found %d devices - %s" % (len(bt_devices), time))

        if is_no_device_found(bt_devices):
            continue  # Don't send the data

        send_data(bt_devices)


if __name__ == "__main__":
    main()
