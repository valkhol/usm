start:
	python -m main

fmt:
	black --line-length=90 --skip-string-normalization .
	isort .

test:
	pytest --cov=app --cov-report term-missing -vvv tests