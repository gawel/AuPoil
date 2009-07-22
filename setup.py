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
      namespace_packages = ['aupoil'],
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'setuptools',
          'Paste',
          'PasteDeploy',
          'PasteScript',
          'WebOb',
          'Mako',
          'SQLAlchemy>=0.5.0',
          'pysqlite',
          'simplejson',
      ],
      entry_points="""
      # -*- Entry points: -*-
      [paste.app_factory]
      main = aupoil.entries:make_app
      [paste.app_install]
      main = aupoil.entries:AuPoilInstaller
      [console_scripts]
      aupoil_admin = aupoil.entries:main
      """,
      )
