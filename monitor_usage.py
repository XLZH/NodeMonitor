#!/usr/bin/python3
# -*- coding: utf-8 -*-

# *************************************************************************
#    > File Name: monitor_usage.py
#    > Author: xlzh
#    > Mail: xiaolongzhang2015@163.com
#    > Created Time: 2024年03月20日 星期三 12时39分12秒
# *************************************************************************

import sys
import time

import asyncio
from tortoise import Tortoise, exceptions
from monitor_client import Disk
from datetime import datetime
from settings import *
from models.model import UsageModel

# the interval of disk usage checking
UsageCheckInterval = 60
LoopInterval = 5


async def get_disk_usage(disk_obj: Disk):
    """
    get the disk state and usage and write to the sqlite database
    """
    disks_list = disk_obj.get_disk_info()
    print(disks_list)
    for disk_info in disks_list:
        try:
            disk_info['update'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            await UsageModel.get(disk_name=disk_info['disk_name'])
            await UsageModel.filter(disk_name=disk_info['disk_name']).update(**disk_info)

        except exceptions.DoesNotExist:
            await UsageModel.create(**disk_info)

    return 0


async def main():
    args = sys.argv
    if len(args) != 2:
        sys.stderr.write("usage: python monitor_usage.py <disk_list>\n")
        sys.exit(-1)

    # connect to the sqlite database
    await Tortoise.init(TORTOISE)  # connect to the sqlite database
    await Tortoise.generate_schemas()  # generate schemas if necessary

    # the disk object used to get the disk status and usage
    input_disks = set(args[1].split(':'))
    disk_obj = Disk(UsageCheckInterval, input_disks)

    while True:
        await get_disk_usage(disk_obj)
        time.sleep(LoopInterval)


if __name__ == '__main__':
    asyncio.run(main())

