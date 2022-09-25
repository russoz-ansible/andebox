#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

requirements = [line.strip() for line in open('requirements.txt').readlines()]

setup(name='andebox',
      version='0.24',
      scripts=['andebox'],
      packages=find_packages(),
      install_requires=requirements,
      )
