from pymongo import MongoClient
import configparser

config = configparser.ConfigParser()
config.read("config/config.ini")

MONGODB_SERVER = config.get("DEFAULT", "MONGODB_SERVER")
MONGODB_PORT = config.getint("DEFAULT", "MONGODB_PORT")


class DatabaseHandler():
    def __init__(self):
        client = MongoClient(MONGODB_SERVER, MONGODB_PORT)
        db = client.sensor_db0
        self.collection = db.sensor_collection0

    def add_to_db(self, data):
        """Adds data to the db"""
        print("Add data to db")
        self.collection.insert(data)

    def get_from_db(self):
        # self.collection.find({"time": {$gte: new Date(ISODate().getTime() - 1000 * 60 * 60)}})
        # x = self.collection.find({}).limit(1)
        print("TODO: get_from_db")
