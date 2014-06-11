limiter
=======

可自定义的CGI速率限制器

例子


```
from lib import utils as au
import limiter

global_limiter = limiter.Limiter()
global_limiter.init(storage_name='igor')

def get_ipaddr(*largs, **kwargs):
    assert len(largs) > 0, 'largs length should be greater than 0'
    req = largs[0]
    return req.client_ip

@au.outer_handler(main_pat='/msg/ajax_info.pat', err_pat='/msg/ajax_info.pat')
@global_limiter.limit('10 per minute', key_func=get_ipaddr)
def normal_vote(req):
    return {'success': True}
```
