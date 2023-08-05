# gumo-core

## Configuration

```python
from gumo.core import configure as core_configure

core_configure(
    google_cloud_project='<Google Cloud Platform Project Name>',
    google_cloud_location='<Project Main Location (Region)>',
)
```

If you need to load environment variables of app.yaml:

```python
import os
import flask
from gumo.core import MockAppEngineEnvironment
# from gumo.core import configure as core_configure


# The call to MockAppEngineEnvironment must precede any other initialization code.
if __name__ == '__main__':
    app_yaml_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'app.yaml'
    )
    MockAppEngineEnvironment.load_app_yaml(app_yaml_path=app_yaml_path)

# core_configure()

# Application Configurations ...
app = flask.Flask(__name__)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
```

## Setup Development Environment

```sh
$ pyenv virtualenv 3.7.2 gumo-core
$ pyenv local 3.7.2/envs/gumo-core

$ make setup
```

## Build and Test

```sh
$ make build

$ make test
```
