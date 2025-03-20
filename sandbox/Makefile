SHELL := /bin/bash
dirname := $(notdir $(patsubst %/,%,$(CURDIR)))

install: # Installs dependencies using poetry.
	poetry install

list: # List of make targets
	@grep '^[^#[:space:]].*:' Makefile

build: # Build the Docker image to simulate ECS build
	cd .. && docker build -t validate-relationships-service-api-sandbox .

clear-examples: # Clears the examples cache (for local development, not used by docker build)
	rm -rf ./api/examples/*/

load-examples: # Load the examples from the specification (for local development, not used by docker build)
	cp -r ../specification/examples/responses/ ./api/examples

format: # Formats the code using black
	poetry run black . --line-length 120

start: load-examples # Starts the Flask app (Don't use this in production)
	poetry run flask --app api.app:app run -p 9000

start-dev: clear-examples load-examples # Starts the Flask app in development mode
	poetry run flask --app api.app:app run -p 9000 --reload --debug

test: # Runs the unit tests using pytest
	poetry run pytest
