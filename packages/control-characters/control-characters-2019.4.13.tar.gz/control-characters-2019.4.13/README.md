<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/pypi/pyversions/control-characters.svg?longCache=True)](https://pypi.org/project/control-characters/)

#### Installation
```bash
$ [sudo] pip install control-characters
```

#### Features
fixes `plistlib`  problem with control characters
```python
>>> plistlib.dump(data, open(path, 'wb'))
...
ValueError: strings can't contains control characters; use bytes instead
```

#### Functions
function|`__doc__`
-|-
`control_characters.remove(string)` |return a string without control characters

#### Examples
environment variables without control characters:
```python
env = dict((k, control_characters.remove(v)) for k, v in os.environ.items())
```

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>