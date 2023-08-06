<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/badge/OS-MacOS-blue.svg?longCache=True)]()
[![](https://img.shields.io/pypi/pyversions/mac-screensaver.svg?longCache=True)](https://pypi.org/project/mac-screensaver/)

#### Installation
```bash
$ [sudo] pip install mac-screensaver
```

#### Functions
function|`__doc__`
-|-
`mac_screensaver.names()` |return a list of screensavers names
`mac_screensaver.preferences.clock()` |return True if "Show with clock" enabled, else False
`mac_screensaver.preferences.idle()` |return screensaver idle time in seconds. 0 if disabled

#### Examples
```python
>>> mac_screensaver.start()
>>> mac_screensaver.pid()
1488
>>> mac_screensaver.stop()
```

```python
>>> mac_screensaver.names()
['Random', 'Flurry', 'Arabesque', 'Word of the Day', 'iTunes Artwork', 'Computer Name', 'Shell', 'FloatingMessage', 'iLifeSlideshows']
>>> mac_screensaver.name()  # current name
'iLifeSlideshows'
```

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>