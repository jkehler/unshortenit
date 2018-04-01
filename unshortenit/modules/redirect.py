from unshortenit.module import UnshortenModule


class Redirect(UnshortenModule):

    name = 'redirect'
    domains = set(['fb.me'])

    def __init__(self, headers: dict = None, timeout: int = 30):
        super().__init__(headers, timeout)

    def unshorten(self, uri: str) -> str:
        res = self.get(uri)
        return res.url
