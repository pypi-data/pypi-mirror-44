<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/pypi/pyversions/rm.svg?longCache=True)](https://pypi.org/project/rm/)

#### Installation
```bash
$ [sudo] pip install rm
```

#### Features
- removes **dirs** and **files**
- **no exception** - skip if path not exists

#### Functions
function|`__doc__`
-|-
`rm.rm(path)` |remove path(s) (if exists)

#### Examples
```python
>>> import rm

>>> rm.rm("path/to/file")  # rm file
>>> rm.rm("path/to/dir")  # rm dir
>>> rm.rm(["path/to/dir","path/to/file"])  # rm multiple paths
>>> rm.rm("not-existing") # no exception
```

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>