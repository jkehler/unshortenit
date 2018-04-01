import pytest
from unshortenit.exceptions import NotFound, UnshortenFailed


@pytest.fixture
def adfly():
    from unshortenit.modules import AdfLy
    return AdfLy()


def test_adfly_valid_link(adfly):
    uri = adfly.unshorten('http://j.gs/AXr9')
    assert uri == 'https://microsoft.com'


def test_adfly_invalid_link(adfly):
    with pytest.raises(UnshortenFailed, message='No ysmm variable found.'):
        adfly.unshorten('http://adf.ly/1icWR')


def test_adfly_nonexistant_link(adfly):
    with pytest.raises(NotFound):
        adfly.unshorten('https://microsoft.com/iamanonexistanturl')
