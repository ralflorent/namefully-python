import pytest

from namefully import FirstName, LastName, Name, NameError, Namefully, NameIndex

from ._helpers import HashParser, find_name_case


@pytest.fixture(scope='module')
def generic_name():
    return Namefully('Mr John Ben Smith Ph.D', context='generic')


@pytest.fixture(scope='module')
def by_first_name():
    return Namefully('Mr John Ben Smith Ph.D', context='by_first_name', ordered_by='first_name')


@pytest.fixture(scope='module')
def by_last_name():
    return Namefully('Mr Smith John Ben Ph.D', context='by_last_name', ordered_by='last_name')


def test_generic_name_has(generic_name):
    assert generic_name.has('prefix') is True
    assert generic_name.has('suffix') is True
    assert generic_name.has('middle_name') is True
    assert generic_name.has_middle is True


def test_generic_name_to_string(generic_name):
    assert str(generic_name) == 'Mr John Ben Smith Ph.D'
    assert generic_name.to_str() == 'Mr John Ben Smith Ph.D'


def test_generic_name_equal(generic_name):
    assert generic_name == Namefully('Mr John Ben Smith Ph.D')
    assert generic_name != Namefully('Mr John Ben Smith')


def test_generic_name_get(generic_name):
    assert generic_name.config is not None
    assert generic_name.config.name == 'generic'
    assert isinstance(generic_name.get('prefix'), Name)
    assert isinstance(generic_name.get('first_name'), FirstName)
    assert isinstance(generic_name.get('last_name'), LastName)
    assert isinstance(generic_name.get('suffix'), Name)

    middles = generic_name.get('middle_name')
    for n in middles:
        assert isinstance(n, Name)


def test_generic_name_to_dict(generic_name):
    assert generic_name.to_dict() == {
        'prefix': 'Mr',
        'first_name': 'John',
        'middle_name': ['Ben'],
        'last_name': 'Smith',
        'suffix': 'Ph.D',
    }


def test_generic_name_format(generic_name):
    assert generic_name.format('short') == 'John Smith'
    assert generic_name.format('long') == 'John Ben Smith'
    assert generic_name.format('public') == 'John S'
    assert generic_name.format('official') == 'Mr SMITH, John Ben Ph.D'

    assert generic_name.format('B') == 'JOHN BEN SMITH'
    assert generic_name.format('F') == 'JOHN'
    assert generic_name.format('L') == 'SMITH'
    assert generic_name.format('M') == 'BEN'
    assert generic_name.format('O') == 'MR SMITH, JOHN BEN PH.D'
    assert generic_name.format('P') == 'MR'
    assert generic_name.format('S') == 'PH.D'

    assert generic_name.format('b') == 'John Ben Smith'
    assert generic_name.format('f') == 'John'
    assert generic_name.format('l') == 'Smith'
    assert generic_name.format('m') == 'Ben'
    assert generic_name.format('o') == 'Mr SMITH, John Ben Ph.D'
    assert generic_name.format('p') == 'Mr'
    assert generic_name.format('s') == 'Ph.D'

    assert generic_name.format('f $l') == 'John S'
    assert generic_name.format('f $l.') == 'John S.'
    assert generic_name.format('f $m. l') == 'John B. Smith'
    assert generic_name.format('$F.$M.$L') == 'J.B.S'
    assert generic_name.format('$p') == ''
    assert Namefully('John Smith').format('o') == 'SMITH, John'


def test_name_created_from_partial():
    assert Namefully.only('John', 'Smith').full == 'John Smith'
    assert Namefully.only(prefix='Mr', first='John', last='Smith', title='us').full == 'Mr. John Smith'


def test_generic_name_to_iterable(generic_name):
    names = generic_name.parts
    assert len(names) == 5
    for n in names:
        assert isinstance(n, Name)


def test_to_iterable_returns_sequence_of_name_parts(generic_name):
    parts = iter(generic_name)
    assert next(parts) == Name.prefix('Mr')
    assert next(parts) == Name.first('John')
    assert next(parts) == Name.middle('Ben')
    assert next(parts) == Name.last('Smith')
    assert next(parts) == Name.suffix('Ph.D')

    with pytest.raises(StopIteration):
        next(parts)  # no more names available


def test_generic_name_case_conversion(generic_name):
    assert generic_name.lower() == 'john ben smith'
    assert generic_name.upper() == 'JOHN BEN SMITH'
    assert generic_name.camel() == 'johnBenSmith'
    assert generic_name.pascal() == 'JohnBenSmith'
    assert generic_name.snake() == 'john_ben_smith'
    assert generic_name.kebab() == 'john-ben-smith'
    assert generic_name.dot() == 'john.ben.smith'
    assert generic_name.toggle() == 'jOHN bEN sMITH'


def test_generic_name_split(generic_name):
    assert generic_name.split() == ['John', 'Ben', 'Smith']


def test_generic_name_join(generic_name):
    assert generic_name.join('+') == 'John+Ben+Smith'


def test_generic_name_flip(generic_name):
    generic_name.flip()  # was before ordered by first_name.
    assert generic_name.birth == 'Smith John Ben'
    assert generic_name.first == 'John'
    assert generic_name.last == 'Smith'
    generic_name.flip()  # flip back to the first_name name order.


def test_by_first_name_create_full_name(by_first_name):
    assert by_first_name.prefix == 'Mr'
    assert by_first_name.first == 'John'
    assert by_first_name.middle == 'Ben'
    assert by_first_name.last == 'Smith'
    assert by_first_name.suffix == 'Ph.D'
    assert by_first_name.birth == 'John Ben Smith'
    assert by_first_name.short == 'John Smith'
    assert by_first_name.long == 'John Ben Smith'
    assert by_first_name.public == 'John S'
    assert by_first_name.full == 'Mr John Ben Smith Ph.D'
    assert by_first_name.full_name() == 'Mr John Ben Smith Ph.D'
    assert by_first_name.full_name(ordered_by='last_name') == 'Mr Smith John Ben Ph.D'
    assert by_first_name.birth_name() == 'John Ben Smith'
    assert by_first_name.birth_name(ordered_by='last_name') == 'Smith John Ben'

    assert by_first_name.size == 5
    assert by_first_name.length == len('John Ben Smith')
    assert len(by_first_name) == len('Mr John Ben Smith Ph.D')


def test_by_first_name_initials(by_first_name):
    assert by_first_name.initials() == ['J', 'B', 'S']
    assert by_first_name.initials(ordered_by='last_name') == ['S', 'J', 'B']
    assert by_first_name.initials(only='first_name') == ['J']
    assert by_first_name.initials(only='middle_name') == ['B']
    assert by_first_name.initials(only='last_name') == ['S']


def test_by_first_name_shorten(by_first_name):
    assert by_first_name.shorten() == 'John Smith'
    assert by_first_name.shorten(ordered_by='last_name') == 'Smith John'


def test_by_first_name_flatten(by_first_name):
    assert by_first_name.flatten(limit=10, by='middle_name') == 'John B. Smith'
    assert by_first_name.flatten(limit=10, by='middle_name', with_period=False) == 'John B Smith'
    assert by_first_name.flatten(limit=10, recursive=True) == 'John B. S.'
    assert by_first_name.flatten(limit=5, recursive=True) == 'J. B. S.'
    assert by_first_name.flatten(limit=10, recursive=True, with_period=False) == 'John Ben S'

    short_name = Namefully('John Smith')
    assert short_name.flatten(limit=10, by='middle_name', with_period=False) == 'John Smith'
    assert short_name.flatten(limit=8, by='first_mid') == 'J. Smith'


def test_by_first_name_zip(by_first_name):
    assert by_first_name.zip() == 'John B. S.'
    assert by_first_name.zip(by='first_name') == 'J. Ben Smith'
    assert by_first_name.zip(by='middle_name') == 'John B. Smith'
    assert by_first_name.zip(by='last_name') == 'John Ben S.'
    assert by_first_name.zip(by='first_mid') == 'J. B. Smith'
    assert by_first_name.zip(by='mid_last') == 'John B. S.'
    assert by_first_name.zip(by='all') == 'J. B. S.'


def test_by_last_name_create_full_name(by_last_name):
    assert by_last_name.prefix == 'Mr'
    assert by_last_name.first == 'John'
    assert by_last_name.middle == 'Ben'
    assert by_last_name.last == 'Smith'
    assert by_last_name.suffix == 'Ph.D'
    assert by_last_name.birth == 'Smith John Ben'
    assert by_last_name.short == 'Smith John'
    assert by_last_name.long == 'Smith John Ben'
    assert by_last_name.public == 'John S'
    assert by_last_name.full == 'Mr Smith John Ben Ph.D'
    assert by_last_name.full_name() == 'Mr Smith John Ben Ph.D'
    assert by_last_name.full_name(ordered_by='first_name') == 'Mr John Ben Smith Ph.D'
    assert by_last_name.birth_name() == 'Smith John Ben'
    assert by_last_name.birth_name(ordered_by='first_name') == 'John Ben Smith'

    assert by_last_name.size == 5
    assert by_last_name.length == len('Smith John Ben')
    assert len(by_last_name) == len('Mr Smith John Ben Ph.D')


def test_by_last_name_initials(by_last_name):
    assert by_last_name.initials() == ['S', 'J', 'B']
    assert by_last_name.initials(ordered_by='first_name') == ['J', 'B', 'S']
    assert by_last_name.initials(only='first_name') == ['J']
    assert by_last_name.initials(only='middle_name') == ['B']
    assert by_last_name.initials(only='last_name') == ['S']


def test_by_last_name_shorten(by_last_name):
    assert by_last_name.shorten() == 'Smith John'
    assert by_last_name.shorten(ordered_by='first_name') == 'John Smith'


def test_by_last_name_flatten(by_last_name):
    assert by_last_name.flatten(limit=10, by='middle_name') == 'Smith John B.'
    assert by_last_name.flatten(limit=10, by='middle_name', with_period=False) == 'Smith John B'

    short_name = Namefully('Smith John', ordered_by='last_name')
    assert short_name.flatten(limit=10, by='middle_name', with_period=False) == 'Smith John'
    assert short_name.flatten(limit=8, by='first_mid', with_period=True) == 'Smith J.'


def test_by_last_name_zip(by_last_name):
    assert by_last_name.zip() == 'S. John B.'
    assert by_last_name.zip(by='mid_last', with_period=False) == 'S John B'
    assert by_last_name.zip(by='first_name') == 'Smith J. Ben'
    assert by_last_name.zip(by='middle_name') == 'Smith John B.'
    assert by_last_name.zip(by='last_name') == 'S. John Ben'
    assert by_last_name.zip(by='first_mid') == 'Smith J. B.'
    assert by_last_name.zip(by='mid_last') == 'S. John B.'
    assert by_last_name.zip(by='all') == 'S. J. B.'


def test_can_be_instantiated_with_string():
    assert Namefully('John Smith').to_str() == 'John Smith'


def test_can_be_instantiated_with_string_list():
    assert Namefully(['John', 'Smith']).to_str() == 'John Smith'


def test_can_be_instantiated_with_json():
    assert Namefully({'first_name': 'John', 'last_name': 'Smith'}).to_str() == 'John Smith'


def test_can_be_instantiated_with_name_list():
    assert Namefully([FirstName('John'), LastName('Smith')]).to_str() == 'John Smith'
    assert Namefully([Name.first('John'), Name.last('Smith'), Name.suffix('Ph.D')]).birth == 'John Smith'


def test_can_be_instantiated_with_custom_parser():
    assert Namefully(HashParser('John#Smith'), context='simpleParser').to_str() == 'John Smith'


def test_try_parse():
    assert Namefully.parse('John') is None

    parsed = Namefully.parse('John Smith')
    assert parsed is not None
    assert parsed.short == 'John Smith'
    assert parsed.first == 'John'
    assert parsed.last == 'Smith'
    assert parsed.middle is None

    parsed = Namefully.parse('John Ben Smith')
    assert parsed is not None
    assert parsed.short == 'John Smith'
    assert parsed.first == 'John'
    assert parsed.last == 'Smith'
    assert parsed.middle == 'Ben'

    parsed = Namefully.parse('John Some Other Name Parts Smith')
    assert parsed is not None
    assert parsed.short == 'John Smith'
    assert parsed.first == 'John'
    assert parsed.last == 'Smith'
    assert parsed.middle == 'Some'
    assert ' '.join(parsed.middle_name()) == 'Some Other Name Parts'

    parsed = Namefully.parse('John "Nickname" Smith Ph.D', index=NameIndex.only(first_name=0, last_name=2, suffix=3))
    assert parsed is not None
    assert parsed.short == 'John Smith'
    assert parsed.first == 'John'
    assert parsed.last == 'Smith'
    assert parsed.suffix == 'Ph.D'
    assert parsed.middle is None


def test_can_be_built_with_name():
    name = find_name_case('byLastName')
    assert name.to_str() == 'Obama Barack'
    assert name.first == 'Barack'
    assert name.last == 'Obama'

    name = find_name_case('manyFirstNames')
    assert name.to_str() == 'Daniel Michael Blake Day-Lewis'
    assert name.first_name(False) == 'Daniel'
    assert name.first_name() == 'Daniel Michael Blake'
    assert name.has_middle is False

    name = find_name_case('manyMiddleNames')
    assert name.to_str() == 'Emilia Isobel Euphemia Rose Clarke'
    assert name.has_middle is True
    assert name.middle_name() == ['Isobel', 'Euphemia', 'Rose']

    name = find_name_case('manyLastNames')
    assert name.to_str() == 'Shakira Isabel Ripoll'
    assert name.last_name() == 'Ripoll'
    assert name.last_name(format='all') == 'Mebarak Ripoll'

    name = find_name_case('withTitling')
    assert name.to_str() == 'Dr. Albert Einstein'
    assert name.prefix == 'Dr.'

    name = find_name_case('withSeparator')
    assert name.to_str() == 'Thiago Da Silva'
    assert name.last_name() == 'Da Silva'

    name = find_name_case('withEnding')
    assert name.to_str() == 'Fabrice Piazza, Ph.D'
    assert name.birth == 'Fabrice Piazza'
    assert name.suffix == 'Ph.D'

    with pytest.raises(NameError):
        find_name_case('noBypass')
    with pytest.raises(NameError):
        Namefully('Mr John Joe Sm1th', bypass=False)
    with pytest.raises(NameError):
        Namefully('Mr John Joe Smith Ph+', bypass=False)
