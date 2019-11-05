#!/bin/sh
set -eux

ln -s "$CONDA_DIR/vnc/Desktop"
start-notebook.sh

exec "$@"
