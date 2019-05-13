from data_handler import DataHandler
from scanner import Scanner
from datetime import datetime
from queue import Queue
from threading import Thread
import sys


def printStats(devices_count, sensor_type):
    time = datetime.now().strftime("%H:%M:%S")
    print("%s | %d {:>4} devices found.".format(
        sensor_type) % (time, devices_count))


def queueScans(scanner):
    jobs = Queue()
    threads_list = list()

    t1 = Thread(target=lambda q: q.put(
        scanner.count_bt_devices()), args=(jobs,))
    t1.daemon = True  # Kill thread on exit
    t1.start()
    threads_list.append(t1)

    t2 = Thread(target=lambda q: q.put(
        scanner.count_wifi_devices()), args=(jobs,))
    t2.daemon = True  # Kill thread on exit
    t2.start()
    threads_list.append(t2)

    # Join threads
    for t in threads_list:
        t.join()
        # t.keepRunning = False

    scan_results = []

    # Get return values from threads
    while not jobs.empty():
        result = jobs.get()
        scan_results.append(result)
    return scan_results


def main():
    scanner = Scanner()
    data_handler = DataHandler()

    while True:
        try:
            data = queueScans(scanner)
            bt_devices_count = data[0]
            wifi_devices_count = data[1]

            sensor_type = "bt"
            printStats(bt_devices_count, sensor_type)
            # data_handler.send_data(bt_devices_count, sensor_type)
            data_handler.save_data(bt_devices_count, sensor_type)

            sensor_type = "wifi"
            printStats(wifi_devices_count, sensor_type)
            # data_handler.send_data(wifi_devices_count, sensor_type)
            data_handler.save_data(wifi_devices_count, sensor_type)

        except (KeyboardInterrupt, SystemExit):
            sys.exit()


if __name__ == "__main__":
    main()
