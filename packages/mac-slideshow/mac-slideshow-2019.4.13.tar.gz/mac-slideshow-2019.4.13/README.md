<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/badge/OS-MacOS-blue.svg?longCache=True)]()
[![](https://img.shields.io/pypi/pyversions/mac-slideshow.svg?longCache=True)](https://pypi.org/project/mac-slideshow/)

#### Installation
```bash
$ [sudo] pip install mac-slideshow
```

#### Classes
class|`__doc__`
-|-
`mac_slideshow.Process` |ScreenSaver process object

#### Functions
function|`__doc__`
-|-
`mac_slideshow.enable()` |enable iLifeSlideshow screensaver
`mac_slideshow.enabled()` |return True if iLifeSlideshow screensaver enabled
`mac_slideshow.restart(path=None)` |restart screensaver and return Process object
`mac_slideshow.path.read()` |return iLifeSlideShows images folder path
`mac_slideshow.path.write(path)` |write iLifeSlideShows images folder path
`mac_slideshow.preferences.read(key)` |return preferences value
`mac_slideshow.preferences.write(key, value)` |write preferences value
`mac_slideshow.style.read()` |return iLifeSlideShows style
`mac_slideshow.style.write(style)` |write iLifeSlideShows style

#### Executable modules
usage|`__doc__`
-|-
`python -m mac_slideshow.path [path]` |read/write iLifeSlideShows screensaver path
`python -m mac_slideshow.start [path]` |start iLifeSlideshows screensaver
`python -m mac_slideshow.style [style]` |read/write iLifeSlideShows screensaver style

#### Examples
```python
>>> import mac_slideshow
>>> ss = mac_slideshow.start()
>>> ss.pid # or mac_slideshow.pid()
1234
>>> ss.stop()  # or mac_slideshow.stop()
```

set images path and start/restart
```python
>>> ss = mac_slideshow.start("~/Library/Screen Savers/folder")
```

preferences
```python
>>> mac_slideshow.path.write("path/to/images")
>>> mac_slideshow.path.read()
'path/to/images'

>>> mac_slideshow.style.write("Classic")
>>> mac_slideshow.style.read()
'Classic'
```

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>