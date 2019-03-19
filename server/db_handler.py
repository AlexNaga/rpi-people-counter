from pymongo import MongoClient
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

MONGODB_SERVER = config.get("DEFAULT", "MONGODB_SERVER")
MONGODB_PORT = config.getint("DEFAULT", "MONGODB_PORT")

class DatabaseHandler():
    def __init__(self):
        client = MongoClient(MONGODB_SERVER, MONGODB_PORT)
        db = client.sensor_db0
        self.collection = db.sensor_collection0


    def add_to_db(self, devices):
        print("Add device to db")
        self.collection.insert_many(devices)