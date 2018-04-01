import pytest
from unshortenit.exceptions import NotFound, UnshortenFailed


@pytest.fixture
def module():
    from unshortenit.modules import ShorteSt
    return ShorteSt()


def test_shortest_valid_link(module):
    uri = module.unshorten('http://sh.st/INTI')
    assert uri == 'https://adf.ly/b2H0Y'


def test_shortest_invalid_link(module):
    with pytest.raises(UnshortenFailed, message='No click_url variable found.'):
        module.unshorten('http://sh.st')


def test_shortest_nonexistant_link(module):
    with pytest.raises(NotFound):
        module.unshorten('https://example.com/iamanonexistanturl')
