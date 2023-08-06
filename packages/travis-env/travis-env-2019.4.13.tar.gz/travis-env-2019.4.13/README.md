<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/pypi/pyversions/travis-env.svg?longCache=True)](https://pypi.org/project/travis-env/)

#### Installation
```bash
$ [sudo] pip install travis-env
```

#### Features
+   add, get, delete Travis CI environment variables

#### Config
```bash
$ travis token
xxx
$ export TRAVIS_TOKEN="xxx"
# export TRAVIS_ENDPOINT="https://api.travis-ci.org"
```

#### Functions
function|`__doc__`
-|-
`travis_env.add(repo, var_name, var_value, public=False)` |add environment variable
`travis_env.update(repo, **kwargs)` |update environment variable

#### Executable modules
usage|`__doc__`
-|-
`python -m travis_env.clear repo` |clear all environment variables
`python -m travis_env.delete repo var_name ...` |delete environment variables by name
`python -m travis_env.set repo var_name var_value` |set environment variable
`python -m travis_env.vars repo` |print environment variable names

#### Examples
```bash
$ python -m travis_env.set WEBHOOK_URL url
$ python -m travis_env.vars
WEBHOOK_URL
```

#### Related projects
+   [`travis-generator` - `.travis.yml` generator](https://pypi.org/project/travis-generator/)
+   [`travis-cron` - manage travis cron](https://pypi.org/project/travis-cron/)
+   [`travis-env` - manage travis environment variables](https://pypi.org/project/travis-env/)
+   [`travis-exec` - execute command for all travis repos](https://pypi.org/project/travis-exec/)

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>