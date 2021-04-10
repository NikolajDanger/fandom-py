# -*- coding: utf-8 -*-
import codecs
import os
import re
import setuptools


def local_file(file):
  return codecs.open(
    os.path.join(os.path.dirname(__file__), file), 'r', 'utf-8'
  )

install_reqs = [
  line.strip()
  for line in local_file('requirements.txt').readlines()
  if line.strip() != ''
]

version = re.search(r"__version__ = \((\d+), (\d+), (\d+)\)",str(local_file('fandom/__init__.py').read())).groups()


setuptools.setup(
  name = "fandom-py",
  version = '.'.join(version),
  author = "Nikolaj Gade",
  description = "fandom API for Python",
  license = "MIT",
  keywords = "python wikipedia API",
  url = "https://github.com/NikolajDanger/fandom-py",
  install_requires = install_reqs,
  packages = ['fandom'],
  long_description = local_file('README.rst').read(),
  classifiers = [
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
  ]
)
