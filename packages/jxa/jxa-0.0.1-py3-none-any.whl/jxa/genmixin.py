import copy
from collections import OrderedDict
from typing import Union, Iterable


def quote_str(arg):
    if isinstance(arg, str):
        return "'{}'".format(arg)
    else:
        return arg


class ReprMixin:
    """
    An universal and dynamic __repr__ method, generates the object constructor.
    
    The method generates the object constructor with fields as arguments.
    Fields to display have to be specified in order in _attrs_filter and
    only object-defined fields are printed.
    
    The method properly quotes str values.
    Optionally set _attrs_ignore_empty to hide empty/None values.
    """
    _attrs_filter = []
    _attrs_ignore_empty = False

    def __repr__(self) -> str:
        # now it supports properties
        fields = [z for z in dir(self) if not callable(getattr(self, z))]
        attrs = set(fields) & set(self._attrs_filter)
        attrs_dict = OrderedDict([(a, self.__getattribute__(a)) for a in attrs])
        attrs_str = ["{}={}".format(arg, quote_str(val))
                     for (arg, val) in attrs_dict.items()
                     if not (self._attrs_ignore_empty and val is None)]

        return "{}({})".format(self.__class__.__name__, ', '.join(attrs_str))

    @classmethod
    def repr_add_attr(cls, attr: Union[str, Iterable[str]]):
        """ adds attr to self._attrs_filter, allows chaining """
        if isinstance(attr, str):
            cls._attrs_filter.append(attr)
        elif isinstance(attr, Iterable):
            cls._attrs_filter.extend(attr)
        else:
            raise TypeError(f"Unsupported type: {type(attr)}")

    @classmethod
    def repr_ignore_empty_attrs(cls, ignore: bool = True) -> None:
        cls._attrs_ignore_empty = ignore


class EqualityMixin:
    """" Delivers __eq__

    Compares only fields as defined by self._compare_fields property.
    You may copy the list from ReprMixin fields _attrs_filter and optionally
    add/remove fields of your choice.

    _compare_fields = copy.copy(_attrs_filter)
    _compare_fields.remove('name')

    It does not compare fields when the other object has it None or undefined.
    """
    _compare_fields = []

    def __eq__(self, o: object) -> bool:
        """ Do not compare fields when None. """
        assert isinstance(o, type(self))
        result = [getattr(self, f) == getattr(o, f)
                  for f in self._compare_fields
                  if getattr(self, f, None) is not None
                  and getattr(o, f, None) is not None
                  ]
        return all(result)

    def __init__(self):
        if not hasattr(self, '_attrs_ignore_empty'):
            self._attrs_ignore_empty = False

        if not self._compare_fields:
            if hasattr(self, '_attrs_filter'):
                self._compare_fields = copy.copy(self._attrs_filter)
            else:
                self._compare_fields = self.__get_my_fields()

    def __get_my_fields(self):
        inst_class_keys = (list(self.__dict__.keys()) +
                           list(self.__class__.__dict__.keys()))
        attrs_dict = OrderedDict(
            [(a, self.__getattribute__(a)) for a in inst_class_keys])

        attrs = [arg for (arg, val) in attrs_dict.items()
                 if (val is not None
                     or (val is None and not self._attrs_ignore_empty)
                     )
                 and not (arg.startswith('_') or callable(val))
                 ]
        return attrs
