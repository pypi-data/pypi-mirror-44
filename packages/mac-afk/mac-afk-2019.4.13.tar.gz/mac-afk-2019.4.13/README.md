<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/badge/OS-MacOS-blue.svg?longCache=True)]()
[![](https://img.shields.io/pypi/pyversions/mac-afk.svg?longCache=True)](https://pypi.org/project/mac-afk/)

#### Installation
```bash
$ [sudo] pip install mac-afk
```

#### Executable modules
usage|`__doc__`
-|-
`python -m mac_afk.days` |macOS afk time in days
`python -m mac_afk.hours` |macOS afk time in hours
`python -m mac_afk.minutes` |macOS afk time in minutes
`python -m mac_afk.seconds` |macOS afk time in seconds

#### Scripts usage
```bash
usage: afk
```

#### Examples
```python
>>> import mac_afk
>>> import time
>>> time.sleep(2); mac_afk.seconds()
2
```

```bash
$ sleep 3 && afk
3
```

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>