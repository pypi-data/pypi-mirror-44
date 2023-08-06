from __future__ import print_function
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import io
import codecs
import os
import sys

import fpu

here = os.path.abspath(os.path.dirname(__file__))



setup(name='fpu',
      version=fpu.__version__,
      description='Functional Programming Utility',
      url='https://github.com/johnklee/fpu',
      author='johnklee',
      author_email='puremonkey2007@gmail.com',
      license='MIT',
      packages=['fpu'],
      zip_safe=False)
