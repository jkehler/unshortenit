#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import PyV8
    adfly_support = True
except:
    adfly_support = False
try:
    from urllib.request import urlsplit
except:
    from urlparse import urlsplit
import re
import os
import requests
from io import open


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

    def unshorten(self, uri, type=None):
        domain = urlsplit(uri).netloc

        if re.search(self._adfly_regex, domain, re.IGNORECASE) or type == 'adfly':
            if adfly_support:
                return self._unshorten_adfly(uri)
            else:
                return uri, 'adf.ly not supported. Install PyV8 to add support.'
        if re.search(self._adfocus_regex, domain, re.IGNORECASE):
            return self._unshorten_adfocus(uri)
        if re.search(self._linkbucks_regex, domain, re.IGNORECASE):
            return self._unshorten_linkbucks(uri)
        if re.search(self._lnxlu_regex, domain, re.IGNORECASE):
            return self._unshorten_lnxlu(uri)

        try:
            # headers stop t.co from working so omit headers if this is a t.co link
            if domain == 't.co':
                r = requests.get(uri)
            else:
                r = requests.get(uri, headers=self._headers)
            return r.url, r.status_code
        except Exception as e:
            return uri, str(e)

    def _unshorten_adfly(self, uri):

        try:
            r = requests.get(uri, headers=self._headers)
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
            r = requests.get(uri, headers=self._headers)
            html = r.text
            link = re.search("Lbjs.TargetUrl.*\;", html)

            if link:
                uri = re.sub("Lbjs.TargetUrl = '|'\;$", '', link.group(0))
                return uri, r.status_code
            else:
                return uri, 'No TargetUrl variable found'
        except Exception as e:
            return uri, str(e)

    def _unshorten_adfocus(self, uri):
        try:
            http_header = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.46 Safari/535.11",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "nl-NL,nl;q=0.8,en-US;q=0.6,en;q=0.4"}

            r = requests.get(uri, headers=http_header)
            html = r.text

            adlink = re.findall("click_url =.*;", html)

            if len(adlink) > 1:
                uri = re.sub('^click_url = "|"\;$', '', adlink[1])
                return uri, r.status_code
            else:
                return uri, 'No click_url variable found'
        except Exception as e:
            return uri, str(e)

    def _unshorten_lnxlu(self, uri):
        try:
            r = requests.get(uri, headers=self._headers)
            html = r.text

            code = re.findall('/\?click\=(.*)\."', html)

            if len(code) > 0:
                payload = {'click': code[0]}
                r = requests.get('http://lnx.lu/', params=payload, headers=self._headers)
                return r.url, r.status_code
            else:
                return uri, 'No click variable found'
        except Exception as e:
            return uri, str(e)


def unshorten(uri, type=None):
    unshortener = UnshortenIt()
    return unshortener.unshorten(uri, type)
