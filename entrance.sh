#!/bin/sh

# 根据运行时参数启动不同的服务
if [ "$1" == "client" ]; then
    python monitor_client.py
elif [ "$1" == "server" ]; then
    python monitor_server.py
else
    echo "[Error] Please specify the command of 'client' or 'server'!"
fi
