PYTHON:= python3
PIP:= pip3

GUNICORN_PORT = 5000
GUNICORN_WORKERS = 2
GUNICORN_TIME_OUT = 600

REQUIREMENTS:= requirements.txt

install:
	@echo "Installing required packages..."
	${PIP} install --upgrade pip
	${PIP} install -r ${REQUIREMENTS}
	@echo "Packages installed successfully."

lint:
	@echo "Linting the code..."
	pylint -r n src

test:
	@echo "Running tests..."
	pytest tests/*

pre-commit:
	@echo "Running pre-commit hooks..."
	pre-commit run --all-files -v

pre-commit-update:
	@echo "Updating pre-commit hooks..."
	pre-commit autoupdate

run:
	@echo "Starting the application..."
	gunicorn --bind 0.0.0.0:${GUNICORN_PORT} main:app --worker-class uvicorn.workers.UvicornWorker --workers ${GUNICORN_WORKERS} --timeout ${GUNICORN_TIME_OUT}

# For Running GUNICORN Locally
# G_WORKERS ?=1
# MODULE = main:app
# GCP_PROJECT_ID = core-search-local
# app_deploy:
# 	GCP_PROJECT_ID=$(GCP_PROJECT_ID) gunicorn -w $(G_WORKERS) -k uvicorn.workers.UvicornWorker $(MODULE)

# app_uvi:
# 	GCP_PROJECT_ID=$(GCP_PROJECT_ID) uvicorn main:app --reload

.PHONY: install lint test pre-commit pre-commit-update run app_deploy app_uvi
