# Dockerfile
# for creating a pre-defined chroot environment for installation
# by creating a docker container for each distribution (In case is necessary) with useful and essential packages

## Pull latest image
FROM archlinux:latest

## Update packages and Install dependencies
RUN pacman -Syu && \
    pacman -S git base-devel vim arch-install-scripts parted python3 python-pip python-ruamel-yaml

## Set Networking

## Set Entry point
ENTRYPOINT ["/bin/bash"]
