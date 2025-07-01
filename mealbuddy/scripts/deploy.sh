#!/bin/bash
set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}🚀 Starting MealBuddy deployment...${NC}"

# Load environment variables
if [ -f .env.prod ]; then
    echo -e "${GREEN}✓ Loading environment variables from .env.prod${NC}"
    export $(grep -v '^#' .env.prod | xargs)
else
    echo -e "${YELLOW}⚠️  .env.prod not found. Using default values.${NC}"
fi

# Ensure Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Build and start services
echo -e "${YELLOW}🚧 Building and starting services...${NC}"
docker-compose -f docker-compose.prod.yml up -d --build

# Run database migrations
echo -e "${YELLOW}🔄 Running database migrations...${NC}"
docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head

# Check if services are healthy
check_service() {
    local service=$1
    local port=$2
    local max_retries=30
    local retries=0
    
    echo -e "${YELLOW}⏳ Waiting for $service to be ready...${NC}"
    
    until nc -z localhost $port > /dev/null 2>&1; do
        if [ $retries -eq $max_retries ]; then
            echo -e "❌ $service is not available after $max_retries retries"
            exit 1
        fi
        
        retries=$((retries+1))
        sleep 2
    done
    
    echo -e "${GREEN}✓ $service is ready on port $port${NC}"
}

# Check if services are up
check_service "Backend" 8000
check_service "Frontend" 3000

# All done!
echo -e "${GREEN}🎉 Deployment completed successfully!${NC}"
echo -e "\nAccess your application at:"
echo -e "- Frontend: http://localhost:3000"
echo -e "- Backend API: http://localhost:8000"
echo -e "- API Documentation: http://localhost:8000/docs\n"

echo -e "${YELLOW}To view logs, run:${NC} docker-compose -f docker-compose.prod.yml logs -f"
echo -e "${YELLOW}To stop the application, run:${NC} docker-compose -f docker-compose.prod.yml down\n"
