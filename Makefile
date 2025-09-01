.PHONY: help build up down logs shell migrate makemigrations collectstatic test clean dev run stop restart local-dev local-migrate local-shell local-superuser local-reset

# Default target
help:
	@echo "EncoreHub Development Commands:"
	@echo ""
	@echo "🐳 Docker Commands:"
	@echo "  build          - Build Docker images"
	@echo "  up             - Start all services"
	@echo "  down           - Stop all services"
	@echo "  logs           - Show logs from all services"
	@echo "  shell          - Open Django shell in Docker"
	@echo "  migrate        - Run database migrations in Docker"
	@echo "  makemigrations - Create new migrations in Docker"
	@echo "  collectstatic  - Collect static files in Docker"
	@echo "  test           - Run tests in Docker"
	@echo "  superuser      - Create Django superuser in Docker"
	@echo "  reset-db       - Reset database in Docker (WARNING: deletes all data)"
	@echo ""
	@echo "💻 Local Development Commands:"
	@echo "  local-dev      - Start local development server"
	@echo "  local-migrate  - Run database migrations locally"
	@echo "  local-shell    - Open Django shell locally"
	@echo "  local-superuser- Create Django superuser locally"
	@echo "  local-reset    - Reset database locally (WARNING: deletes all data)"
	@echo ""
	@echo "🔄 Utility Commands:"
	@echo "  clean          - Clean up containers and volumes"
	@echo "  dev            - Full Docker development setup"
	@echo "  run            - Quick Docker start"
	@echo "  stop           - Stop Docker services"
	@echo "  restart        - Restart Docker services"

# =============================================================================
# Docker Commands
# =============================================================================

# Build Docker images
build:
	docker-compose build

# Start all services
up:
	docker-compose up -d

# Stop all services
down:
	docker-compose down

# Show logs
logs:
	docker-compose logs -f

# Open Django shell
shell:
	docker-compose exec web python manage.py shell

# Run migrations
migrate:
	docker-compose exec web python manage.py migrate

# Create migrations
makemigrations:
	docker-compose exec web python manage.py makemigrations

# Collect static files
collectstatic:
	docker-compose exec web python manage.py collectstatic --noinput

# Run tests
test:
	docker-compose exec web python manage.py test

# Create superuser
superuser:
	docker-compose exec web python manage.py createsuperuser

# Reset database (WARNING: deletes all data)
reset-db:
	docker-compose down -v
	docker-compose up -d db
	sleep 5
	docker-compose exec web python manage.py migrate
	docker-compose exec web python manage.py createsuperuser

# =============================================================================
# Local Development Commands
# =============================================================================

# Start local development server
local-dev:
	@echo "🚀 Starting local development server..."
	python3 manage.py runserver
	@echo "📱 EncoreHub is running at http://localhost:8000"
	@echo "📊 Admin interface: http://localhost:8000/admin"
	@echo "🛑 Press Ctrl+C to stop"

# Run database migrations locally
local-migrate:
	@echo "🔄 Running database migrations..."
	python3 manage.py migrate
	@echo "✅ Migrations completed!"

# Create migrations locally
local-makemigrations:
	@echo "📝 Creating new migrations..."
	python3 manage.py makemigrations
	@echo "✅ Migrations created!"

# Open Django shell locally
local-shell:
	@echo "🐍 Opening Django shell..."
	python3 manage.py shell

# Create Django superuser locally
local-superuser:
	@echo "👤 Creating Django superuser..."
	python3 manage.py createsuperuser

# Collect static files locally
local-collectstatic:
	@echo "📦 Collecting static files..."
	python3 manage.py collectstatic --noinput
	@echo "✅ Static files collected!"

# Reset database locally (WARNING: deletes all data)
local-reset:
	@echo "⚠️  WARNING: This will delete all data!"
	@echo "Are you sure? [y/N] " && read ans && [ $${ans:-N} = y ]
	rm -f db.sqlite3
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	@echo "🔄 Creating fresh database..."
	python3 manage.py makemigrations
	python3 manage.py migrate
	@echo "✅ Database reset complete!"

# =============================================================================
# Utility Commands
# =============================================================================

# Clean up everything
clean:
	docker-compose down -v
	docker system prune -f

# Development workflow with Docker Compose
dev:
	make build
	make up
	sleep 5
	make migrate
	@echo "🚀 EncoreHub is running at http://localhost:8000"
	@echo "📊 Admin interface: http://localhost:8000/admin"
	@echo "📝 Use 'make logs' to view logs"
	@echo "🔧 Use 'make shell' to open Django shell"
	@echo "🛑 Use 'make down' to stop services"

# Run with Docker Compose (simplified)
run:
	docker-compose up -d
	@echo "🚀 EncoreHub is running at http://localhost:8000"

# Stop Docker services
stop:
	docker-compose down
	@echo "🛑 Services stopped"

# Restart services
restart:
	make stop
	make run
	@echo "🔄 Services restarted"

# Quick start (build, up, migrate)
start:
	make build
	make up
	sleep 10
	make migrate
	@echo "EncoreHub is running at http://localhost:8000" 