<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/badge/OS-MacOS-blue.svg?longCache=True)]()
[![](https://img.shields.io/pypi/pyversions/mac-logs.svg?longCache=True)](https://pypi.org/project/mac-logs/)

#### Installation
```bash
$ [sudo] pip install mac-logs
```

#### Features
`~/Library/Logs` MacOS `.log` files

#### Functions
function|`__doc__`
-|-
`mac_logs.errors()` |return a list of `*err*.log` files (`stderr.log`, `err.log`, `error.log`, ...)
`mac_logs.logs(filenames=None, minsize=0)` |return a list of `.log` files
`mac_logs.rm(filenames=None, minsize=0)` |remove `.log` files

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>