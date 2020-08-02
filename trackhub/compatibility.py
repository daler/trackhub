"""
A subset of Python 2/3 compatibility helpers; ideas from the `six` module.
"""

from __future__ import absolute_import
import sys

PY = sys.version_info[0]
PY3 = PY == 3
PY2 = PY == 2

if PY3:
    string_types = str,

if PY2:
    string_types = basestring,


def py2_unicode(cls):
    if PY2:
        if '__str__' not in cls.__dict__:
            raise ValueError(
                'no __str__method defined for {}'.format(cls.__name__))
        cls.__unicode__ = cls.__str__
        cls.__str__ = lambda self: self.__unicode__().encode('utf-8')
    return cls
