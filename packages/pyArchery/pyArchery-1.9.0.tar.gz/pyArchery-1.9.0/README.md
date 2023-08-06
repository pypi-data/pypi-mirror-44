[![Follow Archery on Twitter](https://img.shields.io/twitter/follow/archerysec.svg?style=social&logo=twitter&label=Follow)](https://twitter.com/intent/user?screen_name=archerysec "Follow Archery on Twitter")

[![PyPI - License](https://img.shields.io/pypi/l/Django.svg)](https://github.com/archerysec/archerysec/blob/master/LICENSE) ![PyPI - Django Version](https://img.shields.io/pypi/djversions/djangorestframework.svg) ![Python - Python Version](https://img.shields.io/badge/Python-2.7-red.svg)

[![Road Map](https://img.shields.io/badge/Road-Map-orange.svg)](https://github.com/archerysec/archerysec/projects/1)

[![BlackHat Asia Arsenal 2018](https://github.com/toolswatch/badges/blob/master/arsenal/2018.svg)](https://www.blackhat.com/asia-18/arsenal/schedule/#archery---open-source-vulnerability-assessment-and-management-9837)



# ArcherySec

Archery is an opensource vulnerability assessment and management tool which helps developers and pentesters to perform scans and manage vulnerabilities. Archery uses popular opensource tools to perform comprehensive scanning for web application and network. It also performs web application dynamic authenticated scanning and covers the whole applications by using selenium. The developers can also utilize the tool for implementation of their DevOps CI/CD environment.

[For More details](http://docs.archerysec.info/)

## ArcherySec python package

ArcherySec Python package interacting with Archery using Archery RESTful API. It's allow you to create project, perform scans, extract scan data, etc. For more information please visit our [Developer Website](http://developers.archerysec.info/)

## Quick Start

Several quick start options are available:

- Install with pip: `pip install PyArchery`
- Build locally: `python setup.py build`
- [Download the latest release](https://github.com/target/webinspectapi/releases/latest/)

## Example

```
    # Import the package
    from archery import api

    # Set Archery url
    host = 'http://127.0.0.1:8008'

    # Setup archery connection
    archery = api.ArcheryAPI(host)

    # Provide Archery Credentials for authentication.
    authenticate = archery.archery_auth('admin', 'admin@123A')

    # Collect Token after authentication
    token = authenticate.data
    for key, value in token.viewitems():
        token = value

    # List all Projects
    project = archery.list_project(auth=token)

    # Printing in Json Format
    print project.data_json()
```

