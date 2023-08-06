# -*- coding: utf-8 -*-
"""
    i18n support for aiohttp through babel
"""
from setuptools import setup
from setuptools import find_packages

setup(
    name = "aiohttp-i18n",
    version = "0.0.4",
    packages = find_packages(),
    python_requires='~=3.5',

    install_requires = [
        "aiohttp",
        "babel",
        "aiotask_context",
    ],

    author = "mazvv",
    author_email = "vitalii.mazur@gmail.com",
    description = "i18n support for aiohttp through babel",
    license = "BSD",
    keywords = "aiohttp i18n locale babel localization",
    url="https://bitbucket.org/mazvv/aiohttp_i18n",
)
