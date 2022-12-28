# Self-Documented Makefile see https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html

.DEFAULT_GOAL := help

##################################################################################
############# Docker commands ####################################################

build-dev: ## Build dev docker image
	docker build -f ./Dockerfile --tag web-app:dev .

dev-up: ## Start local containers
	docker-compose up --build  -d

dev-down: ## Stop local containers
	docker-compose down

exec: ## Exec within the container
	docker exec -it movies-app bash

restart: ## Restart the movies app container
	docker restart movies-app

logs: ## Web app logs
	docker logs movies-app

db-logs: ## Postgres db logs
	docker logs movies-db

##################################################################################
############### DJANGO Docker commands ###########################################

makemigrations: ## Run the django makemigrations within the running container
	docker-compose exec movies-app ./manage.py makemigrations

migrate: ## Run the django migrate command within the running container
	docker-compose exec movies-app ./manage.py migrate

test-docker:
	docker-compose exec movies-app pytest . -vv

shell_plus: ## Start django shell command within the running container
	docker-compose exec movies-app ./manage.py shell_plus

sample-movies-docker: ## Create sample movies within the running container
	docker-compose exec movies-app ./manage.py create_sample_movies

#########################################################################################
####################### Local  Setup ####################################################

create-env: ## Create python virtual env
	python -m venv .env && source .env/bin/activate && pip install --upgrade pip

poetry-env: create-env ## Create and install environment for local dev
	  source .env/bin/activate && poetry install

install-hooks: ## Install hooks
	pre-commit install

sample-movies: ## Create sample movies
	source .env/bin/activate && ./manage.py create_sample_movies

init-local-database:
	source .env/bin/activate && ./manage.py makemigrations && ./manage.py migrate

install-local:poetry-env install-hooks init-local-database sample-movies
		echo "🚀 Now you can start the local webserver"

test: ## Run locally pytest with coverage
	pytest -vv -p no:warnings --cov=.
	echo "🚀🚀"

check: ## Run isort black and pylint in all files
	isort .
	black .
	pylint --recursive=y movierama

.PHONY: help build-dev logs db-logs restart exec dev-up dev-up \
make-migrations migrate test test-docker shell_plus create-env install-local\
 sample-data-docker install-hooks init-local-database check

help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)