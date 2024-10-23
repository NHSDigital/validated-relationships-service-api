# validated-relationships-service-api

This is a RESTful FHIR API for the [Validated Relationship Service API](https://digital.nhs.uk/developer/api-catalogue/validated-relationship-service).

It includes:

-   `specification/` This [Open API Specification](https://swagger.io/docs/specification/about/) describes the endpoints, methods and messages exchanged by the API. Use it to generate interactive documentation; the contract between the API and its consumers.
-   `sandbox/` A flask (Python) API to provide mock implementation of the service. It's to be used as interactive documentation to illustrate interactions and concepts. It is not intended to provide an exhaustive/faithful environment suitable for full development and testing.
-   `scripts/` Utilities helpful to developers of this specification.
-   `proxies/` Live (connecting to another service) and sandbox (using the sandbox container) Apigee API Proxy definitions.

Consumers of the API will find developer documentation on the [NHS Digital Developer Hub](https://digital.nhs.uk/developer/api-catalogue/validated-relationship-service).

This repository does _not_ include the Validated Relationship Service FHIR API back-end. That is part of 'Proxy Validated Relationship Service' repository which is not currently open source.

- [validated-relationships-service-api](#validated-relationships-service-api)
  - [Contributing](#contributing)
    - [Licensing](#licensing)
  - [Development \& Testing](#development--testing)
    - [Caveats](#caveats)
      - [Swagger UI](#swagger-ui)
      - [Apigee Portal](#apigee-portal)
    - [Platform setup](#platform-setup)
    - [Detailed folder walk through](#detailed-folder-walk-through)
      - [`/.github`:](#github)
      - [`/azure`:](#azure)
      - [`/proxies`:](#proxies)
      - [`/sandbox`:](#sandbox)
        - [Development](#development)
      - [`/scripts`:](#scripts)
      - [`/specification`:](#specification)
      - [`/tests`:](#tests)
      - [`Makefile`:](#makefile)
      - [`ecs-proxies-containers.yml ` and `ecs-proxies-deploy.yml`:](#ecs-proxies-containersyml--and-ecs-proxies-deployyml)
      - [`manifest_template.yml`:](#manifest_templateyml)
      - [Package management:](#package-management)


## Contributing

Contributions to this project are welcome from anyone, providing that they conform to the [guidelines for contribution](./CONTRIBUTING.md) and the [community code of conduct](./CODE_OF_CONDUCT.md).

### Licensing

This code is dual licensed under the MIT license and the OGL (Open Government License). Any new work added to this repository must conform to the conditions of these licenses. In particular this means that this project may not depend on GPL-licensed or AGPL-licensed libraries, as these would violate the terms of those libraries' licenses.

The contents of this repository are protected by Crown Copyright (C).

## Development & Testing

All development commands and documentation can be found in the [DEVELOPMENT_GUIDE.md](./CONTRIBUTING.md) file.

### Caveats

#### Swagger UI

Swagger UI unfortunately doesn't correctly render `$ref`s in examples, so use `speccy serve` instead.

#### Apigee Portal

The Apigee portal will not automatically pull examples from schemas, you must specify them manually.

### Platform setup

As currently defined in your `proxies` folder, your proxies do pretty much nothing.
Telling Apigee how to connect to your backend requires a _Target Server_, which you should call named `validated-relationships-service-api-target`.
Our _Target Servers_ defined in the [api-management-infrastructure](https://github.com/NHSDigital/api-management-infrastructure) repository.

:bulb: For Sandbox-running environments (`test`) these need to be present for successful deployment but can be set to empty/dummy values.

### Detailed folder walk through

To get started developing your API use this template repo alongside guidance provided by the [API Producer Zone confluence](https://nhsd-confluence.digital.nhs.uk/display/APM/Deliver+your+API)

#### `/.github`:

This folder contains templates that can be customised for items such as opening pull requests or issues within the repo

`/.github/workflows`: This folder contains templates for GitHub action workflows such as:

-   `pr-lint.yaml`: This workflow template shows how to link Pull Request's to Jira tickets and runs when a pull request is opened.
-   `continuous-integration.yml`: This workflow template shows how to publish a Github release when pushing to master.
-   `sandbox-checks.yaml`: This workflow checks the sandbox meets the formatting and linting rules (Black + Flake8). Also it runs the sandbox unit tests (Pytest)
-   `dependency-review.yml`: This workflow checks for any vulnerabilities in dependencies to be added to the project.
-   `codeql-analysis.yml`: This workflow checks for any code vulnerabilities in the project.

#### `/azure`:

Contains templates defining Azure Devops pipelines. By default the following pipelines are available:

-   `azure-build-pipeline.yml`: Assembles the contents of your repository into a single file ("artifact") on Azure Devops and pushes any containers to our Docker registry. By default this pipeline is enabled for all branches.
-   `azure-pr-pipeline.yml`: Deploys ephemeral versions of your proxy/spec to Apigee (and docker containers on AWS) to internal environments. You can run automated and manual tests against these while you develop. By default this pipeline will deploy to internal-dev, but the template can be amended to add other environments as required.
-   `azure-release-pipeline.yml`: Deploys the long-lived version of your pipeline to internal and external environments, typically when you merge to master.

The `project.yml` file needs to be populated with your service names to make them available to the pipelines

`/azure/templates`: Here you can define reusable actions, such as running tests, and call these actions during Azure Devops pipelines.

#### `/proxies`:

This folder contains files relating to your Apigee API proxy.

There are 2 folders `/live` and `/sandbox` allowing you to define a different proxy for sandbox use. By default, this sandbox proxy is implemented to route to the sandbox target server (code for this sandbox is found under /sandbox of this template repo)

Within the `live/apiproxy` and `sandbox/apiproxy` folders are:

`/proxies/default.xml`: Defines the proxy's Flows. Flows define how the proxy should handle different requests. By default, \_ping and \_status endpoint flows are defined.
See the APM confluence for more information on how the [\_ping](https://nhsd-confluence.digital.nhs.uk/display/APM/_ping+endpoint) and [\_status](https://nhsd-confluence.digital.nhs.uk/display/APM/_status+endpoint) endpoints work.

`/policies`: Populated with a set of standard XML Apigee policies that can be used in flows.

`/resources/jsc`: Snippets of javascript code that are used in Apigee Javascript policies. For more info about Javascript policies see [here](https://docs.apigee.com/api-platform/reference/policies/javascript-policy)

`/targets`: The XMLs within these folders set up target definitions which allow connections to external target servers. The sandbox target definition is implemented to route to the sandbox target server (code for this sandbox is found under /sandbox of this template repo). For more info on setting up a target server see the [API Producer Zone confluence](https://nhsd-confluence.digital.nhs.uk/display/APM/Setting+up+a+target+server)

#### `/sandbox`:

Sandbox provides a API for exploring the Proxy API. It uses pre-canned responses to most common scenarios.

##### Development

For information on how to develop the sandbox API see [README.md](sandbox/README.md)

#### `/scripts`:

Contains useful scripts that are used throughout the project, for example in Makefile and Github workflows

#### `/specification`:

Create an OpenAPI Specification to document your API. For more information about developing specifications see the [API Producer Zone confluence](https://nhsd-confluence.digital.nhs.uk/display/APM/Documenting+your+API).

#### `/tests`:

End to End tests. These tests are written in Python and use the PyTest test runner. Before running these tests you will need to set environment variables. The `test_endpoint.py` file provides a template of how to set up tests which test your api endpoints. For more information about testing your API see the [API Producer Zone confluence](https://nhsd-confluence.digital.nhs.uk/display/APM/Testing+your+API).

#### `Makefile`:

Useful make targets to get started including: installing dependencies and running smoke tests.

#### `ecs-proxies-containers.yml ` and `ecs-proxies-deploy.yml`:

These files are required to deploy containers alongside your Apigee proxy during the Azure Devops `azure-build-pipeline`. In this template repo we are deploying our sandbox container which is used as the target server for the sandbox proxy.

`ecs-proxies-containers.yml`: The path to a container's Dockerfile is defined here. This path needs to be defined to allow containers to be pushed to our repository during the `azure-build-pipeline`.

`ecs-proxies-deploy.yml` : Here you can define config for your container deployment.

For more information about deploying ECS containers see the [API Producer Zone confluence](https://nhsd-confluence.digital.nhs.uk/display/APM/Developing+ECS+proxies#DevelopingECSproxies-Buildingandpushingdockercontainers).

#### `manifest_template.yml`:

This file defines 2 dictionaries of fields that are required for the Apigee deployment. For more info see the [API Producer Zone confluence](https://nhsd-confluence.digital.nhs.uk/display/APM/Manifest.yml+reference).

#### Package management:

This template uses poetry for python dependency management, and uses these files: poetry.lock, poetry.toml, pyproject.toml.

Node dependencies of this template project and some npm scripts are listed in: package.json, package-lock.json.
