from data_handler import DataHandler
from scanner import Scanner
from datetime import datetime


def printStats(devices_count, sensor_type):
    time = datetime.now().strftime("%H:%M:%S")
    print("%s | %d {:>4} devices found.".format(
        sensor_type) % (time, devices_count))


def main():
    scanner = Scanner()
    data_handler = DataHandler()

    while True:
        # bt_devices_count = scanner.count_bt_devices()
        # wifi_devices_count = scanner.count_wifi_devices()
        
        from random import randint
        from time import sleep
        sleep(5)
        bt_devices_count = randint(2, 3)
        wifi_devices_count = randint(5, 6)

        sensor_type = "bt"
        printStats(bt_devices_count, sensor_type)
        data_handler.send_data(bt_devices_count, sensor_type)

        sensor_type = "wifi"
        printStats(wifi_devices_count, sensor_type)
        data_handler.send_data(wifi_devices_count, sensor_type)


if __name__ == "__main__":
    main()
