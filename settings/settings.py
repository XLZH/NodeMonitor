#!/usr/bin/python3
# -*- coding: utf-8 -*-

# *************************************************************************
#    > File Name: settings.py
#    > Author: xlzh
#    > Mail: xiaolongzhang2015@163.com
#    > Created Time: 2024年02月15日 星期四 10时25分22秒
# *************************************************************************


__all__ = ['TORTOISE']


# config for Tortoise-orm
TORTOISE = {
    'connections': {
        'default': 'sqlite://db/db.sqlite3'
    },
    'apps': {
        'models': {
            'models': ['models.model'],
            'default_connection': 'default'
        }
    },
    'use_tz': True,
    'timezone': 'Asia/Shanghai'
}

