<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/pypi/pyversions/kill.svg?longCache=True)](https://pypi.org/project/kill/)

#### Installation
```bash
$ [sudo] pip install kill
```

#### Functions
function|`__doc__`
-|-
`kill.kill(pid)` |kill process by pid and return stderr

#### Examples
```python
>>> kill.kill(61024)
>>> kill.kill([61076])
```

errors
```python
>>> kill.kill(9999999)
kill: 999999: No such process

>>> kill.kill(1)
kill: (1) - Operation not permitted
```

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>