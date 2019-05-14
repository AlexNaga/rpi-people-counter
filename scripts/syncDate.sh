#!/bin/bash

ssh root@pipecounter-scanner.local date -s @`( date -u +"%s" )`
