# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from typing import Optional, Any


ATTR_NAME = '__cologler.attributes__'


class AttributeMetaClass(type):
    def __init__(self, name, bases, *args, **kwargs):
        allow_multiple = kwargs.pop('allow_multiple', None)
        multiple_tag = None

        attr_bases = [b for b in bases if isinstance(b, AttributeMetaClass)]
        if len(attr_bases) > 1:
            raise TypeError('attribute does not support multi inherit')

        elif len(attr_bases) == 1:
            attr_base = attr_bases[0]

            if not attr_base._allow_multiple:
                if allow_multiple:
                    raise ValueError(f'attribute {self} cannot allow multiple (inherit from {attr_base})')
                allow_multiple = False
                multiple_tag = attr_base._multiple_tag

        else:
            # the root attribute class
            pass

        if allow_multiple is None:
            allow_multiple = True

        self._allow_multiple = allow_multiple
        self._multiple_tag = multiple_tag or object()

        super().__init__(name, bases, *args, **kwargs)

    def __call__(self, *args, **kwargs):
        def attr_appender(obj):
            attrs_list = vars(obj).get(ATTR_NAME, None)
            if attrs_list is None:
                attrs_list = []
                setattr(obj, ATTR_NAME, attrs_list)
            if not self._allow_multiple:
                for attr_cls, factory in attrs_list:
                    if attr_cls._multiple_tag is self._multiple_tag:
                        raise SyntaxError(f'attribute {self} did not allow multiple')
            def factory():
                attr: Attribute = type.__call__(self, *args, **kwargs)
                attr._origin_target = obj
                return attr
            attrs_list.append(
                # (cls, factory)
                (self, factory)
            )
            return obj
        return attr_appender

    @property
    def allow_multiple(self):
        return self._allow_multiple


class Attribute(metaclass=AttributeMetaClass):
    _origin_target: Any
    _target: Any

    def __init_subclass__(cls, *args, **kwargs):
        # so we can add `allow_multiple` kwargs.
        pass

    @property
    def origin_target(self):
        return self._origin_target

    @property
    def target(self):
        return self._target

    @classmethod
    def _iter_attr_factorys(cls, obj, attr_type=None, *, inherit=False):
        if inherit and isinstance(obj, type):
            for subcls in obj.__mro__:
                yield from cls._iter_attr_factorys(subcls, attr_type, inherit=False)
        else:
            for attr_cls, factory in reversed(vars(obj).get(ATTR_NAME, ())):
                if attr_type is None or issubclass(attr_cls, attr_type):
                    yield factory

    @classmethod
    def _iter_attrs(cls, obj, attr_type=None, *, inherit=False):
        for factory in cls._iter_attr_factorys(obj, attr_type, inherit=inherit):
            attr = factory()
            attr._target = obj
            yield attr

    @classmethod
    def get_attrs(cls, obj, attr_type=None, *, inherit=False):
        '''
        gets the all attrs from `obj` which match `attr_type`.
        '''
        return tuple(cls._iter_attrs(obj, attr_type, inherit=inherit))

    @classmethod
    def get_attr(cls, obj, attr_type, *, inherit=False):
        '''
        gets the first attr from `obj` which match `attr_type`.
        '''
        if attr_type is None:
            raise ValueError
        for attr in cls._iter_attrs(obj, attr_type, inherit=inherit):
            return attr
        return None

    @classmethod
    def has_attr(cls, obj, attr_type, *, inherit=False):
        '''
        check whether the `obj` has some attr.
        '''
        for factory in cls._iter_attr_factorys(obj, attr_type, inherit=inherit):
            return True
        return False
