#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from selenium.webdriver import PhantomJS
    from contextlib import closing
    linkbucks_support = True
except:
    linkbucks_support = False
try:
    from urllib.request import urlsplit, urlparse
except:
    from urlparse import urlsplit, urlparse
import re
import os
import requests
import time
import json
from base64 import b64decode
import random

class UnshortenIt(object):

    _headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Encoding': 'gzip,deflate,sdch',
                'Accept-Language': 'en-US,en;q=0.8',
                'Connection': 'keep-alive',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.69 Safari/537.36'}
    _adfly_regex = r'adf\.ly|q\.gs|j\.gs|u\.bb|ay\.gy'
    _linkbucks_regex = r'linkbucks\.com|any\.gs|cash4links\.co|cash4files\.co|dyo\.gs|filesonthe\.net|goneviral\.com|megaline\.co|miniurls\.co|qqc\.co|seriousdeals\.net|theseblogs\.com|theseforums\.com|tinylinks\.co|tubeviral\.com|ultrafiles\.net|urlbeat\.net|whackyvidz\.com|yyv\.co'
    _adfocus_regex = r'adfoc\.us'
    _lnxlu_regex = r'lnx\.lu'
    _shst_regex = r'sh\.st'
    _this_dir, _this_filename = os.path.split(__file__)
    _timeout = 10

    def unshorten(self, uri, type=None, timeout=10):
        domain = urlsplit(uri).netloc
        self._timeout = timeout

        if re.search(self._adfly_regex, domain, re.IGNORECASE) or type == 'adfly':
            return self._unshorten_adfly(uri)
        if re.search(self._adfocus_regex, domain, re.IGNORECASE) or type =='adfocus':
            return self._unshorten_adfocus(uri)
        if re.search(self._linkbucks_regex, domain, re.IGNORECASE) or type == 'linkbucks':
            if linkbucks_support:
                return self._unshorten_linkbucks(uri)
            else:
                return uri, 'linkbucks.com not supported. Install selenium package to add support.'
        if re.search(self._lnxlu_regex, domain, re.IGNORECASE) or type == 'lnxlu':
            return self._unshorten_lnxlu(uri)
        if re.search(self._shst_regex, domain, re.IGNORECASE):
            return self._unshorten_shst(uri)

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
                ysmm = re.sub(r'var ysmm \= \'|\'\;', '', ysmm[0])

                left = ''
                right = ''

                for c in [ysmm[i:i+2] for i in range(0, len(ysmm), 2)]:
                    left += c[0]
                    right = c[1] + right

                decoded_uri = b64decode(left.encode() + right.encode())[2:].decode()

                if re.search(r'go\.php\?u\=', decoded_uri):
                    decoded_uri = b64decode(re.sub(r'(.*?)u=', '', decoded_uri)).decode()

                return decoded_uri, r.status_code
            else:
                return uri, 'No ysmm variable found'

        except Exception as e:
            return uri, str(e)

    def _unshorten_linkbucks(self, uri):
        try:
            with closing(PhantomJS(
                    service_log_path=os.path.dirname(os.path.realpath(__file__)) + '/ghostdriver.log')) as browser:
                browser.get(uri)

                # wait 5 seconds
                time.sleep(5)

                page_source = browser.page_source

                link = re.findall(r'skiplink(.*?)\>', page_source)
                if link is not None:
                    link = re.sub(r'\shref\=|\"', '', link[0])
                    if link == '':
                        return uri, 'Failed to extract link.'
                    return link, 200
                else:
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

    def _unshorten_shst(self, uri):
        try:
            r = requests.get(uri, headers=self._headers, timeout=self._timeout)
            html = r.text

            session_id = re.findall(r'sessionId\:(.*?)\"\,', html)
            if len(session_id) > 0:
                session_id = re.sub(r'\s\"', '', session_id[0])

                http_header = {
                    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.46 Safari/535.11",
                    "Accept-Encoding": "gzip,deflate,sdch",
                    "Accept-Language": "en-US,en;,q=0.8",
                    "Connection": "keep-alive",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Host": "sh.st",
                    "Referer": uri,
                    "Origin": "http://sh.st",
                    "X-Requested-With": "XMLHttpRequest"
                }

                time.sleep(5)

                payload = {'adSessionId': session_id, 'callback': 'c'}
                r = requests.get('http://sh.st/shortest-url/end-adsession', params=payload, headers=http_header, timeout=self._timeout)
                response = r.content[6:-2].decode('utf-8')
                
                if r.status_code == 200:
                    resp_uri = json.loads(response)['destinationUrl']
                    if resp_uri is not None:
                        uri = resp_uri
                    else:
                        return uri, 'Error extracting url'
                else:
                    return uri, 'Error extracting url'

            return uri, r.status_code

        except Exception as e:
            return uri, str(e)


def unshorten(uri, type=None, timeout=10):
    unshortener = UnshortenIt()
    return unshortener.unshorten(uri, type, timeout)
