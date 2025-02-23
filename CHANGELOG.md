# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [Unreleased]

### Changed
- `dict_to_object` function no longer requires target class to have a parameterless (or with default values) constructor.
- Allow default values in class definitions.
- Raise an error with a meaningful message if an attribute is missing from source dictionary and has no default value.
- Excess attributes in the source dictionary now raise an error instead of being ignored.

## [1.0.0] - 2025-02-09

### Added
- Initial release with the `dict_to_object` function, enabling conversion of dictionaries to objects with type hints.
- Type safety checks for nested collections and custom class attributes.
- Support for handling and validating `Literal` types.
- Error handling for mismatched types, unsupported types (e.g., `Union`, `Optional`), and invalid literal values.
