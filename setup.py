from setuptools import setup
from glob import glob

setup(
  name='bibtools',
  version='0.0.1',
  scripts=glob('src/*.py'),
)