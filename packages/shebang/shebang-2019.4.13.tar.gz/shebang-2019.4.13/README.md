<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/pypi/pyversions/shebang.svg?longCache=True)](https://pypi.org/project/shebang/)

#### Installation
```bash
$ [sudo] pip install shebang
```

#### Functions
function|`__doc__`
-|-
`shebang.get(path)` |return script shebang
`shebang.shebang(path)` |return script shebang. deprecated

#### Executable modules
usage|`__doc__`
-|-
`python -m shebang path` |print script shebang

#### Examples
```python
>>> import shebang

>>> shebang.get("path/to/file.py")
'/usr/bin/env python'

>>> shebang.get("path/to/file.txt")
None

>>> shebang.get("/bin/ls")
None
```

```bash
$ python -m shebang file.py
/usr/bin/env python
```

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>