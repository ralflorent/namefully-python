from namefully import Config


def test_creates_default_configuration():
    config = Config.create()
    assert config.name == 'default'
    assert config.ordered_by == 'first_name'
    assert config.separator == 'space'
    assert config.title == 'uk'
    assert config.bypass is True
    assert config.ending is False
    assert config.surname == 'father'


def test_merges_configuration_with_partial_options():
    config = Config.merge(ordered_by='first_name', separator='colon', title='us', surname='hyphenated', ending=True)
    assert config.name == 'default'
    assert config.ordered_by == 'first_name'
    assert config.separator == 'colon'
    assert config.title == 'us'
    assert config.bypass is True
    assert config.ending is True
    assert config.surname == 'hyphenated'


def test_can_create_more_than_one_configuration():
    default = Config.create('default_config')
    other = Config.merge(name='other_config', ordered_by='last_name', surname='mother', bypass=False)

    assert default.name == 'default_config'
    assert default.ordered_by == 'first_name'
    assert default.separator == 'space'
    assert default.title == 'uk'
    assert default.bypass is True
    assert default.ending is False
    assert default.surname == 'father'

    assert other.name == 'other_config'
    assert other.ordered_by == 'last_name'
    assert other.separator == 'space'
    assert other.title == 'uk'
    assert other.bypass is False
    assert other.ending is False
    assert other.surname == 'mother'


def test_can_create_copy_from_existing_configuration():
    config = Config.create('config')
    copy = config.copy_with(name='config', ordered_by='last_name', surname='mother', bypass=False)
    cloned = copy.clone()

    assert copy.name == 'config_copy'
    assert copy.ordered_by == 'last_name'
    assert copy.separator == 'space'
    assert copy.title == 'uk'
    assert copy.bypass is False
    assert copy.ending is False
    assert copy.surname == 'mother'

    assert cloned.name == 'config_copy_copy'
    assert cloned.ordered_by == 'last_name'
    assert cloned.separator == 'space'
    assert cloned.title == 'uk'
    assert cloned.bypass is False
    assert cloned.ending is False
    assert cloned.surname == 'mother'

    assert config.name == 'config'
    assert config.ordered_by == 'first_name'
    assert config.separator == 'space'
    assert config.title == 'uk'
    assert config.bypass is True
    assert config.ending is False
    assert config.surname == 'father'

    copy.reset()
    assert copy.name == 'config_copy'
    assert copy.ordered_by == 'first_name'
    assert copy.separator == 'space'
    assert copy.title == 'uk'
    assert copy.bypass is True
    assert copy.ending is False
    assert copy.surname == 'father'
