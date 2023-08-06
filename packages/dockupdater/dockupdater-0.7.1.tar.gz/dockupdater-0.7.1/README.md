# Docker + Updater = Dockupdater

[![Release](https://img.shields.io/github/release/dockupdater/dockupdater.svg?style=flat-square)](https://hub.docker.com/r/dockupdater/dockupdater/)
[![Travis](https://img.shields.io/travis/dockupdater/dockupdater/master.svg)](https://travis-ci.org/dockupdater/dockupdater/)
[![Codecov](https://img.shields.io/codecov/c/github/dockupdater/dockupdater/master.svg)](https://codecov.io/gh/dockupdater/dockupdater)
[![Python Version](https://img.shields.io/pypi/pyversions/dockupdater.svg?style=flat-square)](https://pypi.org/project/dockupdater/)
[![Pypi Version](https://img.shields.io/pypi/v/dockupdater.svg?style=flat-square)](https://pypi.org/project/dockupdater/)
[![Latest version](https://images.microbadger.com/badges/version/dockupdater/dockupdater.svg)](https://microbadger.com/images/dockupdater/dockupdater)
[![Docker Pulls](https://img.shields.io/docker/pulls/dockupdater/dockupdater.svg?style=flat-square)](https://hub.docker.com/r/dockupdater/dockupdater/)
[![Layers](https://images.microbadger.com/badges/image/dockupdater/dockupdater.svg)](https://microbadger.com/images/dockupdater/dockupdater)  

Automatically keep your docker services and your docker containers up-to-date with the latest version.

## Overview

**Dockupdater** will monitor (all or specified by a label) running docker containers and running service (in Docker swarm) and update them to the (latest or tagged) available image in the remote registry.

- Push your image to your registry and simply wait your defined interval for dockupdater to find the new image and redeploy your container autonomously.
- Notify you via many platforms courtesy of [Apprise](https://github.com/caronc/apprise) 
- Use with Docker swarm to update services on the latest available version
- Limit your server SSH access
- Useful to keep 3rd party container up-to-date

## Getting Started

More detailed usage and configuration can be found on [the docs](https://dockupdater.dev).

### Docker container

**Dockupdater** is deployed via docker image in a standalone container like so:

```bash
docker run -d --name dockupdater \
  -v /var/run/docker.sock:/var/run/docker.sock \
  dockupdater/dockupdater
```

> This is image is compatible for amd64, arm32, and arm64 CPU architectures

### Docker swarm (service)

**Dockupdater** can be deploy on a service like that:

```bash
version: "3.6"

services:
  dockupdater:
    image: dockupdater/dockupdater
    deploy:
      placement:
        constraints:
          - node.role == manager
```

> Dockupdater need to run on a manager node

## Getting helps

* [Issues list](https://github.com/dockupdater/dockupdater/issues)
* [Documentation](https://dockupdater.dev)
* [Releases and changelogs](https://github.com/dockupdater/dockupdater/releases)
* [Frequently Asked Questions](https://dockupdater.dev/Frequently-Asked-Questions.md)

## Reporting bugs and contributing

All contributions are welcome!

* Want to report a bug or request a feature? Please open [an issue](https://github.com/dockupdater/dockupdater/issues/new).
* Want to help us? Your contribution and your pull request are welcome. We need all the help we can get!
