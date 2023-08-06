Podiant oEmbed
==============

![Build](https://git.steadman.io/podiant/oembed/badges/master/build.svg)
![Coverage](https://git.steadman.io/podiant/oembed/badges/master/coverage.svg)

A simple, flexible oEmbed provider and consumer

## Quickstart

Install oEmbed:

```sh
pip install podiant-oembed
```

Add it to your `INSTALLED_APPS`:
```python
INSTALLED_APPS = (
    ...
    'oembed',
    ...
)
```

## Running tests

To test the app with Django:

```
pip install Django
coverage run --source oembed test_django.py
```

To test the app with Flask:
```
pip install Flask
coverage run --source oembed test_flask.py
```

## Credits

Tools used in rendering this package:

- [Cookiecutter](https://github.com/audreyr/cookiecutter)
- [`cookiecutter-djangopackage`](https://github.com/pydanny/cookiecutter-djangopackage)
