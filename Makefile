.PHONY: fmt
fmt:
	poetry run isort .
	poetry run black --line-length 99 .

.PHONY: install
install:
	poetry install

.PHONY: lint
lint:
	poetry run flake8 --extend-ignore F401 .
	poetry run isort --check --diff .
	poetry run black --check --diff --line-length 99 .

.PHONY: ci-lint
ci-lint:
	flake8 --extend-ignore F401 .
	isort --check --diff .
	black --check --diff --line-length 99 .
