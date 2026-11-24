#!/bin/bash
set -e

export GALAXY_CELERY_BROKER=memory://
export GALAXY_CELERY_BACKEND=cache+memory://
export GALAXY_CONFIG_DATABASE_CONNECTION="sqlite:////export/galaxy/universe.sqlite?isolation_level=IMMEDIATE"
export GALAXY_CONFIG_FILE="/etc/galaxy/galaxy.yml"

cd /galaxy

# Restore shed_tools from persistent volume to Galaxy's internal directory
# This is needed because tools are installed at build time and persisted to /export/galaxy/shed_tools/
SHED_TOOLS_SOURCE="/export/galaxy/shed_tools"
SHED_TOOLS_DEST="/galaxy/database/shed_tools"
if [ -d "$SHED_TOOLS_SOURCE" ] && [ -n "$(ls -A $SHED_TOOLS_SOURCE 2>/dev/null)" ]; then
    echo "Restoring shed tools from persistent volume..."
    mkdir -p "$SHED_TOOLS_DEST"
    cp -r "$SHED_TOOLS_SOURCE"/* "$SHED_TOOLS_DEST"/
    echo "Shed tools restored."
else
    echo "No shed tools found in persistent volume."
fi

# Check if database is already initialized (has workflow table)
DB_PATH="/export/galaxy/universe.sqlite"
DB_INITIALIZED=false
if [ -f "$DB_PATH" ]; then
    if /galaxy_venv/bin/python -c "import sqlite3; conn=sqlite3.connect('$DB_PATH'); c=conn.cursor(); c.execute(\"SELECT name FROM sqlite_master WHERE type='table' AND name='workflow'); print(len(c.fetchall()) > 0)" 2>/dev/null | grep -q True; then
        DB_INITIALIZED=true
    fi
fi

if [ "$DB_INITIALIZED" = false ]; then
    echo "Database not initialized. Running first-time setup..."

    # Initialize database
    echo "Initializing Galaxy database..."
    /galaxy_venv/bin/python scripts/db.py init

    # Run all migrations to completion
    echo "Running database upgrades to completion..."
    /galaxy_venv/bin/python /galaxy/upgrade_db.py
    echo "All database upgrades completed."

    # Start temporary Galaxy for tool installation
    echo "Starting Galaxy for tool installation..."
    /galaxy_venv/bin/gunicorn -b 127.0.0.1:8080 -w 1 --timeout 120 --access-logfile - --error-logfile - --pythonpath lib -k galaxy.webapps.galaxy.workers.Worker 'galaxy.webapps.galaxy.fast_factory:factory()' &
    GUNICORN_PID=$!
    sleep 45

    # Create admin user
    echo "Creating admin user..."
    /galaxy_venv/bin/python /usr/local/bin/create_galaxy_user.py --user "admin@example.org" --password "password" --username "admin" --key "fakekey"

    # Wait for Galaxy API
    echo "Waiting for Galaxy API..."
    for i in {1..30}; do curl -sf http://127.0.0.1:8080/api/version && break || sleep 2; done

    # Install Methylator tools from ToolShed
    echo "Installing Methylator tools from ToolShed..."
    for i in {1..3}; do /tool_deps/_conda/bin/shed-tools install -g "http://127.0.0.1:8080" -a "fakekey" -t /galaxy/tools.yaml && break || sleep 10; done
    /tool_deps/_conda/bin/conda clean --tarballs --yes > /dev/null
    echo "Tools installed."

    # Copy installed tools to persistent volume for future runs
    echo "Copying shed_tools to persistent volume..."
    mkdir -p /export/galaxy/shed_tools
    cp -r /galaxy/database/shed_tools/* /export/galaxy/shed_tools/
    echo "Tools persisted."

    # Import workflows
    echo "Importing workflows..."
    export GALAXY_URL="http://127.0.0.1:8080"
    /galaxy_venv/bin/python /galaxy/import_workflows.py || echo "Warning: Workflow import failed, will retry at runtime"
    echo "Workflows imported."

    # Stop temporary Galaxy
    echo "Stopping temporary Galaxy..."
    kill $GUNICORN_PID
    wait $GUNICORN_PID 2>/dev/null || true
    echo "First-time setup complete."
else
    echo "Database already initialized. Running migrations..."
    /galaxy_venv/bin/python /galaxy/upgrade_db.py
    echo "Database upgrades complete."
fi

# Start Galaxy
exec /galaxy_venv/bin/gunicorn -b 0.0.0.0:80 -w 2 --timeout 120 --access-logfile - --error-logfile - --pythonpath lib -k galaxy.webapps.galaxy.workers.Worker 'galaxy.webapps.galaxy.fast_factory:factory()'