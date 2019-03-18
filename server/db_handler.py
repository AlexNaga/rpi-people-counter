from pymongo import MongoClient

class DatabaseHandler():
    def __init__(self, url, port):
        self.client = client = MongoClient(url, port)
        db = self.client.sensor_data
        collection = db.sensor_collection

