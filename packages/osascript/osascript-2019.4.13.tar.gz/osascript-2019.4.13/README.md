<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/badge/OS-MacOS-blue.svg?longCache=True)]()
[![](https://img.shields.io/pypi/pyversions/osascript.svg?longCache=True)](https://pypi.org/project/osascript/)

#### Installation
```bash
$ [sudo] pip install osascript
```

#### Functions
function|`__doc__`
-|-
`osascript.osascript(applescript, background=False)` |run applescript file/code. deprecated
`osascript.run(applescript, background=False)` |run applescript file/code

#### Examples
```python
>>> import osascript

>>> code,out,err = osascript.run('display dialog "42"')
```

#### Links
+   [osascript(1) Man Page](https://ss64.com/osx/osascript.html)

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>