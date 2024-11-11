# namefully

[![PyPI version][version-img]][version-url]

A Python utility for handling person names.

## Motivation

Have you ever had to format a user's name in a particular order, way, or shape?
Probably yes. If not, it will come at some point. Be patient.

You may want to use this library if:

- you've been repeatedly dealing with users' given names and surnames;
- you need to occasionally format a name in a particular order, way, or shape;
- you keep copy-pasting your name-related business logic for every project;
- you're curious about trying new, cool stuff (e.g., learning Dart).

## Key features

1. Accept different data shapes as input
2. Use optional parameters to access advanced features
3. Format a name as desired
4. Offer support for prefixes and suffixes
5. Access to names' initials
6. Support hyphenated names (and other special characters)
7. Offer predefined validation rules for many writing systems, including the
   Latin and European ones (e.g., German, Greek, Cyrillic, Icelandic characters)

## Advanced features

1. Alter the name order anytime
2. Handle various parts of a surname and a given name
3. Use tokens (separators) to reshape prefixes and suffixes
4. Accept customized parsers (do it yourself)
5. Build a name on the fly (via a builder)
6. Parse non-standard name cases

## Installation

```bash
pip install namefully
```

## Dependencies

None

## Usage

```python
from namefully import Namefully

name = Namefully('Thomas Alva Edison')
print(name.short)  # Thomas Edison
print(name.public)  # Thomas E
print(name.initials(with_mid=True))  # ['T', 'A', 'E']
print(name.format('L, f m'))  # EDISON, Thomas Alva
print(name.zip())  # Thomas A. E.
```

> NOTE: if you intend to use this utility for non-standard name cases such as
> many middle names or last names, some extra work is required. For example,
> using `Namefully.parse()` lets you parse names containing many middle names
> with the risk of throwing a `NameError` when the parsing is not possible.

## Contributing

Visit [CONTRIBUTING.md][contributing-url] for details on the contribution guidelines,
the code of conduct, and the process for submitting pull requests.

## License

The underlying content of this utility is licensed under [MIT][license-url].

<!-- References -->

[version-img]: https://badge.fury.io/py/namefully.svg
[version-url]: https://pypi.python.org/pypi/namefully
[contributing-url]: https://github.com/ralflorent/namefully-python/blob/main/CONTRIBUTING.md
[license-url]: https://github.com/ralflorent/namefully-python/blob/main/LICENSE
