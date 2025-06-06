SHELL=/bin/bash -euo pipefail

#Installs dependencies using poetry.
install-python:
	poetry install --no-root

#Installs dependencies using npm.
install-node:
	npm install --legacy-peer-deps
	cd sandbox && npm install --legacy-peer-deps

#Configures Git Hooks, which are scripts that run given a specified event.
install-git-hooks:
	cp scripts/pre-commit .git/hooks/pre-commit
	chmod +x .git/hooks/pre-commit

#Condensed Target to run all targets above.
install: install-node install-python install-git-hooks

#Run the npm linting script (specified in package.json). Used to check the syntax and formatting of files.
lint:
	find . -name '*.py' -not -path '**/.venv/*' | xargs poetry run flake8

format:
	find . -name '*.py' -not -path '**/.venv/*' | xargs poetry run black --check --line-length 120

format-apply:
	find . -name '*.py' -not -path '**/.venv/*' | xargs poetry run black --line-length 120

#Removes build/ + dist/ directories
clean:
	rm -rf build
	rm -rf dist

#Creates the fully expanded OAS spec in json
publish: clean
	mkdir -p build
	npm run publish 2> /dev/null

#Runs build proxy script
build-proxy:
	scripts/build_proxy.sh

#Files to loop over in release
_dist_include="pytest.ini poetry.lock poetry.toml pyproject.toml Makefile build/. tests"

#Create /dist/ sub-directory and copy files into directory
release: clean publish build-proxy
	mkdir -p dist
	for f in $(_dist_include); do cp -r $$f dist; done
	cp ecs-proxies-deploy.yml dist/ecs-deploy-sandbox.yml
	cp ecs-proxies-deploy.yml dist/ecs-deploy-internal-qa-sandbox.yml
	cp ecs-proxies-deploy.yml dist/ecs-deploy-internal-dev-sandbox.yml

#################
# Test commands #
#################

TEST_CMD := @APIGEE_ACCESS_TOKEN=$(APIGEE_ACCESS_TOKEN) \
		poetry run pytest -v \
		--color=yes \
		--api-name=validated-relationships-service-api \
		--proxy-name=$(PROXY_NAME) \
		-s

PROD_TEST_CMD := $(TEST_CMD) \
		--apigee-app-id=$(APIGEE_APP_ID) \
		--apigee-organization=nhsd-prod \
		--status-endpoint-api-key=$(STATUS_ENDPOINT_API_KEY)

#Command to run end-to-end smoketests post-deployment to verify the environment is working
smoketest:
	$(TEST_CMD) \
	--junitxml=smoketest-report.xml \
	-m smoketest

test:
	$(TEST_CMD) \
	--junitxml=test-report.xml \

smoketest-prod:
	$(PROD_TEST_CMD) \
	--junitxml=smoketest-report.xml \
	-m smoketest

test-prod:
	$(PROD_CMD) \
	--junitxml=test-report.xml \

# Run schema validation check
GREEN  := \033[32m
RESET  := \033[0m



schema-all:
	make schema-get-consent \
	schema-post-consent \
	schema-patch-consent \
	schema-related-person \
	schema-questionnaire \
	schema-errors

schema-get-consent:
	@for file in specification/examples/responses/GET_Consent/*.yaml; do \
		echo "Processing $$file"; \
		poetry run python scripts/validate_schema.py consent "$$(realpath $$file)"; \
		echo -e "$(GREEN)Success!$(RESET)"; \
	done

schema-post-consent:
	@for file in specification/examples/responses/POST_Consent/*.yaml; do \
		echo "Processing $$file"; \
		poetry run python scripts/validate_schema.py operationoutcome "$$(realpath $$file)"; \
		echo -e "$(GREEN)Success!$(RESET)"; \
	done

schema-patch-consent:
	@for file in specification/examples/responses/PATCH_Consent/*.yaml; do \
		echo "Processing $$file"; \
		poetry run python scripts/validate_schema.py operationoutcome "$$(realpath $$file)"; \
		echo -e "$(GREEN)Success!$(RESET)"; \
	done

schema-related-person:
	@for file in specification/examples/responses/GET_RelatedPerson/*.yaml; do \
		echo "Processing $$file"; \
		poetry run python scripts/validate_schema.py relatedperson "$$(realpath $$file)"; \
		echo -e "$(GREEN)Success!$(RESET)"; \
	done

schema-questionnaire:
	@for file in specification/examples/responses/POST_QuestionnaireResponse/*.yaml; do \
		echo "Processing $$file"; \
		poetry run python scripts/validate_schema.py operationoutcome "$$(realpath $$file)"; \
		echo -e "$(GREEN)Success!$(RESET)"; \
	done

schema-errors:
	@for file in specification/examples/responses/errors/*.yaml; do \
		echo "Processing $$file"; \
		poetry run python scripts/validate_schema.py operationoutcome "$$(realpath $$file)"; \
		echo -e "$(GREEN)Success!$(RESET)"; \
	done

schema-get-questionnaire:
	@for file in specification/examples/responses/GET_QuestionnaireResponse/*.yaml; do \
		echo "Processing $$file"; \
		poetry run python scripts/validate_schema.py questionnaireresponse "$$(realpath $$file)"; \
		echo -e "$(GREEN)Success!$(RESET)"; \
	done
