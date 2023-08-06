from __future__ import print_function
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import io
import codecs
import os
import sys

import fpu

here = os.path.abspath(os.path.dirname(__file__))

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())

    return sep.join(buf)

long_description = read('README.md')

setup(name='fpu',
      version=fpu.__version__,
      description='Functional Programming Utility',
      url='https://github.com/johnklee/fpu',
      author='johnklee',
      author_email='puremonkey2007@gmail.com',
      tests_require=['pytest'],
      long_description=long_description,
      license='MIT',
      packages=['fpu'],
      zip_safe=False)
