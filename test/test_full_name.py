import pytest

from namefully import FirstName, FullName, LastName, Name, NameError


@pytest.fixture
def setup_names():
    prefix = Name.prefix('Mr')
    first_name = FirstName('John')
    middle_name = [Name.middle('Ben'), Name.middle('Carl')]
    last_name = LastName('Smith')
    suffix = Name.suffix('Ph.D')
    return (prefix, first_name, middle_name, last_name, suffix)


def run_expectations(full_name: FullName):
    assert isinstance(full_name.prefix, Name)
    assert isinstance(full_name.first_name, FirstName)
    for name in full_name.middle_name:
        assert isinstance(name, Name)
    assert isinstance(full_name.last_name, LastName)
    assert isinstance(full_name.suffix, Name)

    assert full_name.prefix.value == 'Mr'
    assert full_name.first_name.to_str() == 'John'
    assert ' '.join(n.value for n in full_name.middle_name) == 'Ben Carl'
    assert full_name.last_name.value == 'Smith'
    assert full_name.suffix.value == 'Ph.D'


def test_creates_full_name_from_dict_names():
    with pytest.raises(NameError):
        FullName.parse({'firstName': 'J', 'lastName': 'Smith'})
    full_name = FullName.parse(
        {
            'prefix': 'Mr',
            'first_name': 'John',
            'middle_name': 'Ben Carl',
            'last_name': 'Smith',
            'suffix': 'Ph.D',
        }
    )
    run_expectations(full_name)


def test_builds_full_name_as_it_goes(setup_names):
    prefix, first_name, middle_name, last_name, suffix = setup_names
    full_name = FullName()
    full_name.prefix = prefix
    full_name.first_name = first_name
    full_name.middle_name = middle_name
    full_name.last_name = last_name
    full_name.suffix = suffix
    run_expectations(full_name)


def test_builds_full_name_with_no_validation_rules():
    full_name = FullName(name='with_bypass', bypass=True)
    full_name.first_name = FirstName('2Pac')
    full_name.last_name = LastName('Shakur')

    assert isinstance(full_name.first_name, FirstName)
    assert isinstance(full_name.last_name, LastName)
    assert full_name.first_name.value == '2Pac'
    assert full_name.last_name.value == 'Shakur'
    assert full_name.config is not None
    assert full_name.config.name == 'with_bypass'


def test_creates_full_name_as_it_goes_from_raw_strings():
    full_name = FullName()
    full_name.prefix = 'Mr'
    full_name.first_name = 'John'
    full_name.middle_name = ['Ben', 'Carl']
    full_name.last_name = 'Smith'
    full_name.suffix = 'Ph.D'
    run_expectations(full_name)


def test_has_indicates_whether_full_name_has_specific_namon():
    full_name = FullName()
    full_name.prefix = 'Ms'
    full_name.first_name = 'Jane'
    full_name.last_name = 'Doe'

    assert full_name.has('prefix') is True
    assert full_name.has('first_name') is True
    assert full_name.has('middle_name') is False
    assert full_name.has('last_name') is True
    assert full_name.has('suffix') is False
