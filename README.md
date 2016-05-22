===============================
unshortenit
===============================

Unshortens ad-based urls and 301 redirects. Supports adf.ly, lnx.lu, and sh.st.

* Linkbucks.com and adfoc.us support temporarly removed.

Features
--------

- Supports unshortening the following ad-based shortners:
	- Adf.ly and related subdomains
	- Custom adf.ly domains by passing the type='adfly' parameter
	- Sh.st
- Supports any 301 redirected urls
- Python 2.7, 3.3, and 3.4 support

Usage
-----

	import unshortenit

	# Unshorten known ad urls.
	# This call will not generate any HTTP requests unless the passed 
	# URL is a known ad/shortening link, and the library knows how to
	# unshortedn said link.
	unshortened_uri, status = unshortenit.unshorten_only('http://ul.to')

	# Unwrap any HTTP 30x redirects (if present). This will *always* issue a HTTP 
	# HEAD request, even if there is not a  30x redirect on the passed link 
	# (you cannot tell if a redirect is present without making a request).
	unshortened_uri, status = unshortenit.unwrap_30x_only('http://ul.to')

	# Unshorten any ad content, and unwrap any HTTP 30x redirects (if present).
	# Internally, this basically calls unshorten_only(), and then unwrap_30x_only()
	# sequentially on the passed URL, returning early if the unshorten_only()
	# call returned an error.
	unshortened_uri, status = unshortenit.unshorten('http://ul.to')

> All calls will return a tuple (unshortened_uri, status)

> unshortened_uri will contain the unshortened uri. If you pass in a non-shortener url it will return the original url.
> status will contain the status code or any error messages

Installation
------------

    pip install unshortenit

