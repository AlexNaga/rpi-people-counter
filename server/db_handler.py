from pymongo import MongoClient
import configparser
from datetime import datetime

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
        return list(self.collection.find({}, {"_id": False}))  # Return a list
