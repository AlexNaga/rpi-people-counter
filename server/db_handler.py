from easydict import EasyDict as edict
from pymongo import MongoClient
import configparser

config = configparser.ConfigParser()
config.read("config/config.ini")

MONGODB_SERVER = config.get("DEFAULT", "MONGODB_SERVER")
MONGODB_PORT = config.getint("DEFAULT", "MONGODB_PORT")


class DatabaseHandler():
    def __init__(self):
        client = MongoClient(MONGODB_SERVER, MONGODB_PORT)
        db = client.sensor_db
        self.collection = db.sensor_collection

    def add(self, data):
        """Adds data to the db"""
        self.collection.insert(data)

    def get_all(self):
        """Gets all data from the db"""
        all_bt = self.get_all_bt()
        all_wifi = self.get_all_wifi()

        data = edict({"bt_devices": all_bt,
                      "wifi_devices": all_wifi})
        return data

    def get_all_bt(self):
        """Gets all Bluetooth data from the db"""
        return list(self.collection.find({"sensor_type": "bt"}, {"_id": False}))  # Return a list

    def get_all_wifi(self):
        """Gets all Wifi data from the db"""
        return list(self.collection.find({"sensor_type": "wifi"}, {"_id": False}))  # Return a list

    def get_latest(self):
        """Gets the lastest entry from the db"""
        latest_bt = self.get_latest_bt()
        latest_wifi = self.get_latest_wifi()
        return [latest_bt, latest_wifi]  # Return a list

    def get_latest_bt(self):
        """Gets the lastest Bluetooth entry from the db"""
        return self.collection.find({"sensor_type": "bt"}, {"_id": False}).sort(
            [("timestamp", -1)]).limit(1)[0]

    def get_latest_wifi(self):
        """Gets the lastest WiFi entry from the db"""
        return self.collection.find({"sensor_type": "wifi"}, {"_id": False}).sort(
            [("timestamp", -1)]).limit(1)[0]
