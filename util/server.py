import config
import datetime
import os


def cache(path: str, html):
    if not config.cache:
        return html
    root = config.cache_root + os.sep
    directory = root + os.sep.join(path.split('/')[:-1])
    full = root + os.sep.join(path.split('/'))
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(full, 'w', encoding='utf-8') as f:
        f.write(html)
    return html


def support_datetime_default(o):
    if isinstance(o, datetime.date):
        return o.isoformat()
    raise TypeError(repr(o) + " is not JSON serializable")