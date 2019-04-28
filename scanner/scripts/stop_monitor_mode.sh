#!/bin/bash

INTERFACE="wlan1mon"

# Stop monitor mode
sudo airmon-ng stop "{$INTERFACE}"

# Restart DHCP service
sudo dhclient $INTERFACE
