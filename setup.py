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

with open("README.rst", "r", encoding="utf-8") as fh:
  long_description = fh.read()

setuptools.setup(
  name = "fandom-py",
  version = '.'.join(version),
  author = "Nikolaj Gade",
  author_email = "nikolajgade@live.dk",
  description = "Fandom API wrapper for Python",
  long_description = long_description,
  license = "MIT",
  keywords = "python wikia fandom API",
  url = "https://github.com/NikolajDanger/fandom-py",
  install_requires = install_reqs,
  packages = ['fandom'],
  classifiers = [
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
  ]
)
