# This is how you'd Bench a Grape!

## Installation

```
$ pip install -r requirements.txt

$ python setup.py install

```

## package installation on a linux machine (in virtualenv)
```
mkdir benchgrape
cd benchgrape
virtualenv -p python3 benchgrape
source benchgrape/bin/activate
cd benchgrape
pip install --upgrade virtualenv
pip install benchgrape
benchgrape --help
```

## Development

This project includes a number of helpers in the `Makefile` to streamline common development tasks.

Revert an installed package to continue development
```
$ python setup.py develop
```

### Environment Setup

The following demonstrates setting up and working with a development environment:

```
### create a virtualenv for development

$ make virtualenv

$ source env/bin/activate


### run benchgrape cli application

$ benchgrape --help


### run pytest / coverage

$ make test
```


### Releasing to PyPi

Before releasing to PyPi, you must configure your login credentials:

**~/.pypirc**:

```
[pypi]
username = YOUR_USERNAME
password = YOUR_PASSWORD
```

Then use the included helper function via the `Makefile`:

```
$ make dist

$ make dist-upload
```

## Deployments

### Docker

Included is a basic `Dockerfile` for building and distributing `Bench Grape`,
and can be built with the included `make` helper:

```
$ make docker

$ docker run -it benchgrape --help
```
 
## Examples
### Test Websocket Stability
`benchgrape websocket test -n 10 -t 3600 --url https://staging.chatgrape.com --username rs@chatgrape.com --password 'quote-if-special-chars'`

### Load Test data for Benchmark
Test data can be exported on the grape server.
`benchgrape test-data load localhost.json`
