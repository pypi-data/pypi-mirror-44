<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/badge/OS-MacOS-blue.svg?longCache=True)]()
[![](https://img.shields.io/pypi/pyversions/webloc.svg?longCache=True)](https://pypi.org/project/webloc/)

#### Installation
```bash
$ [sudo] pip install webloc
```

#### Functions
function|`__doc__`
-|-
`webloc.read(path)` |return webloc url
`webloc.write(path, url)` |write url to webloc file

#### Executable modules
usage|`__doc__`
-|-
`python -m webloc [url]` |read/write webloc url

#### Examples
```python
>>> import webloc
>>> webloc.write("path.webloc","https://www.google.com/")
>>> webloc.read("path.webloc")
'https://www.google.com/'
```

```bash
$ python -m webloc "path.webloc" "https://www.github.com/"
$ python -m webloc "path.webloc"
https://www.github.com/
```

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>