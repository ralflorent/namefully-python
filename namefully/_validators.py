import re
from abc import ABC, abstractmethod
from typing import Mapping, Optional, Sequence, Union

from ._constants import MAX_NUMBER_OF_NAME_PARTS as _max_names
from ._constants import MIN_NUMBER_OF_NAME_PARTS as _min_names
from ._errors import InputError, ValidationError
from ._name import FirstName, LastName, Name
from ._types import _Namon
from ._utils import NameIndex


class ValidationRule:
    base = re.compile(r'[a-zA-Z\u00C0-\u00D6\u00D8-\u00f6\u00f8-\u00ff\u0400-\u04FFΆ-ωΑ-ώ]')

    # Matches one name part (namon) that is of nature:
    # - Latin (English, Spanish, French, etc.)
    # - European (Greek, Cyrillic, Icelandic, German)
    # - hyphenated
    # - with apostrophe
    # - with space
    namon = re.compile(r'^' + base.pattern + r'+(([' ' -]' + base.pattern + r')?' + base.pattern + r'*)*$')

    # Matches one name part (namon) that is of nature:
    # - Latin (English, Spanish, French, etc.)
    # - European (Greek, Cyrillic, Icelandic, German)
    # - hyphenated
    # - with apostrophe
    first_name = namon

    # Matches 1+ names part (namon) that are of nature:
    # - Latin (English, Spanish, French, etc.)
    # - European (Greek, Cyrillic, Icelandic, German)
    # - hyphenated
    # - with apostrophe
    # - with space
    middle_name = re.compile(r'^' + base.pattern + r'+(([' ' -]' + base.pattern + r')?' + base.pattern + r'*)*$')

    # Matches one name part (namon) that is of nature:
    # - Latin (English, Spanish, French, etc.)
    # - European (Greek, Cyrillic, Icelandic, German)
    # - hyphenated
    # - with apostrophe
    # - with space
    last_name = namon


class Validator(ABC):
    @abstractmethod
    def validate(self, *args, **kwargs):
        raise NotImplementedError

    def is_valid(self, *args, **kwargs):
        try:
            self.validate(*args, **kwargs)
            return True
        except Exception:
            return False


class NameValidator(Validator):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(NameValidator, cls).__new__(cls)
        return cls.instance

    def validate(self, name: Name, type: Optional[str] = None):
        if type in _Namon and name.type != type:
            raise ValidationError(source=name.value, name_type=name.type, message='wrong type')

        if not ValidationRule.namon.match(name.value):
            raise ValidationError(source=name.value, name_type=name.type, message='invalid content')


class NamonValidator(Validator):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(NamonValidator, cls).__new__(cls)
        return cls.instance

    def validate(self, value: Union[str, Name], type: Optional[str] = None):
        if isinstance(value, Name):
            NameValidator().validate(value, type)
        else:
            if not ValidationRule.namon.match(value):
                raise ValidationError(source=value, name_type=type or 'namon', message='invalid content')


class FirstNameValidator(Validator):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(FirstNameValidator, cls).__new__(cls)
        return cls.instance

    def validate(self, value: Union[str, FirstName]):
        if isinstance(value, FirstName):
            for name in value.as_names:
                self.validate(name.value)
        else:
            if not ValidationRule.first_name.match(value):
                raise ValidationError(source=value, name_type='first_name', message='invalid content')


class MiddleNameValidator(Validator):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(MiddleNameValidator, cls).__new__(cls)
        return cls.instance

    def validate(self, value: Union[str, Sequence[str], Sequence[Name]]):
        if isinstance(value, str):
            if not ValidationRule.middle_name.match(value):
                raise ValidationError(source=value, name_type='middle_name', message='invalid content')
        elif isinstance(value, Sequence):
            try:
                validator = NamonValidator()
                for name in value:
                    validator.validate(name, 'middle_name')
            except ValidationError as e:
                raise ValidationError(source=str(value), name_type='middle_name', message=e.message) from e


class LastNameValidator(Validator):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(LastNameValidator, cls).__new__(cls)
        return cls.instance

    def validate(self, value: Union[str, LastName]):
        if isinstance(value, LastName):
            for name in value.as_names:
                self.validate(name.value)
        else:
            if not ValidationRule.last_name.match(value):
                raise ValidationError(source=value, name_type='last_name', message='invalid content')


class NamaValidator(Validator):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(NamaValidator, cls).__new__(cls)
        return cls.instance

    def validate(self, value: Mapping[str, str]):
        self.validate_keys(value)

        if 'prefix' in value:
            NamonValidator().validate(value['prefix'], 'prefix')
        if 'middle_name' in value:
            MiddleNameValidator().validate(value['middle_name'])
        if 'suffix' in value:
            NamonValidator().validate(value['suffix'], 'suffix')

        FirstNameValidator().validate(value['first_name'])
        LastNameValidator().validate(value['last_name'])

    def validate_keys(self, value: Mapping[str, str]):
        length = len(value)
        if length == 0:
            raise InputError(source=None, message='dict[str, str] must not be empty')

        if length < _min_names or length > _max_names:
            raise InputError(
                source=list(value.values()), message=f'expecting a dict of {_min_names}-{_max_names} elements'
            )

        if 'first_name' not in value or 'last_name' not in value:
            raise InputError(source=list(value.values()), message='first_name and last_name keys are required')


class SequenceValidator(Validator):
    def validate(self, values: Sequence[Union[str, Name]]):
        if len(values) < _min_names or len(values) > _max_names:
            raise InputError(
                source=[str(val) for val in values],
                message=f'expecting a list of {_min_names}-{_max_names} elements',
            )


class SequentialNameValidator(SequenceValidator):
    index: NameIndex = NameIndex.base()

    def __new__(cls, index: Optional[NameIndex] = None):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SequentialNameValidator, cls).__new__(cls)
            cls.instance.index = index or NameIndex.base()
        return cls.instance

    def validate_index(self, values: Sequence[Union[str, Name]]):
        super().validate(values)

    def validate_as_str(self, values: Sequence[str]):
        self.validate_index(values)

        FirstNameValidator().validate(values[self.index.first_name])
        LastNameValidator().validate(values[self.index.last_name])

        namon_validator = NamonValidator()
        length = len(values)
        if length >= 3:
            MiddleNameValidator().validate(values[self.index.middle_name])
        if length >= 4:
            namon_validator.validate(values[self.index.prefix], 'prefix')
        if length == 5:
            namon_validator.validate(values[self.index.suffix], 'suffix')

    def validate_as_name(self, values: Sequence[Name]):
        self.validate_index(values)

        if len(values) < _min_names:
            raise InputError(source=[n.value for n in values], message=f'expecting at least {_min_names} names')

        if not any(name.is_first for name in values) or not any(name.is_last for name in values):
            raise InputError(source=[n.value for n in values], message='both first and last names are required')


class Validators:
    namon = NamonValidator()
    nama = NamaValidator()
    prefix = NamonValidator()
    first_name = FirstNameValidator()
    middle_name = MiddleNameValidator()
    last_name = LastNameValidator()
    suffix = NamonValidator()
