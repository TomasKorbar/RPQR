'''
Project: RPQR
Author: Tomáš Korbař (tomas.korb@seznam.cz)
Copyright 2021 - 2021 Tomáš Korbař
'''

from setuptools import find_packages, setup

setup(name='rpqr',
      version='1.0.0',
      description='RPM package query resolver',
      author='Tomas Korbar',
      author_email='tkorbar@redhat.com',
      packages=find_packages(),
      scripts=["bin/RPQROrphaned", "bin/RPQR"]
     )
