#!/bin/bash

# To check for interfaces: iwconfig

INTERFACE="wlan0"

# Start monitor mode
sudo airmon-ng start $INTERFACE

# Restart DHCP service for WiFi interface
sudo dhclient $INTERFACE