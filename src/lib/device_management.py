"""
Device and Disk Management
"""
import os
import sys
import lib.process as process

def format_partition_str(disk_Label, partition_Number=0, storage_Controller="sata"):
    """
    Prepare and Format Partition according to the Storage Controller

    :: Storage Controller Types
    - sata : For SATA/AHCI devices
        Format: /dev/sdX
    - nvme : For NVME devices
        Format: /dev/nvme[device-number]p[partition-number]
    - loop : For Loopback devices
        Format: /dev/loop[device-number]p[partition-number]
    """
    # Initialize Variables
    storage_controller_Partition = ""

    # Conditional Check
    if storage_Controller == "sata":
        # Devices using '/dev/sdX'
        target_partition_Label = "{}{}".format(disk_Label, partition_Number)
    elif storage_Controller == "nvme":
        # Devices using '/dev/nvme[device-number]p[partition-number]
        target_partition_Label = "{}p{}".format(disk_Label, partition_Number)
    elif storage_Controller == "loop":
        # Devices using '/dev/loop[loopback-device-number]p[partition-number]
        target_partition_Label = "{}p{}".format(disk_Label, partition_Number)
    else:
        # Any other devices
        target_partition_Label = "{}{}".format(disk_Label, partition_Number)

    # Return
    return target_partition_Label

def get_block_Information(disk_Label):
    """
    Obtain block information regarding the disk using 'blkid' and
    return the information formatted as a dictionary

    :: Params
    - disk_Label : Your target disk label; i.e. SATA|AHCI = /dev/sdX, NVME = /dev/nvme[disk-number], Loopback = /dev/loop[disk-number]
    """
    # Initialize Variables
    block_Information = {disk_Label : []}

    # Obtain block information
    cmd_str = "blkid".format(disk_Label)
    stdout, stderr, returncode = process.subprocess_Sync(cmd_str)

    # Format stdout to block information
    if stdout != None:
        # Split standard output into rows of entries
        block_Entries = stdout.split("\n")[::-1][1:][::-1]

        # Iterate through every row
        for i in range(len(block_Entries)):
            # Get current row
            curr_row = block_Entries[i]

            # Split the current row by the spacing
            curr_row_spl = curr_row.split(" ")

            # Split the first element by the delimiter ': '
            partition_label = curr_row_spl[0].split(":")[0]

            # Check if specified partition label is in the disk label string
            if (len(partition_label.split(disk_Label)) > 1):
                # After split, there are multiple entries because split was successful
                # Get partition number from partition label
                partition_Number = partition_label.split(disk_Label)[1:][0]

                # Obtain other block info
                curr_row_block_Info = curr_row_spl[1:]

                # Split the block info into keywords and values
                curr_row_block_Mapping = {
                    "partition-label" : partition_label,
                    "device-uuid" : curr_row_block_Info[0].split("=")[1],
                    "block-size" : curr_row_block_Info[1].split("=")[1],
                    "filesystem-type" : curr_row_block_Info[2].split("=")[1],
                    "partuuid" : curr_row_block_Info[3].split("=")[1]
                }

                # Map current row disk label to the block information
                block_Information[disk_Label].append(
                    {
                        partition_Number : curr_row_block_Mapping
                    }
                )

    return block_Information

def design_filesystems_Table(disk_Label, \
                            dir_Mount, \
                            disk_block_Information, \
                            partition_Scheme, \
                            mount_Points\
                            ):
    """
    Design Filesystem Table (fstab) and return the fstab contents

    :: Params
    - disk_Label : The target disk/device path; i.e. SATA|AHCI = /dev/sdX, nvme = /dev/nvmeX, loop = /dev/loopX
        Type: String

    - dir_Mount : The root mount directory
        Type: String

    - disk_block_Information : Dictionary (key-value) mapping) of the disk label information
        Type: Dictionary
        Structure:
            {
                disk_Label : [
                    {
                        "partition-label" : your-partition-label,
                        "device-uuid" : UUID,
                        "block-size" : BLOCK_SIZE,
                        "filesystem-type" : FILESYSTEM_TYPE (i.e. ext4),
                        "partuuid" : PARTUUID
                    }
                ]
            }

    - partition_Scheme : Dictionary containing the mappings of the partition number to the partition information
        Type: Dictionary

    - mount_Points : Dictionary containing the partition names mapped to the mount points
    """
    # Initialize Variables
    default_root_Path = "/"
    fstab_Contents = []

    # Loop through all key values in block information
    for i in range(len(disk_block_Information)):
        # Get current partition's mount point
        curr_partition_Mappings = disk_block_Information[i]

        # Loop through current partition key value mappings
        for part_Number,part_Details in curr_partition_Mappings.items():
            # Convert partition number to integer
            part_Number = int(part_Number)

            # Get partition scheme corresponding to the current partition number
            curr_partition = partition_Scheme[part_Number]

            # Get current partition's number
            curr_partition_Name = curr_partition[0]

            # Get current partition's mount point
            curr_partition_mount_Point = mount_Points[curr_partition_Name]

            # Get block details and Sanitize block details
            partition_Label = part_Details["partition-label"].strip('\"')
            device_UUID = part_Details["device-uuid"].strip('\"')
            block_Size = part_Details["block-size"].strip('\"')
            filesystem_Type = part_Details["filesystem-type"].strip('\"')
            partition_UUID = part_Details["partuuid"].strip('\"')

            # Get partition number
            partition_Number = partition_Label.split(disk_Label)[1:][0]

            # Format mount path
            ## Remove mount directory from current path
            system_mount_Dir = curr_partition_mount_Point.split(dir_Mount)[1:][0]

            ## Set default path if mount path not found (Root)
            if system_mount_Dir == "":
                system_mount_Dir = default_root_Path
            
            # Design filesystem entry for this row
            filesystem_Entry = "# {}\nUUID={}\t{}\t{}\trw,relatime\t".format(partition_Label, device_UUID, system_mount_Dir, filesystem_Type)

            if curr_partition_Name == "Root":
                filesystem_Entry += "0 1"
            else:
                filesystem_Entry += "0 2"

            # Append row into contents list
            fstab_Contents.append(filesystem_Entry)

            # Append newline
            fstab_Contents.append("\n")

    return fstab_Contents

