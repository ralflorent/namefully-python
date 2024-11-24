import pytest

from namefully import Config

@pytest.fixture(autouse=True)
def clear_configs():
    Config.clear() # Clear Config._cache before each test