import os, sys

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = []

if sys.version_info < (2, 7):
    requires = ['argparse']

setup(name='pyramid_command',
      version='0.1',
      description='Console commands manager for Pyramid framework',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Development Status :: 4 - Beta",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web pyramid console',
      packages=['pyramid_command'],
      install_requires=requires,
      include_package_data=True,
      zip_safe=False,
      entry_points = """\
      [paste.app_factory]
      main = intranet:main
      [console_scripts]
      pcommand = pyramid_command:main
      """,
      )
