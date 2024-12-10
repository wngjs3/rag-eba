#!/bin/bash

echo "🔄 Restarting development environment..."
./scripts/docker-stop.sh
./scripts/docker-start.sh 