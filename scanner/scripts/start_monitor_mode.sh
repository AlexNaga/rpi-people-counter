#!/bin/bash

# To check for interfaces: sudo iwconfig
# To check for interfaces: sudo ip a
# To check for interfaces: sudo iw dev

# INTERFACE="wlan0"
INTERFACE="wlp0s20u2"

# Start monitor mode
sudo airmon-ng start $INTERFACE