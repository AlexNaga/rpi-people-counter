from wifi_scan.main import wifi_scan
import bluetooth
import subprocess
import configparser
import time

config = configparser.ConfigParser()
config.read("config/config.ini")

BT_SCAN_DURATION = config.getint("DEFAULT", "BT_SCAN_DURATION_IN_SEC")
WIFI_SCAN_DURATION = config.getint("DEFAULT", "WIFI_SCAN_DURATION_IN_SEC")
WIFI_ADAPTER = config.get("DEFAULT", "WIFI_ADAPTER")


class Scanner:
    def count_bt_devices(self):
        """Scans for nearby Bluetooth devices"""
        bt_devices_count = len(bluetooth.discover_devices(
            duration=BT_SCAN_DURATION))
        return bt_devices_count

    def count_wifi_devices(self):
        """Scans for nearby WiFi devices"""
        # TODO: Implement this

        wifi_devices_count = wifi_scan(WIFI_ADAPTER, WIFI_SCAN_DURATION)
        print(wifi_devices_count)
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
