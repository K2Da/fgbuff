import config
import datetime
import os
import bottle


def cache(func):
    def wrapper(*args, **kwargs):
        html = func(*args, **kwargs)
        if not config.cache:
            return html
        path = bottle.request.path

        root = config.cache_root + os.sep
        directory = root + os.sep.join(path.split('/'))
        full = root + os.sep.join(path.split('/')) + os.sep + '/index.html'
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(full, 'w', encoding='utf-8') as f:
            f.write(html)
        return html

    return wrapper


def support_datetime_default(o):
    if isinstance(o, datetime.date):
        return o.isoformat()
    raise TypeError(repr(o) + " is not JSON serializable")
