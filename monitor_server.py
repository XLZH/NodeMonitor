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
import sys
import asyncio
from tortoise import Tortoise, exceptions
from settings import *
from models.model import NodeModel

MAX_CONNECT = 32  # maximum number of parallel connection


async def handle_connection(socket_reader, socket_writer):
    client_data = await socket_reader.read(1024)
    info_dict = json.loads(client_data.decode('utf-8'))
    print(info_dict)

    try:
        host_name = info_dict['host']
        await NodeModel.get(host=host_name)
        await NodeModel.filter(host=host_name).update(**info_dict)

    except exceptions.DoesNotExist:
        await NodeModel.create(**info_dict)

    socket_writer.close()


async def main():
    args = sys.argv
    if len(args) != 3:
        sys.stderr.write("usage: python monitor_server.py <listen_ip> <listen_port>\n")
        sys.exit(-1)

    listen_ip = args[1]  # the address listened by monitor_server
    listen_port = int(args[2])

    # connect to the sqlite database
    await Tortoise.init(TORTOISE)  # connect to the sqlite database
    await Tortoise.generate_schemas()  # generate schemas if necessary
    server = await asyncio.start_server(handle_connection, listen_ip, listen_port)

    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(main())
