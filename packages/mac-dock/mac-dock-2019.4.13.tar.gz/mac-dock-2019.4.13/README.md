<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/badge/OS-MacOS-blue.svg?longCache=True)]()
[![](https://img.shields.io/pypi/pyversions/mac-dock.svg?longCache=True)](https://pypi.org/project/mac-dock/)

#### Installation
```bash
$ [sudo] pip install mac-dock
```

###### folder options

+   `arrangement`: 1 - name (default), 2 - added, 3 - modification, 4 - creation, 5 - kind
+   `displayas`: 1 - folder, 2 - stack (default)
+   `showas`: 1 - beep, 2 - grid, 3 - list, 4 - auto (default)

#### Functions
function|`__doc__`
-|-
`mac_dock.save()` |save Dock preferences

#### Executable modules
usage|`__doc__`
-|-
`python -m mac_dock.apps.add path ...` |add app to Dock
`python -m mac_dock.apps.bundle` |print Dock apps bundles
`python -m mac_dock.apps.label` |print Dock apps labels
`python -m mac_dock.apps.path` |print Dock apps paths
`python -m mac_dock.apps.rm path ...` |remove app from Dock
`python -m mac_dock.files.add path ...` |add file to Dock
`python -m mac_dock.files.label` |print Dock files labels
`python -m mac_dock.files.path` |print Dock files paths
`python -m mac_dock.files.rm path ...` |remove file from Dock
`python -m mac_dock.folders.add path [options]` |add folder to Dock
`python -m mac_dock.folders.label` |print Dock folders labels
`python -m mac_dock.folders.path` |print Dock folders paths
`python -m mac_dock.folders.rm path ...` |remove folder from Dock

### Examples

##### Preferences
```python
>>> mac_dock.autohide=False
>>> mac_dock.tilesize=85
>>> mac_dock.save()
```

##### CLI
```bash
$ python -m mac_dock.apps.add "/Applications/Safari.app" "/Applications/Siri.app"
$ python -m mac_dock.apps.rm "/Applications/Siri.app" "/Applications/Siri.app"
```
```bash
$ python -m mac_dock.files.rm # rm all files from Dock
$ python -m mac_dock.files.add "path/to/run.command" "path/to/site.webloc"
$ python -m mac_dock.files.rm "path/to/run.command" "path/to/site.webloc"
```
```bash
$ python -m mac_dock.folders.add # rm all folders from Dock
$ python -m mac_dock.folders.add --arrangement=4 --displayas=1 --showas=1 ~/Downloads
$ python -m mac_dock.folders.add --arrangement=1 --displayas=2 --showas=2 ~/Desktop
$ python -m mac_dock.folders.rm ~/Desktop ~/Downloads
```

##### Functions
```python
>>> mac_dock.apps.add(["/Applications/Dashboard.app","/Applications/Safari.app"])
>>> mac_dock.apps.rm(["/Applications/Dashboard.app","/Applications/Safari.app"])
```
```python
>>> mac_dock.files.rm()  # rm all files from Dock
>>> mac_dock.files.add(["path/to/site.webloc"])
>>> mac_dock.files.rm(["path/to/site.webloc"])
```
```python
>>> mac_dock.folders.rm()  # rm all folders from Dock
>>> mac_dock.folders.add("~/Downloads",arrangement=4, displayas=1, showas=1)
>>> mac_dock.folders.rm(["~/Downloads"])
```

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>