#!/usr/bin/env python3

# https://docs.python.org/3.6/distributing/index.html
# https://setuptools.readthedocs.io/en/latest/setuptools.html#developer-s-guide

import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='dtnsim',
    version='1.3',
    author='Hiroyuki Ohsaki',
    author_email='ohsaki@lsnl.jp',
    description='DTN (Delay/Disruption Tolerant Networking) simulator with several agent/mobility models',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/h-ohsaki/dtnsim",
    packages=setuptools.find_packages(),
    install_requires=['Pytess', 'perlcompat', 'cellx', 'graph_tools'],
    scripts=['bin/dtnsim'],
    classifiers=[
        'Programming Language :: Python :: 3',
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        'Operating System :: OS Independent',
    ],
)
