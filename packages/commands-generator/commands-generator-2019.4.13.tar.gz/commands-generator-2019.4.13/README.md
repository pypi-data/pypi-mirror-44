<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/badge/OS-Unix-blue.svg?longCache=True)]()

#### Installation
```bash
$ [sudo] pip install commands-generator
```

#### Features
+   generate **shell commands from scripts**
+   **shell namespaces** - `namespace:command`. folder names as namespaces

#### How it works
scripts (shebang `#!` required):
```
namespace/script.py
namespace/subnamespace/script.sh
```

generated commands:
```
namespace:script
namespace:subnamespace:script
```

#### Config
`~/.bashrc`:

`export PATH=path/to/commands:$PATH`

#### Scripts usage
```bash
usage: commands-generator scripts_dir commands_dir
```

#### Examples
generate `~/.local/share/bin` from `dotfiles/scripts`:

```
dotfiles/scripts/git/commit.sh
dotfiles/scripts/files/python/setup.cfg/create.sh
dotfiles/scripts/web/github.com/push.sh
```

```bash
$ cd path/to/dotfiles
$ commands-generator scripts ~/.local/share/bin
```

generated commands:
```
~/.local/share/bin/git:commit
~/.local/share/bin/files:python:setup.cfg:create
~/.local/share/bin/web:github.com:push
```

usage:
```
$ files:python:requirements.txt:create
$ git:commit
$ web:github.com:push
```

#### Related projects
+   [`classifiers-generator` - python classifiers generator](https://pypi.org/project/classifiers-generator/)
+   [`commands-generator` - shell commands generator](https://pypi.org/project/commands-generator/)
+   [`launchd-generator` - launchd.plist generator](https://pypi.org/project/launchd-generator/)
+   [`readme-generator` - `README.md` generator](https://pypi.org/project/readme-generator/)
+   [`setupcfg-generator` - `setup.cfg` generator](https://pypi.org/project/setupcfg-generator/)
+   [`travis-generator` - `.travis.yml` generator](https://pypi.org/project/travis-generator/)

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>