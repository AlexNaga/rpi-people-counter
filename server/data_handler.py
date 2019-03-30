from bson.json_util import dumps, loads


class DataHandler:
    def from_json(self, json_data):
        """Decode the data from JSON"""
        return loads(json_data)  # Decode JSON data

    def to_json(self, data):
        """Encodes the data to JSON"""
        return dumps(data)  # Encode to JSON
