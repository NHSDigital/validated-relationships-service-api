# Development Guide


- [Development Guide](#development-guide)
  - [Development](#development)
    - [Requirements](#requirements)
    - [Install](#install)
      - [Updating hooks](#updating-hooks)
    - [Environment Variables](#environment-variables)
    - [Make commands](#make-commands)
    - [Testing](#testing)
    - [VS Code Plugins](#vs-code-plugins)
    - [Emacs Plugins](#emacs-plugins)
    - [Speccy](#speccy)

## Development

### Requirements

-   make
-   nodejs + npm/yarn
-   Python 3.8 + [poetry](https://github.com/python-poetry/poetry)
-   Java 8+

### Install

```
$ make install
```

#### Updating hooks

You can install some pre-commit hooks to ensure you can't commit invalid spec changes by accident. These are also run
in CI, but it's useful to run them locally too.

```
$ make install
```

### Environment Variables

Various scripts and commands rely on environment variables being set. These are documented with the commands.

:bulb: Consider using [direnv](https://direnv.net/) to manage your environment variables during development and maintaining your own `.envrc` file - the values of these variables will be specific to you and/or sensitive.

### Make commands

There are `make` commands that alias some of this functionality:

-   `lint` -- Lints the spec and code
-   `publish` -- Outputs the specification as a **single file** into the `build/` directory
-   `serve` -- Serves a preview of the specification in human-readable format

### Testing

Each API and team is unique. We encourage you to use a `test/` folder in the root of the project, and use whatever testing frameworks or apps your team feels comfortable with. It is important that the URL your test points to be configurable. We have included some stubs in the Makefile for running tests.

### VS Code Plugins

-   [openapi-lint](https://marketplace.visualstudio.com/items?itemName=mermade.openapi-lint) resolves links and validates entire spec with the 'OpenAPI Resolve and Validate' command
-   [OpenAPI (Swagger) Editor](https://marketplace.visualstudio.com/items?itemName=42Crunch.vscode-openapi) provides sidebar navigation

### Emacs Plugins

-   [**openapi-yaml-mode**](https://github.com/esc-emacs/openapi-yaml-mode) provides syntax highlighting, completion, and path help

### Speccy

> [Speccy](http://speccy.io/) _A handy toolkit for OpenAPI, with a linter to enforce quality rules, documentation rendering, and resolution._

Speccy does the lifting for the following npm scripts:

-   `test` -- Lints the definition
-   `publish` -- Outputs the specification as a **single file** into the `build/` directory
-   `serve` -- Serves a preview of the specification in human-readable format

(Workflow detailed in a [post](https://developerjack.com/blog/2018/maintaining-large-design-first-api-specs/) on the _developerjack_ blog.)

:bulb: The `publish` command is useful when uploading to Apigee which requires the spec as a single file.
