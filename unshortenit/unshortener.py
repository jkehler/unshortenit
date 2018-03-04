from typing import List

from .module import UnshortenModule


class Unshortener:

    modules = {}
    _default_headers = None
    _default_timeout = None

    def __init__(self, default_timeout: int = None, default_headers: int = None):
        self._default_headers = default_headers
        self._default_timeout = default_timeout

    def register_module(self, module: UnshortenModule, use_defaults: bool = True):
        if use_defaults and self._default_headers:
            module.headers = self._default_headers
        if use_defaults and self._default_timeout:
            module.timeout = self._default_timeout
        self.modules[module.name] = module

    def register_modules(self, modules: List[UnshortenModule], use_defaults: bool = True):
        for module in modules:
            self.register_module(module, use_defaults)

    def unshorten(self, uri: str, module: str = None, timeout: int = 30,
                  unshorten_nested: bool = False) -> str:
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

        return uri
