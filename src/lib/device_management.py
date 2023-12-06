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

