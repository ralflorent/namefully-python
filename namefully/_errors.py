from typing import List, Optional, Union

__all__ = ['NameErrorType', 'NameError', 'InputError', 'ValidationError', 'NotAllowedError', 'UnknownError']

_NameSource = Union[None, str, List[str]]


class NameErrorType:
    INPUT = 'input'
    VALIDATION = 'validation'
    NOT_ALLOWED = 'not_allowed'
    UNKNOWN = 'unknown'


class NameError(Exception):
    _source: _NameSource
    _message: Optional[str]

    def __init__(self, source: _NameSource, message: Optional[str] = None, type: str = NameErrorType.UNKNOWN):
        super().__init__()
        self.name = self.__class__.__name__
        self._source = source
        self._message = message
        self.type = type

    @property
    def source(self) -> str:
        if isinstance(self._source, str):
            return self._source
        if isinstance(self._source, (list, tuple)):
            return ' '.join(self._source)
        return '<unknown>'

    @property
    def message(self) -> str:
        return self._message or ''

    @property
    def has_message(self) -> bool:
        return len(self.message.strip()) > 0

    @staticmethod
    def input(source: _NameSource, message: Optional[str] = None) -> 'InputError':
        return InputError(source=source, message=message)

    @staticmethod
    def validation(
        source: _NameSource, message: Optional[str] = None, name_type: Optional[str] = None
    ) -> 'ValidationError':
        return ValidationError(source=source, message=message, name_type=name_type)

    @staticmethod
    def not_allowed(
        source: _NameSource, message: Optional[str] = None, operation: Optional[str] = None
    ) -> 'NotAllowedError':
        return NotAllowedError(source=source, message=message, operation=operation)

    @staticmethod
    def unknown(
        source: _NameSource, message: Optional[str] = None, error: Optional[Exception] = None
    ) -> 'UnknownError':
        return UnknownError(source=source, message=message, error=error)

    def __str__(self) -> str:
        report = f'{self.name} ({self.source})'
        return f'{report}: {self.message}' if self.has_message else report

    def __repr__(self) -> str:
        return f'<{self.name}>'


class InputError(NameError):
    def __init__(self, source: _NameSource, message: Optional[str] = None):
        super().__init__(source=source, message=message, type=NameErrorType.INPUT)


class ValidationError(NameError):
    @property
    def name_type(self) -> str:
        return self._name_type or ''

    def __init__(self, source: _NameSource, message: Optional[str] = None, name_type: Optional[str] = None):
        super().__init__(source=source, message=message, type=NameErrorType.VALIDATION)
        self._name_type = name_type

    def __str__(self) -> str:
        report = f"{self.name} ({self.name_type}='{self.source}')"
        return f'{report}: {self.message}' if self.has_message else report


class NotAllowedError(NameError):
    @property
    def operation(self) -> Optional[str]:
        return self._operation

    def __init__(self, source: _NameSource, message: Optional[str] = None, operation: Optional[str] = None):
        super().__init__(source=source, message=message, type=NameErrorType.NOT_ALLOWED)
        self._operation = operation

    def __str__(self) -> str:
        report = f'{self.name} ({self.source})'
        if self.operation and len(self.operation.strip()) > 0:
            report = f'{report} - {self.operation}'
        return f'{report}: {self.message}' if self.has_message else report


class UnknownError(NameError):
    @property
    def origin(self) -> Optional[Exception]:
        return self._origin

    def __init__(self, source: _NameSource, message: Optional[str] = None, error: Optional[Exception] = None):
        super().__init__(source=source, message=message, type=NameErrorType.UNKNOWN)
        self._origin = error

    def __str__(self) -> str:
        report = super().__str__()
        if self.origin:
            report = f'{report}\n{self.origin}'
        return report
