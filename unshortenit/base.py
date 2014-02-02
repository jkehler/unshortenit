#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import PyV8
    adfly_support = True
except:
    adfly_support = False
try:
    from urllib.request import urlsplit, urlparse
except:
    from urlparse import urlsplit, urlparse
import re
import os
import requests
from io import open
import time
from random import randint
import json

class UnshortenIt(object):

    _headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Encoding': 'gzip,deflate,sdch',
                'Accept-Language': 'en-US,en;q=0.8',
                'Connection': 'keep-alive',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.69 Safari/537.36'}
    _adfly_regex = r'adf\.ly|q\.gs|j\.gs|u\.bb'
    _linkbucks_regex = r'linkbucks\.com|any\.gs|cash4links\.co|cash4files\.co|dyo\.gs|filesonthe\.net|goneviral\.com|megaline\.co|miniurls\.co|qqc\.co|seriousdeals\.net|theseblogs\.com|theseforums\.com|tinylinks\.co|tubeviral\.com|ultrafiles\.net|urlbeat\.net|whackyvidz\.com|yyv\.co'
    _adfocus_regex = r'adfoc\.us'
    _lnxlu_regex = r'lnx\.lu'
    _this_dir, _this_filename = os.path.split(__file__)
    _timeout = 10

    def __init__(self, adfly_js_file=None):
        if adfly_support:
            self.ctx = PyV8.JSContext()
            self.ctx.enter()
            if adfly_js_file is None:
                adfly_js_file = os.path.join(self._this_dir, 'adfly.js')
            if os.path.isfile(adfly_js_file):
                file = open(adfly_js_file, 'r', encoding="iso-8859-1")
                self.adfly_js = file.read()
                file.close()

    def unshorten(self, uri, type=None, timeout=10):
        domain = urlsplit(uri).netloc
        self._timeout = timeout

        if re.search(self._adfly_regex, domain, re.IGNORECASE) or type == 'adfly':
            if adfly_support:
                return self._unshorten_adfly(uri)
            else:
                return uri, 'adf.ly not supported. Install PyV8 to add support.'
        if re.search(self._adfocus_regex, domain, re.IGNORECASE) or type =='adfocus':
            return self._unshorten_adfocus(uri)
        if re.search(self._linkbucks_regex, domain, re.IGNORECASE) or type == 'linkbucks':
            return self._unshorten_linkbucks(uri)
        if re.search(self._lnxlu_regex, domain, re.IGNORECASE) or type == 'lnxlu':
            return self._unshorten_lnxlu(uri)

        try:
            # headers stop t.co from working so omit headers if this is a t.co link
            if domain == 't.co':
                r = requests.get(uri, timeout=self._timeout)
                return r.url, r.status_code
            # p.ost.im uses meta http refresh to redirect.
            if domain == 'p.ost.im':
                r = requests.get(uri, headers=self._headers, timeout=self._timeout)
                uri = re.findall(r'.*url\=(.*?)\"\.*',r.text)[0]
                return uri, 200
            r = requests.head(uri, headers=self._headers, timeout=self._timeout)
            while True:
                if 'location' in r.headers:
                    r = requests.head(r.headers['location'])
                    uri = r.url
                else:
                    return r.url, r.status_code

        except Exception as e:
            return uri, str(e)

    def _unshorten_adfly(self, uri):

        try:
            r = requests.get(uri, headers=self._headers, timeout=self._timeout)
            html = r.text
            ysmm = re.findall(r"var ysmm =.*\;?", html)

            if len(ysmm) > 0:

                decoded_uri = self.ctx.eval(ysmm[0] + self.adfly_js)
                return decoded_uri, r.status_code
            else:
                return uri, 'No ysmm variable found'

        except Exception as e:
            return uri, str(e)

    def _unshorten_linkbucks(self, uri):
        try:
            retry_limit = 4
            retry_count = 0
            while True:

                r = requests.get(uri, headers=self._headers, timeout=self._timeout)

                html = r.text
                o = urlparse(uri)
                base_url = 'http://' + o.netloc
                time_val = 59550686 #55058824 #15127928
                time_val = randint(1420000, 6400000)


                headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                            'Accept-Encoding': 'gzip,deflate,sdch',
                            'Accept-Language': 'en-US,en;q=0.8',
                            'Connection': 'keep-alive',
                            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.69 Safari/537.36',
                            'Host': o.netloc,
                            'Referer': base_url + '/'}

                tokens = re.findall(r"params\[\(\'To\' \+ \'Ad\' \+ \'ken\' \+ \'Url\'\)\.replace\(\'Ad\', \'\'\)\.replace\(\'Url\'\, \'\'\)\](.*)\;", html)
                if len(tokens) == 4:
                    token = re.sub('\s|\+|\=|\'', '', tokens[2].strip())
                    token += re.sub('\s|\+|\=|\'', '', tokens[3].strip())

                    r = requests.get(base_url + '/scripts/generated/key.js?t=' + str(token) + '&' + str(time_val), headers=headers, timeout=self._timeout)
                    time.sleep(5)
                    r = requests.get(base_url + '/intermission/loadTargetUrl?t=' + str(token), headers=headers, timeout=self._timeout)
                    response = json.loads(r.text)
                    if response['Success'] == True:
                        if 'Url' in response:
                            url = response['Url']
                            return url, r.status_code

                if retry_count < retry_limit:
                    retry_count += 1
                else:
                    break

            return uri, 'Failed to extract link.'

        except Exception as e:
            return uri, str(e)

    def _unshorten_adfocus(self, uri):
        orig_uri = uri
        try:
            http_header = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.46 Safari/535.11",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "nl-NL,nl;q=0.8,en-US;q=0.6,en;q=0.4",
                "Cache-Control": "no-cache",
                "Pragma": "no-cache"
            }

            r = requests.get(uri, headers=http_header, timeout=self._timeout)
            html = r.text

            adlink = re.findall("click_url =.*;", html)

            if len(adlink) > 0:
                uri = re.sub('^click_url = "|"\;$', '', adlink[0])
                if re.search(r'http(s|)\://adfoc\.us/serve/skip/\?id\=', uri):
                    http_header = {
                        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.46 Safari/535.11",
                        "Accept-Encoding": "gzip,deflate,sdch",
                        "Accept-Language": "en-US,en;,q=0.8",
                        "Connection": "keep-alive",
                        "Host": "adfoc.us",
                        "Cache-Control": "no-cache",
                        "Pragma": "no-cache",
                        "Referer": orig_uri,
                    }
                    r = requests.get(uri, headers=http_header, timeout=self._timeout)
                    print(r.headers)

                    uri = r.url
                return uri, r.status_code
            else:
                return uri, 'No click_url variable found'
        except Exception as e:
            return uri, str(e)

    def _unshorten_lnxlu(self, uri):
        try:
            r = requests.get(uri, headers=self._headers, timeout=self._timeout)
            html = r.text

            code = re.findall('/\?click\=(.*)\."', html)

            if len(code) > 0:
                payload = {'click': code[0]}
                r = requests.get('http://lnx.lu/', params=payload, headers=self._headers, timeout=self._timeout)
                return r.url, r.status_code
            else:
                return uri, 'No click variable found'
        except Exception as e:
            return uri, str(e)


def unshorten(uri, type=None, timeout=10):
    unshortener = UnshortenIt()
    return unshortener.unshorten(uri, type, timeout)
