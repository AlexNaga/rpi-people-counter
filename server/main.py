from data_listener import DataListener
from data_sender import DataSender, WebSocketHandler
import tornado.ioloop
import tornado.web
import configparser

config = configparser.ConfigParser()
config.read("config/config.ini")

# The location to receive data from
PHYSICAL_AREA = config.get("DEFAULT", "PHYSICAL_AREA")

WS_SERVER = config.get("DEFAULT", "WS_SERVER")
WS_PORT = config.getint("DEFAULT", "WS_PORT")


def make_app():
    return tornado.web.Application([
        (r"/data", DataSender),
        (r"/ws", WebSocketHandler),
    ])


def main():
    data_listener = DataListener(PHYSICAL_AREA)
    data_listener.start()


if __name__ == "__main__":
    # main()
    # data_sender = DataSender()
    # data_sender.start()

    app = make_app()
    app.listen(WS_PORT)
    tornado.ioloop.IOLoop.current().start()
