# Dockerfile
# for creating a pre-defined chroot environment for installation
# by creating a docker container for each distribution (In case is necessary) with useful and essential packages

## Pull latest image
FROM debian:latest

## Update packages and Install dependencies
RUN apt update -y && apt upgrade -y && \
    apt install -y git base-devel vim arch-install-scripts parted

## Set Networking

## Set Entry point
ENTRYPOINT ["/bin/bash"]
