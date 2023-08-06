<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/badge/OS-MacOS-blue.svg?longCache=True)]()
[![](https://img.shields.io/pypi/pyversions/ubersicht.svg?longCache=True)](https://pypi.org/project/ubersicht/)

#### Installation
```bash
$ [sudo] pip install ubersicht
```

#### Classes
class|`__doc__`
-|-
`ubersicht._coffee.Coffee` |index.coffee generator class
`ubersicht._widgets.Widget` |widget generator class

#### Functions
function|`__doc__`
-|-
`ubersicht.kill()` |kill Übersicht.app process
`ubersicht.pid()` |return Übersicht.app pid
`ubersicht.restart()` |restart Übersicht.app
`ubersicht.start()` |open Übersicht.app
`ubersicht.widgets()` |return a list with widgets paths

#### Examples
generate widget
```python
>>> import ubersicht
>>> widget = ubersicht.Widget(name="name.widget", command="echo hello world", refresh="1s",style="color: red")
>>> widget.create()
>>> widget.path
'/Users/username/Library/Application Support/Übersicht/widgets/name.widget'
```

```bash
$ cat ~/Library/Application Support/Übersicht/widgets/name.widget/index.coffee
command: "echo hello world"

refreshFrequency: '1s'

update: (output, domEl) ->
    $(domEl).empty().append("#{output}")

style: """
color: red
"""
```

#### Links
+   [Uebersicht.app](https://github.com/felixhageloh/uebersicht)

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>