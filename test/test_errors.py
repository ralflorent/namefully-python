from namefully import NameError


def test_base_error():
    error = NameError('sample error message')
    assert isinstance(error, Exception)
    assert repr(error) == '<NameError>'
    assert str(error) == 'NameError: sample error message'
    assert error.name == 'NameError'
    assert error.message == 'sample error message'
