from data_handler import DataHandler
from db_handler import DatabaseHandler
from easydict import EasyDict as edict
from flask import Blueprint

data_api = Blueprint('data_api', __name__)
db_handler = DatabaseHandler()


@data_api.route("/data/all")
def get_all():
    """Returns all the data to the client"""
    data = db_handler.get_all()
    json_data = DataHandler().to_json(data)
    return json_data


@data_api.route("/data/all/bt")
def get_all_bt():
    """Returns all the Bluetooth data to the client"""
    data = db_handler.get_all_bt()
    json_data = DataHandler().to_json(data)
    return json_data


@data_api.route("/data/all/wifi")
def get_all_wifi():
    """Returns all the WiFi data to the client"""
    data = db_handler.get_all_wifi()
    json_data = DataHandler().to_json(data)
    return json_data


@data_api.route("/data/latest")
def get_latest():
    """Returns the latest entry to the client"""
    data = db_handler.get_latest()
    json_data = DataHandler().to_json(data)
    return json_data


@data_api.route("/data/latest/bt")
def get_latest_bt():
    """Returns the latest Bluetooth entry to the client"""
    data = db_handler.get_latest_bt()
    json_data = DataHandler().to_json(data)
    return json_data


@data_api.route("/data/latest/wifi")
def get_latest_wifi():
    """Returns the latest WiFi entry to the client"""
    data = db_handler.get_latest_wifi()
    json_data = DataHandler().to_json(data)
    return json_data


@data_api.route("/data/stats")
def users():
    data = db_handler.get_all()
    bt_devices_count = len(data.bt_devices)
    wifi_devices_count = len(data.wifi_devices)
    total_devices_count = bt_devices_count + wifi_devices_count

    data_dict = edict({"total_devices_count": total_devices_count, "bt_devices_count": bt_devices_count,
                       "wifi_devices_count": wifi_devices_count})
    json_data = DataHandler().to_json(data_dict)
    return json_data
