# encoding: utf-8
'''
@author: Minghao Guo
@contact: mh.guo0111@gmail.com
@software: basenef
@file: base.py
@date: 4/13/2019
@desc:
'''

import types

import attr

from .arithematic_ops import unary_ops, binary_ops


class NefClass:
    '''`NefClass` is suited for storing data objects. It is the most basic class type in
    `srfnef` package. All data and functions would be seriously considered to be defined as a
    Dataclass instance. More specific, only the field `.data` in a `NefClass` would be regarded
    as the only computable part with in an instance. Any other class that defined to contained
    data would a subclass of `NefClass`.
    '''

    def _replace(self, **kwargs):
        '''Creates a new object of the same type of instance, replacing fields with values from
        changes.
        '''
        return attr.evolve(self, **kwargs)

    @classmethod
    def fields(cls):
        '''Returns a tuple of field names for this `DataClass` instance.
        '''
        return [(k, v.type) for (k, v) in attr.fields_dict(cls).items()]

    def items(self, recurse = True):
        '''Return a dictionary of fields for this 'NefClass` instance.
        '''

        return attr.asdict(self, recurse).items()

    def keys(self, recurse = True):
        return list(attr.asdict(self, recurse).keys())

    def values(self, recurse = True):
        return list(attr.asdict(self, recurse).values())

    def map(self, f, *args):
        '''`Map` applis a function to the field `.data` of this NefClass instance, and return a
        new instance with the same type'''
        return self._replace(data = f(self.data, *args))

    @classmethod
    def class_map(cls, **kwargs):
        for key, val in kwargs.items():
            if not callable(val):
                raise ValueError('not callable')
            setattr(cls, key, val)
        return cls

    def __call__(self, **kwargs):
        return self._replace(**kwargs)

    @classmethod
    def __annotations__(cls):
        return attr.fields_dict(cls)


def _update_class_dict(cls: type, *, recurse = True):
    import basenef
    basenef.class_dict.update({cls.__name__: cls.__annotations__})
    if recurse:
        for name, tp in cls.__annotations__.items():
            if name == 'data':
                pass
            elif tp in basenef.BASIC_TYPES:
                pass
            elif tp not in basenef.class_dict:
                _update_class_dict(tp, recurse = recurse)
            else:
                print(f'Warning: {cls.__name__} already in class_dict. Ignored. ')
    return cls


def nef_class(cls):
    '''This function is a decorator that is used to add generated special methods to classes, as
    described below.

    The `nef_class()` decorator examines the class to find fields. A field is defined as class
    variable that has a type annotation. The order of the fields in all of the generated methods
    is the order in which they appear in the class definition.
    Be default the instance decorated by `nef_class` is attributed frozen, which means we prefer
    it to be immutable.

    Some basic arithmetic operators are mounted and would apply on `.data` field.
    '''
    base = attr.s(frozen = True, auto_attribs = True, slots = True)(cls)
    cls_ = types.new_class(base.__name__, (base, NefClass))
    # if bind:
    #     _update_class_dict(cls, recurse = True)
    unary_ops(cls_)
    binary_ops(cls_)
    return cls_


def make_nef_class(dct: dict = {}):
    out_dict = {}
    for class_name, fields in dct.items():
        anns = {}
        namespace = {}
        for field_name, type_ in fields.items():
            if isinstance(type_, str):
                try:
                    from .typings import BASIC_TYPE_CONVERTER
                    type_ = BASIC_TYPE_CONVERTER[type_]
                finally:
                    raise ValueError('A type assignment is required')
            anns[field_name] = type_

        namespace['__annotations__'] = anns

        cls = types.new_class(class_name, exec_body = lambda ns: ns.update(namespace))
        out_dict.update({class_name: nef_class(cls)})
    return out_dict
