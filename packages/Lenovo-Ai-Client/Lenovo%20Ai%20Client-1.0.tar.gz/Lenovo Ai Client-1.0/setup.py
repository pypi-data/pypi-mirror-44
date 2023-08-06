# !/usr/bin/env python
from __future__ import print_function
from setuptools import setup

setup(
    name="Lenovo Ai Client",
    version="1.0",
    author="Chen jie",
    author_email="chenjie_222@163.com",
    description="AI Lenovo",
    long_description=open("README.rst").read(),
    license="Apache License",
    url="",
    packages=['aiClient'],
    install_requires=[
        'requests',
        'simplejson',
        'opencv-python',
    ],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Indexing",
        "Topic :: Utilities",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
