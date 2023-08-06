<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/badge/OS-MacOS-blue.svg?longCache=True)]()
[![](https://img.shields.io/pypi/pyversions/mac-finder.svg?longCache=True)](https://pypi.org/project/mac-finder/)

#### Installation
```bash
$ [sudo] pip install mac-finder
```

#### Functions
function|`__doc__`
-|-
`mac_finder.frontmost()` |return True if Finder is frontmost app, else False
`mac_finder.reveal(path)` |reveal path in Finder
`mac_finder.tell(code)` |execute applescript `tell application "Finder" ...`
`mac_finder.comment.get(path)` |return string with Finder comment
`mac_finder.comment.update(path, comment=None)` |update Finder comment

#### Executable modules
usage|`__doc__`
-|-
`python -m mac_finder.comment path [comment]` |get/update Finder comment
`python -m mac_finder.icon.rm path ...` |remove icon
`python -m mac_finder.icon.update path image` |update icon
`python -m mac_finder.selection` |print Finder selection paths

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>