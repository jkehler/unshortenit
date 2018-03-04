import requests
import re
from urllib.parse import urlsplit

from unshortenit.exceptions import NotFound


DEFAULT_HEADERS = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',  # noqa
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip,deflate,sdch",
    "Connection": "keep-alive",
    "Accept-Language": "nl-NL,nl;q=0.8,en-US;q=0.6,en;q=0.4",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache"
}


class UnshortenModule:

    name = None
    domains = set()
    _domain_regex = None

    def __init__(self, headers: dict = None, timeout: int = None):
        self.headers = headers or DEFAULT_HEADERS
        self.timeout = timeout
        self._build_domain_regex()

    def unshorten(self, uri: str, timeout: int = 30) -> str:
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
