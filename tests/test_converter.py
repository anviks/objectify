import sys
from dataclasses import dataclass
from typing import Any, TypeVar

import pytest

from objectify import dict_to_object

T = TypeVar('T')


def test__primitive_types():
    class Test:
        a: int
        b: str
        c: float
        d: bool
        e: None

    obj = dict_to_object({'a': 1, 'b': 'xyz', 'c': 3.0, 'd': True, 'e': None}, Test)

    assert obj.a == 1
    assert obj.b == 'xyz'
    assert obj.c == 3.0
    assert obj.d is True
    assert obj.e is None


def test__convert_to_dataclass_type__no_init():
    @dataclass(init=False)
    class Test:
        a: int
        b: str
        c: float
        d: bool
        e: None

    obj = dict_to_object({'a': 1, 'b': 'xyz', 'c': 3.0, 'd': True, 'e': None}, Test)

    assert obj.a == 1
    assert obj.b == 'xyz'
    assert obj.c == 3.0
    assert obj.d is True
    assert obj.e is None


def test__collection_types():
    class Test:
        a: list[int]
        b: set[str]
        c: tuple[float, ...]
        d: dict[str, bool]

    obj = dict_to_object({
        'a': [1, 2, 3],
        'b': {'x', 'y', 'z'},
        'c': (1.0, 2.0, 3.0),
        'd': {'x': True, 'y': False}
    }, Test)

    assert obj.a == [1, 2, 3]
    assert obj.b == {'x', 'y', 'z'}
    assert obj.c == (1.0, 2.0, 3.0)
    assert obj.d == {'x': True, 'y': False}


def test__empty_tuple_type__given_empty_tuple():
    class Test:
        a: tuple[()]

    obj = dict_to_object({'a': ()}, Test)

    assert obj.a == ()


def test__empty_tuple_type__given_populated_tuple():
    class Test:
        a: tuple[()]

    with pytest.raises(Exception):
        dict_to_object({'a': (1, 2, 3)}, Test)


@pytest.mark.parametrize('value,clazz', [
    ((), int),
    ((1,), int),
    ((1, 2, 3), int),
    ((), str),
    (('a',), str),
    (('a', 'b', 'c'), str),
    ((), float),
    ((1.0,), float),
    ((1.0, 2.0, 3.0), float),
    ((), bool),
    ((True,), bool),
    ((True, False, True), bool),
    ((), None),
    ((None,), None),
    ((None, None, None), None),
])
def test__variable_length_tuple_type__valid(value: tuple[Any, ...], clazz: type[Any]):
    class Test:
        a: tuple[clazz, ...]

    obj = dict_to_object({'a': value}, Test)

    assert obj.a == value


@pytest.mark.parametrize('value,clazz', [
    ((1, 2, 'a'), int),
    ((1, 2, 3), str),
    ((1.0, 2.0, 'a'), float),
    ((1.0, 2.0, 3.0), bool),
    ((True, False, 'a'), bool),
    ((True, False, True), None),
    ((None, None, 'a'), None),
    ((None, None, None), int),
    ((1, 2, 3), str),
    ((1.0, 2.0, 3.0), bool),
    ((True, False, True), None),
    ((None, None, None), int),
])
def test__variable_length_tuple_type__invalid(value: tuple[Any, ...], clazz: type[Any]):
    class Test:
        a: tuple[clazz, ...]

    with pytest.raises(Exception):
        dict_to_object({'a': value}, Test)


@pytest.mark.parametrize('value,clazz', [
    ((1,), tuple[int]),
    ((1, 2, 3), tuple[int, int, int]),
    (('a',), tuple[str]),
    (('a', 'b', 'c'), tuple[str, str, str]),
    ((1.0,), tuple[float]),
    ((1.0, 2.0, 3.0), tuple[float, float, float]),
    ((True,), tuple[bool]),
    ((True, False, True), tuple[bool, bool, bool]),
    ((None,), tuple[None]),
    ((None, None, None), tuple[None, None, None]),
    ((1, 'abc', 3.0, False, None), tuple[int, str, float, bool, None]),
])
def test__fixed_length_tuple_type__valid(value: tuple[Any, ...], clazz: type[Any]):
    class Test:
        a: clazz

    obj = dict_to_object({'a': value}, Test)

    assert obj.a == value


@pytest.mark.parametrize('value,clazz', [
    ((1, 2, 'a'), tuple[int, int, int]),
    ((1, 2, 3), tuple[str, str, str]),
    (('a', 'b', 'c'), tuple[str, str]),
    (('a', 'b', 'c'), tuple[str, str, str, str]),
    ((1.0, 2.0, 'a'), tuple[float, float, float]),
    ((1.0, 2.0, 3.0), tuple[bool, bool, bool]),
    ((1.0, 2.0, 3.0), tuple[float, float, float, float]),
    ((True, False, 'a'), tuple[bool, bool, bool]),
    ((True, False, True), tuple[None, None, None]),
    ((None, None, 'a'), tuple[int, int, int]),
    ((None, None, None), tuple[str, str, str]),
    ((1, 2, 3), tuple[float, float, float]),
    ((1.0, 2.0, 3.0), tuple[bool, bool, bool]),
    ((True, False, True), tuple[None, None, None]),
    ((None, None, None), tuple[int, int, int]),
    ((1, 'abc', 3.0, False, None), tuple[int, str, float, str, None]),
])
def test__fixed_length_tuple_type__invalid(value: tuple[Any, ...], clazz: type[Any]):
    class Test:
        a: clazz

    with pytest.raises(Exception):
        dict_to_object({'a': value}, Test)


def test__nested_dataclass():
    @dataclass(init=False)
    class Test:
        a: int

    @dataclass(init=False)
    class Nested:
        b: Test

    obj = dict_to_object({'b': {'a': 1}}, Nested)

    assert obj.b.a == 1


def test__nested_dataclass__with_list():
    @dataclass(init=False)
    class Test:
        a: int

    @dataclass(init=False)
    class Nested:
        b: list[Test]

    obj = dict_to_object({'b': [{'a': 1}, {'a': 2}, {'a': 3}]}, Nested)

    assert obj.b[0].a == 1
    assert obj.b[1].a == 2
    assert obj.b[2].a == 3


def test__nested_local_dataclass():
    @dataclass(init=False)
    class Nested:
        a: int
        b: 'Test'

        @dataclass(init=False)
        class Test:
            c: str

    obj = dict_to_object({'a': 1, 'b': {'c': 'xyz'}}, Nested)

    assert obj.a == 1
    assert obj.b.c == 'xyz'


@pytest.mark.skipif(
    sys.version_info < (3, 11),
    reason="Before Python 3.11, 'Test' in list['Test'] does not resolve correctly into a class."
)
def test__nested_local_dataclass__with_list():
    @dataclass(init=False)
    class Nested:
        a: int
        b: list['Test']

        @dataclass(init=False)
        class Test:
            c: str

    obj = dict_to_object({'a': 1, 'b': [{'c': 'xyz'}, {'c': 'abc'}, {'c': '123'}]}, Nested)

    assert obj.a == 1
    assert obj.b[0].c == 'xyz'
    assert obj.b[1].c == 'abc'
    assert obj.b[2].c == '123'


def test__nested_list():
    class Test:
        a: list[list[int]]

    obj = dict_to_object({'a': [[1, 2, 3], [4, 5, 6], [7, 8, 9]]}, Test)

    assert obj.a == [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
