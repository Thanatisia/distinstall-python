"""
The universal linux distribution bootstrap installation template framework/library core 
"""
import os
import sys
import shutil
from pydistinstall.utils import process, device_management
from pydistinstall.utils.chroot.mount import make_mount_dir, mount_partition
from pydistinstall.utils.chroot.execution import format_chroot_Subprocess, chroot_execute_command, chroot_execute_command_List
from pydistinstall.utils.chroot.io import files as chroot_files
from pydistinstall.utils.io.disk import disk_partition_table_Format, partition_make, partition_filesystem_format, partition_set_Bootable, partition_swap_Enable

class BaseInstallation():
    """
    Core Base Installation class
    """
    def __init__(self,
                 disk_label="", disk_max_size="", partition_scheme=None, mount_paths=None, location=None, user_profile=None,
                 distribution_name="arch", disk_type="hdd", storage_controller="sata", disk_part_table="msdos", bootloader_firmware="bios", base_pkgs=["base","linux","linux-firmware","linux-lts","linux-lts-headers","base-devel","nano","vim","networkmanager","os-prober"],
                 network_cfg_hostname="hostname", bootloader="grub", bootloader_directory="/boot/grub", bootloader_params="", default_kernel="linux", platform="i386-pc",
                 cfg=None, MODE="DEBUG", EDITOR="", TARGET_DISK_NAME="", USER="", SUDO_USER=""):
        # Check if a setup configuration dictionary is provided
        if cfg == None:
            # Data Validation: Null Value Check
            if partition_scheme == None: partition_scheme = {}
            if mount_paths == None: mount_paths = {}
            if location == None: location = {}
            if user_profile == None: user_profile = {}

            # Update the configuration settings 
            self.update_configs(disk_label, disk_max_size, partition_scheme, mount_paths, location, user_profile, 
                            distribution_name, disk_type, storage_controller, disk_part_table, bootloader_firmware, base_pkgs,
                            network_cfg_hostname, bootloader, bootloader_directory, bootloader_params, default_kernel, platform)
        else:
            # Initialize  configurations
            self.set_config_map(cfg)
        # Initialize Environment Variables
        self.update_env_variables(MODE, EDITOR, TARGET_DISK_NAME, USER, SUDO_USER)
        # Initialize Variables
        self.package_manager_config_Path = "/etc/pacman.d"
        self.mirrorlist_file_Name = "{}/mirrorlist".format(self.package_manager_config_Path)
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
        self.package_manager_Configurations = """
#
# /etc/pacman.conf
#
# See the pacman.conf(5) manpage for option and repository directives

#
# GENERAL OPTIONS
#
[options]
# The following paths are commented out with their default values listed.
# If you wish to use different paths, uncomment and update the paths.
#RootDir     = /
#DBPath      = /var/lib/pacman/
#CacheDir    = /var/cache/pacman/pkg/
#LogFile     = /var/log/pacman.log
#GPGDir      = /etc/pacman.d/gnupg/
HoldPkg     = pacman glibc
# If upgrades are available for these packages they will be asked for first
SyncFirst   = pacman
#XferCommand = /usr/bin/curl -C - -f %u > %o
#XferCommand = /usr/bin/wget --passive-ftp -c -O %o %u
#CleanMethod = KeepInstalled
Architecture = auto

# Pacman won't upgrade packages listed in IgnorePkg and members of IgnoreGroup
#IgnorePkg   =
#IgnoreGroup =

#NoUpgrade   =
#NoExtract   =

# Misc options
#UseSyslog
#UseDelta
#TotalDownload
CheckSpace
#VerbosePkgLists

# By default, pacman accepts packages signed by keys that its local keyring
# trusts (see pacman-key and its man page), as well as unsigned packages.
#SigLevel = Optional TrustedOnly

# NOTE: You must run `pacman-key --init` before first using pacman; the local
# keyring can then be populated with the keys of all official Arch Linux
# packagers with `pacman-key --populate archlinux`.

#
# REPOSITORIES
#   - can be defined here or included from another file
#   - pacman will search repositories in the order defined here
#   - local/custom mirrors can be added here or in separate files
#   - repositories listed first will take precedence when packages
#     have identical names, regardless of version number
#   - URLs will have $repo replaced by the name of the current repo
#   - URLs will have $arch replaced by the name of the architecture
#
# Repository entries are of the format:
#       [repo-name]
#       Server = ServerName
#       Include = IncludePath
#
# The header [repo-name] is crucial - it must be present and
# uncommented to enable the repo.
#

# The testing repositories are disabled by default. To enable, uncomment the
# repo name header and Include lines. You can add preferred servers immediately
# after the header, and they will be used before the default mirrors.

#[testing]
#SigLevel = PackageRequired
#Include = /etc/pacman.d/mirrorlist

[core]
SigLevel = PackageRequired
Include = /etc/pacman.d/mirrorlist

[extra]
SigLevel = PackageRequired
Include = /etc/pacman.d/mirrorlist

#[community-testing]
#SigLevel = PackageRequired
#Include = /etc/pacman.d/mirrorlist

[community]
SigLevel = PackageRequired
Include = /etc/pacman.d/mirrorlist

# If you want to run 32 bit applications on your x86_64 system,
# enable the multilib repositories as required here.

#[multilib-testing]
#SigLevel = PackageRequired
#Include = /etc/pacman.d/mirrorlist

#[multilib]
#SigLevel = PackageRequired
#Include = /etc/pacman.d/mirrorlist

# An example of a custom package repository.  See the pacman manpage for
# tips on creating your own repositories.
#[custom]
#SigLevel = Optional TrustAll
#Server = file:///home/custompkgs
        """

    # Callback/Event Utility functions
    def update_configs(self, disk_label:str, disk_max_size:str, partition_scheme:dict, mount_paths:dict, location:dict, user_profile:dict, 
                       distribution_name="arch", disk_type="hdd", storage_controller="sata", disk_part_table="msdos", bootloader_firmware="bios", base_pkgs=["base","linux","linux-firmware","linux-lts","linux-lts-headers","base-devel","nano","vim","networkmanager","os-prober"],
                       network_cfg_hostname="hostname", bootloader="grub", bootloader_directory="/boot/grub", bootloader_params="", default_kernel="linux", platform="i386-pc"):
        """
        Update the setup configurations with updated information

        :: Parameter /Signature/Headers

        :: Format
        {
            "distribution-name" : "[arch]",
            "device_Type" : "<hdd|ssd|flashdrive|microSD>", # Your disk/device/file type; i.e. VHD|HDD|SSD|Flashdrive|Microsd etc
            "storage-controller": "[your-storage-controller (sata|nvme|loop)]",
            "device_Size" : "<x {GB | GiB | MB | MiB}>", # The total disk size
            "disk_Label" : os.environ.get("TARGET_DISK_NAME"), # The disk's name/label (i.e. /dev/sdX for SATA, /dev/nvme0np1 for NVME); Default: uses the environment variable '$TARGET_DISK_NAME'
            "disk_partition_Table" : "", # mbr/msdos | gpt
            "bootloader_firmware" : "", # BIOS | UEFI
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
                "base",
                "linux",
                "linux-firmware",
                "linux-lts",
                "linux-lts-headers",
                "base-devel",
                "nano",
                "vim",
                "networkmanager",
                "os-prober",
            ],
            "location" : {
                "Region" : "<your-region (Asia|US etc)>", # Refer to /usr/share/zoneinfo for your region
                "City" : "<your-city (Singapore etc)>", # Refer to /usr/share/zoneinfo/<your-region> for your City
                "Language" : "<language-code (en_US.UTF-8|en_SG.TF-8 etc)>", # Your Language code - refer to /etc/locale.gen for a list of all language codes
                "KeyboardMapping" : "en_UTF-8", # Your Keyboard Mapping - change this if you use this (TODO: 2022-06-17 2314H : At the moment this is not used)
            },
            "user_ProfileInfo"  : {
                # Contains a dictionary (key-value) mapping of a username to its properties/attributes
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
        """
        self.cfg = {
            "distribution-name" : distribution_name,
            "device_Type" : disk_type, # Your disk/device/file type; i.e. VHD|HDD|SSD|Flashdrive|Microsd etc
            "storage-controller": storage_controller, # Your disk's storage controller (i.e. SATA/AHCI for HDD/VHD/VDI/VMDK, NVME for SSD, loop for loopback devices)
            "device_Size" : disk_max_size, # The total disk size
            "disk_Label" : disk_label, # The disk's name/label (i.e. /dev/sdX for SATA, /dev/nvme0np1 for NVME); Default: uses the environment variable '$TARGET_DISK_NAME'
            "disk_partition_Table" : disk_part_table, # mbr/msdos | gpt
            "bootloader_firmware" : bootloader_firmware, # BIOS | UEFI
            "partition_Scheme" : partition_scheme, # This contains your partition scheme
            "mount_Paths" : mount_paths, # This contains the mount paths mapped to the partition name
            "base_pkgs" : base_pkgs, # Add the packages you want to strap in here
            "location" : location, # contains a dictionay mapping of your system's locales and region information
            "user_ProfileInfo"  : user_profile, # Contains a dictionary (key-value) mapping of a username to its properties/attributes
            "networkConfig_hostname" : network_cfg_hostname, # Similar to workspace group name, used in /etc/hostname
            "bootloader" : bootloader, # Your bootloader, at the moment - supported bootloaders are [grub, syslinux], tested: [grub] (TODO: 2022-06-17 2317H : Add more bootloaders (if available))
            "bootloader_directory" : bootloader_directory, # Your Bootloader's boot mount point; Certain bootloaders (i.e. Grub) have different boot directories based on partition table (i.e. MBR/GPT); Default: /boot/<your-bootloader>
            "bootloader_Params" : bootloader_params, # Your Bootloader Parameters - fill this if you have any, leave empty if NIL; (If installing on GPT/UEFI) --efi-directory=/boot
            "default_kernel" : default_kernel, # Your Default Linux Kernel
            "platform_Arch" : platform, # Your Platform Architecture i.e. [ i386-pc | x86_64-efi (for UEFI|GPT)]
        }

    def get_cfg_keys(self):
        """
        Get all keys in the 'cfg' global configurations variable
        """
        return list(self.cfg.keys())

    def get_cfg(self, *cfg_keys):
        """
        Get the currently set configurations ccording to the specified keys

        :: Params
        - cfg_keys : List of all configuration keys to pull from the set configs
            + Type: vargs
            - Format
                + String key (1 layer) : get_cfg("key-name")
                + nested Keys (multi-layer) : get_cfg["parent-root-key", "nested-key-1", "nested-key-2", ...])
        """
        # Initialize Variables
        cfg = self.cfg
        results = [cfg]
        disk_Label = cfg["disk_Label"]
        partition_Table = cfg["disk_partition_Table"] # MBR|MSDOS / GPT
        bootloader_firmware = cfg["bootloader_firmware"] # BIOS / UEFI
        dir_Mount = cfg["mount_Paths"]["Root"]
        region = cfg["location"]["Region"]
        city = cfg["location"]["City"]
        language = cfg["location"]["Language"]
        keyboard_mapping = cfg["location"]["KeyboardMapping"]
        hostname = cfg["networkConfig_hostname"]
        default_Kernel = cfg["default_kernel"]
        bootloader = cfg["bootloader"]
        bootloader_directory = cfg["bootloader_directory"]
        bootloader_optional_Params = cfg["bootloader_Params"]
        bootloader_target_device_Type = cfg["platform_Arch"]

        # Iterate through passed configuration keys
        for i in range(len(cfg_keys)):
            # Get current key
            curr_key = cfg_keys[i]

            # Check the type of the key
            match curr_key:
                case list():
                    ## List element
                    parent_key = curr_key[0] # Get the root key
                    parent_root_val = self.cfg[parent_key] # Get the value mapped to the root key
                    nested_subkeys = curr_key[1:] # Get the child subkeys under the parent key

                    curr_res_val = ""
                    curr_subkey_val = parent_root_val

                    # Iterate the key and subkeys
                    for j in range(len(nested_subkeys)):
                        # Get current subkey
                        curr_subkey = nested_subkeys[j]

                        # Get value of of subkey
                        curr_subkey_val = curr_subkey_val[curr_subkey]

                        # Set the previous value as the current value
                        curr_res_val = curr_subkey_val
                case str():
                    ## String element
                    curr_res_val = self.cfg[curr_key]
                case _:
                    # Invalid type; Default
                    curr_res_val = ""

            # Append into results
            results.append(curr_res_val)

        return results

    def set_config_map(self, cfg):
        """
        Update the configurations dictionary (Key-value mapping) with an updated configuration
        """
        self.cfg = cfg.copy()

    def update_env_variables(self, MODE="DEBUG", EDITOR="", TARGET_DISK_NAME="", USER="", SUDO_USER=""):
        """
        Update Environment Variables
        """
        if MODE != "": 
            self.MODE = MODE
        else:
            self.MODE = os.environ.get("MODE") # Runtime boot mode - DEBUG|RELEASE

        if EDITOR != "": 
            self.EDITOR = EDITOR
        else:
            self.EDITOR = os.environ.get("EDITOR")

        if TARGET_DISK_NAME != "": # The target disk's label (i.e. /dev/sdX for SATA|AHCI, or /dev/nvme0np1 for NVME)
            self.TARGET_DISK_NAME = TARGET_DISK_NAME
        else:
            self.TARGET_DISK_NAME = os.environ.get("TARGET_DISK_NAME")

        if USER != "": # Name of regular user
            self.USER = USER
        else:
            self.USER = os.environ.get("USER") 

        if SUDO_USER != "": # Name of superuser
            self.SUDO_USER = SUDO_USER
        else:
            self.SUDO_USER = os.environ.get("SUDO_USER")

    def print_configurations(self):
        print(self.cfg)

    # Installation stages
    def verify_network(self, ping_Count=5, ipv4_address="8.8.8.8"):
        """
        Step 1: Verify that the host network is working

        :: Params
        - ping_Count : The number of times (counts) the system will ping the target address
            Type: Integer
            Default Value: 5

        - ipv4_address : The IPv4 network address you wish to ping
            Type: String
            Default Value: 8.8.8.8
        """
        # Initialize Variables
        cmd_str = "ping -c {} {}".format(ping_Count, ipv4_address)
        res = False

        # Begin pinging a network and check if there's a response
        ret_Code:int = os.system(cmd_str)
        if ret_Code != 0:
            # Success
            res=True

        # Output
        return res

    def verify_boot_Mode(self):
        """
        Verify motherboard bootloader firmware

        :: Information
        [Boot Mode]
        - BIOS : Legacy
        - UEFI : Modern Universal EFI mode

        :: Output
        - boot_Mode : Returns the boot mode of the system
            Default: bios
            Checks for: uefi

        - result : List of subprocess output elements
            1 : stdout (Standard Output)
                Type: String
            2 : stderr (Standard Error)
                Type: String
            3 : Result/Return Status Code
                Type: Integer
        """
        # Initialize Variables
        boot_Mode:str = "bios"
        target_dir:str = "/sys/firmware/efi/efivars"

        # Check if UEFI directory is located
        if os.path.isdir(target_dir):
            # Directory is found
            boot_Mode = "uefi"

        return boot_Mode

    def update_system_Clock(self):
        """
        Sync NTP
        """
        # Initialize Variables
        ret_Code = 0
        cmd_set_NTP = "timedatectl set-ntp true"
        cmd_check_NTP = "timedatectl status"
        success_flag = False
        stdout = ""
        stderr = ""
        returncode = 0

        # Set NTP
        stdout, stderr, returncode = process.subprocess_Sync(cmd_set_NTP)

        if stderr == "":
            # To check system clock
            stdout, stderr, returncode = process.subprocess_Sync(cmd_check_NTP)

            if returncode == 0:
                # Successfully set system clock
                success_flag = True
            else:
                # Error setting system clock
                success_flag = False

        return stdout, stderr, returncode, success_flag

    def disk_get_information(self, cfg):
        """
        Get the currently-set disk and partition information, such as
        - disk: disk label, disk device type, storage controller
        - partition: partition table, partition scheme
        """
        # Obtain Configuration Key-Values
        disk_Label = cfg["disk_Label"]
        partition_Table = cfg["disk_partition_Table"]
        partition_Scheme = cfg["partition_Scheme"].copy()

        # Check Device Type (i.e. sdX, nvme, loop)
        device_medium_Type = cfg["device_Type"]
        storage_controller = cfg["storage-controller"]

        return [disk_Label, partition_Table, partition_Scheme, device_medium_Type, storage_controller]

    def disk_partitions_create(self, partition_Table, disk_Label, storage_controller, partition_Scheme):
        """
        Create the partitions in the disk's partition scheme and store the partition information in the results list of dictinary
        """
        # Initialize Variables
        cmd_str = ""
        res = []

        # Iterate through all partition rows and properties
        for k,v in partition_Scheme.items():
            part_ID = k
            part_Name = v[0] # General name if MBR/MSDOS, Partition Label for UUID if GPT/UEFI
            part_Type = v[1] # Primary, Logical, Extended etc etc
            part_filesystem = v[2] # ext4, btrfs etc etc
            part_start_Size = v[3]
            part_end_Size = v[4]
            part_Bootable = v[5]
            part_Others = v[6]

            # Initialize Current Dictionary/Mapping
            curr_partition_res = {
                "partition" : {
                    "id" : part_ID, 
                    "name" : part_Name, 
                    "type" : part_Type, 
                    "filesystem" : part_filesystem, 
                    "start-size" : part_start_Size,
                    "end-size" : part_end_Size,
                    "bootable" : part_Bootable,
                    "others" : part_Others
                }
            }

            """
            Making Partitions
            """
            cmd_str = ""
            stdout = ""
            stderr = ""
            returncode = 0
            ## Check if disk label/partition table is MBR or GPT
            if (partition_Table == "msdos") or (partition_Table == "mbr"):
                # Create Partition
                cmd_str, stdout, stderr, returncode = partition_make(disk_Label, part_Type, part_filesystem, part_start_Size, part_end_Size)
            elif (partition_Table == "gpt"):
                # Create Partition using partition label instead of primary,extended or logical
                cmd_str, stdout, stderr, returncode = partition_make(disk_Label, part_Name, part_filesystem, part_start_Size, part_end_Size)

            # Map partition creation
            curr_partition_res["partition-create"] = {"command":cmd_str, "stdout" : stdout, "stderr" : stderr, "rc" : returncode}

            """
            Format partition file system
            """
            cmd_str = ""
            stdout = ""
            stderr = ""
            returncode = 0
            # Format the current partition filesystem
            cmd_str, stdout, stderr, returncode = partition_filesystem_format(disk_Label, storage_controller, part_ID, part_filesystem)

            # Map file system formatting
            curr_partition_res["partition-filesystem-format"] = {"command":cmd_str, "stdout" : stdout, "stderr" : stderr, "rc" : returncode}

            """
            Append dictionary into results list
            """
            res.append(curr_partition_res)

        # Output/Return
        return res

    def format_disk_partition_table(self, disk_Label, partition_Table, uInput_fmt_query="> Would you like to format the disk's partition table? [Y|N]: "):
        """
        Format the partition table of the provided disk lable
        """
        # Initialize Variables

        # Get user's confirmation
        format_conf = input(uInput_fmt_query)
        # Process confirmation
        if (format_conf == "Y") or (format_conf == ""):
            ## Format
            print("(+) Formatting [{}] to [{}]...".format(disk_Label, partition_Table))
            if self.MODE != "DEBUG":
                cmd_str, stdout, stderr, returncode = disk_partition_table_Format(disk_Label, partition_Table)

                # Process status/return code
                if returncode == 0:
                    # Success
                    print("[*] Standard Output: {}".format(stdout))
                else:
                    # Error
                    print("[X] Error executing [{}]: {}".format(cmd_str, stderr))
        else:
            print("[INFO] Skipping disk partition table label formatting")

    def make_partition_scheme(self, disk_Label, storage_controller, partition_Scheme, partition_Table):
        """
        Create the partitions specified in the partition scheme dictionary for the provided disk label and
        Format the filesystems of the partitions specified in the partition scheme
        """
        format_conf = input("> Would you like to format the disk's partition scheme/layout? [Y|N]: ")
        if (format_conf == "Y") or (format_conf == ""):
            ## Format
            res = self.disk_partitions_create(partition_Table, disk_Label, storage_controller, partition_Scheme)

            ## Iterate through the partitions
            for i in range(len(res)):
                # Get current partition specification
                curr_partition = res[i]
                curr_part_spec = curr_partition["partition"]

                # Get the results of the partition creation and formatting flow
                curr_part_create_res = curr_partition["partition-create"]
                curr_part_format_fs_res = curr_partition["partition-filesystem-format"]

                ## Get current parttion specification as variables
                curr_part_id = curr_part_spec["id"]
                curr_part_name = curr_part_spec["name"]
                curr_part_type = curr_part_spec["type"]
                curr_part_fs = curr_part_spec["filesystem"]
                curr_part_start_size = curr_part_spec["start-size"]
                curr_part_end_size = curr_part_spec["end-size"]
                curr_part_bootable = curr_part_spec["bootable"]
                curr_part_others = curr_part_spec["others"]

                # Set partition as bootable
                if curr_part_bootable == True:
                    # Begin execution
                    cmd_str, stdout, stderr, returncode = partition_set_Bootable(partition_Table, disk_Label, curr_part_id)

                    # Process status/return code
                    if returncode == 0:
                        # Success
                        print("[*] Standard Output: {}".format(stdout))
                    else:
                        # Error
                        print("[X] Error executing [{}]: {}".format(cmd_str, stderr))

                ## Check Swap partition
                if curr_part_fs == "swap":
                    # Begin execution
                    ## Perform Swap partition formatting
                    cmd_str, stdout, stderr, returncode  = partition_swap_Enable(disk_Label, curr_part_id)

                    # Process status/return code
                    if returncode == 0:
                        # Success
                        print("[*] Standard Output: {}".format(stdout))
                    else:
                        # Error
                        print("[X] Error executing [{}]: {}".format(cmd_str, stderr))

    def make_partition_mount_dir_Root(self, root_Dir):
        """
        Make the root partition's mount directory
        """
        # Initialize Variables
        cmd_str = ""
        stdout = ""
        stderr = ""
        returncode = -1

        ## Create directories if does not exists
        if not (os.path.isdir(root_Dir)):
            ### Directory does not exist
            stdout = "Directory {} does not exist, creating directory...".format(root_Dir)

            if self.MODE != "DEBUG":
                # Make root mount directory
                cmd_str, stdout, stderr, returncode = make_mount_dir(root_Dir)
        else:
            stderr = "Directory {} exists.".format(root_Dir)

        # Output
        return [cmd_str, stdout, stderr, returncode]

    def make_partition_mount_dir_Boot(self, boot_Dir):
        """
        Make the boot partition's mount directory
        """
        # Initialize Variables
        cmd_str = ""
        stdout = ""
        stderr = ""
        returncode = -1

        ## Create directories if does not exists
        if not (os.path.isdir(boot_Dir)):
            ### Directory does not exist
            stdout = "Directory {} does not exist, creating directory...".format(boot_Dir)

            if self.MODE != "DEBUG":
                # Make root mount directory
                cmd_str, stdout, stderr, returncode = make_mount_dir(boot_Dir)
        else:
            stderr = "Directory {} exists.".format(boot_Dir)

        # Output
        return [cmd_str, stdout, stderr, returncode]

    def make_partition_mount_dir_Others(self,mount_Dir):
        """
        Make the target partition's mount directory
        """
        # Initialize Variables
        cmd_str = ""
        stdout = ""
        stderr = ""
        returncode = -1

        ## Create directories if does not exists
        if not (os.path.isdir(mount_Dir)):
            ### Directory does not exist
            stdout = "Directory {} does not exist, creating directory...".format(mount_Dir)

            if self.MODE != "DEBUG":
                # Make root mount directory
                cmd_str, stdout, stderr, returncode = make_mount_dir(mount_Dir)
        else:
            stderr = "Directory {} exists.".format(mount_Dir)

        # Output
        return [cmd_str, stdout, stderr, returncode]

    def mount_partition_Root(self, disk_Label, root_Dir, partition_Scheme, storage_controller, partition_Name="Root", partition_Number=1):
        """
        Mount Root Partition

        :: Params
        - root_Dir : The root partition mount path
            Type: String

        - partition_Scheme : Key-Value Mapping of the partition scheme design
            Type: Dictionary

        - partition_Name : Name of the current partition
            Type: String
            Default: Root

        - partition_Number : The partition number
            Type: Integer
            Default: 1
        """
        # Initialize Variables

        # Make root mount directory if it doesnt exist
        cmd_str, stdout, stderr, returncode = self.make_partition_mount_dir_Root(root_Dir)
        # Process status/return code
        if returncode == 0:
            # Success
            print("[*] Standard Output: {}".format(stdout))
        else:
            # Error
            print("[X] Error executing [{}]: {}".format(cmd_str, stderr))

        ## --- Processing
        ### Mount the volume to the path
        #### Get information of current partition
        target_Partition = partition_Name
        curr_part_Number = partition_Number

        ##### Search for partition number of the Root partition
        print("Partition Scheme: {}".format(partition_Scheme))
        for k,v in partition_Scheme.items():
            # Get key-value
            part_ID = k
            part_Defn = v

            # Get definition
            part_Name = v[0]

            # Find the Root partition
            if part_Name == target_Partition:
                # Found
                curr_part_Number = part_ID
                break

        ### Obtain current partition's filesystem
        curr_filesystem = partition_Scheme[curr_part_Number][2]

        ### Prepare and Format Partition according to Device Storage Controller Type for Root partition
        target_disk_root_Part = device_management.format_partition_str(disk_Label, curr_part_Number, storage_controller)

        if self.MODE != "DEBUG":
            print("Current Filesystem [Root] => [{}]".format(curr_filesystem))
            cmd_str, stdout, stderr, returncode = mount_partition(curr_filesystem, root_Dir, target_disk_root_Part)
            # Process status/return code
            if returncode == 0:
                # Success
                print("Partition [Root] Mounted.")
            else:
                # Error
                print("Error mounting Partition [Root]: [{}]".format(stderr))

        ### Unset/Remove Root partition from mount list
        partition_Scheme.pop(curr_part_Number)

    def mount_partition_Boot(self, disk_Label, boot_Dir, partition_Scheme, storage_controller, partition_Name="Boot", partition_Number=2):
        """
        Mount Boot Partition

        :: Params
        - root_Dir : The root partition mount path
            Type: String

        - partition_Scheme : Key-Value Mapping of the partition scheme design
            Type: Dictionary

        - partition_Name : Name of the current partition
            Type: String
            Default: Root

        - partition_Number : The partition number
            Type: Integer
            Default: 1
        """
        # Initialize Variables

        # Make boot mount directory if it doesnt exist
        cmd_str, stdout, stderr, returncode = self.make_partition_mount_dir_Boot(boot_Dir)
        # Process status/return code
        if returncode == 0:
            # Success
            print("[*] Standard Output: {}".format(stdout))
        else:
            # Error
            print("[X] Error making directory [{}]: [{}]".format(boot_Dir, stderr))

        ## --- Processing
        ### Mount the volume to the path
        #### Get information of current partition
        target_Partition = partition_Name
        curr_part_Number = partition_Number

        ##### Search for partition number of the Root partition
        print("Partition Scheme: {}".format(partition_Scheme))
        for k,v in partition_Scheme.items():
            # Get key-value
            part_ID = k
            part_Defn = v

            # Get definition
            part_Name = part_Defn[0]

            # Find the Root partition
            if part_Name == target_Partition:
                # Found
                curr_part_Number = part_ID
                break

        curr_filesystem = partition_Scheme[curr_part_Number][2]

        ## --- Processing
        ### Mount the volume to the path
        #### Prepare and Format Partition according to Device Storage Controller Type for Boot partition
        target_disk_boot_Part = device_management.format_partition_str(disk_Label, curr_part_Number, storage_controller)

        print("Current Filesystem [Boot] => [{}]".format(curr_filesystem))
        if self.MODE != "DEBUG":
            cmd_str, stdout, stderr, returncode = mount_partition(curr_filesystem, boot_Dir, target_disk_boot_Part)
            # Process status/return code
            if returncode == 0:
                # Success
                print("Partition [Boot] Mounted.")
            else:
                # Error
                print("Error mounting Partition [Boot]: [{}]".format(stderr))

        ### Unset/Remove Boot partition from mount list
        partition_Scheme.pop(curr_part_Number)

    def mount_partition_Remaining(self, disk_Label, mount_Paths, partition_Scheme, storage_controller):
        """
        Mount all other partitions

        :: Params
        - disk_Label : The target disk you wish to write into
            Type: String

        - partition_Scheme : Key-Value Mapping of the partition scheme design
            Type: Dictionary

        - storage_controller : The type of storage controller your device/disk uses
            Data Type: String
            Controllers:
                SATA
                NVME
                Loop
        """
        print("Partition Scheme: {}".format(partition_Scheme))
        for k,v in partition_Scheme.items():
            part_ID = k
            part_Defn = v

            # Get attributes
            part_Name = v[0]
            part_Type = v[1]
            part_filesystem = v[2]

            # Get mount directory/path
            part_mount_dir = mount_Paths[part_Name]

            # Make mount directories if it doesnt exist
            cmd_str, stdout, stderr, returncode = self.make_partition_mount_dir_Others(part_mount_dir)
            # Process status/return code
            if returncode == 0:
                # Success
                print("[*] Standard Output: {}".format(stdout))
            else:
                # Error
                print("[X] Error making directory [{}]: [{}]".format(part_mount_dir, stderr))

            ## --- Processing
            ### Prepare and Format Partition according to Device Storage Controller Type for the current partition
            target_disk_curr_Part = device_management.format_partition_str(disk_Label, part_ID, storage_controller)

            ### Mount the volume to the path
            print("Current Filesystem [{}] => [{}]".format(part_Name, part_filesystem))
            if self.MODE != "DEBUG":
                cmd_str, stdout, stderr, returncode = mount_partition(part_filesystem, part_mount_dir, target_disk_curr_Part)
                # Process status/return code
                if returncode == 0:
                    # Success
                    print("Partition [{}] Mounted.".format(part_Name))
                else:
                    # Error
                    print("Error mounting Partition [{}]: [{}]".format(part_Name, stderr))

            print("")

    def mount_Disks(self):
        """
        Mount Disks and Partitions
        """
        
        # --- Input
        # Local Variables
        cfg = self.cfg
        disk_Label = cfg["disk_Label"]
        partition_Scheme = cfg["partition_Scheme"].copy()
        partition_Table = cfg["disk_partition_Table"]
        device_medium_Type = cfg["device_Type"]
        storage_controller = cfg["storage-controller"]
        mount_Paths = cfg["mount_Paths"]
        
        print("")

        """
        Mount Root Partition
        """
        mount_dir_Root = mount_Paths["Root"]
        self.mount_partition_Root(disk_Label, mount_dir_Root, partition_Scheme, storage_controller, "Root", 1)

        print("")

        """
        Mount Boot Partition
        """
        mount_dir_Boot = mount_Paths["Boot"]
        self.mount_partition_Boot(disk_Label, mount_dir_Boot, partition_Scheme, storage_controller, "Boot", 2)
        
        print("")

        """
        Mount remaining Partitions
        """
        self.mount_partition_Remaining(disk_Label, mount_Paths, partition_Scheme, storage_controller)

    def select_Mirrors(self, mirrorlist_Path):
        """
        Select Mirrors (WIP)
        """
        print("==============")
        print("Select Mirrors")
        print("==============")
        print("(S) Selecting mirrors...")
        print("{} {}".format(self.EDITOR, mirrorlist_Path))
        print("(D) Mirror selected.")

    def check_package_manager_Configurations(self, mount_Dir):
        """
        Check Package Manager configuration support
        """
        # Initialize Variables
        package_manager_conf_Name = "pacman.conf"
        package_manager_conf_Path = "{}/{}".format(mount_Dir, "etc")
        package_manager_conf_File = "{}/{}".format(package_manager_conf_Path, package_manager_conf_Name)

        # Check if pacman.conf file exists
        while not(os.path.isfile(package_manager_conf_File)):
            # pacman.conf does not exists
            print("Obtaining configuration file {}...".format(package_manager_conf_Name))
            # Copy from host into system
            if self.MODE != "DEBUG":
                shutil.copy2("/etc/pacman.conf", package_manager_conf_File) # Copy script from host to the bootstrapped root filesystem

            # Check if file exists now
            if os.path.isfile(package_manager_conf_File):
                # File exists now
                break
            else:
                # Write configuration template to file
                with open(package_manager_conf_File, "w") as generate_pkg_manager_Config:
                    # Write file
                    generate_pkg_manager_Config.write(self.package_manager_Configurations)

                    # Close file after usage
                    generate_pkg_manager_Config.close()

    def bootstrap_Install(self):
        """
        Bootstrap all essential and must have packaes to mount (/mnt) before the chroot process
        
        [Essential Package Categories]
          Text Editor
          Development
          networkmanager
          Kernels
        """
        # --- Initialize Variables
        # Local Variables
        cfg = self.cfg
        base_packages = cfg["base_pkgs"]
        mount_Point = cfg["mount_Paths"]["Root"]
        stdout = None
        stderr = None
        resultcode = -1
        success_Flag = False

        # --- Processing
        cmd_str = ["pacstrap", mount_Point, *base_packages]

        ## Begin bootstrapping
        stdout, stderr, resultcode = process.subprocess_realtime_print(cmd_str, verbose=True)
        # resultcode = os.system(cmd_str)

        # Check result code
        if resultcode == 0:
            success_Flag = True

        return stdout, stderr, resultcode

    def verify_package_manager_configurations(self):
        """
        Verify Package Manager Configurations
        """
        mount_Point = self.cfg["mount_Paths"]["Root"]
        # Check package manager configuration file
        self.check_package_manager_Configurations(mount_Point)

    def fstab_Generate(self):
        """
        Generate File System Table (fstab)
        """
        # --- Input
        # Local Variables
        cfg = self.cfg
        disk_Label = cfg["disk_Label"]
        mount_Points = cfg["mount_Paths"]
        partition_Scheme = cfg["partition_Scheme"].copy()
        dir_Mount = mount_Points["Root"] # Look for root/mount partition
        fstab_Contents = []
        success_Flag = False
        stderr = ""

        # Generate an fstab file (use -U or -L to define by UUID or labels, respectively):
        # cmd_str = "genfstab -U {}".format(dir_Mount)

        # Execute and get fstab content from command and write into /etc/fstab
        try:
            # Obtain disk block information
            block_Info:dict = device_management.get_block_Information(disk_Label)
            curr_disk_block_info = block_Info[disk_Label]

            ## Begin generating filesystems table
            if len(curr_disk_block_info) > 0:
                # Success
                # Generate filesystems table
                fstab_Contents = device_management.design_filesystems_Table(disk_Label, \
                        dir_Mount, \
                        curr_disk_block_info, \
                        partition_Scheme, \
                        mount_Points \
                )

                # Write into [mount-point]/etc/fstab
                with open("{}/etc/fstab".format(dir_Mount), "a+") as write_fstab:
                    # Write fstab content into file
                    write_fstab.writelines(fstab_Contents)

                    # Close file after usage
                    write_fstab.close()

            success_Flag = True
        except Exception as ex:
            stderr = ex

        return [success_Flag, stderr]

    """
    Chroot Actions
    """
    def sync_Timezone(self, mount_Dir, region, city):
        """
        Synchronize Hardware Clock in chroot
        """
        # Initialize Variables
        chroot_commands = [
            # "echo ======= Time Zones ======"												            # Step 10: Time Zones
            "ln -sf /usr/share/zoneinfo/{}/{} /etc/localtime".format(region, city),						# Step 10: Time Zones; Set time zone
            "hwclock --systohc",																        # Step 10: Time Zones; Generate /etc/adjtime via hwclock
        ]

        # Execute list of commands and return the results in a list
        results = chroot_execute_command_List(chroot_commands, mount_Dir)

        # Output
        return results

    def enable_Locale(self, mount_Dir, language):
        """
        Uncomment and Enable locale/region
        """
        chroot_commands = [
            # "echo ======= Location ======"													        # Step 11: Localization;
            "sed -i '/{}/s/^#//g' /etc/locale.gen".format(language), 									# Step 11: Localization; Uncomment locale using sed
            "locale-gen",																	            # Step 11: Localization; Generate the locales by running
            "echo \"LANG={}\" | tee -a /etc/locale.conf".format(language),								# Step 11: Localization; Set LANG variable according to your locale
        ]

        # Execute list of commands and return the results in a list
        results = chroot_execute_command_List(chroot_commands, mount_Dir)

        # Output
        return results

    def network_Management(self, mount_Dir, hostname):
        """
        Append Network Host file
        """
        chroot_commands = [
            # "echo ======= Network Configuration ======"										        # step 12: Network Configuration;
            "echo \"{}\" | tee -a /etc/hostname".format(hostname),										# Step 12: Network Configuration; Set Network Hostname Configuration; Create hostname file
            "echo \"127.0.0.1   localhost\" | tee -a /etc/hosts",							            # Step 12: Network Configuration; Add matching entries to hosts file
            "echo \"::1         localhost\" | tee -a /etc/hosts",							            # Step 12: Network Configuration; Add matching entries to hosts file
            "echo \"127.0.1.1   {}.localdomain	{}\" | tee -a /etc/hosts".format(hostname, hostname),	# Step 12: Network Configuration; Add matching entries to hosts file
        ]

        # Execute list of commands and return the results in a list
        results = chroot_execute_command_List(chroot_commands, mount_Dir)

        # Output
        return results

    def initialize_Ramdisk(self, mount_Dir, default_Kernel="linux"):
        """
        Format initial ramdisk
        """
        # Initialize Variables
        chroot_commands = [
            # "echo ======= Make Initial Ramdisk ======="										        # Step 13: Initialize RAM file system;
            "mkinitcpio -P {}".format(default_Kernel),												    # Step 13: Initialize RAM file system; Create initramfs image (linux-lts kernel)
        ]

        # Execute list of commands and return the results in a list
        results = chroot_execute_command_List(chroot_commands, mount_Dir)

        # Output
        return results

    def set_root_Password(self, mount_Dir):
        """
        Set Root Password
        """
        # Initialize Variables
        str_root_passwd_change = "passwd || passwd;"
        cmd_root_passwd_change = format_chroot_Subprocess(str_root_passwd_change, mount_Dir)
        stdout = []
        stderr = []
        resultcode = 0
        result = {
            "stdout" : [],
            "stderr" : [],
            "resultcode" : -1,
            "command-string" : ""
        }

        # Open the subprocess and return the process pipe
        proc = process.subprocess_Open(cmd_root_passwd_change, stdout=process.PIPE)

        # While the process is still working
        line = ""
        is_alive = proc.poll()
        while is_alive is None:
            # Still working

            # Check if standard output stream is empty
            if proc.stdout != None:
                line = proc.stdout.readline().decode("utf-8")

                # Check if line is empty
                if line != "":
                    # Append line to standard output
                    stdout.append(line)

            # Check if standard input stream is empty
            if proc.stdin != None:
                # Check if line is entered
                if line != "":
                    # Enter your secret line into the tty
                    proc.stdin.write('{}\n'.format(line))

                    # Enter one more time
                    proc.stdin.write('{}\n'.format(line)) # Write this buffer string into the process' stdin

                    # Flush the standard input stream
                    proc.stdin.flush()

            # Poll and check if is alive
            # If poll == None: Alive, else not Alive
            is_alive = proc.poll()
            # print("Status: {}".format(is_alive))

        # Get output, error and status code
        # stdout = proc.stdout
        stderr = proc.stderr
        resultcode = proc.returncode

        # Map/Append result results
        result["stdout"] = stdout
        result["stderr"] = stderr
        result["resultcode"] = resultcode
        result["command-string"] = cmd_root_passwd_change

        return result

    def format_cmds_for_subprocess_exec(self, *cmds):
        """
        Format the provided command strings into a chroot command string and return in a accumulated list of command lists
        """
        # Initialize Variables
        results = []

        # Check number of commands provided
        if len(cmds) == 1:
            # String
            # Get current command
            curr_cmd_str = cmds[0]
            # Split the commands into a list
            curr_cmd_spl = curr_cmd_str.split()
            # Set the split list into result
            results = curr_cmd_spl
        else:
            # List of commands
            for i in range(len(cmds)):
                # Get current command
                curr_cmd_str = cmds[i]
                # Split the commands into a list
                curr_cmd_spl = curr_cmd_str.split()
                # Append result into the results list
                results.append(curr_cmd_spl)

        # Return
        return results

    def prepare_bootloader_Packages(self, bootloader="grub", partition_Table="msdos"):
        """
        Prepare and consolidate the bootloader packages and return the command to install/execute
        """
        # Initialize Variables
        chroot_commands = []

        # Switch Case bootloader between grub and syslinux
        match bootloader:
            case "grub":
                # Setup bootloader
                chroot_commands.append(["pacman", "-S", "grub"]) # Install Grub Package

                # Check if partition table is GPT
                if partition_Table == "gpt":
                    # Install GPT/(U)EFI dependencies
                    chroot_commands.append(["pacman", "-S", "efibootmgr"])
            case "syslinux":
                ### Syslinux bootloader support is currently still a WIP and Testing
                chroot_commands.append(["pacman", "-S", "syslinux"])

        # --- Processing

        # Return/output
        return chroot_commands

    def install_bootloader_Packages(self, chroot_commands, dir_Mount="/mnt"):
        """
        Install bootloader packages using the prepared command string
        """
        # Initialize Variables
        result = []

        # Check if commands are provided
        if len(chroot_commands) > 0:
            # Iterate through the chroot commands to be executedd
            for i in range(len(chroot_commands)):
                # Get current command
                curr_cmd = chroot_commands[i]

                # Initialize result for current command
                curr_cmd_res = {
                    "stdout" : "",
                    "stderr" : "",
                    "resultcode" : -1,
                    "command-string" : ""
                }

                # Combine into a string
                cmd_str = ";\n".join(curr_cmd)

                # Begin
                curr_cmd_strfmt = ' '.join(curr_cmd)
                results = process.chroot_exec(curr_cmd_strfmt, dir_Mount=dir_Mount)

                # Obtain results value 
                stdout = results["stdout"]
                stderr = results["stderr"]
                resultcode = results["resultcode"]
                cmd_fmt = results["command"]

                # Map/Append result results
                curr_cmd_res["stdout"] = stdout
                curr_cmd_res["stderr"] = stderr
                curr_cmd_res["resultcode"] = resultcode
                curr_cmd_res["command-string"] = cmd_fmt

                # Append current command to the results list
                result.append(curr_cmd_res)

        return result

    def format_boot_dir_cmds(self, bootloader="grub", bootloader_directory="/boot/grub"):
        """
        Prepare the Bootloader directories and Pre-Requisites, as well as the system commands to execute in the new system
        """
        # Initialize Variables
        chroot_commands = []

        # Switch Case bootloader between grub and syslinux
        match bootloader:
            case "grub":
                # Create boot partition directory
                # TODO: This can honestly be a non-subproces command, just use os.mkdir
                chroot_commands.append(["mkdir", "-p", bootloader_directory]) # Create grub folder
            case "syslinux":
                ### Syslinux bootloader support is currently still a WIP and Testing
                # TODO: This can honestly be a non-subproces command, just use os.mkdir and os.copy
                chroot_commands.append(["mkdir", "-p", "/boot/syslinux"])
                chroot_commands.append(["cp", "-r", "/usr/lib/syslinux/bios/*.c32", "/boot/syslinux"])

        # Return/output
        return chroot_commands

    def setup_boot_dir(self, cmd_list, dir_Mount="/mnt"):
        """
        Install and setup the bootloader using the prepared command string
        """
        # Initialize Variables
        result = []

        # Check if commands are provided
        if len(cmd_list) > 0:
            # Iterate through the chroot commands to be executedd
            for i in range(len(cmd_list)):
                # Get current command
                curr_cmd = cmd_list[i]

                # Initialize result for current command
                curr_cmd_res = {
                    "stdout" : "",
                    "stderr" : "",
                    "resultcode" : -1,
                    "command-string" : ""
                }

                # Combine into a string
                cmd_str = ";\n".join(curr_cmd)

                # Begin
                curr_cmd_strfmt = ' '.join(curr_cmd)
                results = process.chroot_exec(curr_cmd_strfmt, dir_Mount=dir_Mount, stderr=process.PIPE)

                # Obtain results value 
                stdout = results["stdout"]
                stderr = results["stderr"]
                resultcode = results["resultcode"]
                cmd_fmt = results["command"]

                # Map/Append result results
                curr_cmd_res["stdout"] = stdout
                curr_cmd_res["stderr"] = stderr
                curr_cmd_res["resultcode"] = resultcode
                curr_cmd_res["command-string"] = cmd_fmt

                # Append current command to the results list
                result.append(curr_cmd_res)

        return result

    def prepare_bootloader_installation(self, disk_Label, bootloader="grub", bootloader_optional_Params="", bootloader_target_Architecture="i386-pc"):
        """
        Prepare the commands required to begin performing a full install of the Bootloader to the new system's Partition Table
        """
        # Initialize Variables
        chroot_commands = []

        # Switch Case bootloader between grub and syslinux
        match bootloader:
            case "grub":
                # Install Bootloader
                chroot_commands.append(["grub-install", "--target={}".format(bootloader_target_Architecture), bootloader_optional_Params, disk_Label])	# Install Grub Bootloader
            case "syslinux":
                ### Syslinux bootloader support is currently still a WIP and Testing
                chroot_commands.append(["extlinux", "--install", "/boot/syslinux"])

        # Return/output
        return chroot_commands

    def begin_bootloader_installation(self, cmd_list, dir_Mount="/mnt"):
        """
        Start the installation of the bootloade to the new system's partition table
        """
        # Initialize Variables
        result = []

        # Check if commands are provided
        if len(cmd_list) > 0:
            # Iterate through the chroot commands to be executedd
            for i in range(len(cmd_list)):
                # Get current command
                curr_cmd = cmd_list[i]

                # Initialize result for current command
                curr_cmd_res = {
                    "stdout" : "",
                    "stderr" : "",
                    "resultcode" : -1,
                    "command-string" : ""
                }

                # Combine into a string
                cmd_str = ";\n".join(curr_cmd)

                # Begin
                curr_cmd_strfmt = ' '.join(curr_cmd)
                results = process.chroot_exec(curr_cmd_strfmt, dir_Mount=dir_Mount, stderr=process.PIPE)

                # Obtain results value 
                stdout = results["stdout"]
                stderr = results["stderr"]
                resultcode = results["resultcode"]
                cmd_fmt = results["command"]

                # Map/Append result results
                curr_cmd_res["stdout"] = stdout
                curr_cmd_res["stderr"] = stderr
                curr_cmd_res["resultcode"] = resultcode
                curr_cmd_res["command-string"] = cmd_fmt

                # Append current command to the results list
                result.append(curr_cmd_res)

        return result

    def prepare_generate_bootloader_configurations(self, disk_Label, bootloader="grub", bootloader_directory="/boot/grub", partition_Table="msdos"):
        """
        Prepare the commands required for the generating of the bootloader configuration files in the new root filesystem
        """

        # Initialize Variables
        chroot_commands = []

        # Switch Case bootloader between grub and syslinux
        match bootloader:
            case "grub":
                # Generate bootloader configuration file
                chroot_commands.append(["grub-mkconfig", "-o", "{}/grub.cfg".format(bootloader_directory)]) # Create grub config
            case "syslinux":
                ### Syslinux bootloader support is currently still a WIP and Testing
                # Check partition table
                if (partition_Table == "msdos") or (partition_Table == "mbr"):
                    chroot_commands.append(["dd", "bs=440", "count=1", "conv=notrunc", "if=/usr/lib/syslinux/bios/mbr.bin", "of={}".format(disk_Label)])
                elif (partition_Table == "gpt"):
                    chroot_commands.append(["sgdisk", disk_Label, "--attributes=1:set:2"])
                    chroot_commands.append(["dd", "bs=440", "conv=notrunc", "count=1", "if=/usr/lib/syslinux/bios/gptmbr.bin", "of={}".format(disk_Label)])

        # Return/output
        return chroot_commands

    def generate_bootloader_Configs(self, cmd_list, dir_Mount="/mnt", bootloader_optional_Params="", bootloader_target_Architecture="i386-pc"):
        """
        Begin generating the bootloader configuration files in the new rootfs boot directory
        """
        # Initialize Variables
        result = []

        # Check if commands are provided
        if len(cmd_list) > 0:
            # Iterate through the chroot commands to be executedd
            for i in range(len(cmd_list)):
                # Get current command
                curr_cmd = cmd_list[i]

                # Initialize result for current command
                curr_cmd_res = {
                    "stdout" : "",
                    "stderr" : "",
                    "resultcode" : -1,
                    "command-string" : ""
                }

                # Combine into a string
                cmd_str = ";\n".join(curr_cmd)

                # Begin
                curr_cmd_strfmt = ' '.join(curr_cmd)
                results = process.chroot_exec(curr_cmd_strfmt, dir_Mount=dir_Mount, stderr=process.PIPE)

                # Obtain results value 
                stdout = results["stdout"]
                stderr = results["stderr"]
                resultcode = results["resultcode"]
                cmd_fmt = results["command"]

                # Map/Append result results
                curr_cmd_res["stdout"] = stdout
                curr_cmd_res["stderr"] = stderr
                curr_cmd_res["resultcode"] = resultcode
                curr_cmd_res["command-string"] = cmd_fmt

                # Append current command to the results list
                result.append(curr_cmd_res)

        return result

    def bootloader_Management(self, disk_Label, dir_Mount="/mnt", bootloader="grub", bootloader_directory="/boot/grub", partition_Table="msdos", bootloader_optional_Params="", bootloader_target_Architecture="i386-pc"):
        """
        NOTE:
        1. Please Edit [osdef] on top with the bootloader information before proceeding
        """
        # Initialize Variables
        combined_res = []

        # Install Bootloader dependencies and packages
        if self.MODE != "DEBUG":
            # Prepare and format the bootloader packages into a command list
            cmd_list = self.prepare_bootloader_Packages(bootloader, partition_Table)
            # Install bootloader packages
            res = self.install_bootloader_Packages(cmd_list, dir_Mount)
            combined_res.append({"title" : "Installing Bootloader Dependencies : {}".format(bootloader), "commands" : cmd_list, "results" : res})

        # Prepare Boot directory
        if self.MODE != "DEBUG":
            # Format and obtain the commands required to create boot directory
            cmd_list = self.format_boot_dir_cmds(bootloader, bootloader_directory)
            # Begin creating boot directory
            res = self.setup_boot_dir(cmd_list, dir_Mount)
            combined_res.append({"title" : "Generating boot directory : {}".format(bootloader_directory), "commands" : cmd_list, "results" : res})

        # Install Bootloader to partition table
        if self.MODE != "DEBUG":
            # Format and obtain the commands required to install the bootloader to the new disk's partition table
            cmd_list = self.prepare_bootloader_installation(disk_Label, bootloader, bootloader_optional_Params, bootloader_target_Architecture)
            # Begin the installation of the bootloader to the new partition table
            res = self.begin_bootloader_installation(cmd_list, dir_Mount)
            combined_res.append({"title" : "Installing bootloader to partition table : {}".format(bootloader), "commands" : cmd_list, "results" : res})

        # Generate Bootloader configurations
        if self.MODE != "DEBUG":
            # Format and obtain the commands required to generate the bootloader configurations to the new rootfs
            cmd_list = self.prepare_generate_bootloader_configurations(disk_Label, bootloader, bootloader_directory, partition_Table)
            # Begin the generating of the bootloader configurations to the new rootfs
            res = self.generate_bootloader_Configs(cmd_list, dir_Mount, bootloader_optional_Params, bootloader_target_Architecture)
            combined_res.append({"title" : "Generating bootloader configurations : {}".format(bootloader), "commands" : cmd_list, "results" : res})

        # Return output
        return combined_res

    def archive_command_Str(self, cmd_str, dir_Mount="/mnt", archive_script_file="chroot-commas.sh"):
        """
        Output command string into a file for archiving
        """
        # Initialize Variables
        mount_Root="{}/root".format(dir_Mount)
        target_directory = "{}/{}".format(mount_Root, archive_script_file)

        # Write commands into file for reusing
        chroot_files.writelines(cmd_str, dir_Mount, archive_script_file)

    """
    Stage Installation Logic
    """
    def device_partition_Manager(self):
        """
        Device & Partition Manager
        """
        # Initialize Variables
        cfg = self.cfg

        # Begin Filesystem Management
        print("[+] Get User Input - Device Information")
        disk_Label, partition_Table, partition_Scheme, device_medium_Type, storage_controller = self.disk_get_information(cfg)

        print("[+] Format the disk's partition table")
        self.format_disk_partition_table(disk_Label, partition_Table)

        print("[+] Create the partitions in the partition scheme and Format the partition's filesystem types")
        self.make_partition_scheme(disk_Label, storage_controller, partition_Scheme, partition_Table)

        print("(D) Partition Completed. ")

    def chroot_sync_timezone(self):
        """
        Sync the timezone NTP in the chroot rootfs virtual environment
        """
        # Initialize Variables
        cfg = self.cfg
        dir_mount = cfg["mount_Paths"]["Root"]
        region = cfg["location"]["Region"]
        city = cfg["location"]["City"]

        # Synchronize the timezone
        results = self.sync_Timezone(dir_mount, region, city)

        # Return result
        return results

    def chroot_enable_locale(self):
        """
        Enable the locale in the chroot rootfs virtual environment
        """
        # Initialize Variables
        cfg = self.cfg
        dir_mount = cfg["mount_Paths"]["Root"]
        language = cfg["location"]["Language"]

        # Enable locale
        results = self.enable_Locale(dir_mount, language)

        # Output/Return
        return results

    def chroot_network_management(self):
        """
        Perform Network Management in the chroot rootfs virtual environment
        """
        # Initialize Variables
        cfg = self.cfg
        dir_mount = cfg["mount_Paths"]["Root"]
        hostname = cfg["networkConfig_hostname"]

        # Perform Network Management
        results = self.network_Management(dir_mount, hostname)

        # Output/Return
        return results

    def chroot_init_ramdisk(self):
        """
        Initialize I/O Ramdisk in the chroot rootfs virtual environment
        """
        # Initialize Variables
        cfg = self.cfg
        dir_mount = cfg["mount_Paths"]["Root"]
        default_Kernel = cfg["default_kernel"]

        # Initialize ramdisk
        results = self.initialize_Ramdisk(dir_mount, default_Kernel)

        # Output/Return
        return results

    def chroot_set_root_passwd(self):
        """
        Set the root password in the chroot rootfs virtual environment
        """
        # Initialize Variables
        cfg = self.cfg
        dir_mount = cfg["mount_Paths"]["Root"]

        # Set root password
        results = self.set_root_Password(dir_mount)

        # Output/Return
        return results

    def chroot_bootloader_management(self):
        """
        Perform Bootloader Management in the chroot rootfs virtual environment
        """
        # Initialize Variables
        cfg = self.cfg
        disk_Label = cfg["disk_Label"]
        partition_Table = cfg["disk_partition_Table"] # MBR|MSDOS / GPT
        bootloader_firmware = cfg["bootloader_firmware"] # BIOS / UEFI
        dir_Mount = cfg["mount_Paths"]["Root"]
        region = cfg["location"]["Region"]
        city = cfg["location"]["City"]
        language = cfg["location"]["Language"]
        keyboard_mapping = cfg["location"]["KeyboardMapping"]
        hostname = cfg["networkConfig_hostname"]
        default_Kernel = cfg["default_kernel"]
        bootloader = cfg["bootloader"]
        bootloader_directory = cfg["bootloader_directory"]
        bootloader_optional_Params = cfg["bootloader_Params"]
        bootloader_target_device_Type = cfg["platform_Arch"]

        # Perform Bootloader Managemnt in chroot
        combined_res = self.bootloader_Management(disk_Label, dir_Mount, bootloader, bootloader_directory, partition_Table, bootloader_optional_Params, bootloader_target_device_Type)

        # Output/Return
        return combined_res

    def begin_chroot_execution(self):
        """
        Execute commands using arch-chroot due to limitations with shellscripting
        """

        # --- Input
        # Local Variables
        cmd_str = []

        cfg = self.cfg
        dir_Mount = cfg["mount_Paths"]["Root"]

        # Chroot Execute
        ## Synchronize Hardware Clock
        print("(+) Time Zones : Synchronize Hardware Clock")

        if self.MODE != "DEBUG":
            results = self.chroot_sync_timezone()

            # Iterate through the list of command results
            for i in range(len(results)):
                # Get current command's output
                curr_cmd_out = results[i]

                # Process result
                command = curr_cmd_out["command-string"]
                stdout = curr_cmd_out["stdout"].rstrip()
                stderr = curr_cmd_out["stderr"].rstrip()
                resultcode = curr_cmd_out["resultcode"]
                if resultcode == 0:
                    # Success
                    if stdout != "":
                        print("{}".format(stdout))
                else:
                    # Error
                    if stderr != "":
                        print("Error [{}] running command [{}]: {}".format(resultcode, command, stderr))

                # Append command string to compilation
                cmd_str.append(' '.join(command))

        print("")

        ## Enable locale/region
        print("(+) Enable Location/Region")
        if self.MODE != "DEBUG":
            results = self.chroot_enable_locale()

            # Iterate through the list of command results
            for i in range(len(results)):
                # Get current command's output
                curr_cmd_out = results[i]

                # Process result
                command = curr_cmd_out["command-string"]
                stdout = curr_cmd_out["stdout"].rstrip()
                stderr = curr_cmd_out["stderr"].rstrip()
                resultcode = curr_cmd_out["resultcode"]
                if resultcode == 0:
                    # Success
                    if stdout != "":
                        print("{}".format(stdout))
                else:
                    # Error
                    if stderr != "":
                        print("Error [{}] running command [{}]: {}".format(resultcode, command, stderr))

                # Append command string to compilation
                cmd_str.append(' '.join(command))

        print("")

        ## Append Network Host file
        print("(+) Network Configuration")
        if self.MODE != "DEBUG":
            results = self.chroot_network_management()

            # Iterate through the list of command results
            for i in range(len(results)):
                # Get current command's output
                curr_cmd_out = results[i]

                # Process result
                command = curr_cmd_out["command-string"]
                stdout = curr_cmd_out["stdout"].rstrip()
                stderr = curr_cmd_out["stderr"].rstrip()
                resultcode = curr_cmd_out["resultcode"]
                if resultcode == 0:
                    # Success
                    if stdout != "":
                        print("{}".format(stdout))
                else:
                    # Error
                    if stderr != "":
                        print("Error [{}] running command [{}]: {}".format(resultcode, command, stderr))

                # Append command string to compilation
                cmd_str.append(' '.join(command))

        print("")

        ## Format initial ramdisk
        print("(+) Making Initial Ramdisk")
        if self.MODE != "DEBUG":
            results = self.chroot_init_ramdisk()

            # Iterate through the list of command results
            for i in range(len(results)):
                # Get current command's output
                curr_cmd_out = results[i]

                # Process result
                command = curr_cmd_out["command-string"]
                stdout = curr_cmd_out["stdout"].rstrip()
                stderr = curr_cmd_out["stderr"].rstrip()
                resultcode = curr_cmd_out["resultcode"]
                if resultcode == 0:
                    # Success
                    if stdout != "":
                        print("{}".format(stdout))
                else:
                    # Error
                    if stderr != "":
                        print("Error [{}] running command [{}]: {}".format(resultcode, command, stderr))

                # Append command string to compilation
                cmd_str.append(' '.join(command))

        print("")

        # Step 14: User Information - Set Root password
        print("(+) Change Root Password")
        if self.MODE != "DEBUG":
            results = self.chroot_set_root_passwd()

            # Process result
            command = results["command-string"]
            stdout = results["stdout"]
            stderr = results["stderr"]
            resultcode = results["resultcode"] 
            if resultcode == 0:
                # Success
                if len(stdout) > 0:
                    for i in range(len(stdout)):
                        # Get current message
                        curr_line = stdout[i]
                        print("{}".format(curr_line))
            else:
                # Error
                if stderr != "":
                    print("Error [{}] running command [{}]: {}".format(resultcode, command, stderr))

            # Append command string to compilation
            cmd_str.append(' '.join(command))

        print("")
        
        # Step 15: Install Bootloader
        print("(+) Install Bootloader in Chroot")
        if self.MODE != "DEBUG":
            results = self.chroot_bootloader_management()

            # Iterate through the list of command results
            for i in range(len(results)):
                # Get current command's output
                curr_cmd_out = results[i]

                curr_cmd_title = curr_cmd_out["title"]
                curr_cmd = curr_cmd_out["commands"]
                curr_cmd_res = curr_cmd_out["results"]

                print("(+) {}".format(curr_cmd_title))
                for j in range(len(curr_cmd_res)):
                    # Get the individual substeps results
                    curr_substep_res = curr_cmd_res[j]

                    # Process result
                    command = curr_substep_res["command-string"]
                    stdout = curr_substep_res["stdout"].rstrip()
                    stderr = curr_substep_res["stderr"].rstrip()
                    resultcode = curr_substep_res["resultcode"] 

                    # Success
                    if stdout != "":
                        print("{}".format(stdout))

                    # Error
                    if stderr != "":
                        if resultcode == 0:
                            print("{}".format(stderr))
                        else:
                            print("Error [{}] running command [{}]: {}".format(resultcode, command, stderr))

                    # Append command string to compilation
                    cmd_str.append(' '.join(command))

                # Print newline
                print("")
        
        print("")

        # Archive the command string into a file
        print("(+) Archiving command strings into a file for re-usage")
        if self.MODE != "DEBUG":
            target_directory = "/root/chroot-comms.sh"
            print("Writing {} => {}".format(cmd_str, target_directory))
            self.archive_command_Str(cmd_str, dir_Mount, target_directory)

            # Execute in the chroot utility
            # Future Codes deemed stable *enough*, thanks Past self for retaining legacy codes
            # for debugging
            self.default_Var["external_scripts"].append(
                ### Append all external scripts used ###
                os.path.join(dir_Mount, target_directory)
            )

        print("")

    def installer(self):
        """
        Complete setup installer
        """
        print("(S) Starting Base Installation...")

        print("========================")
        print("Stage 1: Prepare Network")
        print("========================")

        print("(S) 1. Testing Network...")
        if self.MODE != "DEBUG":
            network_Enabled = self.verify_network()
            if network_Enabled == False:
                cmd_str = "dhcpcd"
                print("")
                print("Executing: {}".format(cmd_str))

                ## Begin executing commands
                stdout, stderr, returncode = process.subprocess_Sync(cmd_str)
                print("Standard Output: {}".format(stdout))
                print("Standard Error: {}".format(stderr))

                # Verify execution status
                if returncode == 0:
                    # Success
                    print("(+) Network is activated")
                else:
                    # Error
                    print("(-) Error starting Network")
            else:
                print("(+) Network is active")
        else:
            tmp = input("Press anything to continue...")

        print("(D) Network testing completed.")

        print("")

        print("==========================================")
        print("Stage 2: Verify Boot Mode (i.e. UEFI/BIOS)")
        print("==========================================")
        
        print("(S) Verifying Boot Mode...")
        if self.MODE != "DEBUG":
            boot_Mode = self.verify_boot_Mode()
            print("(+) Motherboard bootloader firmware boot mode (bios/uefi): {}".format(boot_Mode))
        else:
            tmp = input("Press anything to continue...")

        print("(D) Boot Mode verification completed.")

        print("")

        print("============================")
        print("Stage 3: Update System Clock")
        print("============================")
        
        print("(S) Updating System Clock...")
        if self.MODE != "DEBUG":
            stdout, stderr, resultcode, success_Flag = self.update_system_Clock()
            if success_Flag == False:
                print("(X) Error updating system clock via Network Time Protocol (NTP)")
            else:
                print("(D) System clock updated.")
        else:
            tmp = input("Press anything to continue...")

        print("")

        print("============================")
        print("Stage 4: Partition the Disks")
        print("============================")
        
        print("(S) Starting Disk Management...")
        if self.MODE != "DEBUG":
            success_Flag = self.device_partition_Manager()
            if success_Flag == False:
                print("(X) Error formatting disk and partitions")
        else:
            tmp = input("Press anything to continue...")
        print("(D) Disk Management completed.")

        print("")

        print("====================")
        print("Stage 5: Mount Disks")
        print("====================")
        
        print("(S) Mounting disks...")
        if self.MODE != "DEBUG":
            success_Flag = self.mount_Disks()
            if success_Flag == False:
                print("(X) Error mounting disks")
            print("(D) Disks mounted.")
        else:
            tmp = input("Press anything to continue...")

        print("")

        print("===================================")
        print("Stage 6: Install essential packages")
        print("===================================")
        print("(S) Strapping packages to mount point...")
        if self.MODE != "DEBUG":
            success_Flag = self.bootstrap_Install()
            if success_Flag == False:
                print("(X) Errors bootstrapping packages")
            print("(D) Packages strapped.")
        else:
            tmp = input("Press anything to continue...")

        # Select Mirror List
        print("Selecting Mirror List (IGNORE)")
        if self.MODE != "DEBUG":
            self.select_Mirrors(self.mirrorlist_file_Name)
        else:
            tmp = input("Press anything to continue...")

        # Verify Package Manager Configurations
        print("Verifying Package Manager Configurations")
        if self.MODE != "DEBUG":
            self.verify_package_manager_configurations()
        else:
            tmp = input("Press anything to continue...")

        print("")

        print("===========================================")
        print("Stage 7: Generate fstab (File System Table)")
        print("===========================================")
        print("(S) Generating Filesystems Table in /etc/fstab")
        if self.MODE != "DEBUG":
            success_Flag, stderr = self.fstab_Generate()
            if success_Flag == False:
                print("(X) Error generating filesystems table: {}".format(stderr))
            print("(D) Filesystems Table generated.")
        else:
            tmp = input("Press anything to continue...")

        print("")

        print("===========================")
        print("Stage 8: Chroot and execute")
        print("===========================")

        print("(S) Executing chroot commands")
        if self.MODE != "DEBUG":
            success_Flag = self.begin_chroot_execution() # Execute commands in arch-chroot
            if success_Flag == False:
                print("(X) Error executing commands in chroot")
            print("(D) Commands executed")
        else:
            tmp = input("Press anything to continue...")

        print("")

        print("=======================")
        print("Installation Completed.")
        print("=======================")

    class Host():
        """
        Host-layer utilities class containing functionalities pertaining to the host system operations while generating the root filesystem
        """

    class Chroot():
        """
        Chroot utilities class containing functionalities pertaining to chroot operations used in the base/root filessystem installation
        """
        def __init__(self, cs_base_install):
            self.cs_base_install = cs_base_install

# =========================== #
# Post-Installation Functions #
# =========================== #
class PostInstallation():
    """
    Class for the Post-Installation functions in the installation library/framework
    """
    def __init__(self, cs_base_install=None, cfg=None, MODE="DEBUG"):
        # Local Variables
        if cs_base_install != None:
            self.cfg = cs_base_install.cfg
            self.default_Var = cs_base_install.default_Var
            self.external_scripts = self.default_Var["external_scripts"]
            number_of_external_scripts = len(self.external_scripts)
            # Initialize defaults from configuration file settings if no base installation object is specified
            self.init_Config(self.cfg, MODE)
        else:
            # Initialize defaults from configuration file settings if no base installation object is specified
            self.init_Config(cfg, MODE)
        dir_Mount = self.cfg["mount_Paths"]["Root"]

    def init_Config(self, cfg, MODE="DEBUG"):
        """
        Initialize defaults from configuration file if base installation is not used
        """
        # Update setup to the latest
        self.update_setup(cfg, MODE)

    # Callback/Event Utility functions
    def update_setup(self, cfg, MODE="DEBUG"):
        self.MODE = MODE
        self.cfg = cfg.copy()

    def print_configurations(self):
        print(self.cfg)

    def postinstall_todo(self):
        msg = """
- Please proceed to follow the 'Post-Installation' series of guides
        and/or
- Follow this list of recommendations:"

[Post-Installation TODO]
1. Enable multilib repository :
    Summary:
        If you want to run 32-bit applications on your 64-bit systems
        Uncomment/enable the multilib repository
    i. Edit '/etc/pacman.conf'
    ii. Uncomment [multilib]
    iii. Uncomment 'include = /etc/pacman.d/mirrorlist' below [multilib]
    WIP:
        - Automatic removal of comments in a file
        
# Command and Control
2. [To validate if is done] Set sudo priviledges
        Summary:
            Ability to use 'sudo'
        i. Use 'visudo' to enter the sudo file safely
            i.e.
                $EDITOR=vim sudo visudo
        ii. Uncomment '%wheel ALL=(ALL) ALL' to allow all users under the group 'wheel' to access sudo (with password)

# Administrative
4. Create user account"
 	Summary:"
 		Create user account"
 	i. Add user using the 'useradd' command"
 		useradd -m -g <primary group (default: <username>) -G <secondary/supplementary groups (default: wheel)> -d <custom-profile-directory-path> <username>"
 		i.e."
 			useradd -m -g wheel -d /home/profiles/admin admin"
 			useradd -m -g users -G wheel -d /home/profiles/admin admin"
 	ii. Set password to username"
 		passwd <username>"
 		i.e."
 			let <username> be 'admin':"
 				passswd admin"
 	iii. Test user"
 		su - <username>"
 		sudo whoami"
 	iv. If part iii works : User has been created."

# System Maintenance
4. Swap File"
		Summary:"
			Instead of using swap partitions which are hard to change size, consider using swap files instead"
			- Easy to resize"
			- Easy to remove"
			- Easy to add/allocate"
		i. Allocate/Create swap file"
			fallocate -l <size> /swapfile # <size> : in formats { MB | MiB | GB | GiB }"
			i.e."
				fallocate -l 8.0GB /swapfile"
		ii. Change permission of swapfile to read + write"
			chmod 600 /swapfile"
		iii. Make swapfile"
			mkswap /swapfile"
		iv. Enable the swap file to begin using it"
			swapon /swapfile"
		v. The operating system needs to know that it is safe to use this file everytime it boots up"
			echo \"# /swapfile\" | tee -a /etc/fstab"
			echo \"/swapfile none swap defaults 0 0\" | tee -a /etc/fstab"
			i.e."
				swapfile size = 4GB"
				fallocate -l 4G /swapfile"
				chmod 600 /swapfile"
				mkswap /swapfile"
				swapon /swapfile"
				echo \"# /swapfile\" | tee -a /etc/fstab"
				echo \"/swapfile none swap defaults 0 0\" | tee -a /etc/fstab"
		vi. Verify swap file"
			ls -lh /swapfile"
		vii. Verify swap file allocation"
			free -h"
		viii. If part vii works : Swap file has been created."
        """
        print(msg)

    def postinstall_sanitize(self):
        """
        ==========================
               Sanitize user      
          To sanitize the account 
        from any unnecessary files
        ==========================
        """
        # Local Variables
        cfg = self.cfg
        dir_Mount = cfg["mount_Paths"]["Root"]
        number_of_external_scripts = len(self.default_Var["external_scripts"])

        print("External Scripts created:")
        for i in range(number_of_external_scripts):
            print("[{}] : [{}]".format(i, self.default_Var["external_scripts"][i]))

        print("")

        action = input("What would you like to do to the root scripts? [(C)opy to user|(D)elete|<Leave empty to do nothing>]: ")
        if (action == "C") or (action == "Copy"):
            users = input("Copy to which user? [(A)ll created users|(S)elect]: ")

            # Copy to stated users
            if (users == "A") or (users == "All"):
                # Loop through all users in user_profiles and
                # See if it exists, follow above documentation
                for u_Name, u_Defn in self.cfg["user_ProfileInfo"].items():
                    # Get individual parameters
                    u_primary_Group = u_Defn[0]         # Primary Group
                    u_secondary_Groups = u_Defn[1]      # Secondary Groups
                    u_home_Dir = u_Defn[2]              # Home Directory
                    u_other_Params = u_Defn[3]          # Any other parameters after the first 3

                    for i in range(number_of_external_scripts):
                        curr_script = self.default_Var["external_scripts"][i]
                        print("Copying from [{}] : {} => {}/{}".format(dir_Mount, curr_script, dir_Mount, u_home_Dir))
                        if self.MODE != "DEBUG":
                            shutil.copy2(curr_script, "{}/{}".format(dir_Mount, u_home_Dir)) # Copy script from root to user
            elif (users == "S") or (users == "Select"):
                # User Input
                sel_uhome = input("User name: ")
                sel_primary_group=""
                sel_uhome_dir=""

                # Check if username is in the dictionary
                if sel_uhome in self.cfg["user_ProfileInfo"]:
                    # Username is in
                    # Get the target's profile info
                    target_user_profile = self.cfg["user_ProfileInfo"][sel_uhome]

                    ## Split and obtain individual parameters
                    u_primary_Group = target_user_profile[0]         # Primary Group
                    u_secondary_Groups = target_user_profile[1]      # Secondary Groups
                    u_home_Dir = target_user_profile[2]              # Home Directory
                    u_other_Params = target_user_profile[3]          # Any other parameters after the first 3

                    # Check if user directory exists
                    dir_to_Validate = "{}/{}".format(dir_Mount, u_home_Dir)
                    if os.path.isdir(dir_to_Validate):
                        ## Directory exists
                        for i in range(number_of_external_scripts):
                            curr_script = self.default_Var["external_scripts"][i]
                            print("Copying from [{}] : {} => {}/{}".format(dir_Mount, curr_script, dir_Mount, u_home_Dir))
                            if self.MODE != "DEBUG":
                                shutil.copy2(curr_script, "{}/{}".format(dir_Mount, u_home_Dir)) # Copy script from root to user
                    else:
                        ## Directory does not exist
                        print("User home directory [{}] does not exist.".format(dir_to_Validate))
                else:
                    print("User {} does not exist.".format(sel_uhome))

            print("")

            # Reset script to let user delete if they want to
            self.postinstall_sanitize()
        elif (action == "D") or (action == "Delete"):
            del_conf = input("Delete the scripts? [(Y)es|(N)o|(S)elect]: ")
            # Yes - Delete
            # No - Nothing
            # Select - Allow user to choose
            if (del_conf == "Y") or (del_conf == "Yes"):
                # Delete all
                for i in range(number_of_external_scripts):
                    if self.MODE == "DEBUG":
                        print("Deleting: {}".format(self.default_Var["external_scripts"][i]))
                    else:
                        os.remove(self.default_Var["external_scripts"][i])
            elif (action == "S") or (action == "Select"):
                # Let user choose
                # Seperate all options with delimiter ','
                print("Please enter all files you wish to delete\n	(Seperate all options with delimiter ',')")
                del_selections = input("> : ")

                # Seperate selected options with ',' delimited
                arr_Selected = del_selections.split(",")

                # Delete selected files if not empty
                if del_selections != "":
                    for sel in arr_Selected:
                        # Delete selected files
                        if self.MODE == "DEBUG":
                            print("Deleting: [{}]".format(self.default_Var["external_scripts"][sel]))
                        else:
                            os.remove(self.default_Var["external_scripts"][sel])
        else:
            print("No action.")

    # User Management
    def get_users_Home(self, user_name):
        """
        Get the home directory of a user

        :: Params
        - user_name : The name of the target user
            Type: String
        """
        # Initialize Variables
        home_dir = ""

        # Validate user name is not empty
        if user_name != "":
            # Not Empty
            # Get the home directory of the user
            cmd_str = "su - {} -c \"echo $HOME\""
            home_dir, stderr, returncode = process.subprocess_Sync(cmd_str)
        return home_dir

    def check_user_Exists(self, user_name):
        """
        Check if user exists
        
        :: Params 
        - user_name : Specify the target user to check if exists
            Type: String
        """
        exist_Token=False
        delimiter=":"
        cmd_res_Existence="getent passwd {}".format(user_name)

        # Check if user exists
        res_Existence, stderr, returncode = process.subprocess_Sync(cmd_res_Existence)

        if res_Existence != "":
            # Something is found
            # Check if is the user
            res_is_User = "echo \"{}\" | grep \"^{}:\" | cut -d ':' -f1".format(res_Existence, user_name)

            if res_is_User == user_name:
                exist_Token = True

        return exist_Token

    def useradd_get_default_Params(self):
        """
        Useradd
            - Get Default Parameters
        """
        # Initialize Variables
        user_params = {
            # Keyword = parameters
            "GROUP" : "",
            "HOME"  : "",
            "INACTIVE" : "",
            "EXPIRE" : "",
            "SHELL" : "",
            "SKEL" : "",
            "CREATE_MAIL_SPOOL" : "",
        }

        # Iterate and loop through all keywords to obtain the default parameter
        for k,_ in user_params.items():
            # Get parameter for specified keyword
            tmp_cmd_str = "useradd -D | grep {} | cut -d '=' -f2".format(k)
            curr_keyword_default_Param, stderr, returncode = process.subprocess_Sync(tmp_cmd_str)

            # Map keyword to result default parameters
            user_params[k] = curr_keyword_default_Param

        # Output
        return user_params

    # Post-Installation Stages
    def enable_sudo(self, dir_Mount="/mnt"):
        """
        Enabling sudo in /etc/sudoers via command line
        """
        # Initialize Variables
        return_val = [] # List containing the list [stdout, stderr, resultcode] for each command output
        postinstall_commands = [
            ### Body ###
            # Enable Sudo
            # PostInstall Must Do | Step 1: Enable sudo for group 'wheel'
            "sed -i 's/^#\\s*\\(%wheel\\s\\+ALL=(ALL:ALL)\\s\\+ALL\\)/\\1/' /etc/sudoers",
        ]

        # Run the currently set commands via chroot
        for i in range(len(postinstall_commands)):
            # Get current cmd
            curr_cmd = postinstall_commands[i]

            # Formulate chroot command
            chroot_cmd_fmt = ["arch-chroot", dir_Mount, "/bin/bash", "-c", curr_cmd]

            print("Executing: {}".format(' '.join(chroot_cmd_fmt)))
            if self.MODE != "DEBUG":
                # Execute command line-by-line
                stdout, stderr, resultcode = process.subprocess_Line(chroot_cmd_fmt, stdin=process.PIPE)

                # Append result to entry
                return_val.append([stdout, stderr, resultcode])

        return return_val

    def postinstallation(self):
        """
        Post-Installation Recommendations and TODOs 
        - To be seperated into its own individual scripts for running
        """ 
        ### Header ###

        # Local Variable
        dir_Mount = self.cfg["mount_Paths"]["Root"] # Look for root/mount partition
        postinstall_commands = []

        # Enable sudo
        print("(+) Enable sudo")
        result = self.enable_sudo(dir_Mount)

        for i in range(len(result)):
            # Get current result
            curr_cmd_result = result[i]

            # Expand out
            stdout, stderr, resultcode = curr_cmd_result

            if resultcode == 0:
                # Success
                print("Standard Output: {}".format(stdout))
            else:
                # Error
                print("Error: {}".format(stderr))

        print("")

        ## User Management and Creation
        # User Management
        print("(+) User Management")

        # Loop through all users in user_profiles and
        # See if it exists, follow above documentation
        for u_Name, u_Defn in self.cfg["user_ProfileInfo"].items():
            # Get individual parameters
            u_primary_Group = u_Defn[0]         # Primary Group
            u_secondary_Groups = u_Defn[1]      # Secondary Groups
            u_home_Dir = u_Defn[2]              # Home Directory
            u_other_Params = u_Defn[3]          # Any other parameters after the first 3

            # Check if user exists
            print("(+) Checking for user {}...".format(u_Name))
            if self.MODE == "DEBUG":
                u_Exists = ""
            else:
                # Check if user exists | Empty if Not Found
                cmd_get_Entry = "getent passwd {}".format(u_Name)
                results = process.chroot_exec(cmd_get_Entry, dir_Mount=dir_Mount)
                # Obtain results value 
                u_Exists = results["stdout"]
                stderr = results["stderr"]
                resultcode = results["resultcode"]
                cmd_fmt = results["command"]

            if u_Exists == "":
                # 0 : Does not exist
                print("(-) User [{}] does not exist".format(u_Name))

                u_create_Command="useradd"

                # Get Parameters
                if u_home_Dir != "NIL":
                    # If Home Directory is not Empty
                    u_create_Command += " -m "
                    u_create_Command += " -d {} ".format(u_home_Dir)

                if u_primary_Group != "NIL":
                    # If Primary Group is Not Empty
                    u_create_Command+=" -g {} ".format(u_primary_Group)

                if u_secondary_Groups != "NIL":
                    # If Primary Group is Not Empty
                    u_create_Command+=" -G {} ".format(u_secondary_Groups)

                if u_other_Params != "NIL":
                    # If there are any miscellenous parameters
                    u_create_Command+=" {} ".format(u_other_Params)

                u_create_Command += u_Name
                
                # Append the user creation process
                postinstall_commands.append("{}".format(u_create_Command))

                for i in range(len(postinstall_commands)):
                    # Get current cmd
                    curr_cmd = postinstall_commands[i]

                    # Formulate chroot command
                    chroot_cmd_fmt = ["arch-chroot", dir_Mount, "/bin/bash", "-c", curr_cmd]

                    print("Executing: {}".format(' '.join(chroot_cmd_fmt)))
                    if self.MODE != "DEBUG":
                        stdout, stderr, resultcode = process.subprocess_Line(chroot_cmd_fmt, stdin=process.PIPE)
                        if resultcode == 0:
                            # Success
                            # User is created
                            print("Standard Output: {}".format(stdout))

                            # password change for the new user
                            print("(+) Password change for {}".format(u_Name))
                            passwd_change = "passwd {}".format(u_Name)
                            cmd_user_passwd_change = ["arch-chroot", dir_Mount, "/bin/bash", "-c", passwd_change]

                            print("Executing: {}".format(' '.join(cmd_user_passwd_change)))
                            if self.MODE != "DEBUG":
                                proc = process.subprocess_Open(cmd_user_passwd_change, stdout=process.PIPE)

                                # While the process is still working
                                line = ""
                                is_alive = proc.poll()
                                while is_alive is None:
                                    # Still working

                                    # Check if standard output stream is empty
                                    if proc.stdout != None:
                                        line = proc.stdout.readline()

                                        # Append standard output to list
                                        stdout.append(line.decode("utf-8"))

                                    # Check if standard input stream is empty
                                    if proc.stdin != None:
                                        # Check if line is entered
                                        if line != "":
                                            # Enter your secret line into the tty
                                            proc.stdin.write('{}\n'.format(line))

                                            # Enter one more time
                                            proc.stdin.write('{}\n'.format(line)) # Write this buffer string into the process' stdin

                                            # Flush the standard input stream
                                            proc.stdin.flush()

                                    # Poll and check if is alive
                                    # If poll == None: Alive, else not Alive
                                    is_alive = proc.poll()
                                    # print("Status: {}".format(is_alive))

                                # Get output, error and status code
                                # stdout = proc.stdout
                                stderr = proc.stderr
                                resultcode = proc.returncode
                                # stdout, stderr, resultcode = process.chroot_exec(root_passwd_change)

                        else:
                            # Error
                            print("Error: {}".format(stderr))

        ### Footer ###

        # =============== #
        # Execute Command #
        # =============== #

        # Combine into a string
        cmd_str = ";\n".join(postinstall_commands)
        
        # Cat commands into script file in mount root
        mount_Root = "{}/root".format(dir_Mount)
        script_to_exe = "postinstall-comms.sh"
        target_file = "{}/{}".format(mount_Root, script_to_exe)

        print("Executing: {}".format(cmd_str))
        if self.MODE != "DEBUG":
            # echo "echo -e "$cmd_str" > $mount_Root/$script_to_exe"
            with open(target_file, "a+") as write_postinstall_Commands:
                write_postinstall_Commands.write(cmd_str)
                # Close file after usage
                write_postinstall_Commands.close()

        chroot_exec_Script = [
            "chmod +x {}/{}".format(mount_Root, script_to_exe),
            "arch-chroot {} /bin/bash -c \"/root/{}\"".format(dir_Mount, script_to_exe)
        ]

        # Append external script path to the default variable key "external_scripts"
        self.default_Var["external_scripts"].append(
            ### Append all external scripts used ###
            "{}/{}".format(mount_Root, script_to_exe)
        )

    # Main Post-Installer
    def postinstaller(self):
        print("")

        print("=================")
        print("Post-Installation")
        print("=================")

        print("(S) Starting Basic Post-Installation")

        print("(+) Running post-installation...")
        success_Flag = self.postinstallation()
        if success_Flag == False:
            print("(-) Error detected in post-installation process")
        print("(+) Post-Installation execution completed")

        if self.MODE == "DEBUG":
            tmp = input("Press anything to continue...")

        print("")

        print("========================")
        print("Sanitization and Cleanup")
        print("========================")
        print("(+) Running finalization and sanitization...")
        success_Flag = self.postinstall_sanitize()
        if success_Flag == False:
            print("(-) Error detected in post-installation sanitization and cleanup")

        print("(+) Sanitization completed")

        if self.MODE == "DEBUG":
            tmp = input("Press anything to continue...")

        print("")

        print("(D) Basic Post-Installation processes completed.")

        finish = input("(D) Finished, press anything to quit.")


