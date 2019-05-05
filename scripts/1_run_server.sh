#!/bin/bash

# Remember to start the MongoDB database (mongod) and the MQTT server (mosquitto).

# Start the broker server
echo "Starting server..."
# cd server
cd ~/deploy-folder/server
pipenv run gunicorn run:gunicorn_app --workers=1 --worker-class gevent --bind localhost:8000