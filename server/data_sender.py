from data_handler import DataHandler
import tornado.ioloop
import tornado.web
import tornado.websocket
import configparser

config = configparser.ConfigParser()
config.read("config/config.ini")

WS_SERVER = config.get("DEFAULT", "WS_SERVER")
WS_PORT = config.getint("DEFAULT", "WS_PORT")


class GetAll(tornado.web.RequestHandler):
    """Returns all the data to the client"""

    def initialize(self, db_handler):
        self.db_handler = db_handler

    def get(self):
        data = self.db_handler.get_all()
        json_data = DataHandler().to_json(data)
        self.write(json_data)

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")


class GetAllBt(tornado.web.RequestHandler):
    """Returns all the Bluetooth data to the client"""

    def initialize(self, db_handler):
        self.db_handler = db_handler

    def get(self):
        data = self.db_handler.get_all_bt()
        json_data = DataHandler().to_json(data)
        self.write(json_data)

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")


class GetAllWifi(tornado.web.RequestHandler):
    """Returns all the WiFi data to the client"""

    def initialize(self, db_handler):
        self.db_handler = db_handler

    def get(self):
        data = self.db_handler.get_all_wifi()
        json_data = DataHandler().to_json(data)
        self.write(json_data)

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")


class GetLatest(tornado.web.RequestHandler):
    """Returns the latest entry to the client"""

    def initialize(self, db_handler):
        self.db_handler = db_handler

    def get(self):
        data = self.db_handler.get_latest()
        json_data = DataHandler().to_json(data)
        self.write(json_data)

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")


class GetLatestBt(tornado.web.RequestHandler):
    """Returns the latest Bluetooth entry to the client"""

    def initialize(self, db_handler):
        self.db_handler = db_handler

    def get(self):
        data = self.db_handler.get_latest_bt()
        json_data = DataHandler().to_json(data)
        self.write(json_data)

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")


class GetLatestWifi(tornado.web.RequestHandler):
    """Returns the latest Bluetooth entry to the client"""

    def initialize(self, db_handler):
        self.db_handler = db_handler

    def get(self):
        data = self.db_handler.get_latest_wifi()
        json_data = DataHandler().to_json(data)
        self.write(json_data)

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    clients = []

    def open(self):
        WebSocketHandler.clients.append(self)

    def on_close(self):
        WebSocketHandler.clients.remove(self)

    def on_message(self, message):
        self.send_data(message)  # Forward the data to the clients

    def check_origin(self, origin):
        return True

    @classmethod
    def send_data(cls, data):
        for client in cls.clients:
            client.write_message(data)
