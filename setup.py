#!/usr/bin/env python
# -*- coding: utf-8; mode: python -*-

from setuptools import setup, find_packages
import dbxml2rst
install_requires = [
    'fspath' ]

setup(
    name               = "dbxml2rst"
    , version          = dbxml2rst.__version__
    , description      = dbxml2rst.__description__
    , long_description = dbxml2rst.__doc__
    , url              = dbxml2rst.__url__
    , author           = "Markus Heiser"
    , author_email     = "markus.heiser@darmarIT.de"
    , license          = dbxml2rst.__license__
    , keywords         = "DocBook XML reStructuredText reST"
    , packages         = find_packages(exclude=['docs', 'tests'])
    , install_requires = install_requires
    , scripts          = ["linux-db2rst"]

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    , classifiers = [
        "Development Status :: 5 - Production/Stable"
        , "Intended Audience :: Developers"
        , "Intended Audience :: Other Audience"
        , "License :: OSI Approved :: GNU General Public License v2 (GPLv2)"
        , "Operating System :: OS Independent"
        , "Programming Language :: Python :: 3"
        , "Topic :: Utilities"
        , "Topic :: Documentation :: DocBook-XML"
        , "Topic :: Documentation :: reStructuredText"
        , "Topic :: Software Development :: Documentation"
        , "Topic :: Software Development :: Libraries"
        , "Topic :: Text Processing" ]
)
