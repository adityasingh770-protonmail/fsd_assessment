#!/bin/bash
# Initialize Docker setup for Movie Explorer Platform

set -e

echo "=========================================="
echo "Movie Explorer Platform - Docker Setup"
echo "=========================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✓ Docker and Docker Compose are installed"
echo ""

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from .env.docker.example..."
    cp .env.docker.example .env
    echo "✓ .env file created"
    echo "⚠ Please update .env with your configuration"
else
    echo "✓ .env file already exists"
fi

echo ""
echo "Building Docker images..."
docker-compose build

echo ""
echo "Starting services..."
docker-compose up -d

echo ""
echo "Waiting for services to be healthy..."
sleep 10

# Check if database is ready
echo "Checking database connection..."
docker-compose exec -T db pg_isready -U postgres

echo ""
echo "Initializing database..."
docker-compose exec -T backend python init_db.py

echo ""
echo "Seeding database with sample data..."
docker-compose exec -T backend python seed_data.py

echo ""
echo "=========================================="
echo "✓ Setup Complete!"
echo "=========================================="
echo ""
echo "Services:"
echo "  Frontend: http://localhost:3000"
echo "  Backend:  http://localhost:5000"
echo "  API Docs: http://localhost:5000/api/docs"
echo "  Health:   http://localhost:5000/health"
echo ""
echo "Useful commands:"
echo "  docker-compose logs -f              # View logs"
echo "  docker-compose ps                   # View running services"
echo "  docker-compose down                 # Stop services"
echo "  docker-compose down -v              # Stop and remove volumes"
echo "  docker-compose restart backend      # Restart backend"
echo ""