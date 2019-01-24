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
# RUN ["/bin/bash", "-c", "source activate tess_workshop"]
RUN echo $0
RUN . /opt/conda/etc/profile.d/conda.sh
RUN source activate tess_workshop

RUN python --version
RUN which python
RUN conda env list

# Install ipykernel switcher
# RUN python -m ipykernel install --user \
#     --name tess_workshop \
#     --display-name "Python (tess_workshop)"

# Install ginga, ipywidgets and ipyevents for interactive plots
RUN conda install ginga -y

RUN conda install -c conda-forge ipywidgets -y

RUN pip install ipyevents

RUN jupyter nbextension enable --py --sys-prefix ipyevents

USER root
# RUN apt-get install software-properties-common
# RUN add-apt-repository ppa:ubuntu-toolchain-r/test -y
RUN apt-get update -y
RUN apt-get install gcc -y
RUN apt-get install vim -y
RUN apt-get install emacs -y
RUN apt-get install ssh -y
RUN apt-get install htop -y
RUN apt-get install sysstat -y
RUN apt-get install g++ -y
USER jovyan

# pip packages
RUN pip install --pre astroquery --upgrade
# RUN pip install starry
RUN pip install exoplanet
run python --version
RUN pip install eleanor
RUN pip install tele-scope
RUN pip install celerite
RUN pip install astrocut

RUN conda install -c conda-forge starry -y

# JupyterLab extentions
RUN jupyter labextension install jupyterlab_bokeh

COPY VERSION /home/jovyan
