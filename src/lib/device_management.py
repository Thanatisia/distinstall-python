"""
Device and Disk Management
"""
import os
import sys
import process

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
    cmd_str = "blkid {}".format(disk_Label)
    stdout, stderr, returncode = process.subprocess_Line(cmd_str)

    # Format stdout to block information
    if stdout != None:
        # Iterate through every row
        for i in range(len(stdout)):
            # Get current row
            curr_row = stdout[i]

            # Split the current row by the spacing
            curr_row_spl = curr_row.split(" ")

            # Split the first element by the delimiter ': '
            partition_label = curr_row_spl[0].split(": ")[0]

            # Obtain other block info
            curr_row_block_Info = curr_row_spl[1:]

            # Split the block info into keywords and values
            curr_row_block_Mapping = {
                "partition-label" : partition_label,
                "device-uuid" : curr_row_block_Info[0].split("=")[1],
                "block-size" : curr_row_block_Info[1].split("=")[1],
                "filesystem-type" : curr_row_block_Info[2].split("=")[1],
                "partition-uuid" : curr_row_block_Info[3].split("=")[1]
            }

            # Map current row disk label to the block information
            block_Information[disk_Label].append(
                {
                    i : curr_row_block_Mapping
                }
            )

    return block_Information

