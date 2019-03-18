from data_listener import DataListener

# Config
PHYSICAL_AREA = "lnu/campus"  # The location to receive data from
MQTT_SERVER = "192.168.10.235"
MQTT_PORT = 1883

def main():
    while True:
        data_listener = DataListener(PHYSICAL_AREA, MQTT_SERVER, MQTT_PORT)
        data_listener.start()

if __name__ == "__main__":
    main()
