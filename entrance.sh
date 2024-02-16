#!/bin/sh

# Params:
#   $1: client or server
#   $2: IP, e.g. 192.168.123.123
#   $3: PORT, e.g. 12345

if [ "$SERVICE" == "client" ]; then
    echo "[*] start the service of monitor client ..."
    echo "[*] the server IP and PORT is set with $IP and $PORT ..."
    python monitor_client.py $IP $PORT

elif [ "$SERVICE" == "server" ]; then
    echo "[*] start the service of monitor server ..."
    echo "[*] the listen IP and PORT is set with $IP and $PORT ..."
    python monitor_server.py $IP $PORT

else
    echo "[Error] Please specify the entrance command of 'client' or 'server'!"
fi
