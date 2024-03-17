#!/usr/bin/python3
# -*- coding: utf-8 -*-

# *************************************************************************
#    > File Name: monitor_api.py
#    > Author: xlzh
#    > Mail: xiaolongzhang2015@163.com
#    > Created Time: 2024年03月17日 星期日 19时34分22秒
# *************************************************************************


import sys
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
import asyncio
import uvicorn
from api import *
from settings import *


app = FastAPI()


# register the tortoise-orm database
register_tortoise(app=app, config=TORTOISE)


# api for monitor
app.include_router(monitor, prefix="/api/v1/monitor", tags=["Monitor for all nodes"])


async def main():
    args = sys.argv
    if len(args) != 3:
        sys.stderr.write("usage: python monitor_api.py <listen_ip> <api_port>\n")
        sys.exit(-1)

    listen_ip = args[1]  # the address listened by monitor_api
    api_port = int(args[2])

    # start the api server
    uvicorn.run("monitor_api:app", host=listen_ip, port=api_port, reload=True)


if __name__ == '__main__':
    asyncio.run(main())
