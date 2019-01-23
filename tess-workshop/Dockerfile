# Copyright (c) Association of Universities for Research in Astronomy
# Distributed under the terms of the Modified BSD License.
FROM jupyter/base-notebook:latest

LABEL maintainer="Science Platforms <cbrasseur@stsci.edu>"

# Install Astropy channel
RUN conda config --add channels astropy

# Install Astroconda channel
RUN conda config --add channels http://ssb.stsci.edu/astroconda

# Create 'tess_workshop' environment configured with required packages
RUN conda create --name tess_workshop python=3.6 astropy mkl-service seaborn plotly scikit-learn pymc3 boto3 emcee matplotlib bokeh -y

# ADD VERSION file but delete .devel off of the end
WORKDIR /home/jovyan
ADD README.md .
ADD VERSION .
RUN sed -i 's/\.devel//' ./VERSION
