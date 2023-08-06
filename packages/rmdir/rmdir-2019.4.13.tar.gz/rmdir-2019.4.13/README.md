<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/pypi/pyversions/rmdir.svg?longCache=True)](https://pypi.org/project/rmdir/)

#### Installation
```bash
$ [sudo] pip install rmdir
```

#### Functions
function|`__doc__`
-|-
`rmdir.rmdir(path)` |recursively delete empty directories

#### Examples
```bash
$ find . -depth -type d -exec rmdir {} \; 2>/dev/null
```

```python
>>> import rmdir
>>> rmdir.rmdir(".")
```

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>