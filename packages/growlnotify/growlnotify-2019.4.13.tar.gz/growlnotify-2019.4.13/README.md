<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/badge/OS-MacOS-blue.svg?longCache=True)]()
[![](https://img.shields.io/pypi/pyversions/growlnotify.svg?longCache=True)](https://pypi.org/project/growlnotify/)

#### Installation
```bash
$ [sudo] pip install growlnotify
```

#### Functions
function|`__doc__`
-|-
`growlnotify.args(**kwargs)` |return a list with `growlnotify` cli arguments
`growlnotify.notify(**kwargs)` |run growlnotify

#### Examples
```python
>>> import growlnotify
>>> growlnotify.notify(t="title",m="message")           # -t "title" -m "message"
>>> growlnotify.notify(title="title",message="message") # --title "title" --message "message"
```

`-s`, `--sticky`
```python
>>> growlnotify.notify(title="title",s=True)       # -s
>>> growlnotify.notify(title="title",sticky=True)  # --sticky
```

growlnotify keys
```bash
$ growlnotify --help
```

#### Links
+   [growl.info](http://growl.info/)

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>