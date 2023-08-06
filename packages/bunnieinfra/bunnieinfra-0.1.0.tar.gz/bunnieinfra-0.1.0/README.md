# bunnieinfra

This is a Python library that provides utilities to work with Bunnie infrastructure.

## Upload Python package to PyPI

To upload the Python package, you need to install `twine`:

```shell
$ pip install twine
```

Next, upload the Python package to PyPI:

```shell
# From: https://pypi.org/project/twine/
$ cd python/bunnieinfra
$ python setup.py sdist bdist_wheel
$ twine upload dist/*
```
