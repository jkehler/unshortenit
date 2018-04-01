Extending UnshortenIt
=====================

This library supports extensions by creating your own unshorter modules and registering them. This is useful for any custom sites you may need to handle.

To create your own module you have to subclass :class:`unshortenit.module.UnshortenModule` and implement the ``unshorten()`` method::
    >>> from unshortenit.module import UnshortenModule
    >>> class CustomModule(UnshortenModule):
    ...     name = 'my-custom-module'
    ...     domains = [
    ...         'example.com'
    ...     ]
    ...
    ...     def __init__(self, headers=None, timeout=30):
    ...         super().__init__(headers, timeout)
    ...
    ...     def unshorten(self, uri):
    ...         """ Implement custom unshorten logic here and return result """
    ...         return uri
    ... 
    >>> from unshortenit import UnshortenIt()
    >>> unshortener = UnshortenIt()
    >>> unshortener.register_module(CustomModule)

Adding Additional Domains to Existing modules
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You may extend one of the existing modules by adding additional domains to the domain list::

    >>> from unshortenit import UnshortenIt
    >>> unshortener = UnshortenIt()
    >>> unshortener.modules['meta-refresh'].add_domain('example.com')

Now whenever you pass a url from the example.com domain it will be parsed by the meta refresh module.
