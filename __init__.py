#!/usr/bin/env python
#coding: utf8


#一个可以自定义的接口速率限制器
#使用方法:

from functools import wraps
from limiter import limiter_util, limits, storage

class Limiter(object):
    def __init__(self):
        self._route_limits = {}
        self.limiter = self.storage = None

    def init(self, storage_name='default'):
        self.storage = storage.RedisStorage(storage_name)
        self.limiter = limits.LimitItemManager(self.storage)

    def check_cgi_limit(self, cgi_name, *largs, **kwargs):
        return (
            all([self.limiter.hit(rate_item, key_func(*largs, **kwargs)) \
                    for key_func, rate_item in self._route_limits[cgi_name]])
        )

    def limit(self, limit_str, key_func=None, key_func_args=()):
        def _outer(func):
            cgi_name = '%s.%s' % (func.__module__, func.__name__)
            @wraps(func)
            def _inner(*largs, **kwargs):
                if self.check_cgi_limit(cgi_name, *largs, **kwargs):
                    return func(*largs, **kwargs)
                else:
                    raise errors.RateLimitError()

            self._route_limits.setdefault(cgi_name, [])\
                    .extend([(key_func, rate_item) for rate_item in limiter_util.parse_many(limit_str)])
            return _inner
            

        return _outer
