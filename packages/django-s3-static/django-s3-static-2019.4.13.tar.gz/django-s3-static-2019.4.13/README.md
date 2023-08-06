<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
https://pypi.org/project/django-readme-generator/
-->

[![](https://img.shields.io/pypi/pyversions/django-s3-static.svg?longCache=True)](https://pypi.org/project/django-s3-static/)

#### Installation
```bash
$ [sudo] pip install django-s3-static
```

#### `settings.py`
```python
INSTALLED_APPS = [
    "django_s3_static",
]

AWS_STATIC_BUCKET_NAME = "<name>"
AWS_STATIC_DOMAIN = '%s.s3.amazonaws.com' % AWS_STATIC_BUCKET_NAME
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = "https://%s/" % AWS_STATIC_DOMAIN
```

#### Commands
command|`help`
-|-
`python manage.py s3-static-create` |create s3 bucket and policy
`python manage.py s3-static-sync` |sync static directory with s3 bucket

#### Examples
```bash
$ python manage.py s3-static-create # create s3 bucket and policy
$ python manage.py s3-static-sync   # sync static folder with s3 bucket
```

```html
{% load static %}
<link rel="stylesheet" href="{% static "css/file.css" %}">
```

<p align="center">
    <a href="https://pypi.org/project/django-readme-generator/">django-readme-generator</a>
</p>