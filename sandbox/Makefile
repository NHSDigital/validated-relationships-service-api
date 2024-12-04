SHELL := /bin/bash
dirname := $(notdir $(patsubst %/,%,$(CURDIR)))

install: # Installs dependencies using poetry.
	poetry install --no-root

list: # List of make targets
	@grep '^[^#[:space:]].*:' Makefile

build: # Build the Docker image to simulate ECS build
	cd .. && docker build -t validate-relationships-service-api-sandbox .

load-examples: # Load the examples from the specification (for local development, not used by docker build)
	cp -r ../specification/examples/responses/ ./api/examples

format: # Formats the code using black
	poetry run black .

start: load-examples # Starts the Flask app (Don't use this in production)
	poetry run flask --app api.app:app run -p 9000

start-dev: load-examples # Starts the Flask app in development mode
	poetry run flask --app api.app:app run -p 9000 --reload --debug

test: # Runs the unit tests using pytest
	poetry run pytest
