from typing import List, Optional

from ._errors import NameError
from ._types import _CapsRange, _Namon, _Surname
from ._utils import capitalize, decapitalize

__all__ = ['Name', 'FirstName', 'LastName']


class Name:
    def __init__(self, value: str, *, type: str, caps_range: Optional[str] = None):
        self._caps_range = caps_range in _CapsRange and caps_range or 'initial'
        self._type = type in _Namon and type or 'first_name'
        self.value = value
        if caps_range is not None:
            self.caps(caps_range)

    @property
    def initial(self) -> str:
        return self._initial

    @property
    def value(self) -> str:
        return self._namon

    @value.setter
    def value(self, value: str) -> None:
        self._validate(value)
        self._namon = value
        self._initial = value[0]

    @property
    def type(self) -> str:
        return self._type

    @property
    def length(self) -> int:
        return len(self._namon)

    @property
    def is_prefix(self) -> bool:
        return self._type == 'prefix'

    @property
    def is_first(self) -> bool:
        return self._type == 'first_name'

    @property
    def is_middle(self) -> bool:
        return self._type == 'middle_name'

    @property
    def is_last(self) -> bool:
        return self._type == 'last_name'

    @property
    def is_suffix(self) -> bool:
        return self._type == 'suffix'

    @staticmethod
    def prefix(value: str, caps_range: Optional[str] = None) -> 'Name':
        return Name(value, type='prefix', caps_range=caps_range)

    @staticmethod
    def first(value: str, caps_range: Optional[str] = None) -> 'Name':
        return Name(value, type='first_name', caps_range=caps_range)

    @staticmethod
    def middle(value: str, caps_range: Optional[str] = None) -> 'Name':
        return Name(value, type='middle_name', caps_range=caps_range)

    @staticmethod
    def last(value: str, caps_range: Optional[str] = None) -> 'Name':
        return Name(value, type='last_name', caps_range=caps_range)

    @staticmethod
    def suffix(value: str, caps_range: Optional[str] = None) -> 'Name':
        return Name(value, type='suffix', caps_range=caps_range)

    def to_str(self) -> str:
        return self._namon

    def initials(self) -> List[str]:
        return [self._initial]

    def caps(self, caps_range: Optional[str] = None) -> 'Name':
        self.value = capitalize(self._namon, caps_range or self._caps_range)
        return self

    def decaps(self, caps_range: Optional[str] = None) -> 'Name':
        self.value = decapitalize(self._namon, caps_range or self._caps_range)
        return self

    def _validate(self, name: str):
        if len(name.strip()) < 2:
            raise NameError.input(source=name, message='must be 2+ characters')

    def __str__(self) -> str:
        return self.to_str()

    def __repr__(self) -> str:
        return f'<{self._type}: {self._namon}>'

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Name) and self.value == other.value and self.type == other.type


class FirstName(Name):
    def __init__(self, value: str, *more: str):
        super().__init__(value, type='first_name')
        self._more: List[Name] = []
        for name in more:
            self._validate(name)
            self._more.append(Name.first(name))

    @property
    def has_more(self) -> bool:
        return len(self._more) > 0

    @property
    def length(self) -> int:
        return sum(len(name.value) for name in [self] + self._more)

    @property
    def as_names(self) -> List['Name']:
        return [Name.first(self.value)] + self._more

    @property
    def more(self) -> List[str]:
        return [n.value for n in self._more]

    def to_str(self, with_more=False) -> str:
        if with_more and self.has_more:
            return f"{self.value} {' '.join([n.value for n in self._more])}".strip()
        return self.value

    def initials(self, with_more=False) -> List[str]:
        inits = [self._initial]
        if with_more and self.has_more:
            inits.extend([n._initial for n in self._more])
        return inits

    def caps(self, caps_range: Optional[str] = None) -> 'FirstName':
        caps_range = caps_range or self._caps_range
        self.value = capitalize(self.value, caps_range)
        if self.has_more:
            self._more = [name.caps(caps_range) for name in self._more]
        return self

    def decaps(self, caps_range: Optional[str] = None) -> 'FirstName':
        caps_range = caps_range or self._caps_range
        self.value = decapitalize(self.value, caps_range)
        if self.has_more:
            self._more = [name.decaps(caps_range) for name in self._more]
        return self

    def copy_with(self, *, first: Optional[str] = None, more: Optional[List[str]] = None) -> 'FirstName':
        return FirstName(first or self.value, *more or self.more)


class LastName(Name):
    def __init__(self, father: str, mother: Optional[str] = None, format: str = 'father'):
        super().__init__(father, type='last_name')
        self._mother: Optional[Name] = None
        if mother:
            self._validate(mother)
            self._mother = Name.last(mother)
        self.format = format in _Surname and format or 'father'

    @property
    def father(self) -> str:
        return self.value

    @property
    def mother(self) -> Optional[str]:
        return self._mother and self._mother.value or None

    @property
    def has_mother(self) -> bool:
        return self._mother is not None

    @property
    def length(self) -> int:
        return len(self.value) + (self._mother and self._mother.length or 0)

    @property
    def as_names(self) -> List['Name']:
        names = [Name.last(self.value)]
        if self._mother is not None:
            names.append(self._mother)
        return names

    def to_str(self, format: Optional[str] = None) -> str:
        format = format in _Surname and format or self.format
        mother = self._mother and self._mother.value or ''

        if format == 'father':
            return self.value
        elif format == 'mother':
            return mother
        elif format == 'hyphenated':
            return f'{self.value}-{mother}' if self.has_mother else self.value
        elif format == 'all':
            return f'{self.value} {mother}' if self.has_mother else self.value
        return self.value

    def initials(self, format: Optional[str] = None) -> List[str]:
        format, inits = format or self.format, []

        if format == 'mother' and self._mother is not None:
            inits.append(self._mother._initial)
        elif format in ['hyphenated', 'all']:
            inits.append(self._initial)
            if self._mother is not None:
                inits.append(self._mother._initial)
        else:
            inits.append(self._initial)
        return inits

    def caps(self, caps_range: Optional[str] = None) -> 'LastName':
        caps_range = caps_range or self._caps_range
        self.value = capitalize(self.value, caps_range)
        if self._mother is not None:
            self._mother = self._mother.caps(caps_range)
        return self

    def decaps(self, caps_range: Optional[str] = None) -> 'LastName':
        caps_range = caps_range or self._caps_range
        self.value = decapitalize(self.value, caps_range)
        if self._mother is not None:
            self._mother = self._mother.decaps(caps_range)
        return self

    def copy_with(
        self, *, father: Optional[str] = None, mother: Optional[str] = None, format: Optional[str] = None
    ) -> 'LastName':
        return LastName(father or self.value, mother=mother or self.mother, format=format or self.format)
