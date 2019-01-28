#!/bin/bash
## check in incremented patch version with tag ##


hub="793754315137.dkr.ecr.us-east-1.amazonaws.com"
folder="$1"
if [[ ! $folder ]]; then
    echo "\"publish.sh\" requires exactly 1 argument.

Usage: ./publish.sh FOLDER

Build, commit, tag(git and docker) push the Docker image contained in FOLDER"
    exit 1
fi

set -xe

# reverse pipe so vars are remembered in main shell
read repo major minor patch extra <<< $(sed 's/\./ /g' ./${folder}/VERSION)

$(aws ecr get-login --no-include-email --region us-east-1)

docker build -t ${hub}/${repo}:latest -t ${hub}/${repo}:latest -t ${hub}/${repo}:${major} -t ${hub}/${repo}:${major}.${minor} -t ${hub}/${repo}:${major}.${minor}.${patch} ./${folder}

# make sure your local branch isn't stale
git fetch
$(git rev-parse HEAD) == $(git rev-parse @{u})

# patch++ and tag repo.
temptag=`cat ./${folder}/VERSION`
tag=${temptag%.devel}

awk -F. '{ OFS=FS; $4++ } 1' ./${folder}/VERSION > tmp
mv tmp ./${folder}/VERSION
git add ./${folder}/VERSION
git add ./${folder}/Dockerfile

git commit
git tag -a $tag -m 'auto tag version'
git push
git push --tags

# push to docker 4 times, 3 will be overwritten with next push.
# VERSION string example: tess-workshop.v0.1.0.devel -> full docker tag: [hub]/tess-workshop:v0.1.0
docker push ${hub}/${repo}
