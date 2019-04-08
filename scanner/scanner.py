import bluetooth
import subprocess
import configparser
import time

config = configparser.ConfigParser()
config.read("config/config.ini")

SECONDS_BETWEEN_BT_SCANS = config.getint("DEFAULT", "SECONDS_BETWEEN_BT_SCANS")


class Scanner:
    def count_bt_devices(self):
        """Scans for nearby Bluetooth devices"""
        bt_devices_count = len(bluetooth.discover_devices(
            duration=SECONDS_BETWEEN_BT_SCANS))
        return bt_devices_count

    def count_wifi_devices(self):
        """Scans for nearby WiFi devices"""
        # TODO: Implement this
        print("Starting monitor mode")
        self.start_monitor_mode()

        print("Sleeping 10 seconds...")
        time.sleep(10)
        
        self.stop_monitor_mode()
        print("Exited monitor mode")
        return 0

    def start_monitor_mode(self):
        """Starts the WiFi monitor mode"""
        # TODO: Implement this
        try:
            subprocess.check_output(["./scripts/start_monitor_mode.sh"])
        except subprocess.CalledProcessError:
            print("Error: Couldn't start the monitor mode.")

    def stop_monitor_mode(self):
        """Exits the WiFi monitor mode"""
        # TODO: Implement this
        try:
            subprocess.check_output(["./scripts/stop_monitor_mode.sh"])
        except subprocess.CalledProcessError:
            print("Error: Couldn't stop the monitor mode.")
