# [TBD]

[TBD] is a lightweight library designed to convert a dictionary into a typed object based on a provided type argument.
It allows developers to work seamlessly with dictionaries using dot notation while benefiting from type safety, type hinting, and IDE autocompletion.

The idea behind [TBD] was inspired by TypeScript, where you can take any object, define an interface or type for it,
and "cast" the object to that type. This approach gives you immediate access to types and autocompletion, making writing code more efficient and less error-prone.

In Python, the closest existing standard solution is `TypedDict`, which provides type hints and key autocompletion for dictionaries.
However, its main drawback is that you must still access values using square brackets and string keys (e.g., `data['key']`),
which is less convenient and takes more time compared to dot notation (`data.key`).

This functionality is especially useful when working with large nested payloads (e.g., JSON responses from APIs).
By leveraging [TBD], you can easily map such data to Python objects while maintaining clarity and reducing errors.


## Features

- **Type Safety**: [TBD] ensures that the object's attributes match the specified types.
- **Custom Classes**: [TBD] supports custom classes as type arguments, allowing for more complex object structures.
- **Dataclasses**: [TBD] works seamlessly with dataclasses, providing a simple way to convert dictionaries to dataclass objects.
- **Nested Objects**: [TBD] can handle nested dictionaries and convert them to nested objects.
- **Literal Types**: [TBD] supports `Literal` types for specifying exact values that an attribute can take.
- **Error Handling**: [TBD] raises `TypeError` for mismatched types, unsupported types, and invalid literal values.

## Installation

```bash
pip install [TBD]
```

## Usage

### Simple Example
```python
from [TBD] import dict_to_object


class User:
    name: str
    age: int
    is_active: bool


data = {
    'name': 'Alice',
    'age': 30,
    'is_active': True
}

user = dict_to_object(data, User)
print(user.name)  # 'Alice'
print(user.age)  # 30
print(user.is_active)  # True
```

### Complex Example
```python
from [TBD] import dict_to_object


class Address:
    street: str
    city: str
    zip_code: int


class User:
    name: str
    age: int
    address: list[Address]


data = {
    'name': 'Alice',
    'age': 30,
    'address': [
        {'street': '123 Main St', 'city': 'Springfield', 'zip_code': 12345},
        {'street': '456 Elm St', 'city': 'Rivertown', 'zip_code': 54321}
    ]
}

user = dict_to_object(data, User)
print(user.name)  # 'Alice'
print(user.age)  # 30
print(user.address[0].street)  # '123 Main St'
print(user.address[1].city)  # 'Rivertown'
```
