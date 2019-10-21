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

USER root

# Keep Ubuntu secure
RUN apt-get update -y

# Additional apt packages
RUN apt-get install curl -y

# Install jwst 0.13.7 and dependencies
#####################################################################
RUN . $CONDA_DIR/etc/profile.d/conda.sh &&\
    conda create -n jwst-cal python=3.6.8 &&\
    conda activate jwst-cal &&\
    pip install --upgrade numpy &&\
    # Installing from the 0.13.7 tag instead of the official conda package list, since
    # as of 2019-09-20 the package list has a dependency conflict and can't be installed:
    pip install git+https://github.com/spacetelescope/jwst#0.13.7 &&\
    # We need the pre-release version of astroquery in order to make requests of
    # JWST A-string MAST.
    pip install --upgrade --pre astroquery &&\
    # The aws-cli is used by CRDS to cache files
    pip install --upgrade awscli &&\
    # The example notebook would like to do some plotting
    pip install matplotlib &&\
    # Needed because one of the 0.13.7 dependencies accidentally imported it in non-test code
    # (this issue has been fixed, we're only seeing it because we pinned an old version)
    pip install pytest &&\
    # S3-enabled release of CRDS:
    pip install --upgrade git+https://github.com/spacetelescope/crds.git@7.4.1#egg=crds[aws] &&\
    pip install ipykernel
#####################################################################

# As of 2019-10-21, MIRISim does not install due to astroconda-dev being deprecated.
# # Install MIRISim
# #####################################################################
# ENV MIRISIM_ROOT=/opt/mirisim
# ENV PYSYN_CDBS=$MIRISIM_ROOT/cdbs/

# RUN mkdir -p $MIRISIM_ROOT

# RUN . $CONDA_DIR/etc/profile.d/conda.sh &&\
#     wget http://miri.ster.kuleuven.be/pub/Public/MirisimInstallation/mirisim_install.bash &&\
#     chmod +x mirisim_install.bash &&\
#     # Version 9 corresponds to MIRISim 2.1.0, which is set up with the same reference
#     # files as jwst 0.13.7.
#     ./mirisim_install.bash --version 9 --path $MIRISIM_ROOT &&\
#     rm mirisim_install.bash &&\
#     conda activate mirisim &&\
#     pip install ipykernel
# #####################################################################

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

# Create kernel for jwst-cal environment
RUN mkdir -p /usr/local/share/jupyter/kernels/jwst-cal
COPY kernel.jwst-cal.json /usr/local/share/jupyter/kernels/jwst-cal/kernel.json
COPY logo-32x32.png /usr/local/share/jupyter/kernels/jwst-cal
COPY logo-64x64.png /usr/local/share/jupyter/kernels/jwst-cal

# As of 2019-10-21, MIRISim does not install due to astroconda-dev being deprecated.
# # Create kernel for mirisim environment
# RUN mkdir -p /usr/local/share/jupyter/kernels/mirisim
# COPY kernel.mirisim.json /usr/local/share/jupyter/kernels/mirisim/kernel.json
# COPY logo-32x32.png /usr/local/share/jupyter/kernels/mirisim
# COPY logo-64x64.png /usr/local/share/jupyter/kernels/mirisim

# Clean out the home directory so it mimics a fresh EFS mount (useful for developer testing)
RUN rm -rf /home/jovyan/*
RUN rm -r /home/jovyan/.[a-zA-Z_]*

COPY VERSION /opt

USER $NB_UID
