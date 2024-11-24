import pytest

from namefully import FullName, NameError, NameErrorType, Namefully
from namefully._errors import InputError, NotAllowedError, UnknownError, ValidationError
from namefully._name import FirstName, LastName, Name
from namefully._validators import Validators

NAME = 'Jane Doe'
MESSAGE = 'Wrong name'


@pytest.fixture(scope='module')
def config():
    return {'context': 'error_handling', 'bypass': False}


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
    for k in ['[', '{', '^', '!', '@', '#', 'a', 'c', 'd']:
        with pytest.raises(NotAllowedError):
            name.format(k)


def test_input_error_if_name_keys_are_not_as_expected():
    with pytest.raises(InputError):
        Namefully({})
    with pytest.raises(InputError):
        Validators.nama.validate({'prefix': ''})
    with pytest.raises(InputError):
        Validators.nama.validate({'prefix': 'Mr', 'first_name': 'John'})
    with pytest.raises(InputError):
        Validators.nama.validate({'prefix': 'Mr', 'last_name': 'Smith'})


def test_input_error_if_string_list_has_unsupported_number_of_entries():
    with pytest.raises(InputError):
        Namefully([])
    with pytest.raises(InputError):
        Namefully(['jane'])
    with pytest.raises(InputError):
        Namefully(['ms', 'jane', 'jane', 'janet', 'doe', 'III'])


def test_input_error_if_name_list_has_unsupported_number_of_entries():
    name = Name.first('jane-')
    with pytest.raises(InputError):
        Namefully([])
    with pytest.raises(InputError):
        Namefully([name])
    with pytest.raises(InputError):
        Namefully([name, name, name, name, name, name])


def test_validation_error_when_namon_breaks_validation_rules(config):
    with pytest.raises(ValidationError):
        Namefully('J4ne Doe', **config)
    with pytest.raises(ValidationError):
        Namefully('Jane Do3', **config)


def test_validation_error_if_first_name_breaks_validation_rules(config):
    with pytest.raises(ValidationError):
        Namefully('J4ne Doe', **config)
    with pytest.raises(ValidationError):
        Namefully([FirstName('Jane', 'M4ry'), Name.last('Doe')], **config)


def test_validation_error_if_middle_name_breaks_validation_rules(config):
    with pytest.raises(ValidationError):
        Namefully('Jane M4ry Doe', **config)
    with pytest.raises(ValidationError):
        Validators.middle_name.validate([Name.first('ka7e')])
    with pytest.raises(ValidationError):
        Validators.middle_name.validate([Name.middle('kate;')])
    with pytest.raises(ValidationError):
        Validators.middle_name.validate(['Mary', 'kate;'])
    with pytest.raises(ValidationError):
        Validators.middle_name.validate([Name.middle('Jack'), Name.middle('kate;')])


def test_validation_error_if_last_name_breaks_validation_rules(config):
    with pytest.raises(ValidationError):
        Namefully('Jane Mary Do3', **config)
    with pytest.raises(ValidationError):
        Namefully([FirstName('Jane'), LastName('Doe', 'Sm1th')], **config)


def test_validation_error_if_namon_breaks_validation_rules(config):
    with pytest.raises(ValidationError):
        Validators.prefix.validate(Name.prefix('mr.'))
    with pytest.raises(ValidationError):
        Validators.suffix.validate(Name.suffix('PhD '))
    with pytest.raises(ValidationError):
        Namefully([Name.prefix('mr '), Name.first('John'), Name.last('Doe')], **config)


def test_validation_error_if_dict_name_values_are_incorrect(config):
    with pytest.raises(ValidationError):
        Namefully({'first_name': 'J4ne', 'last_name': 'Doe'}, **config)
    with pytest.raises(ValidationError):
        Validators.nama.validate({'prefix': '', 'first_name': 'Jane', 'last_name': 'Smith'})


def test_validation_error_if_string_list_breaks_validation_rules(config):
    with pytest.raises(ValidationError):
        Namefully(['j4ne', 'doe'], **config)
