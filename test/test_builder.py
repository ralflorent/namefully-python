import pytest

from namefully import FirstName, LastName, Name, NameError
from namefully.builder import NameBuilder


def test_name_builder():
    names = [FirstName('John'), LastName('Smith')]
    middles = [Name.middle('Ben'), Name.middle('Carl')]

    assert NameBuilder.of(*names).build().full == 'John Smith'

    # lifecycle hooks
    def prebuild():
        pass

    def postbuild(n):
        assert n.full == 'John Carl Smith'

    def preclear(n):
        assert n.full == 'John Carl Smith'

    def postclear():
        pass

    builder = NameBuilder.use(
        prebuild=prebuild,
        postbuild=postbuild,
        preclear=preclear,
        postclear=postclear,
    )
    builder.add(*names)
    builder.add(middles[1])
    builder.build()

    assert builder.size == 3  # 3 name parts
    assert builder.prebuild is not None
    assert builder.postclear is not None

    # Test adding first
    builder = NameBuilder()
    builder.add(*names)
    builder.add_first(middles[0])
    assert builder.build().full == 'John Ben Smith'

    # Test removing first
    builder.remove_first()
    assert builder.build().full == 'John Smith'

    # Test removing last and adding new last
    builder.remove_last()
    builder.add_last(LastName('Doe'))
    builder.add(*middles)
    assert builder.build().full == 'John Ben Carl Doe'

    # Test removing specific name and retaining only non-middle names
    builder.remove(names[0])
    builder.retain_where(lambda name: not name.is_middle)
    builder.add(FirstName('Jack'))
    assert builder.build().full == 'Jack Doe'

    # Test adding middle names
    builder.add(*middles)
    assert builder.build().full == 'Jack Ben Carl Doe'

    # Test removing middle names
    builder.remove_where(lambda name: name.is_middle)
    assert builder.build().full == 'Jack Doe'

    # Test clearing and building empty
    builder.clear()
    with pytest.raises(NameError):
        builder.build()
