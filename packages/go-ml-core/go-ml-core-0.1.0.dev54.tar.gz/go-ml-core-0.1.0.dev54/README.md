# go-ml-core

Some share utilities in Gogoro Machine Learning Team.

## Release instructions

- To install essential packages

```
pip3 install setuptools wheel twine
```

- To prepare a ~/.pypirc

```
[distutils]
index-servers = pypi

[pypi]
repository:https://upload.pypi.org/legacy/
username:<username>
password:<password>
```

- To revision new version in setup.py


- To compile and upload

```
python3 setup.py sdist bdist_wheel
twine upload --skip-existing dist/*
```
