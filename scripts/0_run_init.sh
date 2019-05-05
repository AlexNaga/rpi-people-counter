#!/bin/bash

# Change this if needed
WIFI_INTERFACE="wlan0"

# Start WiFI monitor mode
sudo airmon-ng start $WIFI_INTERFACE

# Start the Bluetooth device
sudo btmgmt power on

# Start the MongoDB database
mongod &

# Start the Redis server
redis-server &

# Start the MQTT server
mosquitto -d