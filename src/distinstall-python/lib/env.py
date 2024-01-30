"""
Environment Variable support
"""
# Import Built-in Libraries
import os
import sys

# Declare classes
class Environment():
    """
    Environment Variable Support
    """
    def __init__(self):
        """
        Constructor
        """
        self.EDITOR = os.environ.get("EDITOR")
        self.TARGET_DISK_NAME = os.environ.get("TARGET_DISK_NAME") # The target disk's label (i.e. /dev/sdX for SATA|AHCI, or /dev/nvme0np1 for NVME)
        self.MODE = os.environ.get("MODE") # Runtime boot mode - DEBUG|RELEASE
        self.USER = os.environ.get("USER") # Name of regular user
        self.SUDO_USER = os.environ.get("SUDO_USER") # Name of superuser
