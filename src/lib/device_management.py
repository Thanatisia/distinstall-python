"""
Device and Disk Management
"""
import os
import sys

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

    
