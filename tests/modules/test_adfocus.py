import pytest

from unshortenit.exceptions import NotFound, UnshortenFailed
from unshortenit.unshortenit import DEFAULT_HEADERS


@pytest.fixture
def adfocus():
    from unshortenit.modules import AdFocus
    return AdFocus(headers=DEFAULT_HEADERS)


def test_adfocus_valid_link(adfocus):
    uri = adfocus.unshorten('http://adfoc.us/340347863622')
    assert uri == 'http://www7.zippyshare.com/v/24727439/file.html'


def test_adfocus_invalid_link(adfocus):
    with pytest.raises(UnshortenFailed, message='No click_url variable found.'):
        adfocus.unshorten('http://adf.ly/1icWR')


def test_adfocus_nonexistant_link(adfocus):
    with pytest.raises(NotFound):
        adfocus.unshorten('https://example.com/iamanonexistanturl')
