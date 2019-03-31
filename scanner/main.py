from data_handler import DataHandler
from scanner import Scanner
from datetime import datetime


def printStats(devices_count):
    time = datetime.now().strftime("%H:%M:%S")
    print("%s - %d devices found" % (time, devices_count))


def main():
    scanner = Scanner()
    scanner.start_bt()
    data_handler = DataHandler()

    while True:
        bt_devices_count = scanner.count_bt_devices()
        printStats(bt_devices_count)

        sensor_type = "bt"
        data_handler.send_data(bt_devices_count, sensor_type)

        #     sensor_type = "wifi"
        #     send_data(bt_devices_count, sensor_type)


if __name__ == "__main__":
    main()
