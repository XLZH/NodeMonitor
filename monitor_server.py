#!/usr/bin/python3
# -*- coding: utf-8 -*-

# *************************************************************************
#    > File Name: monitor_server.py
#    > Author: xlzh
#    > Mail: xiaolongzhang2015@163.com
#    > Created Time: 2024年02月15日 星期四 09时54分12秒
# *************************************************************************

import socket
import json
import asyncio
import threading
from tortoise import Tortoise, exceptions
from settings import *
from models.model import NodeModel


MAX_CONNECT = 32  # maximum number of parallel connection


# start the server socket and listen for connection
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_LISTEN, SERVER_PORT))
server_socket.listen(MAX_CONNECT)


async def handle_connection(client_socket):
    info_dict = json.loads(client_socket.recv(1024).decode('utf-8'))
    host_name = info_dict.pop('host')

    try:
        await NodeModel.get(host=host_name)
        await NodeModel.filter(host=host_name).update(**info_dict)

    except exceptions.DoesNotExist:
        info_dict['host'] = host_name
        await NodeModel.create(**info_dict)

    client_socket.close()


def main():
    asyncio.run(Tortoise.init(TORTOISE))  # connect to the sqlite database

    while True:
        try:
            client_socket, client_address = server_socket.accept()
            client_handle = threading.Thread(target=asyncio.run, args=(handle_connection(client_socket),))
            client_handle.start()

        except KeyboardInterrupt:
            server_socket.close()
            asyncio.run(Tortoise.close_connections())
            raise


if __name__ == '__main__':
    main()
