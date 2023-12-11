: "
Docker temporary chroot environment startup and setup script for: Debian
"
# Initialize Variables
container_Name="debian-chroot"
passthrough_device=/dev/sdb
distinstall_python_Path="${1:-$HOME/Desktop}"
image="debian"
version_tag="latest"

## Startup container
docker run -itd --privileged --name=${container_Name} --device=$passthrough_device --network=host -v "$distinstall_python_Path/distinstall-python:/tmp/distinstall-python" ${image}:${version_tag}

## Chroot into container and execute setup steps
docker exec -it ${container_Name} /bin/bash -c "apt update -y && apt upgrade -y && apt install -y build-essential git arch-install-scripts parted vim dhcpcd python3 python-pip python-ruamel-yaml"


