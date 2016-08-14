from __future__ import print_function
from setuptools import setup


def read_md(filename):
    try:
        from pypandoc import convert
        return convert(filename, 'rst')
    except ImportError:
        print('Warning: pypandoc module not found; could '
              'not convert Markdown to RST')
        with open(filename, 'r') as f:
            return f.read()


def read_version():
    import re

    with open('./merge_ics/__init__.py') as f:
        regex = r'^__version__ = [\'"]([^\'"]*)[\'"]'
        return re.search(regex, f.read(), re.M).group(1)


setup(name='merge_ics',
      version=read_version(),
      author='Alberto Garcia-Raboso',
      author_email='agraboso@gmail.com',
      description='Merge RFC5545 calendar files',
      keywords='RFC5545 ics calendar',
      license='MIT',
      url='https://github.com/agraboso/merge_ics',
      platforms=['any'],
      install_requires=['PyYAML >3',
                        'requests >=2.7.0',
                        'icalendar >=3.9.0, <=4'],
      packages=['merge_ics'],
      entry_points={'console_scripts':
                    ['merge_ics=merge_ics.merge_ics:main']},
      include_package_data=True,
      long_description=read_md('README.md'),
      classifiers=['Programming Language :: Python',
                   'Development Status :: 4 - Beta',
                   'Environment :: Console',
                   'Operating System :: OS Independent',
                   'Natural Language :: English',
                   'Topic :: Utilities',
                   'License :: OSI Approved :: MIT License'])
