"""
Disk I/O Processing Handling-related functions and utilities
"""
import os
import sys
from pydistinstall.utils.device_management import format_partition_str
from pydistinstall.utils.process import subprocess_Line, subprocess_Sync

def disk_partition_table_Format(disk_Label, partition_Table):
    """ 
    Format the disk, Create a new partition table label and return the results
    """
    # Initialize Variables
    cmd_str = "parted {} mklabel {}".format(disk_Label, partition_Table)
    stdout = ""
    stderr = ""
    returncode = 0

    # Execute the command line string and return the standard output, error, and status code
    stdout, stderr, returncode = subprocess_Line(cmd_str)

    # Output
    return [cmd_str, stdout, stderr, returncode]

def partition_make(disk_Label, partition_type_label, partition_Filesystem, partition_start_Size, partition_end_Size):
    """
    Making Partitions
    """
    # Initialize Variables
    cmd_str = ""

    # Set command string
    cmd_str = "parted {} mkpart {} {} {} {}".format(disk_Label, partition_type_label, partition_Filesystem, partition_start_Size, partition_end_Size)

    # Create Partition
    stdout, stderr, returncode = subprocess_Sync(cmd_str)

    # Output
    return [cmd_str, stdout, stderr, returncode]

def partition_filesystem_format(disk_Label, storage_controller, part_ID, part_filesystem):
    """
    Format the partition filesystem
    """
    # Initialize Variables
    cmd_str = ""
    stdout = ""
    stderr = ""
    returncode = -1

    ## Prepare and Format Partition according to Device Storage Controller Type
    curr_part = format_partition_str(disk_Label, part_ID, storage_controller)

    if part_filesystem == "fat32":
        cmd_str = "mkfs.fat -F32 {}".format(curr_part)
    elif part_filesystem == "ext4":
        cmd_str = "mkfs.ext4 {}".format(curr_part)
    elif part_filesystem == "swap":
        cmd_str = "mkswap {}{}".format(curr_part)
    else:
        stderr = "Unknown File System: [{}]".format(part_filesystem)

    # Check if command is empty
    if cmd_str != "":
        # Perform partitioning
        stdout, stderr, returncode = subprocess_Sync(cmd_str)

    # Output
    return [cmd_str, stdout, stderr, returncode]

def partition_set_Bootable(partition_Table, disk_Label, part_ID):
    """ 
    Set the specified partition as 'bootable'
    """
    # Initialize VVariables
    cmd_str = ""
    stdout = ""
    stderr = ""
    returncode = 0

    ### Check if disk label is MBR or GPT
    if (partition_Table == "msdos") or (partition_Table == "mbr"):
        cmd_str = "parted {} set {} boot on".format(disk_Label, part_ID)
    elif (partition_Table == "gpt"):
        cmd_str = "parted {} set {} esp on".format(disk_Label, part_ID)

    # Perform Boot set
    stdout, stderr, returncode = subprocess_Sync(cmd_str)

    # Output
    return [cmd_str, stdout, stderr, returncode]

def partition_swap_Enable(disk_Label, part_ID):
    """
    Enable Swap Partition (if created)
    """
    # Initialize Variables
    cmd_str = "swapon {}{}".format(disk_Label, part_ID)

    # Begin Execution
    ## Perform Swap partition formatting
    stdout, stderr, returncode = subprocess_Sync(cmd_str)

    # Output
    return [cmd_str, stdout, stderr, returncode]

