format:
	poetry run isort src tests
	poetry run black src tests

lint:
	poetry run isort src tests --check-only
	poetry run black src tests --check
	poetry run flake8 src
	poetry run mypy src --junit-xml build/mypy_junit.xml

test:
	poetry run pytest tests --no-cov

coverage:
	poetry run pytest --cov=src --cov-report=html:build/coverage --junitxml=build/junit.xml

requirements:
	poetry export -f requirements.txt --without-hashes -o requirements.txt