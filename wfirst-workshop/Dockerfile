# Copyright (c) Association of Universities for Research in Astronomy
# Distributed under the terms of the Modified BSD License.

FROM jupyter/scipy-notebook:a238993ad594
# See https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html
# for a list of what comes with the base image
# python version is: 3.6.8

LABEL maintainer="Science Platforms <cbrasseur@stsci.edu>"

# Environment Variables
ENV MKL_THREADING_LAYER="GNU"
ENV PYTHON_VERSION 3.6
ENV PATH $HOME/bin:$PATH
ENV LD_LIBRARY_PATH $HOME/lib:$LD_LIBRARY_PATH
ENV WEBBPSF_VERSION 0.8.0
ENV PANDEIA_VERSION 1.2.2
ENV PYHOME /opt/conda
ENV pandeia_refdata /opt/pandeia_data-1.2.1_wfirst
ENV PYSYN_CDBS /opt/grp/hst/cdbs
ENV WEBBPSF_DATA_VERSION 0.8.0
ENV WEBBPSF_PATH /opt/webbpsf-data



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
RUN conda install -y astropy=2
RUN conda install -y mkl-service
RUN conda install -y plotly
RUN conda install -y pymc3
RUN conda install -y boto3
RUN conda install -y emcee
RUN conda install -y starry
RUN conda install -y ginga
RUN conda install -y bokeh
RUN conda install -y pyfftw
RUN conda install -y photutils
RUN conda install -y pysynphot  
RUN conda install -y future 
RUN conda install -y pyyaml 
RUN conda install -y pandas

# pip packages
RUN pip install ipywidgets==7.0.0
RUN pip install ipyevents
RUN pip install --pre astroquery --upgrade
RUN pip install exoplanet 
RUN pip install astrocut
RUN pip install eleanor
RUN pip install tele-scope
RUN pip install celerite
RUN pip install corner
RUN pip install bls.py
#RUN pip install galsim skip for right now


# Install Pandeia
RUN pip install --no-cache-dir pandeia.engine==$PANDEIA_VERSION

# Install WebbPSF
#RUN pip install --no-cache-dir webbpsf==$WEBBPSF_VERSION
RUN pip install git+git://github.com/spacetelescope/webbpsf.git@master
RUN pip install git+git://github.com/spacetelescope/poppy.git

# JupyterLab extensions
RUN jupyter nbextension enable --py --sys-prefix ipyevents
RUN jupyter labextension install jupyterlab_bokeh

# Get data
USER root
RUN mkdir -p /opt
RUN chown jovyan /opt

# Include STScI notebooks
RUN mkdir /opt/notebooks
RUN chmod 777 /opt/notebooks

USER jovyan
RUN git clone https://github.com/spacetelescope/notebooks.git /opt/notebooks


# include simulator data
USER jovyan
WORKDIR /opt
# Extract PySynphot reference data
RUN wget -qO- http://ssb.stsci.edu/cdbs/tarfiles/synphot1.tar.gz | tar xvz
RUN wget -qO- http://ssb.stsci.edu/cdbs/tarfiles/synphot2.tar.gz | tar xvz
RUN wget -qO- http://ssb.stsci.edu/cdbs/tarfiles/synphot5.tar.gz | tar xvz

# Extract Pandeia reference data
RUN wget -qO- http://ssb.stsci.edu/pandeia/engine/1.2.1/pandeia_wfirst_data-1.2.1.tar.gz | tar xvz

# Extract WebbPSF reference data
# (note: version number env vars are declared close to where they are used
# to prevent unnecessary rebuilds of the Docker image)
RUN wget -qO- http://www.stsci.edu/~mperrin/software/webbpsf/webbpsf-data-$WEBBPSF_DATA_VERSION.tar.gz | tar xvz

RUN git clone https://github.com/spacetelescope/wfirst-tools /opt/wfirst-tools

# README
COPY platform_readme.txt /opt/README

COPY VERSION /opt

USER root
RUN apt-get install -y libfftw3-3
USER jovyan
RUN conda install -c conda-forge galsim

