from flask_cors import CORS
from routes import data_api
from flask import Flask

app = Flask(__name__)
CORS(app)
app.register_blueprint(data_api)

if __name__ == "__main__":
    print("Starting the server.")
