from lxml import html
from urllib.parse import urlparse
import requests
import re
import time

from unshortenit.module import UnshortenModule
from unshortenit.exceptions import UnshortenFailed


class LinkBucks(UnshortenModule):

    name = 'linkbucks'
    domains = set([
        'linkbucks.com',
        'www.linkbucks.com',
        'www.jzrputtbut.net',
        'any.gs',
        'cash4links.co',
        'cache4files.co',
        'dyo.gs',
        'filesonthe.net',
        'goneviral.com',
        'megaline.co',
        'miniurls.co',
        'qqc.co',
        'seriousdeals.net',
        'theseblogs.com',
        'theseforums.com',
        'tinylinks.co',
        'tubeviral.com',
        'ultrafiles.net',
        'urlbeat.net',
        'whackyvidz.com',
        'yyv.co'
    ])

    def __init__(self, headers: dict = None, timeout: int = 30):
        super().__init__(headers, timeout)

    def unshorten(self, uri: str) -> str:
        session = requests.session()

        res = session.get(uri, headers=self.headers, timeout=self.timeout)

        html_tree = html.fromstring(res.text)
        script_tags = html_tree.xpath(
            "//script[contains(.,'var params')]"
        )

        if len(script_tags) == 0:
            raise UnshortenFailed('Could not find decoder script.')

        lines = script_tags[-1].text_content().split('\n')

        numbers = []
        token = None
        keyUrl = None

        for line in lines:
            line = line.strip()
            if re.match(r"^params\['A.*y'\] \=.*;$", line):
                numbers.append(int(re.findall(r'[0-9]+', line)[0]))
            if re.match(r'^Token\:.*$', line):
                token = re.findall(r"'[0-9a-zA-Z]+'", line)[0].replace("'", '')
            if re.match(r'^KeyUrl\:.*$', line):
                keyUrl = re.findall("'.*'", line)[0].replace("'", '')

        if len(numbers) == 0 or token is None or keyUrl is None:
            raise UnshortenFailed('Failed to extract token and authkey.')

        authKey = sum(set(numbers))
        print(set(numbers), authKey, token, keyUrl)

        keyUrl = 'http://{domain}{keyUrl}'.format(
            domain=urlparse(res.url).netloc,
            keyUrl=keyUrl
        )
        print(keyUrl)

        headers = {
            'Accept': '/',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Host': urlparse(res.url).netloc,
            'Referrer': res.url,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0' # noqa
        }

        session.get(
            'http://www.linkbucks.com/scripts/intermissionLink.v13.js',
            headers=headers,
            timeout=self.timeout
        )
        session.get(keyUrl, headers=headers, timeout=self.timeout)

        params = dict(
            a_b=True,
            aK=authKey,
            t=token
        )

        time.sleep(5)
        intermission_url = 'http://{domain}/intermission/loadTargetUrl'.format(
            domain=urlparse(res.url).netloc
        )
        res = session.get(intermission_url, params=params, headers=headers)
        print(res.text)

        session.close()
        # ak = re.findall(r"params\['A.*y'] \= .*;", script)
        # for k in ak:
        #     print(k)
