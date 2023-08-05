
help: ## Show this help.
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

##

# Tests
test:  ## Run the tests
	pipenv run python -m pytest

typecheck:  ## Run the typecheck checker
	pipenv run python -m mypy dataclass_structor

##

# Perf tests
perf-tests:  ## Run the performace tests
	rm bench.json || true
	pipenv run python tests/perf_tests.py -o bench.json

build-docs:  ## Generate the docs
	pipenv run sphinx-build -b html . ./_build

##

check-format: ## Check that the code formatting is up to snuff
	pipenv run python -m black --diff --check dataclass_structor tests

format:  ## Run the auto formatter against the code
	pipenv run python -m black dataclass_structor tests

lint:  ## Run the the linter across the code
	pipenv run pylint --rcfile=.pylintrc dataclass_structor tests

.PHONY: typecheck test format perf-tests build-docs check-format
