#!/usr/bin/env python

from distutils.core import setup

setup(
    name='GeoApp',
    version='1.0.0',
    packages=['geo_app'],
    install_requires=[
        'flask',
        'furl',
        'pep8',
        'pylint',
        'python-arango',
        'uwsgi',
    ],
)
