import bluetooth
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

SECONDS_BETWEEN_BT_SCANS = config.getint("DEFAULT", "SECONDS_BETWEEN_BT_SCANS")


class Scanner:
    def find_bt_devices(self):
        """Scans for nearby Bluetooth devices"""
        return bluetooth.discover_devices(duration=SECONDS_BETWEEN_BT_SCANS)

    def find_wifi_devices(self):
        """Scans for nearby WiFi devices"""
        # TODO: Implement this
        return None
