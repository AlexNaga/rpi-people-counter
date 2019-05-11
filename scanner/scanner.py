import bluetooth
from wifi.wifi import Wifi
import subprocess
import sys
import threading
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
        try:
            bt_devices_count = len(bluetooth.discover_devices(
                duration=BT_SCAN_DURATION))
            return bt_devices_count
        except Exception as e:
            print("Error: Could not access BT adapter.")
            print(e)
            sys.exit(1)

    def count_wifi_devices(self):
        """Scans for nearby WiFi devices"""
        try:
            self.start_timer(WIFI_SCAN_DURATION)
            wifi_devices_count = wifi.discover_devices(WIFI_SCAN_DURATION)
            self.stop_timer()
            return wifi_devices_count
        except Exception as e:
            print("Error: Could not access WiFi adapter.")
            print(e)
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

    def start_timer(self, scan_duration):
        """Starts the timer"""
        self.t = threading.Thread(target=self.show_timer,
                                  args=(scan_duration,))
        self.t.daemon = True
        self.t.start()  # Start countdown
        self.timestamp_start = time.time()  # Start run-timer

    def stop_timer(self):
        """Exits the timer"""
        self.t.join()  # Stop countdown
        timestamp_end = time.time()  # Stop run-timer
        durationInSec = timestamp_end - self.timestamp_start
        print("%.2f sec | WiFi" % durationInSec)

    def show_timer(self, timeleft):
        """Shows a countdown timer"""
        total = int(timeleft) * 10
        for i in range(total):
            sys.stdout.write("\r")
            timeleft_string = "%ds left" % int((total - i + 1) / 10)
            if (total - i + 1) > 600:
                timeleft_string = "%dmin %ds left" % (
                    int((total - i + 1) / 600), int((total - i + 1) / 10 % 60))
            sys.stdout.write("[%-50s] %d%% %15s" %
                             ("=" * int(50.5 * i / total), 101 * i / total, timeleft_string))
            sys.stdout.flush()
            time.sleep(0.1)
        print("")
