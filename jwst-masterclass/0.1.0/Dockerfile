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

ENV pandeia_refdata=/data/pandeia
ENV WEBBPSF_PATH=/data/webbpsf
ENV PYSYN_CDBS=/data/pysynphot
ENV MIRAGE_DATA=/data/mirage
ENV MIRISIM_ROOT=/data/mirisim

USER root

RUN apt-get update --yes > /dev/null && \
    apt-get install --yes curl && \
    rm -rf /var/lib/apt/lists/*

# Install jwst and dependencies
#####################################################################
RUN . $CONDA_DIR/etc/profile.d/conda.sh &&\
    conda create -n jwst-masterclass python=3.6.8 &&\
    conda activate jwst-masterclass &&\

    pip install git+https://github.com/spacetelescope/jwst --no-cache-dir &&\

    # We need the pre-release version of astroquery in order to make requests of
    # JWST A-string MAST.
    pip install --upgrade --pre astroquery --no-cache-dir &&\

    # install the latest of astropy
    pip install git+https://github.com/astropy/astropy.git &&\

    # The aws-cli is used by CRDS to cache files
    pip install --upgrade awscli --no-cache-dir &&\

    # The example notebook would like to do some plotting
    pip install matplotlib --no-cache-dir &&\

    pip install pytest --no-cache-dir &&\

    # S3-enabled release of CRDS:
    pip install --upgrade git+https://github.com/spacetelescope/crds.git@7.4.1#egg=crds[aws] --no-cache-dir &&\

    # GTVT and MTVT
    pip install git+https://github.com/spacetelescope/jwst_gtvt.git --no-cache-dir &&\

    pip install webbpsf --no-cache-dir &&\

    # Pandeia engine
    pip install pandeia.engine --no-cache-dir &&\

    pip install git+https://github.com/spacetelescope/pysynphot.git -no-cache-dir &&\

    #pip install git+https://github.com/spacetelescope/pandeia-coronagraphy.git --no-cache-dir &&\

    pip install pysiaf --no-cache-dir &&\

    # MIRAGE
    pip install git+https://github.com/spacetelescope/mirage.git --no-cache-dir &&\
    
    pip install ipykernel --no-cache-dir
#####################################################################

# Setup a notebook start hook that populates the home directory.  We do this in a roundabout
# way because the EFS mount isn't available until the server actually starts in the cluster.
RUN mkdir -p /usr/local/bin/start-notebook.d
COPY apply_home_template.sh /usr/local/bin/start-notebook.d
COPY home_template /opt/home_template

# Add content to the global bashrc
COPY global_bashrc /home/jovyan
RUN cat /home/jovyan/global_bashrc >> /etc/bash.bashrc &&\
    rm /home/jovyan/global_bashrc


# Add kernel runner script that ensures conda environment is activated
COPY kernel_runner.py /opt

# Create kernel for jwst-masterclass environment
RUN mkdir -p /usr/local/share/jupyter/kernels/jwst-masterclass
COPY kernel.jwst-masterclass.json /usr/local/share/jupyter/kernels/jwst-masterclass/kernel.json
COPY logo-32x32.png /usr/local/share/jupyter/kernels/jwst-masterclass
COPY logo-64x64.png /usr/local/share/jupyter/kernels/jwst-masterclass

# Clean out the home directory so it mimics a fresh EFS mount (useful for developer testing)
RUN rm -rf /home/jovyan/*
RUN rm -r /home/jovyan/.[a-zA-Z_]*

COPY VERSION /opt

USER $NB_UID

