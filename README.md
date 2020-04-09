# jupyter-docker-stacks
Spacetelescope's Jupyter Docker Stacks are a set of ready to run Docker images containing Jupyter applications intended for use in Jupyterhub.

## Publishing
Simply run `./publish.py [folder]` which will automatically build and publish a given stack to both GitHub (auto-adds Dockerfile and Version and asks for a comment) and the Amazon ECR given in the publish script. This script will attempt to log in to the ECR which necessitates a properly set up .aws file. You can simply run `aws configure` and enter the correct Access ID and Secret Key to set this up right. Note that the script will not continue upon the first failure so you should feel comfortable running it when you want to publish your Dockerfile.

### Development
Running publish.py with the `--dev` flag will cause the script to publish to your stack's development ECR repository.  Instead of tagging the image with version numbers, it will tag with your current GitHub branch name.  The script does not create git repository tags in dev mode.

## Auto-Versioning
Each directory has a VERSION file containing `[stack-name].v[major].[minor].[patch].devel` information. The patch version is automatically updated upon a new publish and used in the following ways:
 * The git repo is tagged at the commit that `publish.py` facilitates.
 * The Docker image that is pushed to Amazon ECR is tagged four times: `latest`, `v[major]`, `v[major].[minor]`, and `v[major].[minor].[patch]`. This is so that you can specify any version of a given stack and you will always get the latest image of that version. For instance, a `docker pull` of `tess-workshop:v0.1` will pull the newest image with that minor version.

Note that the VERSION file in source control is always the one after the one most recently published, because the version is only incremented if the publish.py script is successful.

## Adding a new stack
Simply create a new folder, include (at a minimum) Dockerfile and VERSION (set to `[stack-name].0.1.0.devel`).

## WFIRST SIT science platform
This science platform (based on [JupyterLab](https://jupyterlab.readthedocs.io/en/stable/)) is for use by Science Investigation Team (SIT) members to perform research and develop reprocessing methods.

#### Overview
The platform provides persistent user environments, where files (images, notebooks, etc.) can be stored and accessed during later sessions.  Users can access iPython consoles and terminals, create text files, display images, and create Jupyter notebooks.  A virtual desktop provides access to graphical tools such as DS9 and the Coronagraphic Visibility tool.

Example Jupyter notebooks are provided as a starting point, and users can create new ones for their own work.

#### Included software
The software and tools available on the platform include Python packages used for processing and analyzing data products, Source Extractor, DS9, and others.  A full list of include software can be found [here](https://github.com/spacetelescope/jupyter-docker-stacks/blob/wfirst-sit/wfirst-sit/WFIRST_SOFTWARE.md).

Notable Python packages:
- asdf
- astropy
- astroquery
- boto3
- cfitsio
- cubeviz
- dask
- drizzlepac
- fitsblender
- glue
- matplotlib
- numpy
- pandas
- pandeia.engine
- pysiaf
- scikit-image
- scikit-image
- scipy
- spectral-cube
- stsci
- synphot

#### Authentication
Authentication is done through the MAST portal.  All SIT members will need to create an account to access the science platform.  Navigate to https://wfirst-sit.science.stsci.edu in your browser, and you will be redirected to the authentication page.
