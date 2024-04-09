SHELL := /bin/bash
dirname := $(notdir $(patsubst %/,%,$(CURDIR)))

install: # Installs dependencies using poetry.
	poetry install --no-root

list:
	@grep '^[^#[:space:]].*:' Makefile

build: # Build the Docker image to simulate ECS build
	docker build -t validate-relationships-service-api-sandbox .

format: # Formats the code using black
	poetry run black .

start: # Starts the Flask app (Don't use this in production)
	poetry run flask --app api.app:app run -p 9000

start-dev: # Starts the Flask app in development mode
	poetry run flask --app api.app:app run -p 9000 --reload --debug

test: # Runs the unit tests using pytest
	poetry run pytest
