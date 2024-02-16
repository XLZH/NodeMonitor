#!/bin/sh

# Params:
#   $1: client or server
#   $2: IP, e.g. 192.168.123.123
#   $3: PORT, e.g. 12345

if [ "$SERVICE" == "client" ]; then
    echo "[*] start the service of monitor client ..."
    echo "[*] the server to be connected is $IP:$PORT ..."
    python monitor_client.py $IP $PORT

elif [ "$SERVICE" == "server" ]; then
    echo "[*] start the service of monitor server ..."
    echo "[*] the $IP:$PORT is ready for connections from clients ..."
    python monitor_server.py $IP $PORT

else
    echo "[Error] Please specify the entrance command of 'client' or 'server'!"
fi
