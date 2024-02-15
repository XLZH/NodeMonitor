#!/bin/bash

# 根据运行时参数启动不同的服务
if [ "$1" == "client" ]; then
    python monitor_client.py
elif [ "$1" == "server" ]; then
    python monitor_server.py
else
    echo "[Error] Invalid service ($1) is provided. Please specify 'client' or 'server'!"
fi
