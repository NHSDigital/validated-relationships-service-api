# Development Guide

This documentation is intended for developers to develop the schema, sandbox and proxies. It may be used by developers working within the NHS Digital organisation and outside contributors.

> [!WARNING]
> Some of the documentation and links are specific to the maintainers of this repository and are only available to NHS England staff.

## Table of Contents

-   [Development Guide](#development-guide)
    -   [Table of Contents](#table-of-contents)
    -   [Development](#development)
        -   [Requirements](#requirements)
        -   [Make commands](#make-commands)
        -   [Testing](#testing)
        -   [Platform setup](#platform-setup)
        -   [Detailed folder walk through](#detailed-folder-walk-through)
            -   [`/.github`:](#github)
            -   [`/azure`:](#azure)
            -   [`/proxies`:](#proxies)
            -   [`/scripts`:](#scripts)
            -   [`/specification`:](#specification)
            -   [`/tests`:](#tests)
            -   [`Makefile`:](#makefile)
            -   [`ecs-proxies-containers.yml ` and `ecs-proxies-deploy.yml`:](#ecs-proxies-containersyml--and-ecs-proxies-deployyml)
            -   [`manifest_template.yml`:](#manifest_templateyml)
    -   [Releasing a new schema version](#releasing-a-new-schema-version)
        -   [Caveats](#caveats)
            -   [Swagger UI](#swagger-ui)
            -   [Apigee Portal](#apigee-portal)

## Development

> [!NOTE]
> Sandbox development is not documented here. Please see the [Sandbox README](./sandbox/README.md) for more information.

### Requirements

-   GNU make
-   nodejs 22+
    -   npm 10.8+
-   Python 3.8 +
    -   [poetry](https://github.com/python-poetry/poetry) 1.8+
-   Java 8+

### Make commands

To run the below make targets you will first need to run `make install-node`

There are `make` commands that alias scripts in the `package.json`

-   `lint` -- Lints the spec and code
-   `publish` -- Outputs the specification as a **single file** into the `build/` directory
-   `serve` -- Serves a preview of the specification in human-readable format

### Testing

A minimal Pytest test suite is available under the [tests](./tests) folder. These test the Apigee Proxy is set up. These tests are written in Python and use the PyTest test runner.

A majority of the testing is co-located with the application in the `Proxy Validated Relationship Service` repository that is not currently open source.

The test dependencies can be installed by running `make install` from the root directory of this project.
To run tests run `make test` from the project root. Or for Smoke tests run `make smoketest`

### Platform setup

Apigee is setup for all live environments (dev, qa, int, prod) proxy the request to a target server. The target server on Apigee should be named `validated-relationships-service-api-target`.
Target Servers defined in the [api-management-infrastructure](https://github.com/NHSDigital/api-management-infrastructure/blob/master/ansible/roles/apigee-keystores-refs-targetservers/vars/main/target-servers.yml) repository.

Sandbox environments use Apigee to proxy the request to an AWS ECS container.

### Detailed folder walk through

For further information about Apigee and APIM see [API Producer Zone confluence](https://nhsd-confluence.digital.nhs.uk/display/APM/Deliver+your+API)

#### `/.github`:

`/.github/workflows`: This folder contains GitHub workflows, these workflow are mainly used to check pull requests and publish releases.

-   `pr-lint.yaml`: This workflow links Pull Request's to Jira tickets and runs when a pull request is opened/updated.
-   `continuous-integration.yml`: This workflow publishes a Github release when pushing to master.
-   `sandbox-checks.yaml`: This workflow checks the sandbox meets the formatting and linting rules (Black + Flake8). Also it runs the sandbox unit tests (Pytest)
-   `dependency-review.yml`: This workflow checks for any vulnerabilities in dependencies to be added to the project.
-   `codeql-analysis.yml`: This workflow checks for any code vulnerabilities in the project.

#### `/azure`:

Contains Azure Devops pipelines for building and deploying to Apigee:

-   `azure-build-pipeline.yml`: Assembles the contents of your repository into a single file ("artifact") on Azure Devops and pushes any containers to our Docker registry. This pipeline is enabled for all branches.
-   `azure-pr-pipeline.yml`: Deploys ephemeral versions of your proxy/spec to Apigee (and docker containers on AWS) to internal environments. This will deploy a internal-dev environment and internal-dev-sandbox for each pull request.
-   `azure-release-pipeline.yml`: Deploys the long-lived version of your pipeline to internal and external environments, when you merge to master.

`/azure/templates`: Here you can define reusable actions, such as running tests, and call these actions during Azure Devops pipelines.

#### `/proxies`:

This folder contains files relating to the Apigee API proxy.

There are 2 folders `/live` and `/sandbox` allowing you to define a different proxy for sandbox use. By default, this sandbox proxy is implemented to route to the sandbox target server (code for this sandbox is found under /sandbox of this template repo)

Within the `live/apiproxy` and `sandbox/apiproxy` folders are:

`/proxies/default.xml`: Defines the proxy's Flows. Flows define how the proxy should handle different requests. By default, \_ping and \_status endpoint flows are defined.
See the APM confluence for more information on how the [\_ping](https://nhsd-confluence.digital.nhs.uk/display/APM/_ping+endpoint) and [\_status](https://nhsd-confluence.digital.nhs.uk/display/APM/_status+endpoint) endpoints work.

`/policies`: Populated with a set of standard XML Apigee policies that can be used in flows.

`/resources/jsc`: Snippets of javascript code that are used in Apigee Javascript policies. For more info about Javascript policies see [here](https://docs.apigee.com/api-platform/reference/policies/javascript-policy)

`/targets`: The XMLs within these folders set up target definitions which allow connections to external target servers. The sandbox target definition is implemented to route to the sandbox target server (code for this sandbox is found under /sandbox of this template repo). For more info on setting up a target server see the [API Producer Zone confluence](https://nhsd-confluence.digital.nhs.uk/display/APM/Setting+up+a+target+server)

#### `/scripts`:

Contains useful scripts that are used throughout the project. Mainly Python scripts used in the release process.

#### `/specification`:

Contains the OpenAPI specification - [validated-relationships-service-api.yaml](./specification/validated-relationships-service-api.yaml)

#### `/tests`:

End to End tests. These tests are written in Python and use the PyTest test runner. Before running these tests you will need to set environment variables. The `test_endpoint.py` file provides a template of how to set up tests which test your api endpoints. For more information about testing your API see the [API Producer Zone confluence](https://nhsd-confluence.digital.nhs.uk/display/APM/Testing+your+API).

#### `Makefile`:

Contains make targets to run parts of the project such as installing dependencies and running smoke tests.

#### `ecs-proxies-containers.yml ` and `ecs-proxies-deploy.yml`:

These files are required to deploy containers alongside your Apigee proxy during the Azure Devops `azure-build-pipeline`.

`ecs-proxies-containers.yml`: The path to a container's Dockerfile is defined here. This path needs to be defined to allow containers to be pushed to our repository during the `azure-build-pipeline`. This is used for the sandbox proxy docker container.

`ecs-proxies-deploy.yml` : Here you can define config for your container deployment.

For more information about deploying ECS containers see the [API Producer Zone confluence](https://nhsd-confluence.digital.nhs.uk/display/APM/Developing+ECS+proxies#DevelopingECSproxies-Buildingandpushingdockercontainers).

#### `manifest_template.yml`:

This file defines 2 dictionaries of fields that are required for the Apigee deployment. For more info see the [API Producer Zone confluence](https://nhsd-confluence.digital.nhs.uk/display/APM/Manifest.yml+reference).

## Releasing a new schema version

To release a new version of the schema, follow the steps below:

1. Update the version number in [specification/validated-relationships-service-api.yaml](./specification/validated-relationships-service-api.yaml).
2. Update the Postman collection - [postman/Validate Relationship Service Sandbox.postman_collection.json](./postman/Validate%20Relationship%20Service%20Sandbox.postman_collection.json).
    1. Documentation on how to update the Postman collection can be found [here](https://nhsd-confluence.digital.nhs.uk/pages/viewpage.action?pageId=874694621).
3. Update the sandbox - [sandbox](./sandbox).
4. Create a pull request with the changes.
5. Once the pull request has been approved, merge it into the `master` branch.
6. Request a schema changes are published to the [Validated Relationship Service API](https://digital.nhs.uk/developer/api-catalogue/validated-relationship-service) page.
    1. Documentation on how to update the published specification page can be found [here](https://nhsd-confluence.digital.nhs.uk/display/NPA/Deploy+to+Public+Validated+Relationship+Service+API+Page)

### Caveats

#### Swagger UI

Swagger UI unfortunately doesn't correctly render `$ref`s in examples, so when publishing the schema to the API catalogue it uses `make publish` which under the hood uses `speccy serve` instead.

#### Apigee Portal

The Apigee portal will not automatically pull examples from schemas, you must specify them manually.
