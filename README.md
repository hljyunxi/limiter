limiter
=======

可自定义的CGI速率限制器

例子: 比如下面是一个投票接口， 但是为了防止刷票， 我想限制每个ip每分钟只能投10次，
可以用大家都看得懂的方式来声明哦: 10 per minute, 当然还可以10 per hour(一小时只能访问10次),
就是这么简单。


```
from lib import utils as au
import limiter

global_limiter = limiter.Limiter()
global_limiter.init(storage_name='igor')


def limit_cgi(limit_str, key_func=None, dict_ret=True):
    def _outter(func):
        def _inner(req):
            try:
                return global_limiter.limit(limit_str, key_func)(func)(req)
            except limiter.errors.RateLimitError:
                if dict_ret:
                    return {'success': False, 'msg': '接口调用太频繁'}
                else:
                    return '接口调用太频繁'
        return _inner

    return _outter


def get_ipaddr(*largs, **kwargs):
    assert len(largs) > 0, 'largs length should be greater than 0'
    req = largs[0]
    return req.client_ip


@au.outer_handler(main_pat='/msg/ajax_info.pat', err_pat='/msg/ajax_info.pat')
@limit_cgi('10 per minute', key_func=get_ipaddr)
def vote(req):
    # 投票的CGI逻辑
    return {'success': True}
```
