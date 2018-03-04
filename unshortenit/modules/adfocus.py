import re
import copy

from unshortenit.module import UnshortenModule
from unshortenit.exceptions import UnshortenFailed


class AdFocus(UnshortenModule):

    name = 'adfocus'
    domains = set(['adfoc.us'])

    def __init__(self, headers: dict = None, timeout: int = 30):
        super().__init__(headers, timeout)

    def unshorten(self, uri: str) -> str:
        orig_uri = uri
        res = self.get(uri)

        adlink = re.findall("click_url =.*;", res.text)

        if len(adlink) == 0:
            raise UnshortenFailed('No click_uri variable found.')

        uri = re.sub('^click_url = "|"\;$', '', adlink[0])
        if re.search(r'http(s|)\://adfoc\.us/serve/skip/\?id\=', uri):
            http_header = copy.copy(self.headers)
            http_header["Host"] = "adfoc.us"
            http_header["Referrer"] = orig_uri

            res = self.get(uri, headers=http_header)

            uri = res.url

        return uri
