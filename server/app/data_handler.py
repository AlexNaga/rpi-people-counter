from bson.json_util import dumps, loads


class DataHandler:
    @staticmethod
    def from_json(json_data):
        """Decode the data from JSON"""
        return loads(json_data)  # Decode JSON data

    @staticmethod
    def to_json(data):
        """Encodes the data to JSON"""
        return dumps(data)  # Encode to JSON

    @staticmethod
    def is_device_found(devices_count):
        """Checks if any device found"""
        return devices_count > 0
