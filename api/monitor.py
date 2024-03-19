#!/usr/bin/python3
# -*- coding: utf-8 -*-

# *************************************************************************
#    > File Name: query.py
#    > Author: xlzh
#    > Mail: xiaolongzhang2015@163.com
#    > Created Time: 2024年01月29日 星期一 09时51分16秒
# *************************************************************************


from fastapi import APIRouter, HTTPException
from models.model import NodeModel


__all__ = ['monitor']


monitor = APIRouter()


@monitor.get("/nodes/info60",
             summary="get the server information within 60 seconds for all nodes")
async def get_nodes_all60():
    """
    get the server information (cpu, mem, disk, et.) for all the nodes
    """
    info_list = await NodeModel.all().values(
        'host', 'cpu_60', 'mem_60', 'net_rx_60', 'net_tx_60'
    )

    return {'count': len(info_list), 'info_list': info_list}


@monitor.get("/node/info5",
             summary="get the server information within 5 seconds for given node")
async def get_node_info5(host: str):
    """
    get the server information within 5 seconds for given hostname
    """
    node_info = await NodeModel.filter(host=host).values(
        'host', 'cpu_5', 'mem_5', 'net_rx_5', 'net_tx_5'
    )

    if len(node_info) == 0:
        raise HTTPException(
            status_code=410,
            detail=f"unknown hostname ({host}) is detected!"
        )

    return {'count': 1, 'info5': node_info}


@monitor.get("/node/info60",
             summary="get the server information within 60 seconds for given node")
async def get_node_info60(host: str):
    """
    get the server information within 60 seconds for given hostname
    """
    node_info = await NodeModel.filter(host=host).values(
        'host', 'cpu_60', 'mem_60', 'net_rx_60', 'net_tx_60'
    )

    if len(node_info) == 0:
        raise HTTPException(
            status_code=410,
            detail=f"unknown hostname ({host}) is detected!"
        )

    return {'count': 1, 'info60': node_info}


@monitor.get("/nodes/disk", summary="get the disk status for all nodes")
async def get_nodes_disk():
    """
    get the disk status for all nodes
    """
    disk_list = await NodeModel.all().values(
        'host', 'disk_status', 'disk_failed'
    )

    return {'count': len(disk_list), 'node_disk_list': disk_list}


@monitor.get("/node/disk", summary="get the disk status for given node")
async def get_node_disk(host: str):
    """
    get the disk status for given hostname
    """
    disk_info = await NodeModel.filter(host=host).values(
        'host', 'disk_status', 'disk_failed'
    )

    if len(disk_info) == 0:
        raise HTTPException(
            status_code=410,
            detail=f"unknown hostname ({host}) is detected!"
        )

    return {'count': 1, 'disk': disk_info}
