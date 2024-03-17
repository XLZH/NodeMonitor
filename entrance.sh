#!/bin/sh

# Params:
#   $1: client or server
#   $2: IP, e.g. 192.168.123.123
#   $3: SOCKET_PORT, e.g. 12306
#   $4: API_PORT, e.g. 12307
#   $5: DISKS, e.g. /hracond2:/p300:/hraupload

if [ "$SERVICE" == "client" ]; then
    echo "[*] start the service of monitor client ..."
    echo "[*] the server to be connected is $IP:$SOCKET_PORT ..."
    echo "[*] the mounted disks for the node are $DISKS ..."
    python monitor_client.py $IP $SOCKET_PORT $DISKS

elif [ "$SERVICE" == "server" ]; then
    echo "[*] start the service of monitor server ..."
    echo "[*] the $IP:$SOCKET_PORT is ready for connections from clients ..."
    python monitor_server.py $IP $SOCKET_PORT

elif [ "$SERVICE" == "api" ]; then
    echo "[*] start the service of monitor api ..."
    echo "[*] the $IP:$API_PORT is ready for connections from user ..."
    python monitor_api.py $IP $API_PORT

else
    echo "[Error] Please specify the entrance command of 'client', 'server' or 'api'!"
fi
