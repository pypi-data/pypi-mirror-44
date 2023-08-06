# encoding: utf-8
'''
@author: Minghao Guo
@contact: mh.guo0111@gmail.com
@software: srf_ct
@file: class_schema_parser.py
@date: 4/8/2019
@desc:
'''

import numpy as np

from basenef.base import make_nef_class
from basenef.typings import BASIC_TYPES, BASIC_TYPE_DICT_REVERT, BASIC_TYPE_DICT


def _to_string(o):
    if isinstance(o, np.ndarray):
        return np.array2string(o, separator = ',')
    else:
        return str(o)


def _convert_single_class_to_schema(cls: type, verbose = True):
    kwargs = {}
    out = {}
    for key, _type in cls.fields():
        if not verbose and key.startswith('_'):
            continue
        elif key == 'data':
            kwargs.update({key: 'str'})
        elif _type in BASIC_TYPES:
            kwargs.update({key: BASIC_TYPE_DICT_REVERT[_type]})
        else:
            out.update(_convert_single_class_to_schema(_type, verbose = verbose))
            kwargs.update({key: _type.__name__})

    out.update({cls.__name__: kwargs})
    return out


def convert_class_to_schema(class_dct: dict = None, verbose = True):
    if class_dct is None:
        return {}
    if isinstance(class_dct, type):
        class_dct = {class_dct.__name__: class_dct}
    elif isinstance(class_dct, list):
        class_dct = {cls.__name__: cls for cls in class_dct}

    dct = {}

    for class_name, cls in class_dct.items():
        if class_name in dct:
            pass
        else:
            dct.update(_convert_single_class_to_schema(cls, verbose = verbose))
    return dct


def convert_schema_to_class(schema: dict):
    if isinstance(schema, str):
        import json as json_
        try:
            schema = json_.loads(schema)
        except ValueError('Can not parse schema: ', schema):
            pass
    print(schema)
    out = {}
    for key, subdct in schema.items():
        print(out)
        fields = {}
        for k, v in subdct.items():
            print(k, v)
            if v in BASIC_TYPE_DICT:
                type_ = BASIC_TYPE_DICT[v]
            elif v in schema:
                convert_schema_to_class({'t': schema[v]})
            elif v in out:
                type_ = out[v]
            else:
                raise ValueError(f'Unknown parser for field {k} in {key}')
            fields.update({k: type_})

        cls = make_nef_class({key: fields})[key]
        out.update({key: cls})
    return out
