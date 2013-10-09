#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='unshortenit',
    version='0.1.0',
    description='Unshortens adf.ly,adfoc.us,lnx.lu,linkbucks, and any 301 redirected shortener urls',
    long_description=readme + '\n\n' + history,
    author='Jeff Kehler',
    author_email='jeffrey.kehler@gmail.com',
    url='https://github.com/none/unshortenit',
    packages=[
        'unshortenit',
    ],
    package_dir={'unshortenit': 'unshortenit'},
    include_package_data=True,
    install_requires=[
    ],
    license="BSD",
    zip_safe=False,
    keywords='unshortenit',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.3',
    ],
    test_suite='tests',
)
