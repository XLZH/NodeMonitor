#!/bin/sh

# Params:
#   $1: client or server
#   $2: SERVER_ADDRESS, e.g. 192.168.123.123
#   $3: SERVER_PORT, e.g. 12345

if [ "$SERVICE" == "client" ]; then
    python monitor_client.py $SERVER_IP $SERVER_PORT
elif [ "$SERVICE" == "server" ]; then
    python monitor_server.py $SERVER_PORT
else
    echo "[Error] Please specify the command of 'client' or 'server'!"
fi
