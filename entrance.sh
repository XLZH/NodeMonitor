#!/bin/sh

# Params:
#   $1: client or server
#   $2: SERVER_ADDRESS, e.g. 192.168.123.123
#   $3: SERVER_PORT, e.g. 12345

if [ "$1" == "client" ]; then
    python monitor_client.py $2 $3
elif [ "$1" == "server" ]; then
    python monitor_server.py $3
else
    echo "[Error] Please specify the command of 'client' or 'server'!"
fi
