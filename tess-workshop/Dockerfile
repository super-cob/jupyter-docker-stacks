# Copyright (c) Association of Universities for Research in Astronomy
# Distributed under the terms of the Modified BSD License.

FROM jupyter/scipy-notebook:a238993ad594
# See https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html
# for a list of what comes with the base image
# python version is: 3.6.8

LABEL maintainer="Science Platforms <cbrasseur@stsci.edu>"

# Environment Variables
ENV MKL_THREADING_LAYER="GNU"

# Installing all the unix stuff
USER root
RUN apt-get update -y
RUN apt-get install -y --no-install-recommends apt-utils
RUN apt-get install gcc -y
RUN apt-get install vim -y
RUN apt-get install ssh -y
RUN apt-get install htop -y
RUN apt-get install sysstat -y
RUN apt-get install g++ -y
RUN apt-get install imagemagick -y
RUN apt-get install curl -y

RUN apt-get install libcurl4-openssl-dev -y
RUN apt-get install libxml2 -y
RUN apt-get install libxslt1.1 -y
RUN apt-get install libxml2-dev -y
RUN apt-get install libxslt1-dev -y
RUN apt-get install python-libxml2 -y
RUN apt-get install python-libxslt1 -y
RUN apt-get install python-dev -y
RUN apt-get install python-setuptools -y

RUN easy_install lxml

RUN apt-get install build-essential -y
USER jovyan


# Add astropy, astroconda, and conda-forge channels
RUN conda config --add channels astropy
RUN conda config --add channels http://ssb.stsci.edu/astroconda
RUN conda config --add channels conda-forge 


# Install conda packages
RUN conda update -y conda
RUN conda install -y numpy
RUN conda install -y astropy
RUN conda install -y mkl-service
RUN conda install -y plotly
RUN conda install -y pymc3
RUN conda install -y boto3
RUN conda install -y emcee
RUN conda install -y starry
RUN conda install -y ginga
RUN conda install -y bokeh

# pip packages
RUN pip install ipyevents
RUN pip install --pre astroquery --upgrade
RUN pip install exoplanet 
RUN pip install astrocut
RUN pip install eleanor
RUN pip install tele-scope
RUN pip install celerite

# JupyterLab extensions
RUN jupyter nbextension enable --py --sys-prefix ipyevents
RUN jupyter labextension install jupyterlab_bokeh

# Git repos
RUN cd /opt
RUN git clone https://github.com/spacetelescope/tessworkshop_tutorials.git 
RUN git clone https://github.com/spacetelescope/notebooks.git

# README
COPY platform_readme.txt /opt/README

COPY VERSION /opt
