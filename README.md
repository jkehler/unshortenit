unshortenit
===========

Unshortens ad-based urls and 301 redirects. Supports adf.ly, adfoc.us, and sh.st.

Features
--------

- Supports unshortening the following ad-based shortners:
	- Adf.ly and related subdomains
	- Custom adf.ly domains by passing the module='adfly' parameter
	- Sh.st
	- Adfoc.us
- Supports any 301 redirected urls
- Python 3 support only

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


Installation
------------

    pip install unshortenit

