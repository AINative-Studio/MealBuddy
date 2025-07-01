.PHONY: up down build rebuild logs backend frontend db migrate test

# Start all services
dev: up

# Start all services in detached mode
up:
	docker-compose up -d

# Stop all services
down:
	docker-compose down

# Build all services
build:
	docker-compose build

# Rebuild all services
rebuild:
	docker-compose build --no-cache

dev-rebuild: down rebuild up

# View logs for all services
logs:
	docker-compose logs -f

# Access backend container
backend:
	docker-compose exec backend bash

# Access frontend container
frontend:
	docker-compose exec frontend sh

# Access database
# Example: make db-command command="\dt"
db-command:
	docker-compose exec db psql -U postgres -d mealbuddy_dev -c $(command)

db:
	docker-compose exec db psql -U postgres -d mealbuddy_dev

# Run database migrations
migrate:
	docker-compose exec backend alembic upgrade head

# Run tests
test:
	docker-compose exec backend pytest

# Format code
format:
	docker-compose exec backend black .
	docker-compose exec backend isort .
	docker-compose exec frontend npm run format

# Lint code
lint:
	docker-compose exec backend black --check .
	docker-compose exec backend isort --check-only .
	docker-compose exec backend mypy .
	docker-compose exec frontend npm run lint

# Install frontend dependencies
frontend-install:
	docker-compose exec frontend npm install

# Install backend dependencies
backend-install:
	docker-compose exec backend pip install -r requirements.txt

# Initialize the database
init-db:
	docker-compose up -d db
	@echo "Waiting for database to be ready..."
	@until docker-compose exec db pg_isready -U postgres > /dev/null; do \
		sleep 1; \
	done
	docker-compose exec backend python scripts/init_db.py

# Reset the database (WARNING: This will delete all data!)
reset-db: down
	docker volume rm -f mealbuddy_postgres_data
	make init-db

# Clean up all containers and volumes
clean: down
	docker-compose down -v --remove-orphans
	docker system prune -f

# Show help
help:
	@echo "Available commands:"
	@echo "  make up          - Start all services"
	@echo "  make down        - Stop all services"
	@echo "  make build       - Build all services"
	@echo "  make rebuild     - Rebuild all services"
	@echo "  make dev-rebuild - Rebuild and restart all services"
	@echo "  make logs        - View logs for all services"
	@echo "  make backend     - Access backend container"
	@echo "  make frontend    - Access frontend container"
	@echo "  make db          - Access database"
	@echo "  make migrate     - Run database migrations"
	@echo "  make test        - Run tests"
	@echo "  make format      - Format code"
	@echo "  make lint        - Lint code"
	@echo "  make init-db     - Initialize the database"
	@echo "  make reset-db    - Reset the database (WARNING: deletes all data!)"
	@echo "  make clean       - Clean up all containers and volumes"
