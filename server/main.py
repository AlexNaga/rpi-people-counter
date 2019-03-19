from data_listener import DataListener
from db_handler import DatabaseHandler
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

PHYSICAL_AREA = config.get("DEFAULT", "PHYSICAL_AREA") # The location to receive data from


def main():
    while True:
        data_listener = DataListener(PHYSICAL_AREA)
        data_listener.start()


if __name__ == "__main__":
    main()