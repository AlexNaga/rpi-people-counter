from db_handler import DatabaseHandler
from data_handler import DataHandler
import tornado.ioloop
import tornado.web
import tornado.websocket
import configparser

config = configparser.ConfigParser()
config.read("config/config.ini")

WS_SERVER = config.get("DEFAULT", "WS_SERVER")
WS_PORT = config.getint("DEFAULT", "WS_PORT")


class DataSender(tornado.web.RequestHandler):
    def get(self):
        """Sends the data to the client"""
        db_handler = DatabaseHandler()
        data_handler = DataHandler()
        data = db_handler.get_all()
        json_data = data_handler.to_json(data)
        self.write(json_data)

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        self.write_message(u"You said: " + message)

    def check_origin(self, origin):
        return True
