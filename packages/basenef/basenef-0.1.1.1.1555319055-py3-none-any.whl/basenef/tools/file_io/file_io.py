# encoding: utf-8
'''
@author: Minghao Guo
@contact: mh.guo0111@gmail.com
@software: basenef
@file: file_io.py
@date: 4/14/2019
@desc:
'''

import numpy as np
from scipy import sparse
import os
from basenef.config import RESOURCE_PATH, CACHE_PATH
from basenef.utils import file_hasher


def local_data_saver(data = None):
    import numpy as np
    from scipy import sparse
    from basenef.utils import get_hash_of_timestamp

    cache_path = CACHE_PATH + get_hash_of_timestamp()
    if data is None:
        return -1
    if isinstance(data, np.ndarray):
        np.save(cache_path + '.npy', data)
        ext = '.npy'
        cache_path += ext
    elif isinstance(data, sparse.coo_matrix):
        sparse.save_npz(cache_path + '.npz', data)
        ext = '.npz'
        cache_path += ext
    else:
        raise ValueError(f'Unsupported data type {data.__class__.__name__} saving.')
    hash_ = file_hasher(cache_path)

    res_path = RESOURCE_PATH + hash_ + ext
    if not os.path.isfile(res_path):
        from shutil import move
        move(cache_path, res_path)
    else:
        os.remove(cache_path)

    return res_path


def local_data_loader(filename: str):
    if RESOURCE_PATH not in filename:
        path = RESOURCE_PATH + filename
        for ext in ['.npy', '.npz']:
            if os.path.isfile(path + ext):
                path += ext
                break
        else:
            raise ValueError(f'Cannot find valid resource file with filename / hash: {filename}')
    else:
        path = filename

    if path.endswith('.npy'):
        return np.load(path)
    elif path.endswith('.npz'):
        return sparse.load_npz(path)
    else:
        raise NotImplementedError(f'`local_data_loader` does not support {path} loading.')


#
# def sftp_url_parser(url: str):
#     import re
#     scheme, user, ip_, port, path = re.findall(r'(.*?)://(.*?)@(.*?):(.*?)/(.*?)$', url)[0]
#
#     return scheme, user, int(ip_), port, path
#
#
# def remote_data_saver(filename: str = None, data = None, user = 'nef', hostname = 'localhost',
#                       port = 22, pkey = pkey, is_cache = False):
#     from .sftp import sftp_upload
#
#     if hostname is None or hostname in ['127.0.0.1', 'localhost']:
#         return local_data_saver(filename, data, is_cache = is_cache)
#
#     local_cache_path = local_data_saver(data = data, is_cache = True)
#     if is_cache:
#         remote_dir = f'/home/{user}/Database_nef/caches/'
#     else:
#         remote_dir = f'/home/{user}/Database_nef/resources/'
#     remote_path = remote_dir + local_cache_path.split(['/'])[-1]
#
#     sftp_upload(local_cache_path, remote_path, hostname, port, pkey)
#     return f'sftp://{user}@{hostname}:{port}remote_path'
#
#
# def remote_data_loader(filename: str = None, user = 'nef', hostname = 'localhost', port = 22,
#                        pkey = pkey, is_cache = False):
#     from .sftp import sftp_download
#
#     if hostname is None or hostname in ['127.0.0.1', 'localhost']:
#         return local_data_loader(filename, is_cache = is_cache)
#     if os.path.isfile(CACHE_PATH + filename):
#         return local_data_loader(filename, is_cache = is_cache)
#
#     if is_cache:
#         remote_path = f'/home/{user}/Database_nef/caches/{filename}'
#     else:
#         remote_path = f'/home/{user}/Database_nef/resources/{filename}'
#
#     local_cache_path = CACHE_PATH + filename
#
#     sftp_download(remote_path, local_cache_path, hostname = hostname, port = port, pkey = pkey)
#
#     return local_cache_path(local_cache_path, is_cache = is_cache)
#

def data_saver(data = None):
    return local_data_saver(data)


def data_loader(url: str = None):
    return local_data_loader(url)

#
#
# from urllib.parse import urlparse
