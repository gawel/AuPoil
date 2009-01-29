from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='AuPoil',
      version=version,
      description="A tinyurl like with REST interface",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='wsgi',
      author='Gael Pasgrimaud',
      author_email='gael@gawel.org',
      url='',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'PasteDeploy',
      ],
      entry_points="""
      # -*- Entry points: -*-
      [paste.app_factory]
      main = aupoil:make_app
      """,
      )
