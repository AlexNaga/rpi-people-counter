#!/bin/bash

# Remember to start the MQTT server (mosquitto).

# Start the scanner
echo "Starting scanner..."
cd scanner
pipenv run python main.py