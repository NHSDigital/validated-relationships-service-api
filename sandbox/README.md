# Sandbox

This folder contains a sandbox API for initial development

For more information about building sandbox APIs see the [API Producer Zone confluence](https://nhsd-confluence.digital.nhs.uk/display/APM/Setting+up+your+API+sandbox).

## Table of Contents

- [Sandbox](#sandbox)
  - [Table of Contents](#table-of-contents)
  - [Architecture](#architecture)
  - [Prerequisites](#prerequisites)
  - [Quick Start](#quick-start)
    - [Installing dependencies](#installing-dependencies)
    - [Starting the API](#starting-the-api)
  - [Development](#development)
    - [Starting the API with Hot Reloading](#starting-the-api-with-hot-reloading)
    - [Testing](#testing)
      - [Unit Tests](#unit-tests)
    - [Useful commands](#useful-commands)

## Architecture

The sandbox API is built using Python 3.8 and [Flask](https://flask.palletsprojects.com/en/stable/).

The API is able to be run locally on the host system for development and testing purposes.

The Sandbox is deployed using Docker to AWS ECS; the Dockerfile is located in the root of the repository. This allows Docker to copy in responses from `specification/examples/responses`. The docker container is deployed to AWS ECS using Azure DevOps pipelines.

The [Postman Collection](./postman/Validate_Relationship_Service_Sandbox.postman_collection.json) is used to test the Sandbox API. The tests embedded in the collection are run in GitHub Actions on each Pull Request.

## Prerequisites

-   Python 3.8
-   [Poetry](https://python-poetry.org/docs/)
-   [Docker](https://docs.docker.com/get-docker/)

## Quick Start

Please note all make targets commands are meant to be run from this directory `/sandbox`

### Installing dependencies

To install the sandbox dependencies use `make install`

If you do not have poetry installed you can install the dependencies using `pipx install poetry` and then run `make install`

### Starting the API

To start the API locally use the following command:

```bash
make start
```

The API will be available at [http://localhost:9000](http://localhost:9000)

## Development

Please note all commands are meant to be run from this directory `/sandbox`

### Starting the API with Hot Reloading

To run the API with hot reloading use `make start-dev`

### Testing

#### Unit Tests

Unit tests can be run using `make test`

### Useful commands

For more useful development commands review the [Makefile](Makefile) or run `make list`
