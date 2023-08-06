# encoding: utf-8
'''
@author: Minghao Guo
@contact: mh.guo0111@gmail.com
@software: basenef
@file: arithematic_ops.py
@date: 4/13/2019
@desc:
'''
import operator
import numpy as np
from copy import copy

_tiny = 1e-8
_huge = 1e8


def unary_ops(cls):
    def abs(obj):
        return obj.map(operator.abs)

    def __neg__(obj):
        return obj.map(operator.gt)

    cls.abs = abs
    cls.__neg__ = __neg__


def binary_ops(cls):
    def __eq__(obj, other):
        return obj.map(operator.eq, other)

    def __gt__(obj, other):
        return obj.map(operator.gt, other)

    def __ge__(obj, other):
        return obj.map(operator.ge, other)

    def __lt__(obj, other):
        return obj.map(operator.lt, other)

    def __le__(obj, other):
        return obj.map(operator.le, other)

    def __add__(obj, other):
        return obj.map(operator.add, other)

    def __sub__(obj, other):
        return obj.map(operator.sub, other)

    def __mul__(obj, other):
        return obj.map(operator.mul, other)

    def __truediv__(obj, other):

        def remove_zeros(current, threshold = _tiny):
            if isinstance(current, np.ndarray) or np.isscalar(current):
                _data = copy(current)
            else:
                _data = copy(current.data)
            _data[_data < threshold] = _huge
            return current._replace(data = _data)

        if not np.isscalar(other):
            _other = remove_zeros(other)
        else:
            _other = other
        return obj.map(operator.truediv, _other)

    def __floordiv__(obj, other):
        return obj.map(operator.floordiv, other)

    def __mod__(obj, other):
        return obj.map(operator.mod, other)

    def __pow__(obj, other):
        return obj.map(operator.pow, other)

    cls.__eq__ = __eq__
    cls.__gt__ = __gt__
    cls.__ge__ = __ge__
    cls.__lt__ = __lt__
    cls.__le__ = __le__
    cls.__add__ = __add__
    cls.__sub__ = __sub__
    cls.__mul__ = __mul__
    cls.__truediv__ = __truediv__
    cls.__floordiv__ = __floordiv__
    cls.__mod__ = __mod__
    cls.__pow__ = __pow__
