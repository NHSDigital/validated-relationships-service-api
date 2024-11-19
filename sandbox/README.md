# Sandbox

This folder contains a sandbox API for initial development

For more information about building sandbox APIs see the [API Producer Zone confluence](https://nhsd-confluence.digital.nhs.uk/display/APM/Setting+up+your+API+sandbox).

## Table of Contents

-   [Sandbox](#sandbox)
    -   [Table of Contents](#table-of-contents)
    -   [Prerequisites](#prerequisites)
    -   [Quick Start](#quick-start)
        -   [Installing dependencies](#installing-dependencies)
        -   [Starting the API](#starting-the-api)
    -   [Development](#development)
        -   [Starting the API with Hot Reloading](#starting-the-api-with-hot-reloading)
        -   [Testing](#testing)
            -   [Unit Tests](#unit-tests)
        -   [Useful commands](#useful-commands)

## Prerequisites

-   Python 3.8
-   [Poetry](https://python-poetry.org/docs/)
-   [Docker](https://docs.docker.com/get-docker/)

## Quick Start

Please note all commands are meant to be run from this directory `/sandbox`

### Installing dependencies

To install the dependencies use `make install`

If you do not have poetry installed you can install the dependencies using `pip install poetry` and then run `make install`

### Starting the API

To start the API locally use `make start`

## Development

Please note all commands are meant to be run from this directory `/sandbox`

### Starting the API with Hot Reloading

To run the API with hot reloading use `make start-dev`

### Testing

#### Unit Tests

Unit tests can be run using `make test`

### Useful commands

For more useful development commands review the [Makefile](Makefile) or run `make list`
