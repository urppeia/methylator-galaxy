FROM quay.io/bgruening/galaxy:26.1

LABEL maintainer="Deepak K. Tanwar, dktanwar@hotmail.com"

ENV GALAXY_CONFIG_BRAND="Methylator" \
    GALAXY_ENABLE_AGENTS="true" \
    GALAXY_CONFIG_DATABASE_CONNECTION="sqlite:////export/galaxy/universe.sqlite?isolation_level=IMMEDIATE" \
    GALAXY_CONFIG_FILE_PATH="/export/galaxy/files" \
    GALAXY_CONFIG_NEW_FILE_PATH="/export/galaxy/tmp" \
    GALAXY_CONFIG_TOOL_DATA_PATH="/export/galaxy/tool_data" \
    GALAXY_CONFIG_SHED_TOOL_DATA_PATH="/export/galaxy/shed_tool_data" \
    GALAXY_CONFIG_JOB_WORKING_DIRECTORY="/export/galaxy/job_working_directory" \
    GALAXY_CONFIG_GALAXY_INFRASTRUCTURE_URL="http://localhost:8080" \
    GALAXY_CONFIG_INTERACTIVETOOLS_ENABLE="true" \
    GALAXY_CELERY_BROKER="memory://" \
    GALAXY_CELERY_BACKEND="cache+memory://" \
    NONUSE="postgres,rabbitmq,celery" \
    GALAXY_HANDLER_NUMPROCS="0"

# Install mercurial for ToolShed repository cloning
RUN apt-get update && apt-get install -y mercurial && rm -rf /var/lib/apt/lists/*

WORKDIR /galaxy

# Add visualisations
RUN --mount=type=cache,target=/tmp \
    curl -sL https://github.com/bgruening/galaxytools/archive/master.tar.gz > /tmp/master.tar.gz && \
    tar -xf /tmp/master.tar.gz galaxytools-master/visualisations && \
    mkdir -p config/plugins/visualizations && \
    cp -r galaxytools-master/visualisations/dotplot/ config/plugins/visualizations/ || true && \
    cp -r galaxytools-master/visualisations/dbgraph/ config/plugins/visualizations/ || true && \
    rm -rf galaxytools-master

# Add workflows directory
RUN mkdir -p /home/galaxy/workflows
COPY ../workflows/ /home/galaxy/workflows/

# Copy tool list and import script
COPY ../config/methylator_tool_list.yaml /galaxy/tools.yaml
COPY ../scripts/import_workflows.py /galaxy/import_workflows.py
COPY ../scripts/upgrade_db.py /galaxy/upgrade_db.py

# Create database directory
RUN mkdir -p /export/galaxy

# Create Galaxy config with SQLite (must exist before build-time setup)
RUN mkdir -p /etc/galaxy && \
    printf "galaxy:\n  database_connection: \"sqlite:////export/galaxy/universe.sqlite?isolation_level=IMMEDIATE\"\n  file_path: /export/galaxy/files\n  new_file_path: /export/galaxy/tmp\n  tool_data_path: /export/galaxy/tool_data\n  shed_tool_data_path: /export/galaxy/shed_tool_data\n  shed_tools_dir: /export/galaxy/shed_tools\n  shed_tool_config_file: /etc/galaxy/shed_tool_conf.xml\n  job_working_directory: /export/galaxy/job_working_directory\n  galaxy_infrastructure_url: http://localhost:8080\n  interactivetools_enable: true\n  static_enabled: true\n" > /etc/galaxy/galaxy.yml

# Build-time: Initialize database and install tools
RUN export GALAXY_CONFIG_DATABASE_CONNECTION="sqlite:////export/galaxy/universe.sqlite?isolation_level=IMMEDIATE" && \
    echo "Initializing Galaxy database..." && \
    cd /galaxy && /galaxy_venv/bin/python scripts/db.py init && \
    echo "Running database upgrades to completion..." && \
    /galaxy_venv/bin/python /galaxy/upgrade_db.py && \
    echo "All database upgrades completed." && \
    echo "Starting Galaxy for tool installation..." && \
    /galaxy_venv/bin/gunicorn -b 127.0.0.1:8080 -w 1 --timeout 120 --access-logfile - --error-logfile - --pythonpath lib -k galaxy.webapps.galaxy.workers.Worker 'galaxy.webapps.galaxy.fast_factory:factory()' & \
    GUNICORN_PID=$! && \
    sleep 45 && \
    echo "Creating admin user..." && \
    /galaxy_venv/bin/python /usr/local/bin/create_galaxy_user.py --user "admin@example.org" --password "password" -c "/etc/galaxy/galaxy.yml" --username "admin" --key "fakekey" && \
    echo "Waiting for Galaxy API..." && \
    for i in {1..30}; do curl -sf http://127.0.0.1:8080/api/version && break || sleep 2; done && \
    echo "Installing Methylator tools from ToolShed..." && \
    for i in {1..3}; do /tool_deps/_conda/bin/shed-tools install -g "http://127.0.0.1:8080" -a "fakekey" -t /galaxy/tools.yaml && break || sleep 10; done && \
    /tool_deps/_conda/bin/conda clean --tarballs --yes > /dev/null && \
    echo "Tools installed." && \
    echo "Copying shed_tools to persistent volume..." && \
    mkdir -p /export/galaxy/shed_tools && \
    cp -r /galaxy/database/shed_tools/* /export/galaxy/shed_tools/ && \
    echo "Importing workflows..." && \
    /galaxy_venv/bin/python /galaxy/import_workflows.py && \
    echo "Workflows imported." && \
    echo "Stopping temporary Galaxy..." && \
    kill $GUNICORN_PID && \
    wait $GUNICORN_PID 2>/dev/null || true && \
    echo "Build-time setup complete."

# Create welcome.html from sample
RUN cp /galaxy/static/welcome.sample.html /galaxy/static/welcome.html

# Create shed_tool_conf.xml for ToolShed tools
RUN printf '<?xml version="1.0"?>\n<toolbox tool_path="/export/galaxy/shed_tools">\n</toolbox>\n' > /etc/galaxy/shed_tool_conf.xml

# Runtime entrypoint - bypass gravity, start gunicorn directly
COPY config/docker/methylator-entrypoint.sh /usr/local/bin/methylator-entrypoint.sh
RUN chmod +x /usr/local/bin/methylator-entrypoint.sh

ENTRYPOINT ["/usr/local/bin/methylator-entrypoint.sh"]
CMD []