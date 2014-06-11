#!/usr/bin/env python
#coding: utf8

import redis
try:
    from igor import const
except ImportError:
    class const:
        redis = {
            'host': 'localhost',
            'port': 5379,
        }

REDIS_SYSTEMS = {
    'default': redis.Redis(host="localhost", port=5379),
    'igor': redis.Redis(host=const.redis['host'], port=const.redis['port'])
}


def setup_redis(name, host, port):
    REDIS_SYSTEMS[name] = redis.Redis(host=host, port=port)


def get_redis(name='default'):
    return REDIS_SYSTEMS[name]
