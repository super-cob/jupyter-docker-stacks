# Copyright (c) Association of Universities for Research in Astronomy
# Distributed under the terms of the Modified BSD License.

FROM jupyter/scipy-notebook:a238993ad594
# See https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html
# for a list of what comes with the base image
# python version is: 3.6.8

LABEL maintainer="Science Platforms <cbrasseur@stsci.edu>"

# Environment Variables
ENV MKL_THREADING_LAYER="GNU"
ENV CRDS_PATH=/home/jovyan/crds_cache
ENV CRDS_SERVER_URL=https://jwst-crds.stsci.edu

# Keep Ubuntu secure
USER root
RUN apt-get update -y

# Additional apt packages
RUN apt-get install curl -y

USER jovyan

# Install jwst 0.13.7 and dependencies
RUN wget https://ssb.stsci.edu/releases/jwstdp/0.13.7/latest-linux
RUN conda install --file latest-linux
RUN rm latest-linux

# Additional pip packages
RUN pip install --upgrade --pre astroquery

# Tornado 6.x isn't compatible with Jupyter Notebook:
RUN pip uninstall -y tornado; pip install tornado==5.1.1

# Configure astroquery to use JWST A-string MAST server
RUN mkdir -p /home/jovyan/.astropy/config
COPY --chown=jovyan:users astroquery.cfg /home/jovyan/.astropy/config/

# README
COPY platform_readme.txt /opt/README

COPY VERSION /opt
