from namefully._types import Separator
from namefully._utils import NameIndex, capitalize, decapitalize, toggle_case

FIRST_NAME, LAST_NAME = 'first_name', 'last_name'


def test_name_index_when_first_name():
    indexes = NameIndex.when(FIRST_NAME, 2)
    assert indexes.first_name == 0
    assert indexes.last_name == 1

    indexes = NameIndex.when(FIRST_NAME, 3)
    assert indexes.first_name == 0
    assert indexes.middle_name == 1
    assert indexes.last_name == 2

    indexes = NameIndex.when(FIRST_NAME, 4)
    assert indexes.prefix == 0
    assert indexes.first_name == 1
    assert indexes.middle_name == 2
    assert indexes.last_name == 3

    indexes = NameIndex.when(FIRST_NAME, 5)
    assert indexes.prefix == 0
    assert indexes.first_name == 1
    assert indexes.middle_name == 2
    assert indexes.last_name == 3
    assert indexes.suffix == 4


def test_name_index_when_last_name():
    indexes = NameIndex.when(LAST_NAME, 2)
    assert indexes.last_name == 0
    assert indexes.first_name == 1

    indexes = NameIndex.when(LAST_NAME, 3)
    assert indexes.last_name == 0
    assert indexes.first_name == 1
    assert indexes.middle_name == 2

    indexes = NameIndex.when(LAST_NAME, 4)
    assert indexes.prefix == 0
    assert indexes.last_name == 1
    assert indexes.first_name == 2
    assert indexes.middle_name == 3

    indexes = NameIndex.when(LAST_NAME, 5)
    assert indexes.prefix == 0
    assert indexes.last_name == 1
    assert indexes.first_name == 2
    assert indexes.middle_name == 3
    assert indexes.suffix == 4


def test_name_index_when_wrong_counts():
    indexes = NameIndex.when(FIRST_NAME, 0)
    assert indexes.first_name == 0
    assert indexes.last_name == 1
    assert indexes.prefix == -1
    assert indexes.middle_name == -1
    assert indexes.suffix == -1

    indexes = NameIndex.when(LAST_NAME, 0)
    assert indexes.first_name == 0
    assert indexes.last_name == 1
    assert indexes.prefix == -1
    assert indexes.middle_name == -1
    assert indexes.suffix == -1


def test_capitalize():
    assert capitalize('') == ''
    assert capitalize('stRiNg') == 'String'
    assert capitalize('stRiNg', 'initial') == 'String'
    assert capitalize('StRiNg', 'all') == 'STRING'
    assert capitalize('StRiNg', None) == 'StRiNg'


def test_decapitalize():
    assert decapitalize('') == ''
    assert decapitalize('StRiNg') == 'stRiNg'
    assert decapitalize('StRiNg', 'initial') == 'stRiNg'
    assert decapitalize('StRiNg', 'all') == 'string'
    assert decapitalize('StRiNg', None) == 'StRiNg'


def test_toggle_case():
    assert toggle_case('toggle') == 'TOGGLE'
    assert toggle_case('toGGlE') == 'TOggLe'


def test_separator_tokens():
    assert Separator.tokens() == [',', ':', '"', '', '-', '.', ';', "'", ' ', '_']
    assert Separator.period == ('period', '.')
    assert Separator.space == ('space', ' ')
    assert Separator.empty == ('empty', '')
    assert Separator.hyphen == ('hyphen', '-')
    assert Separator.single_quote == ('single_quote', "'")
    assert Separator.double_quote == ('double_quote', '"')
    assert Separator.comma == ('comma', ',')
    assert Separator.colon == ('colon', ':')
    assert Separator.semi_colon == ('semi_colon', ';')
    assert Separator.underscore == ('underscore', '_')
