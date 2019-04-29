import bluetooth
from wifi.wifi import Wifi
import time
import subprocess
import sys
import configparser
config = configparser.ConfigParser()
config.read("config/config.ini")

BT_SCAN_DURATION = config.getint("DEFAULT", "BT_SCAN_DURATION_IN_SEC")
WIFI_SCAN_DURATION = config.getint("DEFAULT", "WIFI_SCAN_DURATION_IN_SEC")
WIFI_ADAPTER = config.get("DEFAULT", "WIFI_ADAPTER")

wifi = Wifi(WIFI_ADAPTER)


class Scanner:
    def count_bt_devices(self):
        """Scans for nearby Bluetooth devices"""
        try:
            timestamp_start = time.time()  # Start timer
            bt_devices_count = len(bluetooth.discover_devices(
                duration=BT_SCAN_DURATION))
            timestamp_end = time.time()  # Stop timer
            durationInSec = timestamp_end - timestamp_start
            print("%.2f sec | BT" % durationInSec)
            return bt_devices_count
        except Exception as e:
            print("Error: Could not access BT adapter.")
            sys.exit(1)

    def count_wifi_devices(self):
        """Scans for nearby WiFi devices"""
        try:

            timestamp_start = time.time()  # Start timer
            wifi_devices_count = wifi.discover_devices(WIFI_SCAN_DURATION)
            timestamp_end = time.time()  # Stop timer
            durationInSec = timestamp_end - timestamp_start
            print("%.2f sec | WiFi" % durationInSec)
            return wifi_devices_count
        except Exception:
            print("Error: Could not access WiFi adapter.")
            sys.exit(1)

    def start_monitor_mode(self):
        """Starts the WiFi monitor mode"""
        try:
            subprocess.check_output(["./scripts/start_monitor_mode.sh"])
        except subprocess.CalledProcessError:
            print("Error: Could not start the monitor mode.")

    def stop_monitor_mode(self):
        """Exits the WiFi monitor mode"""
        try:
            subprocess.check_output(["./scripts/stop_monitor_mode.sh"])
        except subprocess.CalledProcessError:
            print("Error: Could not stop the monitor mode.")
