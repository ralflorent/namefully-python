_Title = ['uk', 'us']
_CapsRange = ['initial', 'all']
_NameOrder = ['first_name', 'last_name']
_Surname = ['father', 'mother', 'hyphenated', 'all']
_Namon = ['prefix', 'first_name', 'middle_name', 'last_name', 'suffix']


class Separator:
    comma = ('comma', ',')
    colon = ('colon', ':')
    double_quote = ('double_quote', '"')
    empty = ('empty', '')
    hyphen = ('hyphen', '-')
    period = ('period', '.')
    semi_colon = ('semi_colon', ';')
    single_quote = ('single_quote', "'")
    space = ('space', ' ')
    underscore = ('underscore', '_')

    @staticmethod
    def all():
        return dict(
            comma=Separator.comma,
            colon=Separator.colon,
            double_quote=Separator.double_quote,
            empty=Separator.empty,
            hyphen=Separator.hyphen,
            period=Separator.period,
            semi_colon=Separator.semi_colon,
            single_quote=Separator.single_quote,
            space=Separator.space,
            underscore=Separator.underscore,
        )

    @staticmethod
    def tokens():
        return [s[1] for s in Separator.all().values()]
