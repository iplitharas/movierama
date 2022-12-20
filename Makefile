# Self-Documented Makefile see https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html

.DEFAULT_GOAL := help

############# Docker commands ####################
build-dev: ## Build dev docker image
	docker build -f ./Dockerfile --tag web-app:dev .

dev-up: ## Start local containers
	docker-compose up --build  -d

dev-down: ## Stop local containers
	docker-compose down
######################################################

############### DJANGO commands ######################
logs: ## web app logs
	docker logs movies-app

db-logs: ## db logs
	docker logs movies-db

make-migrations: ## Run the migrations
	docker-compose exec movies-app ./manage.py makemigrations

migrate: ## Apply the migrations
	docker-compose exec movies-app ./manage.py migrate

test:
	docker-compose exec movies-app pytest .

shell_plus:
	docker-compose exec movies-app ./manage.py shell_plus
#####################################################

.PHONY: help build-dev logs db-logs make-migrations migrate test python-sh

help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)