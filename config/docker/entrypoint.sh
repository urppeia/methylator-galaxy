#!/bin/bash
set -e

echo "Starting Galaxy..."

# Source the original entrypoint but keep it in background if needed
exec /sbin/docker-entrypoint.sh "$@" &

# Wait for Galaxy to fully start and become healthy
sleep 10
python3 /galaxy/import_workflows.py

# Keep container running
wait
