===============================
unshortenit
===============================

Unshortens ad-based urls and 301 redirects. Supports adf.ly, lnx.lu, linkbucks.com, and adfoc.us


Features
--------

- Supports unshortening the following ad-based shortners:
    - Adf.ly and related subdomains (PyV8 library required)
    - Lnx.lu
    - Linkbucks.com and related subdomains
    - Adfoc.us
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
    pip install requests

In order to enable adf.ly support you will need to install the PyV8 library. This will need to be compiled from source.

* Python 2.7 PyV8 Instructions:
    - sudo apt-get install gyp subversion build-essential libboost-python-dev python2.7-dev libboost-system-dev libboost-thread-dev
    - svn checkout http://v8.googlecode.com/svn/trunk/ v8
    - svn checkout http://pyv8.googlecode.com/svn/trunk/ pyv8-read-only
    - cd v8
    - make dependencies
    - cd ..
    - cd pyv8-read-only
    - V8_HOME=/path/to/v8 python2.7 setup.py build *** This will not work inside a virtualenv. Make sure to deactivate your virtualenv first.
    - python2.7 setup.py install *** You can run this inside your virtualenv to install it.

* Python 3.3 PyV8 Instructions:
    - sudo apt-get install gyp subversion build-essential libboost-python-dev python3.3-dev libboost-system-dev libboost-thread-dev
    - svn checkout http://v8.googlecode.com/svn/trunk/ v8
    - svn checkout http://pyv8.googlecode.com/svn/trunk/ pyv8-read-only
    - cd v8
    - make dependencies
    - cd ..
    - cd pyv8-read-only
    - sed -i.bak s/\'boost\_python\'/\'boost_python-py33\'/ setup.py
    - V8_HOME=/path/to/v8 python3.3 setup.py build *** This will not work inside a virtualenv. Make sure to deactivate your virtualenv first.
    - python3.3 setup.py install *** You can run this inside your virtualenv to install it.
