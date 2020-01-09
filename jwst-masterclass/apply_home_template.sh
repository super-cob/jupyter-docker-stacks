#!/bin/bash

sudo -u jovyan rsync -ur /opt/home_template/ /home/jovyan/
rm /home/jovyan/example_notebooks
sudo -u jovyan ln -s /opt/pandeia-coronagraphy/notebooks /home/jovyan/example_notebooks