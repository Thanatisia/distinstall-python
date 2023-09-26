"""
Setup Function
"""
## Built-in
import os
import sys
import yaml

## External Libraries
from lib.cli import CLIParser
from lib.format import Text
from lib.env import Environment
import app.distributions as dist

class Setup():
    """
    Initialization and setup
    """
    def __init__(self):
        """
        Constructor
        """
        # Initialize Class
        self.cliparser = CLIParser()
        self.fmt_Text = Text()
        self.init_defaults()
        self.init_Variables()

    def init_defaults(self):
        self.cfg = {
            "device_Type" : "<hdd|ssd|flashdrive|microSD>", # Your disk/device/file type; i.e. VHD|HDD|SSD|Flashdrive|Microsd etc
            "device_Size" : "<x {GB | GiB | MB | MiB}>", # The total disk size
            "disk_Label" : os.environ.get("TARGET_DISK_NAME"), # The disk's name/label (i.e. /dev/sdX for SATA, /dev/nvme0np1 for NVME); Default: uses the environment variable '$TARGET_DISK_NAME'
            "disk_partition_Table" : "", # mbr/msdos | gpt
            "bootloader_firmware" : "", # BIOS | UEFI
            "bootloader" : "grub",
            "partition_Scheme" : {
                # This contains your partition scheme
                #
                # [Configuration Synopsis/Syntax]
                # - MBR Partition Table/MSDOS Bootloader Firmware
                #   <partition_Number> : [<partition_Name>, <partition_Type>, <partition_filesystem_Type>, <partition_start_Size>, <partition_end_Size>, <partition_Bootable>, <partition_Others>]
                # - GPT Partition Table/UEFI Bootloader Firmware
                #   <partition_Number> : [<partition_Label>, <partition_Type>, <partition_filesystem_Type>, <partition_start_Size>, <partition_end_Size>, <partition_Bootable>, <partition_Others>]
                #
                # [Notes]
                # - The Boot partition for a GPT partition layout/configuration needs to be an EFI System Partition type
                #
                # Some Manadatory partition names:
                #   - For Boot Partition : 'Boot'
                #   - For Root Partition : 'Root'
                1 : ["Boot", "primary", "ext4", "0%", "1024MiB", True, "NIL"],
                2 : ["Root", "primary", "ext4", "1024MiB", "<x1MiB>", False, "NIL"],
                3 : ["Home", "primary", "ext4", "<x1MiB>", "100%", False, "NIL"],
            },
            "mount_Paths" : {
                # This contains the mount paths mapped to the partition name
                # Note:
                #   - Please seperate all parameters with delimiter ','
                #   - Please seperate all subvalues with delimiter ';'
                #
                # Syntax:
                # [Partition Name] : [mount path]
                #
                # Some Manadatory partition names:
                #   - For Boot Partition : 'Boot'
                #   - For Root Partition : 'Root'
                "Boot" : "/mnt/boot",	# Boot
                "Root" : "/mnt",		# Root
                "Home" : "/mnt/home",	# Home
            },
            "base_pkgs" : [
                # EDIT: MODIFY THIS
                # Add the packages you want to strap in here
                "base"
                "linux"
                "linux-firmware"
                "linux-lts"
                "linux-lts-headers"
                "base-devel"
                "nano"
                "vim"
                "networkmanager"
                "os-prober"
            ],
            "location" : {
                "Region" : "<your-region (Asia|US etc)>", # Refer to /usr/share/zoneinfo for your region
                "City" : "<your-city (Singapore etc)>", # Refer to /usr/share/zoneinfo/<your-region> for your City
                "Language" : "<language-code (en_US.UTF-8|en_SG.TF-8 etc)>", # Your Language code - refer to /etc/locale.gen for a list of all language codes
                "KeyboardMapping" : "en_UTF-8", # Your Keyboard Mapping - change this if you use this (TODO: 2022-06-17 2314H : At the moment this is not used)
            },
            "user_ProfileInfo"  : {
                # Append this and append a [n]="\${user_ProfileInfo[<n-1>]}" in
                # 	user_Info
                # Note:
                #	- Please seperate all parameters with delimiter ','
                #	- Please seperate all subvalues with delimiter ';'
                # Syntax:
                # 
                #	<username> : [
                #       <primary_group>,
                #       <secondary_group (put NIL if none),
                #       <custom_directory_path (put NIL if none)>,
                #       <any_other_Parameters>
                #   ]
                # 
                "username" : ["wheel", "NIL", "/home/profiles/username", "NIL"]
            },
            "networkConfig_hostname" : "<your-network-hostname>", # Similar to workspace group name, used in /etc/hostname
            "bootloader" : "<your-bootloader>", # Your bootloader, at the moment - supported bootloaders are [grub, syslinux], tested: [grub] (TODO: 2022-06-17 2317H : Add more bootloaders (if available))
            "bootloader_directory" : "/boot/<your-bootloader>", # Your Bootloader's boot mount point; Certain bootloaders (i.e. Grub) have different boot directories based on partition table (i.e. MBR/GPT); Default: /boot/<your-bootloader>
            "bootloader_Params" : "", # Your Bootloader Parameters - fill this if you have any, leave empty if NIL; (If installing on GPT/UEFI) --efi-directory=/boot
            "default_kernel" : "<linux-kernel>", # Your Default Linux Kernel
            "platform_Arch" : "<platform-architecture>", # Your Platform Architecture i.e. [ i386-pc | x86_64-efi (for UEFI|GPT)]
        }

    def init_prog_Info(self, program_scriptname, program_appName, program_Type, program_Version, program_Mode, distribution, config_Name="config.yaml"):
        # Initialize Variables
        self.PROGRAM_SCRIPTNAME = program_scriptname
        self.PROGRAM_NAME = program_appName
        self.PROGRAM_TYPE = program_Type
        self.PROGRAM_VERSION = program_Version
        self.MODE = program_Mode # { DEBUG | RELEASE }
        self.DISTRO = distribution
        self.cfg_name = config_Name

    def init_Variables(self):
        """
        Initialize Variables
        """
        # Initialize system variables
        self.default_Var = {
            ## Lists
            ### Stores all external scripts created
            "external_scripts" : [],
            ## Associative Array/Dictionaries
            ### Device and Partitions
            "device_Parameters" : {},
            "partition_Configuration" : {},
            "partition_Parameters" : {},
            "partition_Layout" : {},
            ### Mounts
            "mount_Group" : {},
            ### Region & Location
            "location" : {},
            ### Packages
            "pkgs" : {},
            ### User Control
            "user_Info" : {},
            ### Network Configurations
            "network_config" : {},
            ### Operating System Definitions
            "osdef" : {},
            ### Linux Definitions
            "linux" : {},
        }

    def generate_config(self, cfg_fname="config.yaml"):
        """
        Generate a template env config file
        that will contain the variables to be used 
        in the install script
        """
        with open(cfg_fname, "a+") as write_config:
            # write_config.writelines(cfg)
            yaml.dump(self.cfg, write_config) # Dump dictionary object into YAML file
            print("Config file template generated.")
            # Close file after usage
            write_config.close()

    def load_config(self, cfg_fname="config.yaml"):
        """
        Load the specified configuration file

        :: Params
        - cfg_fname : The configuration filename; Leave it empty to use the default configuration filename
            Type: String
            Defaults: config.yaml
        """
        configs = {}
        with open(cfg_fname, "r+") as read_config:
            """
            Read configuration file
            """
            # Load configuration into Dictionary object
            configs = yaml.safe_load(read_config)

            # Close after usage
            read_config.close()
        return configs

    def start(self):
        """
        Start setup
        """
