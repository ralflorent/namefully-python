import pytest

from namefully import FirstName, LastName, Name, NameError


@pytest.fixture(scope='module')
def first_name():
    return FirstName('John', 'Ben', 'Carl')


@pytest.fixture
def last_name():
    return LastName(father='Smith', mother='Doe')


def test_throws_exception_if_name_has_less_than_2_characters():
    with pytest.raises(NameError):
        Name.first('')
    with pytest.raises(NameError):
        FirstName('John', 'B')
    with pytest.raises(NameError):
        LastName('Smith', 'D')


def test_create_name_marked_with_specific_type():
    name = Name.middle('John')
    assert name.value == 'John'
    assert name.length == 4
    assert str(name) == 'John'
    assert name.type == 'middle_name'
    assert not name.is_prefix
    assert not name.is_first
    assert name.is_middle == True
    assert not name.is_last
    assert not name.is_suffix


def test_create_name_with_initial_capitalized():
    assert Name('ben', type='first_name', caps_range='initial').value == 'Ben'


def test_create_name_fully_capitalized():
    assert Name('rick', type='first_name', caps_range='all').value == 'RICK'


def test_equal_return_true_if_both_names_are_equal():
    name = Name.middle('John')
    assert name == Name.middle('John')
    assert name != Name.middle('Johnx')
    assert name != Name.prefix('John')


def test_initials_return_only_the_initials_of_the_name():
    assert Name.middle('John').initials() == ['J']


def test_caps_capitalize_the_name_afterwards():
    name = Name.middle('John')
    assert name.caps().value == 'John'
    assert name.caps('all').value == 'JOHN'


def test_decaps_decapitalize_the_name_afterwards():
    name = Name.first('MORTY')
    assert name.decaps().value == 'mORTY'
    assert name.decaps('all').value == 'morty'


def test_create_first_name():
    name = FirstName('John')
    assert str(name) == 'John'
    assert name.more == []
    assert name.type == 'first_name'
    assert name.length == 4


def test_create_first_name_with_additional_parts(first_name):
    assert str(first_name) == 'John'
    assert first_name.more == ['Ben', 'Carl']
    assert first_name.type == 'first_name'


def test_has_more_indicate_if_a_first_name_has_more_than_1_name_part(first_name):
    assert first_name.has_more
    assert not FirstName('John').has_more


def test_copy_with_make_a_copy_of_the_first_name_with_specific_parts(first_name):
    copy = first_name.copy_with(first='Jacky', more=['Bob'])
    assert str(copy) == 'Jacky'
    assert copy.more == ['Bob']
    assert copy.type == 'first_name'


def test_as_names_return_the_name_parts_as_a_pile_of_names(first_name):
    names = first_name.as_names
    assert len(names) == 3
    assert str(names[0]) == 'John'
    assert str(names[1]) == 'Ben'
    assert str(names[2]) == 'Carl'
    for name in names:
        assert isinstance(name, Name)
        assert name.type == 'first_name'


def test_to_string_return_a_string_version_of_the_first_name(first_name):
    assert str(first_name) == 'John'
    assert first_name.to_str(with_more=True) == 'John Ben Carl'


def test_initials_return_only_the_initials_of_the_specified_parts(first_name):
    assert first_name.initials() == ['J']
    assert first_name.initials(with_more=True) == ['J', 'B', 'C']


def test_caps_capitalize_first_name_afterwards():
    name = FirstName('john', 'ben', 'carl')
    assert name.caps().to_str() == 'John'
    assert name.caps().to_str(with_more=True) == 'John Ben Carl'


def test_caps_capitalize_all_parts_of_first_name_afterwards(first_name):
    assert first_name.caps('all').to_str() == 'JOHN'
    assert first_name.caps('all').to_str(with_more=True) == 'JOHN BEN CARL'


def test_decaps_decapitalize_a_first_name_afterwards():
    name = FirstName('JOHN', 'BEN', 'CARL')
    assert name.decaps().to_str() == 'jOHN'
    assert name.decaps().to_str(with_more=True) == 'jOHN bEN cARL'


def test_decaps_decapitalize_all_parts_of_a_first_name_afterwards():
    name = FirstName('JOHN', 'BEN', 'CARL')
    assert name.decaps('all').to_str() == 'john'
    assert name.decaps('all').to_str(with_more=True) == 'john ben carl'


def test_create_last_name_with_father_surname_only():
    name = LastName('Smith')
    assert name.father == 'Smith'
    assert not name.has_mother
    assert name.mother is None
    assert name.to_str(format='mother') == ''
    assert name.type == 'last_name'
    assert name.length == 5


def test_create_last_name_with_both_surnames(last_name):
    assert last_name.father == 'Smith'
    assert last_name.has_mother
    assert last_name.length == 8
    assert last_name.to_str(format='mother') == 'Doe'
    assert last_name.type == 'last_name'


def test_create_last_name_with_formats():
    assert LastName('Smith', 'Doe', format='mother').to_str() == 'Doe'
    assert LastName('Smith', 'Doe', 'hyphenated').to_str() == 'Smith-Doe'
    assert LastName('Smith', 'Doe', format='all').to_str() == 'Smith Doe'


def test_as_names_return_object_names(last_name):
    names = last_name.as_names
    assert len(names) == 2
    assert str(names[0]) == 'Smith'
    assert str(names[1]) == 'Doe'
    for name in names:
        assert isinstance(name, Name)
        assert name.type == 'last_name'


def test_to_str_outputs_last_name_with_specific_formats(last_name):
    assert last_name.to_str() == 'Smith'
    assert last_name.to_str(format='mother') == 'Doe'
    assert last_name.to_str(format='hyphenated') == 'Smith-Doe'
    assert last_name.to_str(format='all') == 'Smith Doe'


def test_last_name_return_only_initials_of_specified_parts(last_name):
    assert last_name.initials() == ['S']
    assert last_name.initials(format='mother') == ['D']
    assert last_name.initials(format='hyphenated') == ['S', 'D']
    assert last_name.initials(format='all') == ['S', 'D']


def test_caps_capitalize_last_names_afterwards():
    name = LastName('sánchez')
    assert name.caps().to_str() == 'Sánchez'
    assert name.caps('all').to_str() == 'SÁNCHEZ'


def test_caps_capitalize_all_parts_of_last_name_afterwards(last_name):
    assert last_name.caps('all').to_str() == 'SMITH'
    assert last_name.caps('all').to_str(format='all') == 'SMITH DOE'


def test_decaps_decapitalize_last_names_afterwards():
    name = LastName('SMITH', 'DOE')
    assert name.decaps().to_str() == 'sMITH'
    assert name.decaps().to_str(format='all') == 'sMITH dOE'


def test_decaps_decapitalize_all_parts_of_last_names_afterwards():
    name = LastName('SMITH', 'DOE')
    assert name.decaps(caps_range='all').to_str() == 'smith'
    assert name.decaps(caps_range='all').to_str(format='all') == 'smith doe'


def test_copy_with_make_a_copy_of_last_names_with_specific_parts(last_name):
    copy = last_name.copy_with(father='Moss')
    assert copy.father == 'Moss'
    assert copy.has_mother
    assert copy.length == 7
    assert copy.to_str(format='mother') == 'Doe'
    assert copy.type == 'last_name'

    copy = last_name.copy_with(mother='Kruger')
    assert copy.father == 'Smith'
    assert copy.has_mother
    assert copy.length == 11
    assert copy.to_str(format='mother') == 'Kruger'
    assert copy.type == 'last_name'
