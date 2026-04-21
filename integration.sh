#!/bin/bash
set -e
echo "Starting Integration Tests..."
# Wait for services to be ready
sleep 15
# Check Frontend
curl -f http://localhost:3000 || exit 1
# Check API
curl -f http://localhost:8000/health || exit 1
echo "All services are up!"
