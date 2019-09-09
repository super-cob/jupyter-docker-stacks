#!/bin/bash

if [[ ! -e /home/jovyan/example_notebooks ]]; then
    cp -R /opt/example_notebooks /home/jovyan/
    chown -R jovyan:users /home/jovyan/example_notebooks
fi
