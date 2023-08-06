# encoding: utf-8
'''
@author: Minghao Guo
@contact: mh.guo0111@gmail.com
@software: basenef
@file: utils.py
@date: 4/14/2019
@desc:
'''

import sys
import tqdm as tqdm_
import hashlib
import platform

if 'Windows' in platform.system():
    separator = '\\'
else:
    separator = '/'


def is_notebook():
    '''check if the current environment is `ipython`/ `notebook`
    '''
    return 'ipykernel' in sys.modules


def tqdm(*args, **kwargs):
    '''same as tqdm.tqdm
    Automatically switch between `tqdm.tqdm` and `tqdm.tqdm_notebook` accoding to the runtime
    environment.
    '''
    if is_notebook():
        return tqdm_.tqdm_notebook(*args, **kwargs)
    else:
        return tqdm_.tqdm(*args, **kwargs)


def hasher(o):
    m = hashlib.sha256()
    from .typings import BASIC_TYPES
    if isinstance(o, BASIC_TYPES):
        m.update(str(o).encode('utf-8'))
    else:
        for key, val in o.items():
            if key.startswith('_'):
                continue
            if not isinstance(val, dict):
                m.update(str(val).encode('utf-8'))
            else:
                m.update(hasher(val))
    return m.hexdigest()


def file_hasher(path: str):
    import os
    if os.path.isdir(path):
        raise ValueError('Only file can be hashed')

    BLOCKSIZE = 65536
    m = hashlib.sha256()

    with open(path, 'rb') as fin:
        buf = fin.read(BLOCKSIZE)
        while len(buf) > 0:
            m.update(buf)
            buf = fin.read(BLOCKSIZE)
    return m.hexdigest()


def get_local_ip():
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('www.baidu.com', 0))
        ip = s.getsockname()[0]
    except:
        ip = "x.x.x.x"
    finally:
        s.close()
    return ip


def get_hash_of_timestamp():
    import time
    m = hashlib.sha256()
    timestamp = time.time()
    m.update(str(timestamp).encode('utf-8'))
    return m.hexdigest()
