import json
from datetime import datetime
from easydict import EasyDict as edict

class DataHandler:
    def add_area_to_data(self, data, area):
        result = []

        for log in data:
            obj = edict({"device_id":log["device_id"], "time":log["time"], "area":area})
            result.append(obj)
    
        return result

    def from_json(self, json_data):
        """Decode the data from JSON"""
        data = json.loads(json_data) # Decode JSON data
        return data