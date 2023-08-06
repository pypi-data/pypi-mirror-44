<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/badge/OS-MacOS-blue.svg?longCache=True)]()
[![](https://img.shields.io/pypi/pyversions/mac-volume.svg?longCache=True)](https://pypi.org/project/mac-volume/)

#### Installation
```bash
$ [sudo] pip install mac-volume
```

#### Functions
function|`__doc__`
-|-
`mac_volume.change(volume)` |change volume
`mac_volume.get()` |return volume

#### Executable modules
usage|`__doc__`
-|-
`python -m mac_volume [volume]` |set/get volume

#### Examples
```python
>>> import mac_volume
>>> mac_volume.change(10)
>>> mac_volume.get()
10
>>> mac_volume.mute()
>>> mac_volume.muted()
True
>>> mac_volume.unmute()
```

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>