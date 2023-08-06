# bunnieshared

This is a Python project that contains shared dependencies for Bunnie broker.

## Upload Python package to PyPI

To upload the Python package, you need to install `twine`:

```shell
$ pip install twine
```

Next, upload the Python package to PyPI:

```shell
# From: https://pypi.org/project/twine/
$ python setup.py sdist bdist_wheel
$ twine upload dist/*
```
