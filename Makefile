####################################################################################################################
# Testing, auto formatting, type checks, & Lint checks

format:
	python -m black -S --line-length 79 .

isort:
	isort .

lint: 
	docker exec webserver flake8 /opt/airflow/dags

ci: isort format type lint 