.PHONY: help build up down restart logs clean

.DEFAULT_GOAL := help

help: ## Show this help message
	@echo "ReportFlow - Docker Management"
	@echo "==============================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-16s\033[0m %s\n", $$1, $$2}'

build: ## Build or rebuild application container images
	docker compose build

up: ## Start the entire ecosystem (App, Worker, Keycloak, Redis, DB)
	docker compose up -d

down: ## Stop and tear down all ecosystem containers
	docker compose down

restart: down up ## Restart all services

logs: ## Tail logs for all running services
	docker compose logs -f

logs-app: ## Tail logs only for FastAPI and Celery worker
	docker compose logs -f api worker

clean: ## Prune dangling Docker containers, volumes, and local cache
	docker compose down -v --remove-orphans
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf downloads/*.csv