.PHONY: help up down build logs clean install migrate seed test lint format

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

up: ## Start all services
	docker compose up -d

down: ## Stop all services
	docker compose down

build: ## Build all services
	docker compose build

logs: ## Show logs from all services
	docker compose logs -f

clean: ## Remove all containers and volumes
	docker compose down -v --remove-orphans

install: ## Install dependencies for backend and frontend
	docker compose run --rm backend pip install -r requirements.txt
	docker compose run --rm frontend npm install

migrate: ## Run database migrations
	docker compose run --rm backend alembic upgrade head

seed: ## Seed the database with demo data
	docker compose run --rm backend python -m app.scripts.seed

test: ## Run tests
	docker compose run --rm backend pytest
	docker compose run --rm frontend npm test

lint: ## Run linting
	docker compose run --rm backend flake8
	docker compose run --rm frontend npm run lint

format: ## Format code
	docker compose run --rm backend black .
	docker compose run --rm frontend npm run format