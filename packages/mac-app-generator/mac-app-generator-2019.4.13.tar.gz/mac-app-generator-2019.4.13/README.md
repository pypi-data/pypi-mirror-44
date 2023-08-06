<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/badge/OS-MacOS-blue.svg?longCache=True)]()
[![](https://img.shields.io/pypi/pyversions/mac-app-generator.svg?longCache=True)](https://pypi.org/project/mac-app-generator/)

#### Installation
```bash
$ [sudo] pip install mac-app-generator
```

#### Features
shell (mini) and python (full) versions

#### Classes
class|`__doc__`
-|-
`mac_app_generator.App` |Mac app generator. writable properties: `app_folder`, `app_name`, `app_path`, `app_code`, `app_script`, `app_image`, `app_stderr`, `app_stdout`, `app_env`. methods: `create_app()`

#### Scripts usage
```bash
usage: mac-app-generator script app [image]
```

#### Examples
create app from shell script
```bash
$ mac-app-generator script.sh name.app
$ mac-app-generator script.sh name.app Icon.png
```

create app from python script
```python
>>> mac_app.App(app_script="file.py", app_path="name.app").create_app()
```

create app from a python class
```python
import mac_app_generator
class MyApp(mac_app_generator.App):
    def run(self):
        pass

if __name__ == "__main__":
    MyApp().run()
```

```python
>>> MyApp().create_app()
```

#### Related projects
+   [`commands-generator` - shell commands generator](https://pypi.org/project/commands-generator/)
+   [`launchd-generator` - launchd.plist generator](https://pypi.org/project/launchd-generator/)
+   [`readme-generator` - `README.md` generator](https://pypi.org/project/readme-generator/)
+   [`setupcfg-generator` - `setup.cfg` generator](https://pypi.org/project/setupcfg-generator/)
+   [`travis-generator` - `.travis.yml` generator](https://pypi.org/project/travis-generator/)

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>