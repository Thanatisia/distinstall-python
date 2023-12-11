: "
Docker temporary chroot environment startup and setup script for: ArchLinux
"
# Initialize Variables
container_Name="arch-chroot"
passthrough_device=/dev/sdb
distinstall_python_Path="${1:-$HOME/Desktop}"
image="archlinux"
version_tag="latest"

## Startup container
docker run -itd --privileged --name=${container_Name} --device=$passthrough_device --network=host -v "$distinstall_python_Path/distinstall-python:/tmp/distinstall-python" ${image}:${version_tag}

## Chroot into container and execute setup steps
docker exec -it ${container_Name} /bin/bash -c "pacman -Syu && pacman -S base-devel git arch-install-scripts parted vim dhcpcd python3 python-pip python-ruamel-yaml"


