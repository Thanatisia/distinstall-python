"""
Library/Module containing functions and utilities relating to handling files within a Chroot/new root filesystem (rootfs) virtual environment (aka container)
"""
import os
import sys

def write(contents, dir_Mount="/mnt", destination="new-file.txt"):
    """
    Write the provided string into the destination file in the specified chroot mount/rootfs directory

    :: Params
    - contents : Specify the content string you wish to write into the destination file in the mount/root filesystem directory
        + Type: String
    - dir_Mount : Specify the mount/root filesystem directory to chroot into
        + Type: String
        + Default: "/mnt"
    - destination : Specify the destination output file within the mount directory to write the contents into
        + Type: String
        + Default: "new-file.txt"
    """
    # Initialize Variables
    target_directory = "{}/{}".format(dir_Mount, destination)

    # Write commands into file for reusing
    with open(target_directory, "a+") as write_chroot_Commands:
        # Write to file
        write_chroot_Commands.write(contents)

        # Close file after usage
        write_chroot_Commands.close()

def writelines(contents, dir_Mount="/mnt", destination="new-file.txt"):
    """
    Write the provided list of strings into the destination file in the specified chroot mount/rootfs directory

    :: Params
    - contents : Specify the content string you wish to write into the destination file in the mount/root filesystem directory
        + Type: List<String>
    - dir_Mount : Specify the mount/root filesystem directory to chroot into
        + Type: String
        + Default: "/mnt"
    - destination : Specify the destination output file within the mount directory to write the contents into
        + Type: String
        + Default: "new-file.txt"
    """
    # Initialize Variables
    target_directory = "{}/{}".format(dir_Mount, destination)

    # Write commands into file for reusing
    with open(target_directory, "a+") as write_chroot_Commands:
        # Write to file
        write_chroot_Commands.write(contents)

        # Close file after usage
        write_chroot_Commands.close()

