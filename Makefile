.PHONY: fmt
fmt:
	poetry run isort selenium_playground/
	poetry run black --line-length 99 selenium_playground/

.PHONY: install
install:
	poetry install

.PHONY: lint
lint:
	poetry run flake8 --extend-ignore F401 selenium_playground/
	poetry run mypy selenium_playground/
	poetry run isort --check --diff selenium_playground/
	poetry run black --check --diff --line-length 99 selenium_playground/

.PHONY: ci-lint
ci-lint:
	flake8 --extend-ignore F401 selenium_playground/
	mypy selenium_playground/
	isort --check --diff selenium_playground/
	black --check --diff --line-length 99 selenium_playground/
