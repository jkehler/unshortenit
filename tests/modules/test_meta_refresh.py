import pytest
from unshortenit.exceptions import NotFound, UnshortenFailed


@pytest.fixture
def module():
    from unshortenit.modules import MetaRefresh
    return MetaRefresh()


def test_meta_refresh_valid_link(module):
    uri = module.unshorten('https://href.li/?https://example.com')
    assert uri == 'https://example.com'
    uri = module.unshorten('https://anonymz.com/?https://example.com')
    assert uri == 'https://example.com'


def test_meta_refresh_invalid_link(module):
    with pytest.raises(UnshortenFailed, message='No meta refresh tag present.'):
        module.unshorten('https://example.com')


def test_meta_refresh_nonexistant_link(module):
    with pytest.raises(NotFound):
        module.unshorten('https://example.com/iamanonexistanturl')
