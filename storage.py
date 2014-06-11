#!/usr/bin/env python
#coding: utf8

import redis

from limiter import errors
from limiter import redis_helper

class BaseStorage(object):
    def __init__(self):
        pass

    def get(self, key):
        raise errors.NotImplementError()
    
    def set(self, key):
        raise errors.NotImplementError()


class RedisStorage(BaseStorage):
    def __init__(self, name="default"):
        self.storage = redis_helper.get_redis(name)

    def get(self, key):
        return self.storage.get(key)

    def set_and_get(self, key, expire_time):
        try:
            return self.storage.incr(key)
        finally:
            self.storage.expire(key, expire_time)


class MemcacheStorage(BaseStorage):
    pass

