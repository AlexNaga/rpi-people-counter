#!/bin/bash

INTERFACE="wlan0mon"

# Stop monitor mode
sudo airmon-ng stop "{$INTERFACE}"

# Restart DHCP service for WiFi interface
sudo dhclient $INTERFACE
