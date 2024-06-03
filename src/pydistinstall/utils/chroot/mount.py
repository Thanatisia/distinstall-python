"""
Changing of Root/Mounting-related helper wrapper functions
"""
import os
import sys
from pydistinstall.utils.process import subprocess_Line

def make_mount_dir(dir_path):
    """
    Create directories if does not exists
    """
    # Initialize Variables
    cmd_str = ""
    stdout = ""
    stderr = ""
    returncode = -1

    ### Check if directory exists
    if not (os.path.isdir(dir_path)):
        """
        ### Directory does not exist
        cmd_str = "mkdir -p {}".format(dir_path)

        ### Make the directories
        stdout, stderr, returncode = process.subprocess_Line(cmd_str)
        """

        try:
            # Make the directory using built-in
            os.mkdir(dir_path)

            # Check if directory exists now
            if os.path.isdir(dir_path):
                # Set return code as 0
                returncode = 0

                # Set standard output
                stdout = "Directory {} created successfully".format(dir_path)
        except Exception as ex:
            stderr = str(ex)
    else:
        stderr = "Directory {} exists.".format(dir_path)

    # Output
    return [cmd_str, stdout, stderr, returncode]

def mount_partition(curr_filesystem, root_Dir, root_partition_Label):
    """
    Mount a partition to a mount directory
    """
    # Initialize Variables
    cmd_str = ""
    stdout = ""
    stderr = ""
    returncode = -1

    ## Check filesystem of current partition
    if (curr_filesystem == "fat32"):
        ## Check filesystem for FAT32
        ## FAT32 formatting is in vfat
        cmd_str = "mount -t vfat {} {}".format(root_partition_Label, root_Dir)
    else:
        ## Check filesystem for any other filesystems
        """
        mount -t ext4 /dev/sdX2 /mnt
        mount -t ext4 /dev/sdX1 /mnt/boot 
        mount -t ext4 /dev/sdX3 /mnt/home
        """
        cmd_str = "mount -t {} {} {}".format(curr_filesystem, root_partition_Label, root_Dir)

    # Execute command
    # stdout, stderr = process.subprocess_Sync(cmd_str)
    stdout, stderr, returncode = subprocess_Line(cmd_str)

    # Output
    return [cmd_str, stdout, stderr, returncode]

