.PHONY: all
all: clean setup test lint mypy

.PHONY: setup
setup: pyproject.toml
	poetry check
	poetry install

.PHONY: test
test:
	poetry run pytest --cov=arc_to_sqlite/ --cov-report=xml

.PHONY: coverage.xml
coverage.xml: test

.PHONY: coverage
coverage: coverage.xml
	poetry run coverage html
	open htmlcov/index.html

.PHONY: lint
lint:
	poetry run black --check .
	poetry run isort --check .
	poetry run ruff check .

.PHONY: lintfix
lintfix:
	poetry run black .
	poetry run isort .
	poetry run ruff check . --fix

.PHONY: mypy
mypy:
	poetry run mypy arc_to_sqlite/

.PHONY: clean
clean:
	rm -fr ./.mypy_cache
	rm -fr ./.pytest_cache
	rm -fr ./.ruff_cache
	rm -fr ./dist
	rm -f .coverage
	rm -f coverage.xml
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete
	poetry env remove --all

.PHONY: arc.db
arc.db:
	poetry run arc-to-sqlite arc.db \
		~/Library/Mobile\ Documents/iCloud\~com\~bigpaua\~LearnerCoacher/ \
		--spatialite

.PHONY: datasette
datasette:
	poetry run datasette serve arc.db \
		--metadata metadata.yml \
		--load-extension=spatialite

.PHONY: ci
ci: setup test lint mypy
