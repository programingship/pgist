#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: sw=4 ts=4 expandtab ai

import os
from setuptools import setup, find_packages

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup (
    name="pgist",
    version="0.1",
    packages=find_packages(),
    license="Apache License 2.0",
    description="A Python command-line wrapper with github3.py library to access GitHub Gist",
    long_description=README,
    author="Lingchao Xin",
    author_email="douglarek@outlook.com",
    keywords="python gist",
    scripts=['pgist'],
    install_requires=["github3.py >= 0.7.1"],
    platforms="Python 2.7",
    )

