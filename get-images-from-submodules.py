from queue import Empty
from git import Repo
from github import Github
from pathlib import Path

import docker
import os, shutil
import json

includeVersion = os.getenv("INCLUDE_VERSION", 'False').lower() in ('true')

baseFolder="/github/workspace"
configPath = "/.github/fiware/config.json"
submodulesFolder = "/submodules"

def get_releases_for_submodule(submodule, repo):

    Repo.clone_from(submodule.url, submodulesFolder)
    config_file = Path(submodulesFolder + configPath)
    githubRepo = submodule.url.replace('https://github.com/', '').replace('.git', '')

    containers = []
    if config_file.is_file():
        print("Config exists for " + submodule.url)
        versionList = []
        with open(submodulesFolder + configPath) as json_file:
            cl = []
            containersWithReg = []
            data = json.load(json_file)
            registryList=(data['dockerregistry'])
            containerList=(data['docker'])
            for container in containerList:
                print(container)
                if container != '':
                    cl.append(container)
            if not registryList: 
                containersWithReg.extend(cl)
            else:
                for registry in registryList:
                    if registry != '':
                        for container in cl:
                            containersWithReg.append(registry + "/" + container)
            

            github = Github()
            repository = github.get_repo(githubRepo)
            if includeVersion:
                for release in repository.get_releases():
                    for container in containersWithReg:
                        client = docker.from_env()
                        try:
                            client.images.pull(container + ":"+release.tag_name)
                            containers.append(container + ":"+release.tag_name)
                        except:
                            print("Image does not exist: " + container + ":" + release.tag_name)
            else:
                containers.append(container)
    else:
        print("No config file exists: " + githubRepo)

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

