from data_listener import DataListener
from db_handler import DatabaseHandler

# MQTT config
PHYSICAL_AREA = "lnu/campus"  # The location to receive data from
MQTT_SERVER = "192.168.10.235"
MQTT_PORT = 1883

# MongoDB config
MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017

def main():
    while True:
        # db_handler = DatabaseHandler(MONGODB_SERVER, MONGODB_PORT)

        data_listener = DataListener(PHYSICAL_AREA, MQTT_SERVER, MQTT_PORT)
        data_listener.start()

if __name__ == "__main__":
    main()
