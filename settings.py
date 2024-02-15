#!/usr/bin/python3
# -*- coding: utf-8 -*-

# *************************************************************************
#    > File Name: settings.py
#    > Author: xlzh
#    > Mail: xiaolongzhang2015@163.com
#    > Created Time: 2024年02月15日 星期四 10时25分22秒
# *************************************************************************


__all__ = [
    'TORTOISE',
    'SERVER_LISTEN',
    'SERVER_ADDRESS',
    'SERVER_PORT'
]


# config for Tortoise-orm
TORTOISE = {
    'connections': {
        'default': 'sqlite://db/db.sqlite3'
    },
    'apps': {
        'models': {
            'models': ['models.model', 'aerich.models'],
            'default_connection': 'default'
        }
    },
    'use_tz': False,
    'timezone': 'Asia/Shanghai'
}


SERVER_LISTEN = '0.0.0.0'  # the address listened by monitor_server
SERVER_ADDRESS = '127.0.0.1'  # the address used by monitor_client
SERVER_PORT = 35601

