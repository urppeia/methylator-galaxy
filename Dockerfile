FROM quay.io/bgruening/galaxy:24.1

LABEL maintainer="Deepak K. Tanwar, dktanwar@hotmail.com"

ENV GALAXY_CONFIG_BRAND="Methylator" \
    GALAXY_ROOT="/galaxy" \
    GALAXY_HOME="/home/galaxy"

# Adding the tool definitions to the container
ADD methylator_tool_list.yaml ${GALAXY_ROOT}/tools.yaml

# Note: Tools will be installed when the container is first run.
# The Galaxy instance needs to be running for tool installation.
# Users can install tools after container startup by running:
# docker exec <container_id> install-tools /galaxy/tools.yaml

RUN mkdir -p $GALAXY_HOME/workflows

# Add workflow files
ADD ./workflows/ $GALAXY_HOME/workflows/

# Add visualisations
RUN curl -sL https://github.com/bgruening/galaxytools/archive/master.tar.gz > master.tar.gz && \
    tar -xf master.tar.gz galaxytools-master/visualisations && \
    mkdir -p config/plugins/visualizations && \
    cp -r galaxytools-master/visualisations/dotplot/ config/plugins/visualizations/ || true && \
    cp -r galaxytools-master/visualisations/dbgraph/ config/plugins/visualizations/ || true && \
    rm -rf master.tar.gz galaxytools-master

# Container Style
#ADD assets/img/full_logo.png $GALAXY_CONFIG_DIR/web/welcome_image.png
#ADD welcome.html $GALAXY_CONFIG_DIR/web/welcome.html
