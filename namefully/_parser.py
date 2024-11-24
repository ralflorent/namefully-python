from abc import ABC, abstractmethod
from typing import Any, List, Mapping, Sequence

from ._config import Config
from ._errors import InputError
from ._full_name import FullName
from ._name import FirstName, LastName, Name
from ._types import Separator
from ._utils import NameIndex
from ._validators import SequentialNameValidator, Validators

__all__ = ['Parser']


class Parser(ABC):
    def __init__(self, raw: Any) -> None:
        self.raw = raw

    @abstractmethod
    def parse(self, **options) -> FullName:
        raise NotImplementedError

    @staticmethod
    def build(text: str) -> 'Parser':
        parts = text.strip().split(Separator.space[1])
        length = len(parts)
        if length == 0 or length == 1:
            raise InputError(source=text, message='cannot build from invalid input')
        elif length == 2 or length == 3:
            return StringParser(text)
        else:
            last = parts.pop()
            first, *middles = parts
            return SequentialStringParser([first, ' '.join(middles), last])


class StringParser(Parser):
    def __init__(self, raw: str) -> None:
        super().__init__(raw)

    def parse(self, **options) -> FullName:
        config = Config.merge(**options)
        names = self.raw.split(config.separator)
        return SequentialStringParser(names).parse(**options)


class SequentialStringParser(Parser):
    def __init__(self, names: Sequence[str]) -> None:
        super().__init__(names)

    def parse(self, **options) -> FullName:
        full_name = FullName(**options)

        raw: List[str] = [name.strip() for name in self.raw]
        length = len(raw)
        index = NameIndex.when(full_name.config.ordered_by, length)
        validator = SequentialNameValidator(index)

        if full_name.config.bypass:
            validator.validate_index(raw)
        else:
            validator.validate_as_str(raw)

        full_name.first_name = raw[index.first_name]
        full_name.last_name = raw[index.last_name]

        if length >= 3:
            full_name.middle_name = raw[index.middle_name].split(full_name.config.separator)
        if length >= 4:
            full_name.prefix = raw[index.prefix]
        if length == 5:
            full_name.suffix = raw[index.suffix]

        return full_name


class SequentialNameParser(Parser):
    def __init__(self, names: Sequence[Name]) -> None:
        super().__init__(names)

    def parse(self, **options) -> FullName:
        full_name = FullName(**options)

        raw: List[Name] = self.raw
        SequentialNameValidator().validate_as_name(raw)

        for name in raw:
            if name.is_prefix:
                full_name.prefix = name
            elif name.is_suffix:
                full_name.suffix = name
            elif name.is_first:
                first_name = name if isinstance(name, FirstName) else FirstName(name.value)
                full_name.first_name = first_name
            elif name.is_middle:
                full_name.middle_name.append(name)
            elif name.is_last:
                last_name = LastName(
                    father=name.value,
                    mother=name.mother if isinstance(name, LastName) else None,
                    format=full_name.config.surname,
                )
                full_name.last_name = last_name

        return full_name


class NamaParser(Parser):
    def __init__(self, names: Mapping[str, str]) -> None:
        super().__init__(names)

    def parse(self, **options) -> FullName:
        config = Config.merge(**options)
        raw: Mapping[str, str] = self.raw

        if config.bypass:
            Validators.nama.validate_keys(raw)
        else:
            Validators.nama.validate(raw)

        return FullName.parse(raw, **options)
