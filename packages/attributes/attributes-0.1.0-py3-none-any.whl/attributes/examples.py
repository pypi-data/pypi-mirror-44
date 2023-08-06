# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
# this is a example to use Attribute.
# ----------

from .core import Attribute

class info(Attribute):
    '''
    add `info` to target.

    ``` py
    @info('name', 'eva')
    class Person: pass
    assert info.get_value(Person, 'name') == 'eva'
    ```
    '''

    def __init__(self, name, value):
        super().__init__()
        self.name = name
        self.value = value

    @classmethod
    def get_as_dict(cls, obj, *, inherit=False):
        ''' gets all `info` and combine as a single `dict` '''
        d = {}
        for attr in reversed(cls.get_from(obj, inherit=inherit)):
            # reversed so we can override parent.
            d[attr.name] = attr.value
        return d

    @classmethod
    def get_value(cls, obj, name, default=None, *, inherit=False):
        ''' gets the first `info` match that `name` '''
        for attr in cls.get_from(obj, inherit=inherit):
            if attr.name == name:
                return attr.value
        return default

class props(Attribute):
    '''
    add `props` to target.

    ``` py
    @props(name='eva')
    class Person: pass
    assert props.get_as_dict(Person)['name'] == 'eva'
    ```
    '''

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    @classmethod
    def get_as_dict(cls, obj, *, inherit=False):
        attrs = cls.get_from(obj, inherit=inherit)
        d = {}
        for attr in reversed(attrs):
            # reversed so we can override parent.
            d.update(attr.kwargs)
        return d
