#!/bin/bash

echo "📋 Showing development environment logs..."
docker-compose -f docker-compose.dev.yml logs -f 