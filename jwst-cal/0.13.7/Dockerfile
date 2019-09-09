# Copyright (c) Association of Universities for Research in Astronomy
# Distributed under the terms of the Modified BSD License.

FROM jupyter/scipy-notebook:a238993ad594
# See https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html
# for a list of what comes with the base image
# python version is: 3.6.8

LABEL maintainer="Science Platforms <cbrasseur@stsci.edu>"

# Environment variables
ENV MKL_THREADING_LAYER="GNU"

# CRDS environment variables
ENV CRDS_PATH=/home/jovyan/crds_cache
ENV CRDS_SERVER_URL=https://jwst-serverless.stsci.edu
ENV CRDS_S3_ENABLED=1
ENV CRDS_S3_RETURN_URI=0
ENV CRDS_MAPPING_URI=s3://dmd-test-crds/mappings/jwst
ENV CRDS_REFERENCE_URI=s3://dmd-test-crds/references/jwst
ENV CRDS_CONFIG_URI=s3://dmd-test-crds/config/jwst
ENV CRDS_USE_PICKLES=0
ENV CRDS_DOWNLOAD_MODE=plugin
ENV CRDS_DOWNLOAD_PLUGIN='crds_s3_get ${SOURCE_URL} ${OUTPUT_PATH} ${FILE_SIZE} ${FILE_SHA1SUM}'
ENV CRDS_CONTEXT=jwst_0535.pmap

# Keep Ubuntu secure
USER root
RUN apt-get update -y

# Additional apt packages
RUN apt-get install curl -y

# Setup the notebook start hooks directory
RUN mkdir -p /usr/local/bin/start-notebook.d

# Configure astroquery to use JWST A-string MAST server.  We can't
# just copy an astroquery.cfg to the jovyan user's home directory
# because that directory isn't mounted until the container is
# launched by Kubernetes.
COPY create_astroquery_cfg.sh /usr/local/bin/start-notebook.d/

# Copy the example notebooks to the user's home directory, if missing.
COPY example_notebooks /opt/example_notebooks
COPY create_example_notebooks.sh /usr/local/bin/start-notebook.d/

USER jovyan

# Install jwst 0.13.7 and dependencies
RUN wget https://ssb.stsci.edu/releases/jwstdp/0.13.7/latest-linux
RUN conda install --file latest-linux
RUN rm latest-linux

# latest-linux specifies astropy 4.0.0.dev13236, but we actually need 3.2.1
RUN pip uninstall -y astropy; pip install astropy==3.2.1

# Additional pip packages
RUN pip install --upgrade --pre astroquery
RUN pip install --upgrade awscli

# S3-enabled release of CRDS:
RUN pip install --upgrade git+https://github.com/spacetelescope/crds.git@7.4.1#egg=crds[aws]

# Tornado 6.x isn't compatible with Jupyter Notebook:
RUN pip uninstall -y tornado; pip install tornado==5.1.1

# README
COPY platform_readme.txt /opt/README

COPY VERSION /opt
