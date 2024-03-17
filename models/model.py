#!/usr/bin/python3
# -*- coding: utf-8 -*-

# *************************************************************************
#    > File Name: model.py
#    > Author: xlzh
#    > Mail: xiaolongzhang2015@163.com
#    > Created Time: 2024年02月15日 星期四 10时20分36秒
# *************************************************************************

from tortoise import fields
from tortoise.models import Model


class NodeModel(Model):
    id = fields.IntField(pk=True, description="the id of the node host")
    host = fields.CharField(max_length=31, description="the hostname of the node")
    cpu_5 = fields.CharField(max_length=15, description="average ratio of cpu in 5 seconds")
    cpu_60 = fields.CharField(max_length=15, description="average ratio of cpu in 60 seconds")
    mem_5 = fields.CharField(max_length=15, description="average ratio of memory in 5 seconds")
    mem_60 = fields.CharField(max_length=15, description="average ratio of memory in 60 seconds")
    net_rx_5 = fields.CharField(max_length=31, description="average receive bytes of network in 5 seconds")
    net_tx_5 = fields.CharField(max_length=31, description="average send bytes of network in 5 seconds")
    net_rx_60 = fields.CharField(max_length=31, description="average receive bytes of network in 60 seconds")
    net_tx_60 = fields.CharField(max_length=31, description="average send bytes of network in 60 seconds")
    disk_status = fields.IntField(description="the current status of the disk")
    disk_failed = fields.CharField(max_length=255, description="disks that failed to mount")
    update = fields.CharField(max_length=31, description="time to update the node info")

    class Meta:
        table = "node"
        table_description = "node status (memory, cpu and network)"

