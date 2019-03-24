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

    def get_from_db(self):
        # self.collection.find({"time": {$gte: new Date(ISODate().getTime() - 1000 * 60 * 60)}})
        # x = self.collection.find({}).limit(1)

        import pprint
        x = self.collection.find({"device_id": "94:65:2D:D8:BB:C6"})


        for device in x:
            
            for i in x:
                print(i)
                pprint.pprint(x)
