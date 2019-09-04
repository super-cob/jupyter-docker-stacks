#!/bin/bash

if [[ ! -e /home/jovyan/.astropy/config/astroquery.cfg ]]; then
    mkdir -p /home/jovyan/.astropy/config

    cat <<EOF > /home/jovyan/.astropy/config/astroquery.cfg
[mast]

# Override MAST server with JWST A-string so we have access to
# relevant data:
server = https://pwjwdmsauiweb.stsci.edu
EOF

    chown -R jovyan:users /home/jovyan/.astropy
fi
