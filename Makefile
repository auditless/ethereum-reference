install: FORCE  # Pull in local project dependencies
	pipenv install
	pipenv lock --pre

test: FORCE  # Run tests
	pipenv run pytest --doctest-modules

format: FORCE  # Auto-format Python code
	pipenv run black src

types: FORCE  # Type check
	pipenv run mypy --ignore-missing-imports src/*

run: FORCE  # Generate and print markdown file to stdout
	pipenv run python -m src.main

live: FORCE  # Create a live reload server
	ls src/* | entr -s "pipenv run python -m src.main"

FORCE: 
