import json
from datetime import datetime


class DataHandler:
    def from_json(self, json_data):
        """Decode the data from JSON"""
        return json.loads(json_data)  # Decode JSON data
