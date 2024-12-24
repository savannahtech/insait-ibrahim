# Makefile for Docker Commands

# Set your service names
APP_NAME = flask-app
DB_NAME = db

# Command to build the Docker image
build:
	docker compose -f docker-compose.yml build

# Command to run the container
run:
	docker compose -f docker-compose.yml up --no-build --abort-on-container-exit --remove-orphans

# Build and run the containers at once
build-run:
	docker compose -f docker-compose.yml up --build

# Command to run tests inside the container
test:
	docker-compose exec flask-app pytest

# Stop the containers
down:
	docker compose -f docker-compose.yml down --remove-orphans

# Run migrations inside the Docker container
migrate:
	docker-compose exec flask-app alembic upgrade head

# Create migrations inside the Docker container
create-migrations:
	docker-compose exec flask-app alembic revision --autogenerate -m "Initial migration"


