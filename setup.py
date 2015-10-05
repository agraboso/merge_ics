import re
from setuptools import setup

try:
  from pypandoc import convert
  read_md = lambda f: convert(f, 'rst')
except ImportError:
  print('Warning: pypandoc module not found, could not convert Markdown to RST')
  read_md = lambda f: open(f, 'r').read()

with open('./merge_ics/__init__.py') as f:
  version = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.M).group(1)

setup(
  name = 'merge_ics',
  version = version,
  author = 'Alberto Garcia-Raboso',
  author_email = 'agraboso@gmail.com',
  description = 'Merge RFC5545 calendar files',
  keywords = 'RFC5545 ics calendar',
  license = 'MIT',
  url = 'https://github.com/agraboso/merge_ics',
  platforms = ['any'],
  install_requires = [
    'PyYAML >3',
    'requests >=2.7.0',
    'icalendar >=3.9.0, <=4'
    ],
  packages = ['merge_ics'],
  entry_points = {
    'console_scripts': ['merge_ics = merge_ics.merge_ics:main']
    },
  include_package_data = True,
  long_description = read_md('README.md'),
  classifiers = [
    'Programming Language :: Python',
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Operating System :: OS Independent',
    'Natural Language :: English',
    'Topic :: Utilities',
    'License :: OSI Approved :: MIT License'
    ]
  )
