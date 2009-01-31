from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='AuPoilCli',
      version=version,
      description="AuPoil client",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Gael Pasgrimaud',
      author_email='gael@gawel.org',
      url='',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      namespace_packages = ['aupoil', 'aupoil.cli'],
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
          'setuptools',
          'Paste',
          'WebOb',
          'simplejson',
      ],
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      aupoil = aupoil.cli.entries:main
      """,
      )
