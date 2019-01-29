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


# Activate the tess_workshop environment
RUN echo "source activate tess_workshop" > ~/.bashrc
ENV PATH /opt/conda/envs/tess_workshop/bin:$PATH

#RUN python --version
#RUN which python
#RUN conda env list

# Install ginga, ipywidgets and ipyevents for interactive plots
RUN conda install ginga -y
RUN conda install -c conda-forge ipywidgets -y
RUN pip install ipyevents
RUN jupyter nbextension enable --py --sys-prefix ipyevents

USER root
RUN apt-get update -y
RUN apt-get install gcc -y
RUN apt-get install vim -y
RUN apt-get install emacs -y
RUN apt-get install ssh -y
RUN apt-get install htop -y
RUN apt-get install sysstat -y
RUN apt-get install g++ -y
#RUN apt-get install curl -y

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

# pip packages
RUN pip install --pre astroquery --upgrade
RUN pip install exoplanet
RUN pip install tele-scope
RUN pip install celerite
RUN pip install astrocut
RUN pip install eleanor
#RUN pip install starry -v


COPY VERSION /opt
