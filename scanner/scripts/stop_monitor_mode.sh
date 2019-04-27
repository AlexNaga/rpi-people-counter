#!/bin/bash

INTERFACE="wlan0"
# INTERFACE="wlp0s20u2"

# Stop monitor mode
sudo airmon-ng stop "{$INTERFACE}mon"

# Restart DHCP service
sudo dhclient $INTERFACE
