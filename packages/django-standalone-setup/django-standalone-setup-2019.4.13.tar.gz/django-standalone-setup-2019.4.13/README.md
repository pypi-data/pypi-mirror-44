<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
https://pypi.org/project/django-readme-generator/
-->

[![](https://img.shields.io/pypi/pyversions/django-standalone-setup.svg?longCache=True)](https://pypi.org/project/django-standalone-setup/)

#### Installation
```bash
$ [sudo] pip install django-standalone-setup
```

#### Features
calls `django.setup` once only

#### Config
```bash
$ export DJANGO_SETTINGS_MOULE='django_settings'
```

`site-package/django_settings.py`
```python
INSTALLED_APPS = [
    'your_app',
]
DATABASES = {
    'default': {
        ...
    }
}
```

#### Examples
`script.py`
```python
# !/usr/bin/env python
import django_standalone_setup # at the top of module
...
```

<p align="center">
    <a href="https://pypi.org/project/django-readme-generator/">django-readme-generator</a>
</p>