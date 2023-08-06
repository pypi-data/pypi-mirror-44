# -*- coding: utf-8 -*-

from pyrepetier import __version__
import setuptools

setuptools.setup(
    name = 'pyrepetier',
    version = __version__,
    description = 'Repetier Server API library',
    author = 'Morten Trab',
    license= 'MIT',
    url = 'https://github.com/mtrab/pyrepetier',
    packages=setuptools.find_packages(),
)
