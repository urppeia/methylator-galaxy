FROM quay.io/bgruening/galaxy:26.1

LABEL maintainer="Deepak K. Tanwar, dktanwar@hotmail.com"

ENV GALAXY_CONFIG_BRAND="Methylator" \
    GALAXY_ROOT="/galaxy" \
    GALAXY_HOME="/home/galaxy" \
    GALAXY_ENABLE_AGENTS="true"

WORKDIR ${GALAXY_ROOT}

# Add visualisations
RUN --mount=type=cache,target=/tmp \
    curl -sL https://github.com/bgruening/galaxytools/archive/master.tar.gz > /tmp/master.tar.gz && \
    tar -xf /tmp/master.tar.gz galaxytools-master/visualisations && \
    mkdir -p config/plugins/visualizations && \
    cp -r galaxytools-master/visualisations/dotplot/ config/plugins/visualizations/ || true && \
    cp -r galaxytools-master/visualisations/dbgraph/ config/plugins/visualizations/ || true && \
    rm -rf galaxytools-master

RUN mkdir -p ${GALAXY_HOME}/workflows

COPY ../config/methylator_tool_list.yaml ${GALAXY_ROOT}/tools.yaml
COPY ../scripts/install_methylator_tools.py ${GALAXY_ROOT}/
RUN chmod +x ${GALAXY_ROOT}/install_methylator_tools.py

COPY ../scripts/import_workflows.py ${GALAXY_ROOT}/
RUN chmod +x ${GALAXY_ROOT}/import_workflows.py

COPY ../workflows/ ${GALAXY_HOME}/workflows/
