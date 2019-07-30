# jupyter-docker-stacks
Spacetelescope's Jupyter Docker Stacks are a set of ready to run Docker images containing Jupyter applications intended for use in Jupyterhub.

## Publishing
simply run `./publish.py [folder]` which will automatically build and publish a given stack to both GitHub (auto-adds Dockerfile and Version and asks for a comment) and the Amazon ECR given in the publish script. This script will attempt to log in to the ECR which necessitates a properly set up .aws file. You can simply run `aws configure` and enter the correct Access ID and Secret Key to set this up right. Note that the script will not continue upon the first failure so you should feel comfortable running it when you want to publish your Dockerfile.

## Auto-Versioning
Each directory has a VERSION file containing `[stack-name].v[major].[minor].[patch].devel` information. The patch version is automatically updated upon a new publish and used in the following ways:
 * The git repo is tagged at the commit that `publish.py` facilitates.
 * The Docker image that is pushed to Amazon ECR is tagged four times: `latest`, `v[major]`, `v[major].[minor]`, and `v[major].[minor].[patch]`. This is so that you can specify any version of a given stack and you will always get the latest image of that version. For instance, a `docker pull` of `tess-workshop:v0.1` will pull the newest image with that minor version.

note that the VERSION file in source control is always the one after the one most recently published, because the version is only incremented if the publish.py script is successful.
 
## Adding a new stack
Simply create a new folder, include (at a minimum) Dockerfile and VERSION (set to `[stack-name].0.1.0.devel`). 
