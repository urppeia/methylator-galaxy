#!/bin/bash
# Script to install Methylator tools in a running Galaxy container

set -e

GALAXY_URL="${1:-http://localhost:8080}"
GALAXY_ADMIN_USER="${2:-admin}"
GALAXY_ADMIN_PASSWORD="${3:-password}"
CONTAINER_ID="${4:-}"

echo "Installing Methylator tools..."
echo "Galaxy URL: $GALAXY_URL"
echo "Admin user: $GALAXY_ADMIN_USER"

# If container ID provided, run inside container
if [ -n "$CONTAINER_ID" ]; then
    echo "Running install inside container $CONTAINER_ID..."
    docker exec "$CONTAINER_ID" bash -c "
        cd /galaxy
        export GALAXY_URL=$GALAXY_URL
        export GALAXY_ADMIN_USER=$GALAXY_ADMIN_USER
        export GALAXY_ADMIN_PASSWORD=$GALAXY_ADMIN_PASSWORD
        
        # Wait for Galaxy to be ready
        echo 'Waiting for Galaxy to be ready...'
        for i in {1..60}; do
            if curl -s \$GALAXY_URL/api/version > /dev/null 2>&1; then
                echo 'Galaxy is ready!'
                break
            fi
            echo 'Galaxy not ready yet, waiting... ('"\$i"'/60)'
            sleep 10
        done
        
        # Install tools
        install-tools /galaxy/tools.yaml
    "
else
    # Run locally
    echo "Running install locally..."
    export GALAXY_URL=$GALAXY_URL
    export GALAXY_ADMIN_USER=$GALAXY_ADMIN_USER
    export GALAXY_ADMIN_PASSWORD=$GALAXY_ADMIN_PASSWORD
    
    # Wait for Galaxy to be ready
    echo 'Waiting for Galaxy to be ready...'
    for i in {1..60}; do
        if curl -s $GALAXY_URL/api/version > /dev/null 2>&1; then
            echo 'Galaxy is ready!'
            break
        fi
        echo 'Galaxy not ready yet, waiting... ('$i'/60)'
        sleep 10
    done
    
    # Install tools
    install-tools /galaxy/tools.yaml
fi

echo "Tool installation complete!"
echo "Access Galaxy at: $GALAXY_URL"
