from typing import Dict, Optional

from ._constants import *
from ._types import _CapsRange

__all__ = ['NameIndex']


class NameIndex:
    """
    A fixed set of values to handle specific positions for a list of names.

    When using the original name order, this follows that order based on the
    count of elements. It is expected that the list has to be between two and
    five elements. Consequently, the order of appearance set in the config
    influences how the parsing is carried out.

    Ordered by first name, the parser works as follows:
    - 2 elements: first_name last_name
    - 3 elements: first_name middle_name last_name
    - 4 elements: prefix first_name middle_name last_name
    - 5 elements: prefix first_name middle_name last_name suffix

    Ordered by last name, the parser works as follows:
    - 2 elements: last_name first_name
    - 3 elements: last_name first_name middle_name
    - 4 elements: prefix last_name first_name middle_name
    - 5 elements: prefix last_name first_name middle_name suffix

    For example, `Jane Smith` (ordered by first name) is expected to be indexed:
    `['Jane', 'Smith']`.

    Note that a user can leverage this indexing mechanism to parse name parts that
    don't follow the original name order due to randomness.
    """

    def __init__(self, prefix: int, first_name: int, middle_name: int, last_name: int, suffix: int):
        self.prefix = prefix
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.suffix = suffix

    def to_dict(self) -> Dict[str, int]:
        return {
            'prefix': self.prefix,
            'first_name': self.first_name,
            'middle_name': self.middle_name,
            'last_name': self.last_name,
            'suffix': self.suffix,
        }

    @staticmethod
    def base() -> 'NameIndex':
        """The default or base indexing: first_name last_name."""
        return NameIndex(-1, 0, -1, 1, -1)

    @staticmethod
    def only(first_name: int, last_name: int, *, prefix: int = -1, suffix: int = -1, middle_name: int = -1):
        return NameIndex(prefix, first_name, middle_name, last_name, suffix)

    @staticmethod
    def when(order: str, count: int = 2) -> 'NameIndex':
        if order == 'first_name':
            if count == 2:  # first name + last name
                return NameIndex(-1, 0, -1, 1, -1)
            elif count == 3:  # first name + middle name + last name
                return NameIndex(-1, 0, 1, 2, -1)
            elif count == 4:  # prefix + first name + middle name + last name
                return NameIndex(0, 1, 2, 3, -1)
            elif count == 5:  # prefix + first name + middle name + last name + suffix
                return NameIndex(0, 1, 2, 3, 4)
            else:
                return NameIndex.base()
        elif order == 'last_name':
            if count == 2:  # last name + first name
                return NameIndex(-1, 1, -1, 0, -1)
            elif count == 3:  # last name + first name + middle name
                return NameIndex(-1, 1, 2, 0, -1)
            elif count == 4:  # prefix + last name + first name + middle name
                return NameIndex(0, 2, 3, 1, -1)
            elif count == 5:  # prefix + last name + first name + middle name + suffix
                return NameIndex(0, 2, 3, 1, 4)
            else:
                return NameIndex.base()
        else:
            return NameIndex.base()


def capitalize(s: str, caps_range: Optional[str] = 'initial') -> str:
    if not s or caps_range not in _CapsRange:
        return s
    initial, rest = s[0].upper(), s[1:].lower()
    return initial + rest if caps_range == 'initial' else s.upper()


def decapitalize(s: str, caps_range: Optional[str] = 'initial') -> str:
    if not s or caps_range not in _CapsRange:
        return s
    initial, rest = s[0].lower(), s[1:]
    return initial + rest if caps_range == 'initial' else s.lower()


def toggle_case(s: str) -> str:
    chars = []
    for c in s:
        if c.isupper():
            chars.append(c.lower())
        else:
            chars.append(c.upper())
    return ''.join(chars)
