<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/pypi/pyversions/slicedict.svg?longCache=True)](https://pypi.org/project/slicedict/)

#### Installation
```bash
$ [sudo] pip install slicedict
```

#### Functions
function|`__doc__`
-|-
`slicedict.slice(d, keys)` |return dictionary with given keys

#### Examples
```python
>>> import slicedict

>>> medatata = dict(name="pkgname", version="1.0.0", somekey="value")
>>> slicedict.slice(medatata, ["name", "version"])
{'version': '1.0.0', 'name': 'pkgname'}
```

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>