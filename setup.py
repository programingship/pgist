#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: sw=4 ts=4 expandtab ai

import os
from setuptools import setup, find_packages

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup (
    name='pgist',
    version='0.3',
    packages=find_packages(),
    license=open('LICENSE').read(),
    description='A Python command-line wrapper with github3.py library to access GitHub Gist',
    long_description=README,
    author='Lingchao Xin',
    author_email='douglarek@outlook.com',
    url='https://github.com/douglarek/pgist',
    package_data={'': ['LICENSE',]},
    scripts=['pgist'],
    install_requires=['github3.py >= 0.7.1'],
    zip_safe=False,
    classifiers=(
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'Natural Language :: English',
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.2',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: Implementation :: CPython',
        ),
    )

