import requests
import re
from urllib.parse import urlsplit

from unshortenit.exceptions import NotFound


class UnshortenModule:

    name = None
    domains = set()
    _domain_regex = None

    def __init__(self, headers: dict = None, timeout: int = 30):
        self.headers = headers
        self.timeout = timeout
        self._build_domain_regex()

    def unshorten(self, uri: str, timeout: int = None) -> str:
        raise NotImplementedError

    def _build_domain_regex(self):
        regex_str = r'^(' + r'|'.join(self.domains) + r')$'
        regex_str = re.sub(r'\.', '\.', regex_str)
        self._domain_regex = re.compile(regex_str)

    def get(self, uri: str, headers: dict = None, timeout: int = None) -> requests.Response:
        res = requests.get(uri, headers=headers or self.headers, timeout=timeout or self.timeout)
        if res.status_code != 200:
            raise NotFound(res.status_code)
        return res

    def is_match(self, url):
        domain = urlsplit(url).netloc
        return self._domain_regex.match(domain)

    def add_domain(self, domain):
        self.domains.add(domain)
        self._build_domain_regex()
