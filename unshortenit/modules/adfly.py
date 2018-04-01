import re
from base64 import b64decode

from unshortenit.module import UnshortenModule
from unshortenit.exceptions import UnshortenFailed


class AdfLy(UnshortenModule):

    name = 'adfly'
    domains = set([
        'adf.ly',
        'j.gs',
        'q.gs',
        'u.bb',
        'ay.gy',
        'atominik.com',
        'tinyium.com',
        'microify.com'
    ])

    def __init__(self, headers: dict = None, timeout: int = 30):
        super().__init__(headers=headers, timeout=timeout)

    def unshorten(self, uri: str) -> str:
        """ http://j.gs/AXr9 """
        res = self.get(uri)

        ysmm = re.findall(r'var ysmm =.*\;?', res.text)

        if len(ysmm) == 0:
            raise UnshortenFailed('No ysmm variable found.')

        # Decode the ysmm variable and extract the actual link
        ysmm = re.sub(r'var ysmm \= \'|\'\;', '', ysmm[0])

        left = ''
        right = ''

        for c in [ysmm[i:i+2] for i in range(0, len(ysmm), 2)]:
            left += c[0]
            right = c[1] + right

        # Additional digit arithmetic
        encoded_uri = list(left + right)
        numbers = ((i, n) for i, n in enumerate(encoded_uri) if str.isdigit(n))
        for first, second in zip(numbers, numbers):
            xor = int(first[1]) ^ int(second[1])
            if xor < 10:
                encoded_uri[first[0]] = str(xor)

        decoded_uri = b64decode("".join(encoded_uri).encode())[16:-16].decode()

        if re.search(r'go\.php\?u\=', decoded_uri):
            decoded_uri = b64decode(re.sub(r'(.*?)u=', '', decoded_uri)).decode()

        return decoded_uri
