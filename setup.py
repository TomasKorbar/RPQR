'''
Project: RPQR
Author: Tomáš Korbař (tomas.korb@seznam.cz)
Copyright 2021 - 2021 Tomáš Korbař
'''

from distutils.core import setup

setup(name='rpqr',
      version='1.0',
      description='RPM package query resolver',
      author='Tomas Korbar',
      author_email='tkorbar@redhat.com',
      packages=['rpqr'],
      install_requires=['networkx'],
      scripts=["bin/RPQROrphaned"]
     )
