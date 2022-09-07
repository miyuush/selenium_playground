.PHONY: install

fmt:
	black .

install:
	poetry install
