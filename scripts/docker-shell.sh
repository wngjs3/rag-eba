#!/bin/bash

echo "🐚 Connecting to development container shell..."
docker-compose -f docker-compose.dev.yml exec dev bash 