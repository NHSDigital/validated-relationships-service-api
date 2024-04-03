SHELL := /bin/bash
dirname := $(notdir $(patsubst %/,%,$(CURDIR)))

install:
	cd .. && make install-python

list:
	@grep '^[^#[:space:]].*:' Makefile

build:
	cp ../pyproject.toml . && cp ../poetry.lock . && cp ../poetry.toml .
	docker build -t validate-relationships-service-api-sandbox .
	rm -f pyproject.toml poetry.lock poetry.toml

test:
	poetry run pytest
