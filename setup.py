#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import unshortenit

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.md').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='unshortenit',
    version=unshortenit.__version__,
    description='Unshortens adf.ly, sh.st, and any 301 redirected shortener urls',
    long_description=readme + '\n\n' + history,
    author='Jeff Kehler',
    author_email='jeffrey.kehler@gmail.com',
    url='https://github.com/DevKeh/unshortenit',
    packages=[
        'unshortenit',
    ],
    package_dir={'unshortenit': 'unshortenit'},
    include_package_data=True,
    install_requires=['requests'
    ],
    license="MIT",
    zip_safe=False,
    keywords='unshortener adf.ly lnx.lu sh.st shortener',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
    ],
    test_suite='tests',
)
