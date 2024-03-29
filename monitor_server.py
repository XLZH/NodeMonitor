#!/usr/bin/python3
# -*- coding: utf-8 -*-

# *************************************************************************
#    > File Name: monitor_server.py
#    > Author: xlzh
#    > Mail: xiaolongzhang2015@163.com
#    > Created Time: 2024年02月15日 星期四 09时54分12秒
# *************************************************************************

import json
import sys
import asyncio
from datetime import datetime
from tortoise import Tortoise, exceptions
from settings import *
from models.model import NodeModel


async def receive_client_data(socket_reader, socket_writer):
    client_data = await socket_reader.read(1024)

    try:
        # data that not really come from client
        info_dict = json.loads(client_data.decode('utf-8'))
    except json.JSONDecodeError:
        socket_writer.close()
        return

    try:
        info_dict['update'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await NodeModel.get(host=info_dict['host'])
        await NodeModel.filter(host=info_dict['host']).update(**info_dict)

    except exceptions.DoesNotExist:
        await NodeModel.create(**info_dict)

    socket_writer.close()
    return


async def main():
    args = sys.argv
    if len(args) != 3:
        sys.stderr.write("usage: python monitor_server.py <listen_ip> <socket_port>\n")
        sys.exit(-1)

    listen_ip = args[1]  # the address listened by monitor_server
    socket_port = int(args[2])

    # connect to the sqlite database
    await Tortoise.init(TORTOISE)  # connect to the sqlite database
    await Tortoise.generate_schemas()  # generate schemas if necessary
    server = await asyncio.start_server(receive_client_data, listen_ip, socket_port)
    async with server:
        await server.serve_forever()

    await Tortoise.close_connections()


if __name__ == '__main__':
    asyncio.run(main())
