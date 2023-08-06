# Manage Conf

[![CircleCI](https://circleci.com/gh/sam-atkins/manageconf/tree/master.svg?style=svg)](https://circleci.com/gh/sam-atkins/manageconf/tree/master)
<a href="https://github.com/ambv/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

## Description

Builds a config object based on environment variables, settings files and (optional) parameters stored in AWS System Manager Parameter Store.

The config object merges in config, overriding any previous key/value pairs, in the following order:

- ENV
- default config: default.yml
- stage config: {stage}.yml
- remote config: remote_settings (AWS param store)

Available to download as a package on [PyPi](https://pypi.org/project/manageconf/).

### Settings Files

Set an environment variable with the key name `project_config_dir`. It is important this is set before the package is imported. The value of `project_config_dir` should be the location of your `/settings` folder.

Set-up your settings folder, adding in configuration to the appropriate file.

```
-- /settings
----          default.yml
----          {stage}.yml
----          {stage}.yml
```

Example configuration:

```yaml
# default.yml
project_name: example-project

# local.yml
use_remote_settings: false

# dev.yml
use_remote_settings: true
```

### AWS

Add parameters in your AWS account with paths that match this pattern:

`/{project_name}/{stage}/`

If you set `use_remote_settings: true` in a stage.yml config file, the package will attempt to fetch the parameters from the store that have this base path.

Using the example configuration above, the path would be:

```
/example-project/dev/
```

### Usage

Make sure you set `project_config_dir` before importing.

```python
from manageconf import Config, get_config

SECRET_KEY = get_config("SECRET_KEY")
DEBUG = get_config("DEBUG", True)
```

## Development

### Install

Requires [Poetry](https://poetry.eustace.io).

```bash
# create a Python3 virtual environment
virtualenv -p python3 env

# activate the virtual env
source env/bin/activate

# install requirements
poetry install
```

### Tests

```bash
# run tests
pytest -vv

# coverage report in the Terminal
pytest --cov=manageconf tests/

# coverage report in HTML
pytest --cov-report html --cov=manageconf tests/
```
