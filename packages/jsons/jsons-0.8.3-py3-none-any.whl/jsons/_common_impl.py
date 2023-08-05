"""
PRIVATE MODULE: do not import (from) it directly.

This module contains implementations of common functionality that can be used
throughout `jsons`.
"""
import warnings
from importlib import import_module
from typing import Callable, Optional
from jsons.exceptions import UnknownClassError

META_ATTR = '-meta'  # The name of the attribute holding meta info.


class StateHolder:
    """
    This class holds the registered serializers and deserializers.
    """
    _classes_serializers = list()
    _classes_deserializers = list()
    _serializers = dict()
    _deserializers = dict()
    _announced_classes = dict()
    _suppress_warnings = False

    @classmethod
    def _warn(cls, msg, *args, **kwargs):
        if not cls._suppress_warnings:
            msg_ = ('{} You can suppress warnings like this using '
                    'jsons.suppress_warnings().'.format(msg))
            warnings.warn(msg_, *args, **kwargs)


def get_class_name(cls: type,
                   transformer: Optional[Callable[[str], str]] = None,
                   fully_qualified: bool = False,
                   fork_inst: Optional[type] = StateHolder) -> Optional[str]:
    """
    Return the name of a class.
    :param cls: the class of which the name if to be returned.
    :param transformer: any string transformer, e.g. ``str.lower``.
    :param fully_qualified: if ``True`` return the fully qualified name (i.e.
    complete with module name).
    :param fork_inst if given, it uses this fork of ``JsonSerializable`` for
    finding the class name.
    :return: the name of ``cls``, transformed if a transformer is given.
    """
    if cls in fork_inst._announced_classes:
        return fork_inst._announced_classes[cls]
    cls_name = _get_simple_name(cls)
    module = _get_module(cls)
    transformer = transformer or (lambda x: x)
    if not cls_name and hasattr(cls, '__origin__'):
        origin = cls.__origin__
        cls_name = get_class_name(origin, transformer,
                                  fully_qualified, fork_inst)
    if not cls_name:
        cls_name = str(cls)
    if fully_qualified and module:
        cls_name = '{}.{}'.format(module, cls_name)
    cls_name = transformer(cls_name)
    return cls_name


def get_cls_from_str(cls_str: str, source: object, fork_inst) -> type:
    try:
        splitted = cls_str.split('.')
        module_name = '.'.join(splitted[:-1])
        cls_name = splitted[-1]
        cls_module = import_module(module_name)
        cls = getattr(cls_module, cls_name)
        if not cls or not isinstance(cls, type):
            cls = _lookup_announced_class(cls_str, source, fork_inst)
    except (ImportError, AttributeError, ValueError):
        cls = _lookup_announced_class(cls_str, source, fork_inst)
    return cls


def _lookup_announced_class(
        cls_str: str,
        source: object,
        fork_inst: type) -> type:
    cls = fork_inst._announced_classes.get(cls_str)
    if not cls:
        msg = ('Could not find a suitable type for "{}". Make sure it can be '
               'imported or that is has been announced.'.format(cls_str))
        raise UnknownClassError(msg, source, cls_str)
    return cls


def _get_simple_name(cls: type) -> str:
    cls_name = getattr(cls, '__name__', None)
    if not cls_name:
        cls_name = getattr(cls, '_name', None)
    if not cls_name:
        cls_name = repr(cls)
        cls_name = cls_name.split('[')[0]  # Remove generic types.
        cls_name = cls_name.split('.')[-1]  # Remove any . caused by repr.
    return cls_name


def _get_module(cls: type) -> Optional[str]:
    builtin_module = str.__class__.__module__
    module = cls.__module__
    if module and module != builtin_module:
        return module


def get_parents(cls: type, lizers: list) -> list:
    """
    Return a list of serializers or deserializers that can handle a parent
    of ``cls``.
    :param cls: the type that
    :param lizers: a list of serializers or deserializers.
    :return: a list of serializers or deserializers.
    """
    parents = []
    for cls_ in lizers:
        try:
            if issubclass(cls, cls_):
                parents.append(cls_)
        except TypeError:
            pass  # Some types do not support `issubclass` (e.g. Union).
    return parents
