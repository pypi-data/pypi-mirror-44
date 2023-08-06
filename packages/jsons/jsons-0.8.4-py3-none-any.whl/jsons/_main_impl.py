"""
PRIVATE MODULE: do not import (from) it directly.

This module contains the implementation of the main functions of jsons, such
as `load` and `dump`.
"""
import json
from json import JSONDecodeError
from typing import Dict, Callable, Optional, Union, Tuple, Sequence
from jsons._common_impl import (
    get_class_name,
    get_parents,
    StateHolder,
    get_cls_from_str, get_cls_and_meta, determine_precedence
)
from jsons.exceptions import (
    DecodeError,
    DeserializationError,
    JsonsError,
    SerializationError
)

VALID_TYPES = (str, int, float, bool, list, tuple, set, dict, type(None))
RFC3339_DATETIME_PATTERN = '%Y-%m-%dT%H:%M:%S'


def dump(obj: object,
         cls: Optional[type] = None,
         fork_inst: Optional[type] = StateHolder,
         **kwargs) -> object:
    """
    Serialize the given ``obj`` to a JSON equivalent type (e.g. dict, list,
    int, ...).

    The way objects are serialized can be finetuned by setting serializer
    functions for the specific type using ``set_serializer``.

    You can also provide ``cls`` to specify that ``obj`` needs to be serialized
    as if it was of type ``cls`` (meaning to only take into account attributes
    from ``cls``). The type ``cls`` must have a ``__slots__`` defined. Any type
    will do, but in most cases you may want ``cls`` to be a base class of
    ``obj``.
    :param obj: a Python instance of any sort.
    :param cls: if given, ``obj`` will be dumped as if it is of type ``type``.
    :param fork_inst: if given, it uses this fork of ``JsonSerializable``.
    :param kwargs: the keyword args are passed on to the serializer function.
    :return: the serialized obj as a JSON type.
    """
    if cls and not hasattr(cls, '__slots__'):
        raise SerializationError('Invalid type: "{}". Only types that have a '
                                 '__slots__ defined are allowed when '
                                 'providing "cls".'
                         .format(get_class_name(cls, fork_inst=fork_inst,
                                                fully_qualified=True)))
    cls_ = cls or obj.__class__
    serializer = _get_serializer(cls_, fork_inst)
    kwargs_ = {
        'fork_inst': fork_inst,
        **kwargs
    }
    announce_class(cls_, fork_inst=fork_inst)
    try:
        return serializer(obj, cls=cls, **kwargs_)
    except Exception as err:
        raise SerializationError(str(err))


def load(json_obj: object,
         cls: Optional[type] = None,
         strict: bool = False,
         fork_inst: Optional[type] = StateHolder,
         attr_getters: Optional[Dict[str, Callable[[], object]]] = None,
         **kwargs) -> object:
    """
    Deserialize the given ``json_obj`` to an object of type ``cls``. If the
    contents of ``json_obj`` do not match the interface of ``cls``, a
    DeserializationError is raised.

    If ``json_obj`` contains a value that belongs to a custom class, there must
    be a type hint present for that value in ``cls`` to let this function know
    what type it should deserialize that value to.


    **Example**:

    >>> from typing import List
    >>> import jsons
    >>> class Person:
    ...     # No type hint required for name
    ...     def __init__(self, name):
    ...         self.name = name
    >>> class Family:
    ...     # Person is a custom class, use a type hint
    ...         def __init__(self, persons: List[Person]):
    ...             self.persons = persons
    >>> loaded = jsons.load({'persons': [{'name': 'John'}]}, Family)
    >>> loaded.persons[0].name
    'John'

    If no ``cls`` is given, a dict is simply returned, but contained values
    (e.g. serialized ``datetime`` values) are still deserialized.

    If `strict` mode is off and the type of `json_obj` exactly matches `cls`
    then `json_obj` is simply returned.

    :param json_obj: the dict that is to be deserialized.
    :param cls: a matching class of which an instance should be returned.
    :param strict: a bool to determine if the deserializer should be strict
    (i.e. fail on a partially deserialized `json_obj` or on `None`).
    :param fork_inst: if given, it uses this fork of ``JsonSerializable``.
    :param attr_getters: a ``dict`` that may hold callables that return values
    for certain attributes.
    :param kwargs: the keyword args are passed on to the deserializer function.
    :return: an instance of ``cls`` if given, a dict otherwise.
    """
    if _should_skip(json_obj, cls, strict):
        return json_obj
    if isinstance(cls, str):
        cls = get_cls_from_str(cls, json_obj, fork_inst)
    cls, meta_hints = _check_and_get_cls_and_meta_hints(
        json_obj, cls, fork_inst, kwargs.get('_inferred_cls', False))

    deserializer = _get_deserializer(cls, fork_inst)
    kwargs_ = {
        'strict': strict,
        'fork_inst': fork_inst,
        'attr_getters': attr_getters,
        'meta_hints': meta_hints,
        **kwargs
    }
    try:
        return deserializer(json_obj, cls, **kwargs_)
    except Exception as err:
        if isinstance(err, JsonsError):
            raise
        raise DeserializationError(str(err), json_obj, cls)


def _should_skip(json_obj: object, cls: type, strict: bool):
    if not strict and (json_obj is None or type(json_obj) == cls):
        return True


def _get_serializer(cls: type,
                    fork_inst: Optional[type] = StateHolder) -> callable:
    serializer = _get_lizer(cls, fork_inst._serializers,
                            fork_inst._classes_serializers, fork_inst)
    return serializer


def _get_deserializer(cls: type,
                      fork_inst: Optional[type] = StateHolder) -> callable:
    deserializer = _get_lizer(cls, fork_inst._deserializers,
                              fork_inst._classes_deserializers, fork_inst)
    return deserializer


def _get_lizer(cls: type,
               lizers: Dict[str, callable],
               classes_lizers: list,
               fork_inst: type) -> callable:
    cls_name = get_class_name(cls, str.lower, fork_inst=fork_inst,
                              fully_qualified=True)
    lizer = lizers.get(cls_name, None)
    if not lizer:
        parents = get_parents(cls, classes_lizers)
        if parents:
            pname = get_class_name(parents[0], str.lower, fork_inst=fork_inst,
                                   fully_qualified=True)
            lizer = lizers[pname]
    return lizer


def dumps(obj: object,
          jdkwargs: Optional[Dict[str, object]] = None,
          *args,
          **kwargs) -> str:
    """
    Extend ``json.dumps``, allowing any Python instance to be dumped to a
    string. Any extra (keyword) arguments are passed on to ``json.dumps``.

    :param obj: the object that is to be dumped to a string.
    :param jdkwargs: extra keyword arguments for ``json.dumps`` (not
    ``jsons.dumps``!)
    :param args: extra arguments for ``jsons.dumps``.
    :param kwargs: Keyword arguments that are passed on through the
    serialization process.
    passed on to the serializer function.
    :return: ``obj`` as a ``str``.
    """
    jdkwargs = jdkwargs or {}
    dumped = dump(obj, *args, **kwargs)
    return json.dumps(dumped, **jdkwargs)


def loads(str_: str,
          cls: Optional[type] = None,
          jdkwargs: Optional[Dict[str, object]] = None,
          *args,
          **kwargs) -> object:
    """
    Extend ``json.loads``, allowing a string to be loaded into a dict or a
    Python instance of type ``cls``. Any extra (keyword) arguments are passed
    on to ``json.loads``.

    :param str_: the string that is to be loaded.
    :param cls: a matching class of which an instance should be returned.
    :param jdkwargs: extra keyword arguments for ``json.loads`` (not
    ``jsons.loads``!)
    :param args: extra arguments for ``jsons.loads``.
    :param kwargs: extra keyword arguments for ``jsons.loads``.
    :return: a JSON-type object (dict, str, list, etc.) or an instance of type
    ``cls`` if given.
    """
    jdkwargs = jdkwargs or {}
    try:
        obj = json.loads(str_, **jdkwargs)
    except JSONDecodeError as err:
        raise DecodeError('Could not load a dict; the given string is not '
                          'valid JSON.', str_, cls, err)
    else:
        return load(obj, cls, *args, **kwargs)


def dumpb(obj: object,
          encoding: str = 'utf-8',
          jdkwargs: Optional[Dict[str, object]] = None,
          *args,
          **kwargs) -> bytes:
    """
    Extend ``json.dumps``, allowing any Python instance to be dumped to bytes.
    Any extra (keyword) arguments are passed on to ``json.dumps``.

    :param obj: the object that is to be dumped to bytes.
    :param encoding: the encoding that is used to transform to bytes.
    :param jdkwargs: extra keyword arguments for ``json.dumps`` (not
    ``jsons.dumps``!)
    :param args: extra arguments for ``jsons.dumps``.
    :param kwargs: Keyword arguments that are passed on through the
    serialization process.
    passed on to the serializer function.
    :return: ``obj`` as ``bytes``.
    """
    jdkwargs = jdkwargs or {}
    dumped_dict = dump(obj, *args, **kwargs)
    dumped_str = json.dumps(dumped_dict, **jdkwargs)
    return dumped_str.encode(encoding=encoding)


def loadb(bytes_: bytes,
          cls: Optional[type] = None,
          encoding: str = 'utf-8',
          jdkwargs: Optional[Dict[str, object]] = None,
          *args,
          **kwargs) -> object:
    """
    Extend ``json.loads``, allowing bytes to be loaded into a dict or a Python
    instance of type ``cls``. Any extra (keyword) arguments are passed on to
    ``json.loads``.

    :param bytes_: the bytes that are to be loaded.
    :param cls: a matching class of which an instance should be returned.
    :param encoding: the encoding that is used to transform from bytes.
    :param jdkwargs: extra keyword arguments for ``json.loads`` (not
    ``jsons.loads``!)
    :param args: extra arguments for ``jsons.loads``.
    :param kwargs: extra keyword arguments for ``jsons.loads``.
    :return: a JSON-type object (dict, str, list, etc.) or an instance of type
    ``cls`` if given.
    """
    if not isinstance(bytes_, bytes):
        raise DeserializationError('loadb accepts bytes only, "{}" was given'
                                   .format(type(bytes_)), bytes_, cls)
    jdkwargs = jdkwargs or {}
    str_ = bytes_.decode(encoding=encoding)
    return loads(str_, cls, jdkwargs=jdkwargs, *args, **kwargs)


def set_serializer(func: callable,
                   cls: Union[type, Sequence[type]],
                   high_prio: bool = True,
                   fork_inst: type = StateHolder) -> None:
    """
    Set a serializer function for the given type. You may override the default
    behavior of ``jsons.load`` by setting a custom serializer.

    The ``func`` argument must take one argument (i.e. the object that is to be
    serialized) and also a ``kwargs`` parameter. For example:

    >>> def func(obj, **kwargs):
    ...    return dict()

    You may ask additional arguments between ``cls`` and ``kwargs``.

    :param func: the serializer function.
    :param cls: the type or sequence of types this serializer can handle.
    :param high_prio: determines the order in which is looked for the callable.
    :param fork_inst: if given, it uses this fork of ``JsonSerializable``.
    :return: None.
    """
    if isinstance(cls, Sequence):
        for cls_ in cls:
            set_serializer(func, cls_, high_prio, fork_inst)
    elif cls:
        index = 0 if high_prio else len(fork_inst._classes_serializers)
        fork_inst._classes_serializers.insert(index, cls)
        cls_name = get_class_name(cls, fork_inst=fork_inst,
                                  fully_qualified=True)
        fork_inst._serializers[cls_name.lower()] = func
    else:
        fork_inst._serializers['nonetype'] = func


def set_deserializer(func: callable,
                     cls: Union[type, Sequence[type]],
                     high_prio: bool = True,
                     fork_inst: type = StateHolder) -> None:
    """
    Set a deserializer function for the given type. You may override the
    default behavior of ``jsons.dump`` by setting a custom deserializer.

    The ``func`` argument must take two arguments (i.e. the dict containing the
    serialized values and the type that the values should be deserialized into)
    and also a ``kwargs`` parameter. For example:

    >>> def func(dict_, cls, **kwargs):
    ...    return cls()

    You may ask additional arguments between ``cls`` and ``kwargs``.

    :param func: the deserializer function.
    :param cls: the type or sequence of types this serializer can handle.
    :param high_prio: determines the order in which is looked for the callable.
    :param fork_inst: if given, it uses this fork of ``JsonSerializable``.
    :return: None.
    """
    if isinstance(cls, Sequence):
        for cls_ in cls:
            set_deserializer(func, cls_, high_prio, fork_inst)
    elif cls:
        index = 0 if high_prio else len(fork_inst._classes_deserializers)
        fork_inst._classes_deserializers.insert(index, cls)
        cls_name = get_class_name(cls, fork_inst=fork_inst,
                                  fully_qualified=True)
        fork_inst._deserializers[cls_name.lower()] = func
    else:
        fork_inst._deserializers['nonetype'] = func


def suppress_warnings(
        do_suppress: Optional[bool] = True,
        fork_inst: Optional[type] = StateHolder):
    """
    Suppress (or stop suppressing) warnings.
    :param do_suppress: if ``True``, warnings will be suppressed from now on.
    :param fork_inst: if given, it uses this fork of ``JsonSerializable``.
    :return: None.
    """
    fork_inst._suppress_warnings = do_suppress


def announce_class(
        cls: type,
        cls_name: Optional[str] = None,
        fork_inst: type = StateHolder):
    """
    Announce the given cls to jsons to allow jsons to deserialize a verbose
    dump into that class.
    :param cls: the class that is to be announced.
    :param cls_name: a custom name for that class.
    :param fork_inst: if given, it uses this fork of ``JsonSerializable``.
    :return: None.
    """
    cls_name = cls_name or get_class_name(cls, fully_qualified=True,
                                          fork_inst=fork_inst)
    fork_inst._announced_classes[cls] = cls_name
    fork_inst._announced_classes[cls_name] = cls


def _check_and_get_cls_and_meta_hints(
        json_obj: object,
        cls: type,
        fork_inst: type,
        inferred_cls: bool) -> Tuple[type, Optional[dict]]:
    # Check if json_obj is of a valid type and return the cls.
    if type(json_obj) not in VALID_TYPES:
        invalid_type = get_class_name(type(json_obj), fork_inst=fork_inst,
                                      fully_qualified=True)
        valid_types = [get_class_name(typ, fork_inst=fork_inst,
                                      fully_qualified=True)
                       for typ in VALID_TYPES]
        msg = ('Invalid type: "{}", only arguments of the following types are '
               'allowed: {}'.format(invalid_type, ", ".join(valid_types)))
        raise DeserializationError(msg, json_obj, cls)
    if json_obj is None:
        raise DeserializationError('Cannot load None with strict=True',
                                   json_obj, cls)

    cls_from_meta, meta = get_cls_and_meta(json_obj, fork_inst)
    meta_hints = meta.get('classes', {}) if meta else {}
    return determine_precedence(
        cls, cls_from_meta, type(json_obj), inferred_cls), meta_hints
