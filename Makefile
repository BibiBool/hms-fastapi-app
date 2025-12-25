##############################################################################
# Testing, auto formatting, type checks, & Lint checks

format:
	python -m black -S --line-length 80 .

isort:
	isort .

lint: 
	flake8 /opt/airflow/dags

ci: isort format lint 