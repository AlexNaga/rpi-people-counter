from data_listener import DataListener
from db_handler import DatabaseHandler
import configparser

config = configparser.ConfigParser()
config.read("config/config.ini")

# The location to receive data from
PHYSICAL_AREA = config.get("DEFAULT", "PHYSICAL_AREA")


def main():
    data_listener = DataListener(PHYSICAL_AREA)
    data_listener.start()

if __name__ == "__main__":
    main()
    # db_handler = DatabaseHandler()
    # db_handler.get_from_db()
