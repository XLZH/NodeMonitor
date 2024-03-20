#!/usr/bin/python3
# -*- coding: utf-8 -*-

# *************************************************************************
#    > File Name: query.py
#    > Author: xlzh
#    > Mail: xiaolongzhang2015@163.com
#    > Created Time: 2024年01月29日 星期一 09时51分16秒
# *************************************************************************


from fastapi import APIRouter, HTTPException
from models.model import NodeModel, UsageModel


__all__ = ['monitor']


monitor = APIRouter()


@monitor.get("/info5", summary="get the server information within 5 seconds")
async def get_node_info5(host: str):
    """
    get the server information (cpu, mem, disk, et.) within 5 seconds
    """
    if host == 'all':
        info_list = await NodeModel.all().values('host', 'cpu_5', 'mem_5', 'net_rx_5', 'net_tx_5')
        return {'count': len(info_list), 'info_list': info_list}

    # get the info5 for given node by hostname
    node_info = await NodeModel.filter(host=host).values('host', 'cpu_5', 'mem_5', 'net_rx_5', 'net_tx_5')
    if len(node_info) == 0:
        raise HTTPException(status_code=410, detail=f"unknown hostname ({host}) is detected!")

    return {'count': 1, 'info_list': node_info}


@monitor.get("/info60", summary="get the server information within 60 seconds")
async def get_node_info60(host: str):
    """
    get the server information (cpu, mem, disk, et.)
    """
    if host == 'all':
        info_list = await NodeModel.all().values('host', 'cpu_60', 'mem_60', 'net_rx_60', 'net_tx_60')
        return {'count': len(info_list), 'info_list': info_list}

    # get the info60 for given node by hostname
    node_info = await NodeModel.filter(host=host).values('host', 'cpu_60', 'mem_60', 'net_rx_60', 'net_tx_60')
    if len(node_info) == 0:
        raise HTTPException(status_code=410, detail=f"unknown hostname ({host}) is detected!")

    return {'count': 1, 'info_list': node_info}


@monitor.get("/disk", summary="get the disk status")
async def get_node_disk(host: str):
    """
    get the disk status for 'all' nodes or given host
    """
    if host == 'all':
        disk_list = await NodeModel.all().values('host', 'disk_status', 'disk_failed')
        return {'count': len(disk_list), 'disk_list': disk_list}

    # get the disk status for given node by hostname
    disk_info = await NodeModel.filter(host=host).values('host', 'disk_status', 'disk_failed')
    if len(disk_info) == 0:
        raise HTTPException(status_code=410, detail=f"unknown hostname ({host}) is detected!")

    return {'count': 1, 'disk_list': disk_info}


@monitor.get("/usage", summary="get the disk usage")
async def get_disk_usage():
    """
    get the disk usage for all mounted disks
    """
    disk_list = await UsageModel.all()

    if len(disk_list) == 0:
        raise HTTPException(status_code=411, detail="may be there are no disks provided")

    return {'count': len(disk_list), 'disk_list': disk_list}
