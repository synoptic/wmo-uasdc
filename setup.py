#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='wmo-uasdc',
      version='1.0.0',
      description='Utilities for WMO UASDC project',
      author='James Simkins',
      author_email='james.simkins@synopticdata.com',
      url='https://github.com/synoptic/wmo-uasdc',
      packages=['uas-utils'],
      package_dir={'wmo-uasdc': 'uas-utils'},
      )
