===============================
unshortenit
===============================

Unshortens ad-based urls and 301 redirects. Supports adf.ly, lnx.lu, linkbucks.com, and adfoc.us


Features
--------

- Supports unshortening the following ad-based shortners:
    - Adf.ly and related subdomains
    - Custom adf.ly domains by passing the type='adfly' parameter
    - Lnx.lu
    - Linkbucks.com and related subdomains (Selenium library with PhantomJS required)
    - Adfoc.us
    - Sh.st
- Supports any 301 redirected urls
- Python 2.7 and 3.3 support

Usage
-----

    import unshortenit
    unshortened_uri,status = unshortenit.unshorten('http://ul.to')

> unshortenit.unshorten will return a tuple (unshortened_uri,status)

> unshortened_uri will contain the unshortened uri. If you pass in a non-shortener url it will return the original url.
> status will contain the status code or any error messages

Installation
------------

    pip install unshortenit

In order to enable linkbucks.com support you will need to install selenium along with PhantomJS.
