Quickstart
==========

Installation
^^^^^^^^^^^^

This package is available via the PIP repository. To install this package simply run this commmand::

    $ pip install unshortenit

Usage
^^^^^

Using this library is very simple::

    >>> from unshortenit import UnshortenIt
    >>> unshortener = UnshortenIt()
    >>> uri = unshortener.unshorten('https://href.li/?https://example.com')
    >>> print(uri)
    https://example.com

Advanced Usage
^^^^^^^^^^^^^^

You can override the default timeout value and default headers globally for all modules via the UnshortenIt initializer::

    >>> from unshortenit import UnshortenIt
    >>> unshortener = UnshortenIt(default_timeout=30, default_headers=dict())

By default the library will not make any HTTP request if the url provided does not match any of the modules url patterns.
To override this you may pass ``force=True`` to the ``unshorten`` method.

If you wish to force a specific module to be used for a link you may do so by using the ``module='module_name'`` parameter on the ``unshorten`` method.
This is useful for ad-based shorteners that allow people to use custom domains or if you know a link is a meta refresh type.

In some cases you may come across shorteners that are nested one after another. By default the library will not check if the returned link is also another shortener link.
If you wish to force it to always check the returned link as well you may pass ``unshorten_nested=True`` to the ``unshorten`` method.

Exceptions
^^^^^^^^^^

Exceptions will not be handled by the module and will be passed up to the caller. You will need to wrap the unshorten call in your own try, except blocks.

This module includes 2 custom Exceptions ``unshortenit.exceptions.NotFound`` and ``unshortenit.exceptions.UnshortenFailed``.
The first will be triggered if the url returns a 404 status code. The later will occur if some sort of issue happened during the unshortening process.
All other exceptions will be the default python requests library exceptions.