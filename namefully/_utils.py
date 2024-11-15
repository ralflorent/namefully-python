from typing import Optional

__all__ = ['capitalize', 'decapitalize']


def capitalize(s: str, caps_range: Optional[str] = 'initial') -> str:
    if not s or caps_range not in ['initial', 'all']:
        return s
    initial, rest = s[0].upper(), s[1:].lower()
    return initial + rest if caps_range == 'initial' else s.upper()


def decapitalize(s: str, caps_range: Optional[str] = 'initial') -> str:
    if not s or caps_range not in ['initial', 'all']:
        return s
    initial, rest = s[0].lower(), s[1:]
    return initial + rest if caps_range == 'initial' else s.lower()
