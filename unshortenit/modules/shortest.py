import re
import copy
import time
import json
import requests

from unshortenit.module import UnshortenModule
from unshortenit.exceptions import UnshortenFailed


class ShorteSt(UnshortenModule):

    name = 'shortest'
    domains = ['sh.st', 'festyy.com', 'ceesty.com']

    def __init__(self, headers: dict = None, timeout: int = 30):
        super().__init__(headers, timeout)

    def unshorten(self, uri: str) -> str:
        res = self.get(uri)

        session_id = re.findall(r'sessionId\:(.*?)\"\,', res.text)
        if len(session_id) == 0:
            raise UnshortenFailed('No sessionId variable found.')

        if len(session_id) > 0:
            session_id = re.sub(r'\s\"', '', session_id[0])

            http_header = copy.copy(self.headers or {})
            http_header["Content-Type"] = "application/x-www-form-urlencoded"
            http_header["Host"] = "sh.st"
            http_header["Referer"] = uri
            http_header["Origin"] = "http://sh.st"
            http_header["X-Requested-With"] = "XMLHttpRequest"

            time.sleep(5)

            payload = {'adSessionId': session_id, 'callback': 'c'}
            r = requests.get(
                'http://sh.st/shortest-url/end-adsession',
                params=payload,
                headers=http_header,
                timeout=self.timeout
            )
            response = r.content[6:-2].decode('utf-8')

            if r.status_code == 200:
                resp_uri = json.loads(response)['destinationUrl']
                if resp_uri is not None:
                    uri = resp_uri
                else:
                    raise UnshortenFailed('Error extracting url.')
            else:
                raise UnshortenFailed('Error extracting url.')

        return uri
