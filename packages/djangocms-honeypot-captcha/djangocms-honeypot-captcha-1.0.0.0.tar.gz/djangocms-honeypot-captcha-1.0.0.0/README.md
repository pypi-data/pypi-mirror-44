# Djangocms Honeypot Captcha

This python module is open-source, available here: https://gitlab.com/what-digital/djangocms-honeypot-captcha/

## Credits
- most of the code has been taken from https://github.com/mixkorshun/django-antispam/

## Versioning and Packages

- versioning is done in versioning in `djangocms_honeypot_captcha/__init__.py`
- for each version a tag is added to the gitlab repository in the form of `^(\d+\.)?(\d+\.)?(\*|\d+)$`, example: 0.1
- There is a PyPI version which relies on the gitlab tags (the download_url relies on correct gitlab tags being set): https://pypi.org/project/djangocms-honeypot-captcha/
- There is a DjangoCMS / Divio Marketplace add-on which also relies on the gitlab tags: https://marketplace.django-cms.org/en/addons/browse/djangocms-honeypot-captcha/

In order to release a new version of the Divio add-on:

- Increment version number in `addons-dev/djangocms-honeypot-captcha/djangocms_honeypot_captcha/__init__.py`
- divio addon validate
- divio addon upload
- Then git add, commit and tag with the version number

Then, in order to release a new pypi version:

- python3 setup.py sdist bdist_wheel
- twine upload --repository-url https://test.pypi.org/legacy/ dist/*
- twine upload dist/*

## Development

- cd into this project
- activate a working djangocms virtualenv
- pip install -e .
- install the project

## Dependencies

- None so far

## Setup

- install the add-on on divio.com or via pypi
- update your templates/djangocms_honeypot_captcha to reflect your frontend toolchain situation

