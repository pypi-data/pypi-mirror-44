#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

import importlib

dependencies = [ 'QtPy>=1.7.0' ]

for binding in ['PySide2', 'PyQt5', 'PySide', 'PyQt']:
	spec = importlib.util.find_spec(binding)
	if spec is not None:
		break
else:
	dependencies.append('PySide2>=5.12.2')

setup(
	name='argparseqt',
	version='0.1',
	description='The easiest way to make Qt GUIs using the argparse standard module',
	author='Dominic Canare',
	author_email='dom@dominiccanare.com',
	packages=['argparseqt'],
	install_requires=dependencies,
)
