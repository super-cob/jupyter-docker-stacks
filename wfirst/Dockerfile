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
ENV PYHOME /opt/conda
ENV pandeia_refdata /opt/pandeia_data-1.2.1_wfirst
ENV WEBBPSF_PATH /data/webbpsf
ENV PYSYN_CDBS /data/pysynphot
ENV MIRISIM_ROOT /data/mirisim
ENV MIRAGE_DATA /data/mirage

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

# Installing all the unix stuff
USER root

RUN apt-get update -y
RUN apt-get install -y --no-install-recommends apt-utils
RUN apt-get install -y gcc vim ssh htop sysstat g++ imagemagick curl \
    libcurl4-openssl-dev libxml2 libxslt1.1 libxml2-dev libxslt1-dev \
    python-libxml2 python-libxslt1 python-dev python-setuptools \
    build-essential libfftw3-3 rsync

RUN easy_install lxml

USER jovyan

# Install WFIRST packages into the base environment
COPY base-environment.yml /tmp
RUN conda env update --name base --file /tmp/base-environment.yml

# Install JWST cal code
COPY jwst-cal-environment.yml /tmp

RUN . $CONDA_DIR/etc/profile.d/conda.sh && \
    conda env create -f /tmp/jwst-cal-environment.yml

# Install MIRISim
COPY miricle-linux-py35.0.txt /tmp

RUN . $CONDA_DIR/etc/profile.d/conda.sh && \
    conda create --yes --name mirisim --file /tmp/miricle-linux-py35.0.txt && \
    conda activate mirisim && \
    pip install --upgrade git+https://github.com/spacetelescope/crds.git@7.4.1.2#egg=crds[aws] && \
    pip install ipykernel

# Install MIRaGe
COPY mirage-environment.yml /tmp

RUN . $CONDA_DIR/etc/profile.d/conda.sh && \
    conda env create -f /tmp/mirage-environment.yml

# JupyterLab extensions
RUN jupyter nbextension enable --py --sys-prefix ipyevents
RUN jupyter labextension install jupyterlab_bokeh

# Get data
USER root

# Add kernel runner script that ensures conda environment is activated
COPY kernel_runner.py /opt

# Create kernel for jwst-cal environment
RUN mkdir -p /usr/local/share/jupyter/kernels/jwst-cal
COPY kernel.jwst-cal.json /usr/local/share/jupyter/kernels/jwst-cal/kernel.json
COPY logo-32x32.png /usr/local/share/jupyter/kernels/jwst-cal
COPY logo-64x64.png /usr/local/share/jupyter/kernels/jwst-cal

# Create kernel for mirisim environment
RUN mkdir -p /usr/local/share/jupyter/kernels/mirisim
COPY kernel.mirisim.json /usr/local/share/jupyter/kernels/mirisim/kernel.json
COPY logo-32x32.png /usr/local/share/jupyter/kernels/mirisim
COPY logo-64x64.png /usr/local/share/jupyter/kernels/mirisim

# Create kernel for mirage environment
RUN mkdir -p /usr/local/share/jupyter/kernels/mirage
COPY kernel.mirage.json /usr/local/share/jupyter/kernels/mirage/kernel.json
COPY logo-32x32.png /usr/local/share/jupyter/kernels/mirage
COPY logo-64x64.png /usr/local/share/jupyter/kernels/mirage

# Setup a notebook start hook that populates the home directory.  We do this in a roundabout
# way because the EFS mount isn't available until the server actually starts in the cluster.
RUN mkdir -p /usr/local/bin/start-notebook.d
COPY apply_home_template.sh /usr/local/bin/start-notebook.d
COPY home_template /opt/home_template
RUN git clone https://github.com/spacetelescope/notebooks.git /opt/home_template/notebooks
RUN git clone https://github.com/spacetelescope/wfirst-tools /opt/home_template/wfirst-tools

# Extract Pandeia reference data
RUN wget -qO- http://ssb.stsci.edu/pandeia/engine/1.2.1/pandeia_wfirst_data-1.2.1.tar.gz | tar xvz -C /opt

COPY VERSION /opt

USER jovyan



