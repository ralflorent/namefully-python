from typing import Optional

from ._constants import *
from ._types import _CapsRange

__all__ = ['NameIndex']


class NameIndex:
    """
    A fixed set of values to handle specific positions for list of names.

    As for list of names, this helps to follow a specific order based on the
    count of elements. It is expected that the list has to be between two and
    five elements. Also, the order of appearance set in the configuration
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

    """

    def __init__(self, prefix: int, first_name: int, middle_name: int, last_name: int, suffix: int):
        self.prefix = prefix
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.suffix = suffix

    @staticmethod
    def base() -> 'NameIndex':
        """The default or base indexing: first_name last_name."""
        return NameIndex(-1, 0, -1, 1, -1)

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
