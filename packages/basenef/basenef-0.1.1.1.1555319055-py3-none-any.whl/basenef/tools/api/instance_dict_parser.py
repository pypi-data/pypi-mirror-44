# encoding: utf-8
'''
@author: Minghao Guo
@contact: mh.guo0111@gmail.com
@software: srf_ct
@file: instance_dict_parser.py
@date: 4/9/2019
@desc:
'''
from basenef.typings import BASIC_TYPE_DICT_REVERT, BASIC_TYPE_CONVERTER
from basenef.base import NefClass


def _convert_single_instance_to_dict(obj: NefClass = None, *, verbose = True):
    if obj is None:
        raise ValueError('valid instance are needed.')

    kwargs = {'classname': obj.__class__.__name__}
    for key, _type in obj.__class__.fields():
        if not verbose and key.startswith('_'):
            continue
        if key == 'data':
            from basenef.tools.file_io import data_saver
            res_path = data_saver(getattr(obj, key))
            kwargs.update({'data': res_path})  # should be file_io here
        elif _type in BASIC_TYPE_DICT_REVERT:
            kwargs.update({key: getattr(obj, key)})
        else:
            kwargs.update(
                {key: _convert_single_instance_to_dict(getattr(obj, key), verbose = verbose)})

    return kwargs


def convert_instance_to_dict(objs_dct: dict, *, verbose = True):
    if isinstance(objs_dct, NefClass):
        objs_dct = {str(0): objs_dct}
    elif isinstance(objs_dct, list):
        objs_dct = {str(ind): obj for ind, obj in enumerate(objs_dct)}

    kwargs = {}
    for key, obj in objs_dct.items():
        kwargs.update({key: _convert_single_instance_to_dict(obj, verbose = verbose)})
    return kwargs


def convert_dict_to_instance(dct: dict, *, schema: dict):
    if schema is None:
        raise ValueError('A valid schema is needed.')
    if isinstance(schema, str):
        import json as json_
        try:
            schema = json_.loads(schema)
        except ValueError('Can not parse schema: ', schema):
            pass
    out = {}
    for key, val in dct.items():
        if 'classname' in val:
            classname = val['classname']
            if classname not in schema:
                raise ValueError(f'can not find valid class assigned for {key} in the first arg')
            cls = schema[classname]
            print(1, cls)
            if isinstance(cls, dict):
                from .class_schema_parser import convert_schema_to_class
                cls = convert_schema_to_class(schema)[classname]
                print(2, convert_schema_to_class(schema))
        else:
            raise ValueError(f"can not find valid classname in dct.['{key}']")

        kwargs = {}
        print(cls)
        for field, type_ in cls.fields():
            sub_ = val[field]
            if field.startswith('_'):
                continue
            elif field == 'data':
                from basenef.tools.file_io import data_loader
                kwargs.update({field: data_loader(sub_)})
            elif isinstance(sub_, dict):
                kwargs.update(
                    {field: convert_dict_to_instance({field: sub_}, schema = schema)[field]})
            else:
                kwargs.update({field: BASIC_TYPE_CONVERTER[type_.__name__](sub_)})
        out.update({key: cls(**kwargs)})
    return out
