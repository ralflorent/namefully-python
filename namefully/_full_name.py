from typing import Any, List, Mapping, Optional, Sequence, Union

from ._config import Config
from ._errors import NameError
from ._name import FirstName, LastName, Name
from ._validators import Validators

__all__ = ['FullName']


class FullName:
    """
    The core component of this utility.

    This component is comprised of five entities that make it easy to handle a
    full name set: prefix, first name, middle name, last name, and suffix.
    This class is intended for internal processes. However, it is understandable
    that it might be needed at some point for additional purposes. For this reason,
    it's made available.

    It is recommended to avoid using this class unless it is highly necessary or
    a custom parser is used for uncommon use cases. This utility tries to cover
    as many use cases as possible.

    Additionally, an optional configuration can be used to indicate some specific
    behaviors related to that name handling.
    """

    _first_name: FirstName
    _last_name: LastName

    def __init__(self, **options: Any):
        self._config = Config.merge(**options)
        self._prefix: Optional[Name] = None
        self._middle_name: List[Name] = []
        self._suffix: Optional[Name] = None

    @property
    def prefix(self) -> Optional[Name]:
        return self._prefix

    @property
    def first_name(self) -> FirstName:
        return self._first_name

    @property
    def middle_name(self) -> List[Name]:
        return self._middle_name

    @property
    def last_name(self) -> LastName:
        return self._last_name

    @property
    def suffix(self) -> Optional[Name]:
        return self._suffix

    @property
    def config(self) -> Config:
        return self._config

    @property
    def size(self) -> int:
        return len(self.to_iterable(flat=True))

    @prefix.setter
    def prefix(self, name: Union[None, str, Name]):
        if name is None:
            return

        if not self._config.bypass:
            Validators.prefix.validate(name)
        prefix = name.value if isinstance(name, Name) else name
        self._prefix = Name.prefix(f'{prefix}.' if self._config.title == 'us' else prefix)

    @first_name.setter
    def first_name(self, name: Union[str, FirstName]):
        if not self._config.bypass:
            Validators.first_name.validate(name)
        self._first_name = name if isinstance(name, FirstName) else FirstName(name)

    @middle_name.setter
    def middle_name(self, names: Union[str, Sequence[str], Sequence[Name]]):
        if not self._config.bypass:
            Validators.middle_name.validate(names)
        if isinstance(names, str):
            names = [names]
        self._middle_name = [Name.middle(name) if isinstance(name, str) else name for name in names]

    @last_name.setter
    def last_name(self, name: Union[str, LastName]):
        if not self._config.bypass:
            Validators.last_name.validate(name)
        self._last_name = name if isinstance(name, LastName) else LastName(name)

    @suffix.setter
    def suffix(self, name: Union[None, str, Name]):
        if name is None:
            return

        if not self._config.bypass:
            Validators.suffix.validate(name)
        self._suffix = Name.suffix(name.value if isinstance(name, Name) else name)

    def has(self, namon: str) -> bool:
        if namon in ['first', 'first_name', 'last', 'last_name']:
            return True
        if namon == 'prefix':
            return self._prefix is not None
        if namon == 'suffix':
            return self._suffix is not None
        if namon in ['middle', 'middle_name']:
            return len(self._middle_name) > 0
        return False

    def to_iterable(self, flat: bool = False) -> Sequence[Name]:
        names: List[Name] = []
        names.extend(self._middle_name)
        if self._prefix:
            names.append(self._prefix)
        if flat:
            names.extend(self._first_name.as_names)
            names.extend(self._last_name.as_names)
        else:
            names.append(self._first_name)
            names.append(self._last_name)
        if self._suffix:
            names.append(self._suffix)
        return tuple(names)

    @staticmethod
    def parse(names: Mapping[str, str], **options: Any) -> 'FullName':
        try:
            full_name = FullName(**options)
            full_name.prefix = names.get('prefix')
            full_name.first_name = names['first_name']
            full_name.middle_name = names.get('middle_name', [])
            full_name.last_name = names['last_name']
            full_name.suffix = names.get('suffix')
            return full_name
        except NameError as error:
            raise error
        except Exception as exc:
            raise NameError.unknown(
                source=list(names.values()),
                message='could not parse Mapping[str, str] content',
                error=exc,
            ) from exc
