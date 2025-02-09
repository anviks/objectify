import sys
import types
import typing
from typing import Any, get_type_hints, get_origin, get_args, Collection, Literal, TypeVar

__all__ = ['dict_to_object']

T = TypeVar('T')


def dict_to_object(source_dict: dict[str, Any], target_type: type[T]) -> T:
    """
    Convert a dictionary to an object of the specified type.

    This function will create an instance of the specified type and populate its attributes with the values from the
    dictionary. The dictionary keys must match the attribute names of the target type.

    The following types are supported:

    - Primitive types (str, int, float, bool, NoneType)
    - Custom classes (fields have to be defined like in dataclasses)
    - Dataclasses
    - Collection types (list, set, tuple, dict)
    - Nested collections and custom classes
    - Literal types
    - Type aliases, including TypeAliasType (Python 3.12+)

    The following types are not supported:

    - Union types
    - Optional types

    :param source_dict: The dictionary to convert to an object.
    :param target_type: The type of the object to create.
    :return:
    """
    constructor = target_type.__init__
    assert isinstance(constructor, types.FunctionType | types.WrapperDescriptorType), "Unexpected constructor type."
    target_instance = object.__new__(target_type)

    for attr, sub_type in get_type_hints(target_type).items():
        sub_source = source_dict[attr]
        sub_instance = transform_element(sub_source, sub_type)
        setattr(target_instance, attr, sub_instance)

    return target_instance


def handle_collection(source_collection: Collection[Any], _type: type):
    collection = _type()
    origin = get_origin(_type)
    type_args = get_args(_type)

    if issubclass(origin, list):
        sub_type = type_args[0]

        for sub_source in source_collection:
            sub_instance = transform_element(sub_source, sub_type)
            collection.append(sub_instance)

    elif issubclass(origin, tuple):
        if len(type_args) == 2 and type_args[1] is Ellipsis:
            sub_type = type_args[0]

            for sub_source in source_collection:
                sub_instance = transform_element(sub_source, sub_type)
                collection += (sub_instance,)

        else:
            for sub_type, sub_source in zip(type_args, source_collection, strict=True):
                sub_instance = transform_element(sub_source, sub_type)
                collection += (sub_instance,)

    elif issubclass(origin, set):
        sub_type = type_args[0]

        for sub_source in source_collection:
            sub_instance = transform_element(sub_source, sub_type)
            collection.add(sub_instance)

    elif issubclass(origin, dict):
        key_type, value_type = type_args
        assert isinstance(source_collection, dict)

        for key_source, value_source in source_collection.items():
            key_instance = transform_element(key_source, key_type)
            value_instance = transform_element(value_source, value_type)

            collection[key_instance] = value_instance

    return collection


def transform_element(sub_source: Collection[Any], sub_type: type):
    if sys.version_info >= (3, 12) and isinstance(sub_type, typing.TypeAliasType):  # novermin
        sub_type = sub_type.__value__

    if sub_type is None:
        sub_type = types.NoneType

    sub_origin = get_origin(sub_type) or sub_type

    if sub_origin in (typing.Union, types.UnionType):
        raise TypeError("Union and Optional types are not supported.")

    if sub_origin is Literal:
        if sub_source not in get_args(sub_type):
            raise ValueError(f"Value {sub_source} is not a valid literal for type {sub_type}.")
        sub_instance = sub_source
    elif is_collection_type(sub_origin):
        sub_instance = handle_collection(sub_source, sub_type)
    elif is_primitive_type(sub_type):
        assert isinstance(sub_source, sub_type)
        sub_instance = sub_source
    else:
        assert isinstance(sub_source, dict)
        sub_instance = dict_to_object(sub_source, sub_type)

    return sub_instance


def is_collection_type(origin: type):
    return issubclass(origin, list | set | tuple | dict)


def is_primitive_type(_type: type):
    return issubclass(_type, str | int | float | bool | types.NoneType)
