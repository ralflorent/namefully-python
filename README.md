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

## Additional Settings

Below are enlisted the options supported by `namefully`.

### ordered_by

`first_name | last_name` - default: `first_name`

Indicates the order in which names appear when provided as raw string values or
string array values. The first element can either be the given name (e.g., `Jon Snow`)
or the surname (e.g., `Snow Jon`).

```python
>>> from namefully import Namefully
>>> name = Namefully('Smith John Joe', ordered_by='last_name')
>>> name.last
'Smith'
>>> name = Namefully(['Edison', 'Thomas'], ordered_by='last_name')
>>> name.first
'Thomas'
```

> **NOTE**: This option also affects all the other results of the API. In other
> words, the results will prioritize the order of appearance set in the first
> place for the other operations. Keep in mind that in some cases, it can be
> altered on the go. See the example below.

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

Potential separators are: empty, comma, colon, double quotes, hyphen, period,
semicolon, single quote, white space, and underscore.

_Only valid for raw string values_, this option indicates how to split the parts
of a raw string name under the hood.

```python
>>> from namefully import Namefully
>>> name = Namefully('John,Smith', separator=',')
>>> name.full
'John Smith'
```

### title

`uk | us` - default: `uk`

Abides by the ways the international community defines an abbreviated title.
American and Canadian English follow slightly different rules for abbreviated
titles than British and Australian English. In North American English, titles
before a name require a period: `Mr., Mrs., Ms., Dr.`. In British and Australian
English, no periods are used in these abbreviations.

```python
>>> from namefully import Namefully
>>> name = Namefully.only(first_name='John', last_name='Smith', prefix='Mr', title='us')
>>> name.full
'Mr. John Smith'
>>> name.prefix
'Mr.'
```

### ending

`bool` - default: `False`

Sets an ending character after the full name (a comma before the suffix actually).

```python
>>> from namefully import Namefully
>>> name = Namefully.only(first_name='John', last_name='Smith', suffix='PhD', ending=True)
>>> name.full
'John Smith, PhD'
>>> name.suffix
'PhD'
```

### surname

`father | mother | hyphenated | all` - default: `father`

Defines the distinct formats to output a compound surname (e.g., Hispanic surnames).

```python
>>> from namefully import Namefully, FirstName, LastName
>>> name = Namefully([FirstName('John'), LastName('Doe', 'Smith')], surname='hyphenated')
>>> name.full
'John Doe-Smith'
```

### bypass

`bool` - default: `True`

Skips all the validators (i.e., validation rules, regular expressions).

```python
>>> from namefully import Namefully
>>> name = Namefully({'first_name': 'John', 'last_name': 'Smith', 'suffix': 'MSc'}, bypass=False)
Traceback (most recent call last):
  ...
NameError: The suffix 'MSc' is not valid.
```

To sum it all up, the default values are:

```python
{
   'ordered_by': 'first_name',
   'separator': ' ',
   'title': 'uk',
   'ending': False,
   'bypass': True,
   'surname': 'father'
}
```

## Do It Yourself

Customize your own parser to indicate the full name yourself.

```python
from namefully import Namefully, Parser, FullName

class SimpleParser(Parser):
    def parse(self, **options) -> FullName:
        first_name, last_name = self.raw.split('#')
        return FullName.parse({'first_name': first_name, 'last_name': last_name}, options)

name = Namefully(SimpleParser('Juan#Garcia'))
print(name.full)  # Juan Garcia
```

## Concepts and examples

The name standards used for the current version of this library are as follows:

`[prefix] first_name [middle_name] last_name [suffix]`

The opening `[` and closing `]` brackets mean that these parts are optional. In
other words, the most basic/typical case is a name that looks like this:
`John Smith`, where `John` is the _firstName_ and `Smith`, the _lastName_.

> NOTE: Do notice that the order of appearance matters and (as shown in
> [ordered_by](#ordered_by)) can be altered through configured parameters. By default,
> the order of appearance is as shown above and will be used as a basis for
> future examples and use cases.

Once imported, all that is required to do is to create an instance of
`Namefully` and the rest will follow.

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

`namefully` does not have support for certain use cases:

- mononame: `Plato`. A workaround is to set the mononame as both first and last name;
- multiple prefixes: `Prof. Dr. Einstein`.

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
[ci-img]: https://github.com/ralflorent/namefully-python/workflows/CI/badge.svg
[ci-url]: https://github.com/ralflorent/namefully-python/actions/workflows/ci.yml

[contributing-url]: https://github.com/ralflorent/namefully-python/blob/main/CONTRIBUTING.md
