#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from distutils.core import setup
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="SpoKlient",
    version="1.0.0",
    author="Francisco Dias",
    author_email="vvgrem@gmail.com",
    maintainer="Konrad Gądek",
    maintainer_email="kgadek@gmail.com",
    description="Office 365 Library for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vgrem/Office365-REST-Python-Client",
    install_requires=['requests', 'adal'],
    extras_require={
        'NTLMAuthentication': ["requests_ntlm"]
    },
    tests_require=['nose'],
    test_suite='nose.collector',
    license="MIT",
    keywords="git",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries"
    ],
    packages=setuptools.find_packages(),
    package_data={
        'spoklient': ["runtime/auth/SAML.xml"]
    }
)

