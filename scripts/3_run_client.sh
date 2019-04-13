#!/bin/bash

# Remember to start the MongoDB database (mongod) and the MQTT server (mosquitto).

# Start the data listener
cd client
npm run watch
# node browserSync.js
