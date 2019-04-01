from data_listener import DataListener
from db_handler import DatabaseHandler
from data_sender import GetAll, GetAllBt, GetAllWifi, GetLatest, GetLatestBt, GetLatestWifi, WebSocketHandler
from tornado import ioloop, web
import configparser

config = configparser.ConfigParser()
config.read("config/config.ini")

WS_SERVER = config.get("DEFAULT", "WS_SERVER")
WS_PORT = config.getint("DEFAULT", "WS_PORT")


def make_app():
    db_handler = DatabaseHandler()

    return web.Application([
        (r"/data/all", GetAll, {"db_handler": db_handler}),
        (r"/data/all/bt", GetAllBt, {"db_handler": db_handler}),
        (r"/data/all/wifi", GetAllWifi, {"db_handler": db_handler}),

        (r"/data/latest", GetLatest, {"db_handler": db_handler}),
        (r"/data/latest/bt", GetLatestBt, {"db_handler": db_handler}),
        (r"/data/latest/wifi", GetLatestWifi, {"db_handler": db_handler}),

        (r"/ws", WebSocketHandler),
    ])


if __name__ == "__main__":
    print("Starting the server.")
    app = make_app()
    app.listen(WS_PORT)
    ioloop.IOLoop.current().start()
