# Copyright (c) Association of Universities for Research in Astronomy
# Distributed under the terms of the Modified BSD License.
#FROM jupyter/base-notebook:latest
FROM jupyter/scipy-notebook:latest

LABEL maintainer="Science Platforms <cbrasseur@stsci.edu>"

# Installing all the unix stuff
USER root
RUN apt-get update -y
RUN apt-get install gcc -y
RUN apt-get install vim -y
RUN apt-get install emacs -y
RUN apt-get install ssh -y
RUN apt-get install htop -y
RUN apt-get install sysstat -y
RUN apt-get install g++ -y

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


# Add Astropy channel
RUN conda config --add channels astropy

# Add Astroconda channel
RUN conda config --add channels http://ssb.stsci.edu/astroconda

# Add conda-forge channel
RUN conda config --add channels conda-forge 

# Create 'tess_workshop' environment configured with required packages
#RUN conda create --name tess_workshop python=3.6 astropy mkl-service seaborn plotly scikit-learn pymc3 boto3 emcee matplotlib bokeh jupyter starry ipywidgets ginga -y

Run conda install astropy -y
RUN conda install --quiet --yes \
    'astropy' \
    'mkl-service' \
    'seaborn' \
    'plotly' \
    'scikit-learn' \
    'pymc3' \
    'boto3' \
    'emcee' \
    'matplotlib' \
    'bokeh' \
    'jupyter' \
    'starry' \
    'ipywidgets' \
    'ginga' 

# pip packages
RUN pip install ipyevents
RUN jupyter nbextension enable --py --sys-prefix ipyevents
RUN pip install --pre astroquery --upgrade
RUN pip install exoplanet
RUN pip install astrocut
RUN pip install eleanor

USER jovyan

RUN pip install tele-scope
RUN pip install celerite

COPY VERSION /opt
