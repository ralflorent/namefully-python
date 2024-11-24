# namefully

[![PyPI version][version-img]][version-url]
[![Downloads][downloads-img]][version-url]
[![CI build][ci-img]][ci-url]
[![License][license-img]][license-url]

Name handling made easy.

## Installation

```bash
pip install namefully
```

> **Note**: Python 3.7+ is required.

## Usage

```python
>>> from namefully import Namefully
>>> name = Namefully('Thomas Alva Edison')
>>> name.short
'Thomas Edison'
>>> name.public
'Thomas E'
>>> name.initials(with_mid=True)
['T', 'A', 'E']
>>> name.format('L, f m')
'EDISON, Thomas Alva'
>>> name.zip()
'Thomas A. E.'
```

> **NOTE**: if you intend to use this utility for non-standard name cases such as
> many middle names or last names, some extra work is required. For example,
> using `Namefully.parse()` lets you parse names containing many middle names
> with the risk of throwing a `NameError` when the parsing is not possible.

See [examples] or [test cases] for more details.

## Additional Settings

Below are enlisted additional settings supported by `namefully`. Use the following
keyword arguments to customize the output of the name parts.

### ordered_by

`first_name | last_name` - default: `first_name`

`ordered_by` specifies the order of name pieces when provided as raw string values
or string array values.

```python
>>> from namefully import Namefully
>>> name = Namefully('Smith John Joe', ordered_by='last_name')
>>> name.last
'Smith'
>>> name = Namefully(['Edison', 'Thomas'], ordered_by='last_name')
>>> name.first
'Thomas'
```

> **Note**: The order of appearance set initially will be prioritized in other
> operations. However, it can be adjusted dynamically as needed. See the example below.

```python
>>> from namefully import Namefully
>>> name = Namefully('Smith John Joe', ordered_by='last_name')
>>> name.full
'Smith John Joe'
>>> name.full_name(ordered_by='first_name')
'John Joe Smith'
```

### separator

`'' | , | : | " | - | . | ; | ' | ' ' | _]` - default: `' '` (white space)

Supported separators are: empty, comma, colon, double quotes, hyphen, period,
semicolon, single quote, white space, and underscore.
Though _only valid for raw string values_, `separator` indicates how to split the
parts of a raw string name under the hood. If you want more control, use a custom
`Parser`.

```python
>>> from namefully import Namefully
>>> name = Namefully('John,Smith', separator=',')
>>> name.full
'John Smith'
```

### title

`uk | us` - default: `uk`

`title` abides by the ways the international community defines an abbreviated title.
American and Canadian English follow slightly different rules for abbreviated
titles than British and Australian English. In North American English, titles
before a name require a period: `Mr., Mrs., Ms., Dr.`. In British and Australian
English, no periods are used in these abbreviations.

```python
>>> from namefully import Namefully
>>> name = Namefully.only(prefix='Mr', first='John', last='Smith', title='us')
>>> name.full
'Mr. John Smith'
>>> name.prefix
'Mr.'
```

### ending

`bool` - default: `False`

This sets an ending character after the full name (a comma before the suffix actually).

```python
>>> from namefully import Namefully
>>> name = Namefully.only('John', 'Smith', suffix='PhD', ending=True)
>>> name.full
'John Smith, PhD'
>>> name.suffix
'PhD'
```

### surname

`father | mother | hyphenated | all` - default: `father`

`surname` defines the distinct formats to output a compound surname (e.g., Hispanic surnames).

```python
>>> from namefully import Namefully, FirstName, LastName
>>> name = Namefully([FirstName('John'), LastName('Doe', 'Smith')], surname='hyphenated')
>>> name.full
'John Doe-Smith'
```

### bypass

`bool` - default: `True`

This will bypass all the built-in validators (i.e., validation rules, regular expressions).

```python
>>> from namefully import Namefully
>>> name = Namefully.only('Jane', 'Smith', suffix='M.Sc', bypass=False)
Traceback (most recent call last):
  ...
ValidationError (suffix='M.Sc'): invalid content
```

To sum it all up, the default values are:

```python
>>> from namefully import Config
>>> config = Config.create()
>>> config
<Config: default>
>>> config.to_dict()
{'name': 'default', 'ordered_by': 'first_name', 'separator': ' ', 'title': 'uk', 'ending': False, 'bypass': False, 'surname': 'father'}
```

## Do It Yourself

Customize your own parser to indicate the full name yourself.

```python
from namefully import Namefully, Parser, FullName

class SimpleParser(Parser):
    def parse(self, **options) -> FullName:
        fn, ln = self.raw.split('#')
        return FullName.parse({'first_name': fn, 'last_name': ln}, **options)

name = Namefully(SimpleParser('Juan#Garcia'))
print(name.full)  # Juan Garcia
```

## Concepts and examples

The name standards used for the current version of this library are as follows:

`[prefix] first_name [middle_name] last_name [suffix]`

The opening `[` and closing `]` brackets mean that these parts are optional. In
other words, the most basic/typical case is a name that looks like this:
`John Smith`, where `John` is the _firstName_ and `Smith`, the _lastName_.

> **NOTE**: Do note that the order of appearance matters and (as shown in [ordered_by](#ordered_by))
> can be altered through configured parameters. By default, the order of appearance
> is as shown above and will be used as a basis for future examples and use cases.

### Basic cases

Let us take a common example:

`Mr John Joe Smith PhD`

So, this utility understands the name parts as follows:

- prefix: `Mr`
- first name: `John`
- middle name: `Joe`
- last name: `Smith`
- suffix: `PhD`
- full name: `Mr John Joe Smith PhD`
- birth name: `John Joe Smith`
- short version: `John Smith`
- flattened: `John J. S.`
- initials: `J J S`
- public: `John S`
- salutation: `Mr Smith`

### Limitations

`namefully` does not support certain use cases:

- mononame: `Plato` - a workaround is to set the mononame as both first and last name;
- multiple prefixes or suffixes: `Prof. Dr. Einstein`.

## Contributing

Visit [CONTRIBUTING.md][contributing-url] for details on the contribution guidelines,
the code of conduct, and the process for submitting pull requests.

## License

The underlying content of this utility is licensed under [MIT][license-url].

<!-- References -->

[version-img]: https://img.shields.io/pypi/v/namefully
[version-url]: https://pypi.python.org/pypi/namefully
[license-img]: https://img.shields.io/pypi/l/namefully
[license-url]: https://github.com/ralflorent/namefully-python/blob/main/LICENSE
[downloads-img]: https://img.shields.io/pypi/dm/namefully
[ci-img]: https://github.com/ralflorent/namefully-python/workflows/Build/badge.svg
[ci-url]: https://github.com/ralflorent/namefully-python/actions/workflows/build.yml

[contributing-url]: https://github.com/ralflorent/namefully-python/blob/main/CONTRIBUTING.md
[examples]: https://github.com/ralflorent/namefully-python/blob/main/examples/main.py
[test cases]:https://github.com/ralflorent/namefully-python/blob/main/test
