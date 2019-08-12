#!/usr/bin/env python3
# check in incremented patch version with tag

from argparse import ArgumentParser
from pathlib import Path
import subprocess
import os
import sys


def parse_args():
    parser = ArgumentParser("publish.py", description="build, commit, tag (git and Docker) and push a Docker image")
    parser.add_argument("folder_path", help="directory containing, at minimum, Dockerfile and VERSION files")

    return parser.parse_args()


def is_integer(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


def main():
    folder_path = Path(parse_args().folder_path).absolute()
    dockerfile_path = folder_path/"Dockerfile"
    version_path = folder_path/"VERSION"

    assert folder_path.is_dir(), "folder_path must be a directory"
    assert dockerfile_path.exists(), "missing Dockerfile"
    assert version_path.exists(), "missing VERSION"

    # Change to the directory so git commands act on the correct repository
    os.chdir(folder_path)

    with version_path.open() as version_file:
        version_parts = version_file.read().strip().split(".")

    repo = version_parts[0]
    if is_integer(version_parts[-1]):
        versions = version_parts[1:]
        extra = []
    else:
        # The version is permitted to end with an arbitrary string (.devel, for example):
        versions = version_parts[1:-1]
        extra = version_parts[-1:]

    assert is_integer(versions[-1]), "the last version number must be an integer"

    # Confirm that local and remote are at the same revision
    subprocess.check_call(["git", "fetch"])
    our_hash = subprocess.check_output(["git", "rev-parse", "HEAD"])
    upstream_hash = subprocess.check_output(["git", "rev-parse", "@{u}"])
    assert our_hash == upstream_hash, "local and/or remote are missing commits"

    # Ask aws-cli to generate a Docker login command and execute it
    login_command = subprocess.check_output(["aws", "ecr", "get-login", "--no-include-email", "--region", "us-east-1"])
    subprocess.check_call(login_command, shell=True)

    docker_hub_url = login_command.decode("utf-8").split(" ")[-1].strip()
    assert docker_hub_url.startswith("https://")
    docker_hub_hostname = docker_hub_url[len("https://"):]

    # Build the docker image, adding tags for latest and each level of the version
    docker_command = ["docker", "build"]
    tags = ["latest"] + [".".join(versions[0:i]) for i in range(1, len(versions) + 1)]
    for tag in tags:
        full_tag = f"{docker_hub_hostname}/{repo}:{tag}"
        docker_command.extend(["-t", full_tag])
    docker_command.append(str(folder_path))
    subprocess.check_call(docker_command)

    # Advance the rightmost version by one and save the result back to the VERSION file
    new_versions = versions.copy()
    new_versions[-1] = str(int(new_versions[-1]) + 1)
    with version_path.open("w") as version_file:
        version_file.write(".".join([repo] + new_versions + extra))
        version_file.write("\n")

    # Commit any changes in the directory (user will be prompted for a commit message)
    subprocess.check_call(["git", "add", "."])
    subprocess.check_call(["git", "commit"])
    subprocess.check_call(["git", "tag", "-a", ".".join([repo] + versions), "-m", "auto tag version"])
    subprocess.check_call(["git", "push"])
    subprocess.check_call(["git", "push", "--tags"])

    # Push the new image to the Docker repository
    subprocess.check_call(["docker", "push", f"{docker_hub_hostname}/{repo}"])


if __name__ == "__main__":
    main()
