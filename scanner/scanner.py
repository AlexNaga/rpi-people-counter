import bluetooth
from wifi.wifi import Wifi
import subprocess
import time
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
        bt_devices_count = len(bluetooth.discover_devices(
            duration=BT_SCAN_DURATION))
        return bt_devices_count

    def count_wifi_devices(self):
        """Scans for nearby WiFi devices"""
        wifi_devices_count = wifi.discover_devices(WIFI_SCAN_DURATION)
        return wifi_devices_count

    def start_monitor_mode(self):
        """Starts the WiFi monitor mode"""
        try:
            subprocess.check_output(["./scripts/start_monitor_mode.sh"])
        except subprocess.CalledProcessError:
            print("Error: Couldn't start the monitor mode.")

    def stop_monitor_mode(self):
        """Exits the WiFi monitor mode"""
        try:
            subprocess.check_output(["./scripts/stop_monitor_mode.sh"])
        except subprocess.CalledProcessError:
            print("Error: Couldn't stop the monitor mode.")
