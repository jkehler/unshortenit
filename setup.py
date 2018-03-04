from setuptools import setup, find_packages
import os


here = os.path.abspath(os.path.dirname(__file__))

readme = open('README.md').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

about = {}
with open(os.path.join(here, 'unshortenit', '__version__.py'), 'r') as f:
    exec(f.read(), about)

setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    long_description=readme + '\n\n' + history,
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    packages=find_packages(),
    package_data={'': ['LICENSE']},
    include_package_data=True,
    zip_safe=True,
    setup_requires=['pytest-runner<=3.0.1'],
    tests_require=['pytest'],
    install_requires=[
        'requests>=2.18.4',
        'click>=6.7',
        'lxml>=4.1.1'
    ],
    license=about['__license__'],
    keywords='unshortener adf.ly lnx.lu sh.st shortener',
    entry_points='''
    [console_scripts]
    unshortenit=unshortenit.cli:cli
    ''',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ]
)
