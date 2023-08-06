<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/pypi/pyversions/replace.svg?longCache=True)](https://pypi.org/project/replace/)

#### Installation
```bash
$ [sudo] pip install replace
```

#### Functions
function|`__doc__`
-|-
`replace.replace(source, replacement)` |replace multiple elements/substrings and return result

#### Examples
```python
import replace
>>> replace.replace(["3.6","3.7","3.8"], {"3.7": "3.7-dev", "3.8": "3.8-dev"})
["3.6","3.7-dev","3.8-dev""3.8"]
```

```python
>>> replace.replace("package/module.py", {"/": ".", ".py": ""})
"package.module"
```

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>