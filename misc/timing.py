import logging
from functools import wraps
from time import time

log = logging.getLogger(__name__)


def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        message = 'func:%r args:[%r, %r] took: %2.4f sec' % (f.__name__, args, kw, te - ts)
        print(message)
        log.info(message)
        return result

    return wrap
