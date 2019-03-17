import bluetooth
from datetime import datetime
from time import sleep


def find_devices():
    """Scan for nearby Bluetooth devices"""
    return bluetooth.discover_devices(duration=2)


while True:
    nearby_devices = find_devices()
    print("Found %d devices" % len(nearby_devices))

    for mac_address in nearby_devices:
        date = datetime.now().strftime('%Y-%m-%d')
        hour = datetime.now().strftime('%H')
        print("%s - %s" % (mac_address, date))
