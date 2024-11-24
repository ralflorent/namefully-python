from namefully import FirstName, FullName, LastName, Name, Namefully, Parser

NAME_CASES = {
    'simpleName': {'name': 'John Smith', 'options': {'context': 'simpleName'}},
    'byLastName': {'name': 'Obama Barack', 'options': {'context': 'byLastName', 'ordered_by': 'last_name'}},
    'manyFirstNames': {
        'name': [FirstName('Daniel', 'Michael', 'Blake'), LastName('Day-Lewis')],
        'options': {'context': 'manyFirstNames'},
    },
    'manyMiddleNames': {
        'name': [
            FirstName('Emilia'),
            Name.middle('Isobel'),
            Name.middle('Euphemia'),
            Name.middle('Rose'),
            LastName('Clarke'),
        ],
        'options': {'context': 'manyMiddleNames'},
    },
    'manyLastNames': {
        'name': [FirstName('Shakira', 'Isabel'), LastName('Mebarak', 'Ripoll')],
        'options': {'context': 'manyLastNames', 'surname': 'mother'},
    },
    'withTitling': {
        'name': {'prefix': 'Dr', 'first_name': 'Albert', 'last_name': 'Einstein'},
        'options': {'context': 'withTitling', 'title': 'us'},
    },
    'withEnding': {
        'name': {'first_name': 'Fabrice', 'last_name': 'Piazza', 'suffix': 'Ph.D'},
        'options': {'context': 'withEnding', 'ending': True},
    },
    'withSeparator': {
        'name': 'Thiago, Da Silva',
        'options': {'context': 'withSeparator', 'separator': ','},
    },
    'noBypass': {
        'name': {'prefix': 'Mme', 'first_name': 'Marine', 'last_name': 'Le Pen', 'suffix': 'M.Sc.'},
        'options': {'context': 'noBypass', 'bypass': False, 'ending': True, 'title': 'us'},
    },
}


def find_name_case(case: str) -> Namefully:
    name_case = NAME_CASES[case]
    return Namefully(name_case['name'], **name_case['options'])


class HashParser(Parser):
    def parse(self, **options) -> FullName:
        first_name, last_name = self.raw.split('#')
        return FullName.parse({'first_name': first_name, 'last_name': last_name}, **options)
