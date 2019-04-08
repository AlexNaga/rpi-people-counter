#!/bin/bash

# Stop monitor mode
airmon-ng stop wlan0mon

# Restart DHCP service
dhclient wlan0