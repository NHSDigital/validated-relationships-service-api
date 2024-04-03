SHELL := /bin/bash
dirname := $(notdir $(patsubst %/,%,$(CURDIR)))

install:
	poetry install

list:
	@grep '^[^#[:space:]].*:' Makefile

build:
	docker build -t validate-relationships-service-api-sandbox .

start:
	poetry run flask --app api.app:app run -p 9000

start-dev:
	poetry run flask --app api.app:app run -p 9000 --reload --debug

test:
	poetry run pytest
