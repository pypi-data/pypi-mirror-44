#!/usr/bin/env python
# coding=utf-8

import os
import io

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as fp:
    README = fp.read()

# this module can be zip-safe if the zipimporter implements iter_modules or if
# pkgutil.iter_importer_modules has registered a dispatch for the zipimporter.
try:
    import pkgutil
    import zipimport
    zip_safe = hasattr(zipimport.zipimporter, "iter_modules") or \
        zipimport.zipimporter in pkgutil.iter_importer_modules.registry.keys()
except (ImportError, AttributeError):
    zip_safe = False

setup(
    name='data-anonymizer-mapper',
    version='0.1.0',
    description="Anonymizer is a Python package that generates fake data for you, especially useful with pandas dataframes.",
    long_description=README,
    classifiers=[
        # See https://pypi.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
    ],
    keywords='faker anonymizer data test mock generator pandas dataframe anonymize',
    author='samiriff',
    author_email='samiriff@gmail.com',
    url='https://github.com/samiriff/anonymizer',
    download_url='https://github.com/samiriff/anonymizer/archive/0.1.0.tar.gz',
    license='MIT License',
    packages=find_packages(exclude=["docs", "tests", "tests.*"]),
    platforms=["any"],
    zip_safe=zip_safe,
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    install_requires=[
        "faker",
    ],
)
