<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/badge/OS-macOS-blue.svg?longCache=True)]()

#### Installation
```bash
$ [sudo] pip install mac-app-factory
```

#### Benefits
+   create multiple macOS apps with one command

#### Features
+   super fast (pure shell)
+   safe (native apps ignored)

#### How it works
```
<name>.app
├── Contents
│   ├── MacOS
│   │   └── executable
│   ├── Resources
│   │   └── Icon.icns
│   └── Info.plist
│   executable          # edit this file. shebang required
│   <image>.png         # copy any png image
│   reveal.sh           # helper for reveal folder from your IDE
```

#### Scripts usage
```bash
usage: mac-app-factory path ...
```

#### Examples
```bash
$ mac-app-factory path/to/my-finder-toolbar-apps path/to/my-dock-apps
```

```bash
$ mac-app-factory path/to/name1.app path/to/name2.app
```

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>