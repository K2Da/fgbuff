import config
import os


def cache(path: str, html):
    root = config.cache_root + os.sep
    directory = root + os.sep.join(path.split('/')[:-1])
    full = root + os.sep.join(path.split('/'))
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(full, 'w', encoding='utf-8') as f:
        f.write(html)
    return html
