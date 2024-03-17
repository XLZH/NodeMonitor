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


@monitor.get("/nodes", summary="get the server information for all the nodes")
async def get_nodes_info():
    """
    get the server information (cpu, mem, disk, et.) for all the nodes
    """
    node_list = await NodeModel.all()

    return {'count': len(node_list), 'node_list': node_list}
