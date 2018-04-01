from typing import List
import requests

from .module import UnshortenModule
from .modules import AdfLy, AdFocus, ShorteSt, MetaRefresh
from unshortenit import __version__


DEFAULT_HEADERS = {
    'User-Agent': 'unshortenit {}'.format(__version__),
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.5',
    'Cache-Control': "no-cache",
}


class UnshortenIt:

    modules = {}
    _default_headers = None
    _default_timeout = None

    def __init__(self, default_timeout: int = 30, default_headers: dict = None):
        self._default_headers = default_headers or DEFAULT_HEADERS
        self._default_timeout = default_timeout

        self.register_modules([
            AdfLy,
            AdFocus,
            ShorteSt,
            MetaRefresh
        ])

    def register_module(self, module: UnshortenModule):
        if not isinstance(module, UnshortenModule):
            module = module(headers=self._default_headers, timeout=self._default_timeout)
        self.modules[module.name] = module

    def register_modules(self, modules: List[UnshortenModule]):
        for module in modules:
            self.register_module(module)

    def unshorten(self, uri: str, module: str = None, timeout: int = None,
                  unshorten_nested: bool = False, force: bool = False) -> str:

        timeout = timeout or self._default_timeout

        if module and module in self.modules:
            return self.modules[module].unshorten(uri)

        if unshorten_nested:
            last_uri = uri
            while True:
                matched = False
                for k, m in self.modules.items():
                    if m.is_match(uri):
                        matched = True
                        uri = m.unshorten(uri)
                        if uri == last_uri:
                            break
                        last_uri = uri
                if not matched:
                    break
        else:
            for k, m in self.modules.items():
                if m.is_match(uri):
                    return m.unshorten(uri)

        res = requests.get(uri, timeout=timeout, headers=self._default_headers)
        return res.url
