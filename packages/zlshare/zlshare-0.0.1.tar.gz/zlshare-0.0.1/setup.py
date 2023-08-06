#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from os.path import dirname, join
from setuptools import (
    find_packages,
    setup,
)

from pip.req import parse_requirements


with open(join(dirname(__file__), 'zlshare/VERSION.txt'), 'rb') as f:
    version = f.read().decode('ascii').strip()

setup(
    name='zlshare',
    version=version,
    description='zlshare',
    packages=find_packages(exclude=[]),
    author='Nathan Lu',
    url='',
    author_email='luqy@zealink.com',
    license='Apache License v2',
    package_data={'': ['*.*']},
    install_requires=[str(ir.req) for ir in parse_requirements("requirements.txt", session=False)],
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)