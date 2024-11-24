import re
from typing import List, Mapping, Optional, Sequence, Union

from ._config import Config
from ._constants import ALLOWED_TOKENS
from ._errors import NameError
from ._full_name import FullName
from ._name import FirstName, LastName, Name
from ._parser import NamaParser, Parser, SequentialNameParser, SequentialStringParser, StringParser
from ._utils import decapitalize, toggle_case


class Namefully:
    """
    A utility for organizing person names in a specific order, format, or structure.

    While `namefully` is user-friendly, it does not automatically determine which
    part of the name is which (e.g., prefix, suffix, first, last, or middle names).
    It relies on the roles assigned to each name part to perform internal operations
    and save additional processing. Additionally, `Namefully` can be created using
    various raw data formats, providing flexibility to developers without binding
    them to a specific data format. By closely following the API reference, developers
    can effectively use this utility to save time in formatting names.

    `namefully` also functions as a trapdoor. Once raw data is provided and validated,
    developers can access the name information in numerous effective ways, but
    *no editing* is possible. If the name is incorrect, a new instance of `Namefully`
    must be created, ensuring immutability. The primary objective of this utility is
    to facilitate the manipulation of person names.

    The name standards used in the current version of this library are as follows:
        `[prefix] firstName [middleName] lastName [suffix]`
    The square brackets indicate optional parts. The most basic and typical case
    is a name like `John Smith`, where `John` is the first name and `Smith` is the
    last name.

    For more information on name standards, see:
        https://departments.weber.edu/qsupport&training/Data_Standards/Name.htm

    **IMPORTANT**: The order of appearance (or name order) matters and can be altered
    through configuration parameters, which will be discussed later. By default,
    the order of appearance is as shown above and will be used as the basis for future
    examples and use cases.

    To use this utility, simply create an instance of `Namefully` and the rest will follow.

    Terminologies used throughout the library:
    - namon: a single piece of a name (e.g., first name)
    - nama: two or more pieces of a name (e.g., first name + last name)

    Happy name handling 😊!
    """

    def __init__(
        self,
        names: Union[str, Sequence[str], Sequence[Name], Mapping[str, str], FullName, Parser],
        *,
        context: Optional[str] = None,
        ordered_by: str = 'first_name',
        separator: str = ' ',
        title: str = 'uk',
        ending: bool = False,
        bypass: bool = True,
        surname: str = 'father',
    ) -> None:
        self._full_name = self.__to_parser(names).parse(
            name=context,
            ordered_by=ordered_by,
            separator=separator,
            title=title,
            ending=ending,
            bypass=bypass,
            surname=surname,
        )

    def __str__(self) -> str:
        return self.full

    def __repr__(self) -> str:
        return f'<Namefully: {self.full}>'

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Namefully) and self.full == other.full

    @staticmethod
    def parse(text: str) -> Optional['Namefully']:
        try:
            return Namefully(Parser.build(text))
        except Exception:
            return None

    @staticmethod
    def only(
        first: Union[str, FirstName],
        last: Union[str, LastName],
        *,
        prefix: Union[None, str, Name] = None,
        suffix: Union[None, str, Name] = None,
        middles: Union[None, Sequence[str], Sequence[Name]] = None,
        context: Optional[str] = None,
        ordered_by: Optional[str] = None,
        separator: Optional[str] = None,
        title: Optional[str] = None,
        ending: bool = False,
        bypass: bool = True,
        surname: Optional[str] = None,
    ) -> 'Namefully':
        full_name = FullName(
            name=context,
            ordered_by=ordered_by,
            separator=separator,
            title=title,
            ending=ending,
            bypass=bypass,
            surname=surname,
        )
        full_name.prefix = prefix
        full_name.first_name = first
        full_name.middle_name = middles or []
        full_name.last_name = last
        full_name.suffix = suffix
        return Namefully(full_name)

    @property
    def config(self) -> Config:
        return self._full_name.config

    @property
    def length(self) -> int:
        """The number of characters of the birth name, including spaces."""
        return len(self.birth)

    @property
    def size(self) -> int:
        """The number of names parts."""
        return self._full_name.size

    @property
    def has_middle(self) -> bool:
        return self._full_name.has('middle')

    @property
    def prefix(self) -> Optional[str]:
        return self._full_name.prefix.value if self._full_name.prefix else None

    @property
    def first(self) -> str:
        return self.first_name()

    @property
    def middle(self) -> Optional[str]:
        return self.middle_name()[0] if self.has_middle else None

    @property
    def last(self) -> str:
        return self.last_name()

    @property
    def suffix(self) -> Optional[str]:
        return self._full_name.suffix.value if self._full_name.suffix else None

    @property
    def birth(self) -> str:
        return self.birth_name()

    @property
    def short(self) -> str:
        return self.shorten()

    @property
    def long(self) -> str:
        return self.birth

    @property
    def full(self) -> str:
        return self.full_name()

    @property
    def parts(self):
        return self._full_name.to_iterable()

    @property
    def public(self) -> str:
        return self.format('f $l')

    @property
    def salutation(self) -> str:
        return self.format('p l')

    def get(self, namon: str) -> Union[None, Name, List[Name]]:
        if namon == 'prefix':
            return self._full_name.prefix
        elif namon == 'first_name':
            return self._full_name.first_name
        elif namon == 'middle_name':
            return self._full_name.middle_name
        elif namon == 'last_name':
            return self._full_name.last_name
        elif namon == 'suffix':
            return self._full_name.suffix
        return None

    def to_dict(self) -> Mapping[str, Union[None, str, List[str]]]:
        return {
            'prefix': self.prefix,
            'first_name': self.first,
            'middle_name': self.middle_name(),
            'last_name': self.last,
            'suffix': self.suffix,
        }

    def to_str(self) -> str:
        return self.full

    def has(self, namon: str) -> bool:
        return self._full_name.has(namon)

    def full_name(self, ordered_by: Optional[str] = None) -> str:
        sep, names = ',' if self.config.ending else '', []
        ordered_by = ordered_by or self.config.ordered_by

        if self.prefix:
            names.append(self.prefix)
        if ordered_by in ['first', 'first_name', 'firstname']:
            names.extend([self.first, *self.middle_name(), self.last + sep])
        else:
            names.extend([self.last, self.first, ' '.join(self.middle_name()) + sep])
        if self.suffix:
            names.append(self.suffix)

        return ' '.join(names).strip()

    def birth_name(self, ordered_by: Optional[str] = None) -> str:
        ordered_by = ordered_by or self.config.ordered_by
        if ordered_by in ['first', 'first_name', 'firstname']:
            return ' '.join([self.first, *self.middle_name(), self.last])
        else:
            return ' '.join([self.last, self.first, *self.middle_name()])

    def first_name(self, with_more: bool = True) -> str:
        return self._full_name.first_name.to_str(with_more=with_more)

    def middle_name(self) -> List[str]:
        return [name.value for name in self._full_name.middle_name]

    def last_name(self, format: Optional[str] = None) -> str:
        return self._full_name.last_name.to_str(format=format)

    def initials(self, ordered_by: Optional[str] = None, only: Optional[str] = None) -> List[str]:
        initials = []
        first_inits = self._full_name.first_name.initials()
        mid_inits = [n.initial for n in self._full_name.middle_name]
        last_inits = self._full_name.last_name.initials()

        ordered_by = ordered_by or self.config.ordered_by
        only = only in ['birth_name', 'first_name', 'middle_name', 'last_name'] and only or 'birth_name'

        if only != 'birth_name':
            if only == 'first_name':
                initials.extend(first_inits)
            elif only == 'middle_name':
                initials.extend(mid_inits)
            else:
                initials.extend(last_inits)
        elif ordered_by in ['first', 'first_name', 'firstname']:
            initials.extend(first_inits + mid_inits + last_inits)
        else:
            initials.extend(last_inits + first_inits + mid_inits)

        return initials

    def shorten(self, ordered_by: Optional[str] = None) -> str:
        ordered_by = ordered_by or self.config.ordered_by
        if ordered_by in ['first', 'first_name', 'firstname']:
            return ' '.join([self._full_name.first_name.value, self._full_name.last_name.to_str()])
        else:
            return ' '.join([self._full_name.last_name.to_str(), self._full_name.first_name.value])

    def flatten(
        self,
        limit: int = 20,
        by: str = 'middle_name',
        with_period: bool = True,
        recursive: bool = False,
        with_more: bool = False,
        surname: Optional[str] = None,
    ) -> str:
        if self.length <= limit:
            return self.full

        sep = '.' if with_period else ''
        fn = self._full_name.first_name.to_str()
        mn = ' '.join(self.middle_name())
        ln = self._full_name.last_name.to_str()
        has_mid = self.has_middle
        f = sep.join(self._full_name.first_name.initials(with_more)) + sep
        l = sep.join(self._full_name.last_name.initials(surname)) + sep
        m = sep.join(n.initial for n in self._full_name.middle_name) + sep if has_mid else ''
        name = []

        if self.config.ordered_by == 'first_name':
            if by == 'first_name':
                name = [f, mn, ln] if has_mid else [f, ln]
            elif by == 'last_name':
                name = [fn, mn, l] if has_mid else [fn, l]
            elif by == 'middle_name':
                name = [fn, m, ln] if has_mid else [fn, ln]
            elif by == 'first_mid':
                name = [f, m, ln] if has_mid else [f, ln]
            elif by == 'mid_last':
                name = [fn, m, l] if has_mid else [fn, l]
            elif by == 'all':
                name = [f, m, l] if has_mid else [f, l]
        else:
            if by == 'first_name':
                name = [ln, f, mn] if has_mid else [ln, f]
            elif by == 'last_name':
                name = [l, fn, mn] if has_mid else [l, fn]
            elif by == 'middle_name':
                name = [ln, fn, m] if has_mid else [ln, fn]
            elif by == 'first_mid':
                name = [ln, f, m] if has_mid else [ln, f]
            elif by == 'mid_last':
                name = [l, fn, m] if has_mid else [l, fn]
            elif by == 'all':
                name = [l, f, m] if has_mid else [l, f]

        flat = ' '.join(name)
        if recursive and len(flat) > limit:
            next_by = {
                'first_name': 'middle_name',
                'middle_name': 'last_name',
                'last_name': 'first_mid',
                'first_mid': 'mid_last',
                'mid_last': 'all',
                'all': 'all',
            }.get(by, by)
            if next_by == by:
                return flat

            return self.flatten(
                limit=limit,
                by=next_by,
                with_period=with_period,
                recursive=recursive,
                with_more=with_more,
                surname=surname,
            )
        return flat

    def zip(self, by: str = 'mid_last', with_period: bool = True) -> str:
        return self.flatten(limit=0, by=by, with_period=with_period)

    def format(self, pattern: str) -> str:
        """
        Formats the full name as desired.
        Args:
            pattern (str): Character used to format the name.

        String format:
        --------------
        - 'short': typical first + last name
        - 'long': birth name (without prefix and suffix)
        - 'public': first name combined with the last name's initial.
        - 'official': official document format

        Character format:
        ------------
        - 'b': birth name
        - 'B': capitalized birth name
        - 'f': first name
        - 'F': capitalized first name
        - 'l': last name
        - 'L': capitalized last name
        - 'm': middle names
        - 'M': capitalized middle names
        - 'o': official document format
        - 'O': official document format in capital letters
        - 'p': prefix
        - 'P': capitalized prefix
        - 's': suffix
        - 'S': capitalized suffix

        Punctuations:
        -------------
        - '.': period
        - ',': comma
        - ' ': space
        - '-': hyphen
        - '_': underscore
        - '$': an escape character to select only the initial of the next char.

        Examples:
        ---------
        Given the name `Joe Jim Smith`, use `format` with the `pattern` string.
        - format('l f') => 'Smith Joe'
        - format('L, f') => 'SMITH, Joe'
        - format('short') => 'Joe Smith'
        - format() => 'SMITH, Joe Jim'
        - format(r'f $l.') => 'Joe S.'

        Note:
        -----
        The escape character is only valid for the birth name parts: first, middle, and last names.
        """

        if pattern == 'short':
            return self.short
        if pattern == 'long':
            return self.long
        if pattern == 'public':
            return self.public
        if pattern == 'official':
            pattern = 'o'

        group = ''
        formatted = []
        for char in pattern:
            if char not in ALLOWED_TOKENS:
                raise NameError.not_allowed(
                    source=self.full, operation='format', message=f'unsupported character <{char}> from {pattern}.'
                )
            group += char
            if char == '$':
                continue
            formatted.append(self.__map(group) or '')
            group = ''
        return ''.join(formatted).strip()

    def flip(self) -> None:
        if self.config.ordered_by == 'first_name':
            self._full_name.config.update_order('last_name')
        else:
            self._full_name.config.update_order('first_name')

    def split(self, sep: Union[str, re.Pattern] = re.compile(r"[' -]")) -> List[str]:
        return re.sub(sep, ' ', self.birth).split(' ')

    def join(self, sep: str = ' ') -> str:
        return sep.join(self.split())

    def capitalize(self) -> str:
        return self.birth.capitalize()

    def upper(self) -> str:
        return self.birth.upper()

    def lower(self) -> str:
        return self.birth.lower()

    def camel(self) -> str:
        return decapitalize(self.pascal())

    def pascal(self) -> str:
        return ''.join(name.capitalize() for name in self.split())

    def snake(self) -> str:
        return '_'.join(name.lower() for name in self.split())

    def kebab(self) -> str:
        return '-'.join(name.lower() for name in self.split())

    def dot(self) -> str:
        return '.'.join(name.lower() for name in self.split())

    def toggle(self) -> str:
        return toggle_case(self.birth)

    def __to_parser(
        self, names: Union[str, Sequence[str], Sequence[Name], Mapping[str, str], FullName, Parser]
    ) -> Parser:
        if isinstance(names, Parser):
            return names
        elif isinstance(names, str):
            return StringParser(names)
        elif isinstance(names, Sequence):
            if all(isinstance(name, str) for name in names):
                return SequentialStringParser(names)  # type: ignore
            elif all(isinstance(name, Name) for name in names):
                return SequentialNameParser(names)  # type: ignore
        elif isinstance(names, Mapping):
            return NamaParser(names)
        elif isinstance(names, FullName):
            return SequentialNameParser(names.to_iterable())
        raise NameError.input(source=str(names), message='cannot parse raw data; review expected data types')

    def __map(self, char: str) -> Optional[str]:
        if char in ['.', ',', ' ', '-', '_']:
            return char
        elif char == 'b':
            return self.birth
        elif char == 'B':
            return self.birth.upper()
        elif char == 'f':
            return self.first
        elif char == 'F':
            return self.first.upper()
        elif char == 'l':
            return self.last
        elif char == 'L':
            return self.last.upper()
        elif char in ['m', 'M']:
            middle_name = ' '.join(self.middle_name())
            return middle_name if char == 'm' else middle_name.upper()
        elif char in ['o', 'O']:
            sep, names = ',' if self.config.ending else '', []
            if self.prefix:
                names.append(self.prefix)
            names.append(f'{self.last},'.upper())
            if self.has_middle:
                names.extend([self.first, ' '.join(self.middle_name()) + sep])
            else:
                names.append(self.first + sep)
            if self.suffix:
                names.append(self.suffix)
            nama = ' '.join(names).strip()
            return nama if char == 'o' else nama.upper()
        elif char == 'p':
            return self.prefix
        elif char == 'P':
            return self.prefix.upper() if self.prefix else None
        elif char == 's':
            return self.suffix
        elif char == 'S':
            return self.suffix.upper() if self.suffix else None
        elif char in ['$f', '$F']:
            return self._full_name.first_name.initial
        elif char in ['$l', '$L']:
            return self._full_name.last_name.initial
        elif char in ['$m', '$M']:
            return self.middle[0] if self.middle else None
        else:
            return None
