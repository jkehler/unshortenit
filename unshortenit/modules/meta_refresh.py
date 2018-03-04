from lxml import html
from urllib.parse import urljoin

from unshortenit.module import UnshortenModule
from unshortenit.exceptions import UnshortenFailed


class MetaRefresh(UnshortenModule):

    name = 'meta-refresh'
    domains = [
        'href.li',
        'anonymz.com'
    ]

    def __init__(self, headers: dict = None, timeout: int = 30):
        super().__init__(headers, timeout)

    def unshorten(self, uri: str) -> str:
        res = self.get(uri)

        html_tree = html.fromstring(res.text)
        meta_attr = html_tree.xpath(
            "//meta[translate(@http-equiv, 'REFSH', 'refsh') = 'refresh']/@content"
        )
        if not meta_attr:
            raise UnshortenFailed('No meta refresh tag present.')

        _, url = meta_attr[0].split(';')
        if url.strip().lower().startswith('url='):
            url = url[5:]
            if not url.startswith('http'):
                url = urljoin(res.url, url)

            return url
        else:
            raise UnshortenFailed('Failed to extract meta refresh tag.')
