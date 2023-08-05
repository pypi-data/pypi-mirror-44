# gumo-core

## Setup Development Environment

```sh
$ pyenv virtualenv 3.7.2 gumo-core
$ pyenv local 3.7.2/envs/gumo-core

$ make setup
```

## Test

```sh
$ make test
```

## Build and Deploy

```sh
$ make test-deploy  # for https://test.pypi.org
## or
$ make deploy  # for https://pypi.org
```
