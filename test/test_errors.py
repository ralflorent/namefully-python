import pytest

from namefully import (
    FullName,
    InputError,
    NameError,
    NameErrorType,
    Namefully,
    NotAllowedError,
    UnknownError,
    ValidationError,
)

NAME = 'Jane Doe'
MESSAGE = 'Wrong name'


def test_can_be_created_with_message_only():
    error = NameError(NAME, MESSAGE)
    assert isinstance(error, Exception)
    assert error.source == NAME
    assert error.message == MESSAGE
    assert error.type == NameErrorType.UNKNOWN
    assert f'NameError ({NAME}): {MESSAGE}' in str(error)


def test_can_be_created_for_wrong_inputs():
    error = InputError(source=['Jane', 'Doe'], message=MESSAGE)
    assert isinstance(error, NameError)
    assert error.message == MESSAGE
    assert error.source == NAME
    assert error.type == NameErrorType.INPUT
    assert f'InputError ({NAME}): {MESSAGE}' in str(error)


def test_can_be_created_for_validation_purposes():
    error = ValidationError(source=['Jane', 'Doe'], name_type='first_name', message=MESSAGE)
    assert isinstance(error, NameError)
    assert error.message == MESSAGE
    assert error.source == NAME
    assert error.type == NameErrorType.VALIDATION
    assert f"ValidationError (first_name='Jane Doe'): {MESSAGE}" in str(error)


def test_can_be_created_for_unsupported_operations():
    error = NotAllowedError(source=NAME, operation='lower', message=MESSAGE)
    assert isinstance(error, NameError)
    assert error.message == MESSAGE
    assert error.source == NAME
    assert error.type == NameErrorType.NOT_ALLOWED
    assert f'NotAllowedError ({NAME}) - lower: {MESSAGE}' in str(error)


def test_can_be_created_for_unknown_use_cases():
    error = UnknownError(source=None, error=Exception('something'))
    assert isinstance(error, NameError)
    assert error.source == '<unknown>'
    assert error.origin is not None
    assert error.type == NameErrorType.UNKNOWN
    assert 'UnknownError (<unknown>)' in str(error)


def test_unknown_error_is_thrown_when_failed_to_parse_full_name():
    with pytest.raises(NameError) as error:
        FullName.parse({})
    assert error.value.type == NameErrorType.UNKNOWN


def test_not_allowed_error_is_thrown_if_wrong_params_during_formatting():
    name = Namefully(NAME)
    assert name.format('f') == 'Jane'
    for k in ['[', '{', '^', '!', '@', '#', 'a', 'c', 'd']:
        with pytest.raises(NotAllowedError):
            name.format(k)
