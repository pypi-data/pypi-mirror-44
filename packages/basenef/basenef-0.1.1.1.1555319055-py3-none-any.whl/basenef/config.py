# encoding: utf-8
'''
@author: Minghao Guo
@contact: mh.guo0111@gmail.com
@software: nef
@file: config.py
@date: 4/15/2019
@desc:
'''
import os
from .utils import separator

''' required directories'''
DATABASE_PATH = os.environ['HOME'] + separator + 'Database_nef' + separator
RESOURCE_PATH = DATABASE_PATH + 'resources' + separator
SCHEMA_PATH = DATABASE_PATH + 'schemas' + separator
CACHE_PATH = DATABASE_PATH + 'caches' + separator
LOG_PATH = DATABASE_PATH + 'logs' + separator
DOC_PATH = DATABASE_PATH + 'docs' + separator

_PATH_LIST = [DATABASE_PATH, RESOURCE_PATH, SCHEMA_PATH, CACHE_PATH, LOG_PATH, DOC_PATH]

for _path in _PATH_LIST:
    if not os.path.isdir(_path):
        os.mkdir(_path)
