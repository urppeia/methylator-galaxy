FROM quay.io/bgruening/galaxy:26.1

LABEL maintainer="Deepak K. Tanwar, dktanwar@hotmail.com"

ENV GALAXY_CONFIG_BRAND="Methylator" \
    GALAXY_ROOT="/galaxy" \
    GALAXY_HOME="/home/galaxy" \
    GALAXY_ENABLE_AGENTS="true"

# Set working directory for clarity
WORKDIR ${GALAXY_ROOT}

# Install Galaxy MCP Server for AI agent integration
RUN --mount=type=cache,target=/root/.cache/pip \
    python3 -m pip install --upgrade pip && \
    python3 -m pip install galaxy-mcp bioblend

# Add visualisations (less frequently changed than configs)
RUN --mount=type=cache,target=/tmp \
    curl -sL https://github.com/bgruening/galaxytools/archive/master.tar.gz > /tmp/master.tar.gz && \
    tar -xf /tmp/master.tar.gz galaxytools-master/visualisations && \
    mkdir -p config/plugins/visualizations && \
    cp -r galaxytools-master/visualisations/dotplot/ config/plugins/visualizations/ || true && \
    cp -r galaxytools-master/visualisations/dbgraph/ config/plugins/visualizations/ || true && \
    rm -rf galaxytools-master

# Setup workflow directory (directory creation is cheap, do early)
RUN mkdir -p ${GALAXY_HOME}/workflows

# Add tool definitions and scripts (more frequently changed, added after stable layers)
COPY ../config/methylator_tool_list.yaml ${GALAXY_ROOT}/tools.yaml
COPY ../scripts/install_methylator_tools.py ${GALAXY_ROOT}/
RUN chmod +x ${GALAXY_ROOT}/install_methylator_tools.py

# Add workflow files (frequently changed, added last)
COPY ../workflows/ ${GALAXY_HOME}/workflows/

# Note: Tools will be installed after container startup.
# Use the install_methylator_tools.py script or run install-tools manually.
# See ../README.md for instructions.

# Container Style
#COPY ../assets/img/full_logo.png $GALAXY_CONFIG_DIR/web/welcome_image.png
#COPY ../welcome.html $GALAXY_CONFIG_DIR/web/welcome.html
