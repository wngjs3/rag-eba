#!/bin/bash

echo "🚀 Starting development environment..."
docker-compose -f docker-compose.dev.yml up -d
echo "✅ Development environment is running"
echo "💡 To check logs: ./scripts/docker-logs.sh" 