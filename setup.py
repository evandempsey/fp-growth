#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='pyfpgrowth',
    version='1.0',
    description="A Python implementation of the Frequent Pattern Growth algorithm.",
    long_description=readme + '\n\n' + history,
    author="Evan Dempsey",
    author_email='me@evandempsey.io',
    url='https://github.com/evandempsey/fp-growth',
    packages=[
        'pyfpgrowth',
    ],
    package_dir={'pyfpgrowth':
                 'pyfpgrowth'},
    include_package_data=True,
    install_requires=requirements,
    python_requires='>=3.8',
    license="ISCL",
    zip_safe=False,
    keywords='pyfpgrowth',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
