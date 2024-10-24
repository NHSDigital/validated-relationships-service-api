# validated-relationships-service-api

This is a RESTful FHIR API for the [Validated Relationship Service API](https://digital.nhs.uk/developer/api-catalogue/validated-relationship-service).

Consumers of the API will find developer documentation on the [NHS Digital Developer Hub](https://digital.nhs.uk/developer/api-catalogue/validated-relationship-service).

This repository does _not_ include the Validated Relationship Service FHIR API back-end. That is part of 'Proxy Validated Relationship Service' repository which is not currently open source.

## Table of Contents

-   [validated-relationships-service-api](#validated-relationships-service-api)
    -   [Table of Contents](#table-of-contents)
    -   [Repository Structure](#repository-structure)
    -   [Contributing](#contributing)
    -   [Development \& Testing](#development--testing)
        -   [Licensing](#licensing)

## Repository Structure

This repository includes:

-   [specification/validated-relationships-service-api.yaml](./specification/validated-relationships-service-api.yaml) - The [Open API Specification](https://swagger.io/docs/specification/about/) describes the endpoints, methods and messages exchanged by the API. Use it to generate interactive documentation; the contract between the API and its consumers.
-   `sandbox/` - A flask (Python) API to provide mock implementation of the service. It's to be used as interactive documentation to illustrate interactions and concepts. It is not intended to provide an exhaustive/faithful environment suitable for full development and testing.
-   `scripts/` - Utilities helpful to developers for the development and release of the specification.
-   `proxies/` - Live and sandbox Apigee API Proxy definitions.

## Contributing

Contributions to this project are welcome from anyone, providing that they conform to the [guidelines for contribution](./CONTRIBUTING.md) and the [community code of conduct](./CODE_OF_CONDUCT.md).

## Development & Testing

All development commands and documentation can be found in [DEVELOPMENT_GUIDE.md](./DEVELOPMENT_GUIDE.md).

### Licensing

This code is dual licensed under the MIT license and the OGL (Open Government License). Any new work added to this repository must conform to the conditions of these licenses. In particular this means that this project may not depend on GPL-licensed or AGPL-licensed libraries, as these would violate the terms of those libraries' licenses.

The contents of this repository are protected by Crown Copyright (C).
