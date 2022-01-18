import imp
from git import Repo
from github import Github
from pathlib import Path

import os, shutil
import json

baseFolder="/github/workspace"
configPath = "/.github/fiware/config.json"
submodulesFolder = "/submodules"

def get_releases_for_submodule(submodule, repo):

    Repo.clone_from(submodule.url, submodulesFolder)
    config_file = Path(submodulesFolder + configPath)
    containers = []
    if config_file.is_file():
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++Config exists for " + submodule.url)
        cl = []
        versionList = []
        with open(submodulesFolder + configPath) as json_file:
            data = json.load(json_file)
            containerList=(data['docker'])
            for container in containerList:
                print(container)
                if container != '':
                    cl.append(container)
            github = Github()

            githubRepo = submodule.url.replace('https://github.com/', '').replace('.git', '')
            repository = github.get_repo(githubRepo)
            for release in repository.get_releases():
                for container in cl:
                    containers.append(container + ":"+release.tag_name)
    shutil.rmtree(submodulesFolder)
    return containers

repo = Repo(baseFolder)
allContainers = []
for submodule in repo.submodules:
    subList = get_releases_for_submodule(submodule, repo)
    print(subList)
    allContainers.extend(subList)

print(allContainers)

print(f"::set-output name=containers::{allContainers}")

