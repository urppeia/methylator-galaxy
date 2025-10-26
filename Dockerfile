FROM quay.io/bgruening/galaxy:24.1

MAINTAINER Deepak K. Tanwar, dktanwar@hotmail.com

ENV GALAXY_CONFIG_BRAND="Methylator"

# Adding the tool definitions to the container
ADD methylator_tool_list.yaml $GALAXY_ROOT/tools.yaml

# Install tools
RUN install-tools $GALAXY_ROOT/tools.yaml && \
    /tool_deps/_conda/bin/conda clean --tarballs --yes > /dev/null && \
    rm /export/galaxy-central/ -rf

RUN mkdir -p $GALAXY_HOME/workflows

# Add workflow
ADD ./workflows/* $GALAXY_HOME/workflows/

# Download training data and populate the data library
RUN startup_lite && \
    sleep 30 && \
    workflow-install --workflow_path $GALAXY_HOME/workflows/ -g http://localhost:8080 -u $GALAXY_DEFAULT_ADMIN_USER -p $GALAXY_DEFAULT_ADMIN_PASSWORD

# Add visualisations
RUN curl -sL https://github.com/bgruening/galaxytools/archive/master.tar.gz > master.tar.gz && \
    tar -xf master.tar.gz galaxytools-master/visualisations && \
    cp -r galaxytools-master/visualisations/dotplot/ config/plugins/visualizations/ && \
    cp -r galaxytools-master/visualisations/dbgraph/ config/plugins/visualizations/ && \
    rm -rf master.tar.gz rm galaxytools-master
# Container Style
#ADD assets/img/full_logo.png $GALAXY_CONFIG_DIR/web/welcome_image.png
#ADD welcome.html $GALAXY_CONFIG_DIR/web/welcome.html
