[![banner](https://raw.githubusercontent.com/oceanprotocol/art/master/github/repo-banner%402x.png)](https://oceanprotocol.com)

# oceandb-driver-interface

> 🐳 Ocean DB driver interface(Python).
> [oceanprotocol.com](https://oceanprotocol.com)

[![Travis (.com)](https://img.shields.io/travis/com/oceanprotocol/oceandb-driver-interface.svg)](https://travis-ci.com/oceanprotocol/oceandb-driver-interface)
[![PyPI](https://img.shields.io/pypi/v/oceandb-driver-interface.svg)](https://pypi.org/project/oceandb-driver-interface/)
[![GitHub contributors](https://img.shields.io/github/contributors/oceanprotocol/oceandb-driver-interface.svg)](https://github.com/oceanprotocol/oceandb-driver-interface/graphs/contributors)

---

## Table of Contents

  - [Features](#features)
  - [Quick-start](#quick-start)
  - [Environment variables](#environment-variables)
  - [Plugins availables](#plugins-availables)
  - [How to develop a plugin](#how-to-develop-a-plugin)
  - [Code style](#code-style)
  - [Testing](#testing)
  - [New Version](#new-version)
  - [License](#license)

---

## Features

High-level, plugin-bound Ocean DB functions. You should implement a plugin class extending this module to connect with Ocean DB.


## Quick-start


Abstract interface for all persistence layer plugins.
Expects the following to be defined by the subclass:

* type - A string denoting the type of plugin (e.g. BigchainDB).
* write - Write an object in OceanDB
* read - Read the registry for a provided id
* update - Update an object in OceanDB
* delete - Delete the registry for a provided id
* list - List the elements saved in OceanDB

Once you have your plugin, the way to use it is the following:


You have to provide a configuration with the following information:

```yaml
    [oceandb]

    enabled=true            # In order to enable or not the plugin
    module=bigchaindb       # You can use one the plugins already created. Currently we have mongodb and bigchaindb.
    module.path=            # You can specify the location of your custom plugin.
    db.hostname=localhost   # Address of your persistence.
    db.port=9985            # Port of yout persistence database.

    # In order to use SSL, configure below options.
    db.ssl=true             # If *true*, connections will be made using HTTPS, else using HTTP
    db.verify_certs=false   # If *true*, CA certificate will be verified
    db.ca_cert_path=        # If verifyCerts is *true*, then path to the CA cert should be provided here
    db.client_key=          # If db server needs client verification, then provide path to your client key
    db.client_cert_path=    # If db server needs client verification, then provide path to your client cert

    # If you choose bigchaindb you have to provide this:
    secret=                 # A secret that serves as a seed.
    db.namespace=namespace  # Namespace that you are going to use in bigchaindb
    db.app_id=              # App id of your bigchaindb application.
    db.app_key=             # App key of your bigchaindb application.

    # If you choose mongodb you have to provide this:
    db.username=travis      # If you are using authentication, mongodb username.
    db.password=test        # If you are using authentication, mongodb password.
    db.name=test            # Mongodb database name
    db.collection=col       # Mongodb collection name

    # If you choose elastic-search you have to provide this:
    db.username=elastic     # If you are using authentication, elasticsearch username.
    db.password=changeme    # If you are using authentication, elasticsearch password.
    db.index=oceandb        # Elasticsearch index name
```

## Environment variables

When you want to instantiate an Oceandb plugin you can provide the next environment variables:


- **$CONFIG_PATH** -> If you provide the config path Oceandb is going to run using this config values.
- **$MODULE** -> If you provide the module, you are going to select one of the modules. 

## Plugins availables

At the moment we have developed two plugins:

* Bigchaindb (https://github.com/oceanprotocol/oceandb-bigchaindb-driver)
* Mongodb (https://github.com/oceanprotocol/oceandb-mongodb-driver)


## How to develop a plugin

To create a plugin you have to create a class called Plugin extending AbstractPlugin.

You could find an example in https://github.com/oceanprotocol/oceandb-bigchaindb-driver


## Code style

The information about code style in python is documented in this two links [python-developer-guide](https://github.com/oceanprotocol/dev-ocean/blob/master/doc/development/python-developer-guide.md)
and [python-style-guide](https://github.com/oceanprotocol/dev-ocean/blob/master/doc/development/python-style-guide.md).
    
## Testing

Automatic tests are setup via Travis, executing `tox`.
Our test use pytest framework.

## New Version

The `bumpversion.sh` script helps to bump the project version. You can execute the script using as first argument {major|minor|patch} to bump accordingly the version.

## License

```
Copyright 2018 Ocean Protocol Foundation Ltd.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.