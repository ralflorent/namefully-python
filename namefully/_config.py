from typing import Dict, Optional

from ._types import _NameOrder, _Separator, _Surname, _Title


class Config:
    _cache: Dict[str, 'Config'] = {}

    def __new__(cls) -> None:
        raise RuntimeError('use Config.create() to create Config instances')

    def __init__(
        self,
        name: str,
        *,
        ordered_by: str = 'first_name',
        separator: str = 'space',
        title: str = 'uk',
        ending: bool = False,
        bypass: bool = True,
        surname: str = 'father',
    ) -> None:
        self._name: str = name
        self._ordered_by: str = ordered_by in _NameOrder and ordered_by or 'first_name'
        self._separator: str = separator in _Separator and separator or 'space'
        self._title: str = title in _Title and title or 'uk'
        self._ending: bool = ending
        self._bypass: bool = bypass
        self._surname: str = surname in _Surname and surname or 'father'

    @property
    def ordered_by(self) -> str:
        return self._ordered_by

    @property
    def separator(self) -> str:
        return self._separator

    @property
    def title(self) -> str:
        return self._title

    @property
    def ending(self) -> bool:
        return self._ending

    @property
    def bypass(self) -> bool:
        return self._bypass

    @property
    def surname(self) -> str:
        return self._surname

    @property
    def name(self) -> str:
        return self._name

    @classmethod
    def create(cls, name: str = 'default') -> 'Config':
        if name not in cls._cache:
            instance = object.__new__(cls)
            instance.__init__(name)
            cls._cache[name] = instance
        return cls._cache[name]

    @classmethod
    def merge(
        cls,
        *,
        name: Optional[str] = None,
        ordered_by: Optional[str] = None,
        separator: Optional[str] = None,
        title: Optional[str] = None,
        ending: Optional[bool] = None,
        bypass: Optional[bool] = None,
        surname: Optional[str] = None,
    ) -> 'Config':
        config = cls.create(name or 'default')
        config._ordered_by = ordered_by if ordered_by is not None else config.ordered_by
        config._separator = separator if separator is not None else config.separator
        config._title = title if title is not None else config.title
        config._ending = ending if ending is not None else config.ending
        config._bypass = bypass if bypass is not None else config.bypass
        config._surname = surname if surname is not None else config.surname
        return config

    def copy_with(
        self,
        *,
        name: Optional[str] = None,
        ordered_by: Optional[str] = None,
        separator: Optional[str] = None,
        title: Optional[str] = None,
        ending: Optional[bool] = None,
        bypass: Optional[bool] = None,
        surname: Optional[str] = None,
    ) -> 'Config':
        name = name or self._name + '_copy'
        config = Config.create(self._gen_new_name(name))
        config._ordered_by = ordered_by if ordered_by is not None else self._ordered_by
        config._separator = separator if separator is not None else self._separator
        config._title = title if title is not None else self._title
        config._ending = ending if ending is not None else self._ending
        config._bypass = bypass if bypass is not None else self._bypass
        config._surname = surname if surname is not None else self._surname
        return config

    def clone(self) -> 'Config':
        return self.copy_with()

    def reset(self) -> None:
        self._ordered_by = 'first_name'
        self._separator = 'space'
        self._title = 'uk'
        self._ending = False
        self._bypass = True
        self._surname = 'father'
        Config._cache[self._name] = self

    def update_order(self, order: str) -> None:
        if order and order != self._ordered_by:
            Config._cache[self._name]._ordered_by = order

    def _gen_new_name(self, name: str) -> str:
        return name if name != self._name and name not in Config._cache else self._gen_new_name(f'{name}_copy')