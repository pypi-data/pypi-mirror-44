from setuptools import setup, find_packages

with open('requirements.txt') as f:
  required = f.read().splitlines()

setup(name="bunnieinfra", version="0.1.1", packages=find_packages(), install_requires=required)
