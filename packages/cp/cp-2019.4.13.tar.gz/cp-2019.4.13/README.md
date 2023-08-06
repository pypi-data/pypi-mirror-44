<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/pypi/pyversions/cp.svg?longCache=True)](https://pypi.org/project/cp/)

#### Installation
```bash
$ [sudo] pip install cp
```

#### Functions
function|`__doc__`
-|-
`cp.cp(source, target, force=True)` |Copy the directory/file src to the directory/file target

#### Examples
```python
>>> import cp

>>> cp.cp(src,dst)
>>> cp.cp(src,dst) # skip, exists
>>> cp.cp(src,dst,force=True) # force cp
```

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>