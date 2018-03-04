from setuptools import setup, find_packages


readme = open('README.md').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')


setup(
    name='unshortenit',
    version='0.4.0',
    description='Unshortens adf.ly, sh.st, and any 301 redirected shortener urls',
    long_description=readme + '\n\n' + history,
    author='Jeff Kehler',
    author_email='jeffrey.kehler@gmail.com',
    url='https://github.com/jkehler/unshortenit',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests',
        'click'
    ],
    license="MIT",
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
        'Programming Language :: Python',
    ],
    test_suite='tests',
)
