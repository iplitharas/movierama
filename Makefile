# Self-Documented Makefile see https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html

.DEFAULT_GOAL := help

start-local: ## Start django server
	./manage.py runserver

dev-up: ## Start local containers
	docker-compose up -d

dev-down: ## Stop local containers
	docker-compose down

build-dev: ## Build dev docker image
	docker build -f ./Dockerfile --tag web-app:dev .

.PHONY: help start-local build-dev

help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)