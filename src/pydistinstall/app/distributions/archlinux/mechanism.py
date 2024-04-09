"""
Primary Installation Mechanism
"""
import os
import sys
import shutil
from ....lib import utils, env, user_management, device_management, process
from ....lib.env import Environment

class BaseInstallation():
    def __init__(self, setup):
        # Initialize Environment variable class 
        self.update_setup(setup)
        self.package_manager_config_Path = "/etc/pacman.d"
        self.mirrorlist_file_Name = "{}/mirrorlist".format(self.package_manager_config_Path)
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
    def update_setup(self, setup):
        self.setup = setup
        self.env = setup.env
        self.cfg = setup.cfg.copy()
        self.default_Var = setup.default_Var.copy()

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

        if self.env.MODE == "DEBUG":
            print(cmd_str)
            res = True
        else:
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

        if self.env.MODE == "DEBUG":
            # Set NTP
            print(cmd_set_NTP)
            # To check system clock
            print(cmd_check_NTP)
            success_flag = True
        else:
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

    def device_partition_Manager(self):
        """
        Device & Partition Manager
        """
        # Initialize Variables
        cfg = self.cfg
        cmd_str = ""

        # Begin Filesystem Management
        print("(+) Get User Input - Device Information")

        disk_Label = cfg["disk_Label"]
        partition_Table = cfg["disk_partition_Table"]
        partition_Scheme = cfg["partition_Scheme"].copy()

        # Check Device Type (i.e. sdX, nvme, loop)
        device_medium_Type = cfg["device_Type"]
        storage_controller = cfg["storage-controller"]

        print("")

        print("(+) Get User Input - Partition Information")

        """
        Formatting Partition Table
        """
        # Format & Create Label partition table
        format_conf = input("Would you like to format the disk's partition table? [Y|N]: ")
        if (format_conf == "Y") or (format_conf == ""):
            ## Format
            print("(+) Formatting [{}] to [{}]...".format(disk_Label, partition_Table))

            cmd_str = "parted {} mklabel {}".format(disk_Label, partition_Table)

            print("Executing: {}".format(cmd_str))
            if self.env.MODE != "DEBUG":
                # print("parted {} mklabel {}".format(device_Name, device_Label))
                # Open Subprocess Pipe
                # proc = Popen(["parted", device_Name, "mklabel", device_Label])
                stdout, stderr, returncode = process.subprocess_Line(cmd_str)
                if returncode == 0:
                    # Success
                    print("Standard Output: {}".format(stdout))
                else:
                    # Error
                    print("Error executing [{}]: {}".format(cmd_str, stderr))

        print("")

        format_conf = input("Would you like to format the disk's partition scheme/layout? [Y|N]: ")
        if (format_conf == "Y") or (format_conf == ""):
            ## Format
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

                """
                Formatting Partitions
                """
                print("(+) Creating Partition [{}]".format(part_ID))

                # Create Partition
                ## Check if disk label/partition table is MBR or GPT
                if (partition_Table == "msdos") or (partition_Table == "mbr"):
                    # Set command string
                    cmd_str = "parted {} mkpart {} {} {} {}".format(disk_Label, part_Type, part_filesystem, part_start_Size, part_end_Size)
                elif (partition_Table == "gpt"):
                    # Using partition label instead of primary,extended or logical
                    cmd_str = "parted {} mkpart {} {} {} {}".format(disk_Label, part_Name, part_filesystem, part_start_Size, part_end_Size)

                print("Executing: {}".format(cmd_str))
                if self.env.MODE != "DEBUG":
                    # check if string is empty
                    # Perform Partition Table formatting
                    stdout, stderr, returncode = process.subprocess_Sync(cmd_str)
                    print("Standard Output: {}".format(stdout))

                ## Prepare and Format Partition according to Device Storage Controller Type
                curr_part = device_management.format_partition_str(disk_Label, part_ID, storage_controller)

                ## Format file system
                if part_filesystem == "fat32":
                    cmd_str = "mkfs.fat -F32 {}".format(curr_part)
                elif part_filesystem == "ext4":
                    cmd_str = "mkfs.ext4 {}".format(curr_part)
                elif part_filesystem == "swap":
                    cmd_str = "mkswap {}{}".format(curr_part)
                else:
                    print("(-) Unknown File System: [{}]".format(part_filesystem))

                print("Executing: {}".format(cmd_str))
                if self.env.MODE != "DEBUG":
                    # Perform partitioning
                    stdout, stderr, returncode = process.subprocess_Sync(cmd_str)
                    print("Standard Output: {}".format(stdout))

                ## Check bootable
                if part_Bootable == True:
                    ### Check if disk label is MBR or GPT
                    if (partition_Table == "msdos") or (partition_Table == "mbr"):
                        cmd_str = "parted {} set {} boot on".format(disk_Label, part_ID)
                    elif (partition_Table == "gpt"):
                        cmd_str = "parted {} set {} esp on".format(disk_Label, part_ID)

                    # Begin Execution
                    print("Executing: {}".format(cmd_str))
                    if self.env.MODE != "DEBUG":
                        # Perform Boot set
                        stdout, stderr, returncode = process.subprocess_Sync(cmd_str)
                        print("Standard Output: {}".format(stdout))

                ## Check Swap partition
                if part_filesystem == "swap":
                    cmd_str = "swapon {}{}".format(disk_Label, part_ID)

                    # Begin Execution
                    print("Executing: {}".format(cmd_str))
                    if self.env.MODE != "DEBUG":
                        ## Perform Swap partition formatting
                        stdout, stderr, returncode = process.subprocess_Sync(cmd_str)
                        print("Standard Output: {}".format(stdout))

        print("")

        print("(D) Partition Completed. ")

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

        ## Create directories if does not exists
        if not (os.path.isdir(root_Dir)):
            ### Directory does not exist
            cmd_str = "mkdir -p {}".format(root_Dir)

            print("Directory {} does not exist, creating directory...".format(root_Dir))
            print("Executing: {}".format(cmd_str))
            if self.env.MODE != "DEBUG":
                ## Mount root partition
                # stdout, stderr = process.subprocess_Sync(cmd_str)
                stdout, stderr, returncode = process.subprocess_Line(cmd_str)
                print("Standard Output: {}".format(stdout))
        else:
            print("Directory {} exists.".format(root_Dir))

        ## --- Processing
        ### Mount the volume to the path
        #### Get information of current partition
        target_Partition = partition_Name
        curr_part_Number = partition_Number

        ##### Search for partition number of the Root partition
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

        curr_filesystem = partition_Scheme[curr_part_Number][2]

        #### Prepare and Format Partition according to Device Storage Controller Type for Root partition
        target_disk_root_Part = device_management.format_partition_str(disk_Label, curr_part_Number, storage_controller)

        #### Check filesystem of current partition
        print("Current Filesystem [Root] => [{}]".format(curr_filesystem))
        if (curr_filesystem == "fat32"):
            # FAT32 formatting is in vfat
            cmd_str = "mount -t vfat {} {}".format(target_disk_root_Part, root_Dir)
                
            print("Executing: {}".format(cmd_str))
            if self.env.MODE != "DEBUG":
                ## Check filesystem for FAT32
                # stdout, stderr = process.subprocess_Sync(cmd_str)
                stdout, stderr, returncode = process.subprocess_Line(cmd_str)
                if returncode == 0:
                    # Success
                    print("Partition [Root] Mounted.")
                else:
                    # Error
                    print("Error mounting Partition [Root]")
        else:
            # Any other filesystems
            """
            mount -t ext4 /dev/sdX2 /mnt
            mount -t ext4 /dev/sdX1 /mnt/boot 
            mount -t ext4 /dev/sdX3 /mnt/home
            """
            cmd_str = "mount -t {} {} {}".format(curr_filesystem, target_disk_root_Part, root_Dir)
                
            print("Executing: {}".format(cmd_str))
            if self.env.MODE != "DEBUG":
                ## Check other filesystems
                # stdout, stderr = process.subprocess_Sync(cmd_str)
                stdout, stderr, returncode = process.subprocess_Line(cmd_str)
                if returncode == 0:
                    # Success
                    print("Partition [Root] Mounted.")
                else:
                    # Error
                    print("Error mounting Partition [Root]")

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

        ## Create directories if does not exists
        if not (os.path.isdir(boot_Dir)):
            ### Directory does not exist
            cmd_str = "mkdir -p {}".format(boot_Dir)

            print("Directory {} does not exist, creating directory...".format(boot_Dir))
            print("Executing: {}".format(cmd_str))
            if self.env.MODE != "DEBUG":
                ## Mount boot partition
                # stdout, stderr = process.subprocess_Sync(cmd_str)
                stdout, stderr, returncode = process.subprocess_Line(cmd_str)
                print("Standard Output: {}".format(stdout))
        else:
            print("Directory {} exists.".format(boot_Dir))

        ## --- Processing
        ### Mount the volume to the path
        #### Get information of current partition
        target_Partition = partition_Name
        curr_part_Number = partition_Number

        ##### Search for partition number of the Root partition
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

        curr_filesystem = partition_Scheme[curr_part_Number][2]

        ## --- Processing
        ### Mount the volume to the path
        #### Prepare and Format Partition according to Device Storage Controller Type for Boot partition
        target_disk_boot_Part = device_management.format_partition_str(disk_Label, curr_part_Number, storage_controller)

        #### Check filesystem
        print("Current Filesystem [Boot] => [{}]".format(curr_filesystem))
        if curr_filesystem == "fat32":
            # FAT32 formatting is in vfat
            cmd_str = "mount -t vfat {} {}".format(target_disk_boot_Part, boot_Dir)

            print("Executing: {}".format(cmd_str))
            if self.env.MODE != "DEBUG":
                ## Check FAT32 partition scheme for Boot partition
                stdout, stderr, returncode = process.subprocess_Sync(cmd_str)
                print("Standard Output: {}".format(stdout))

                if returncode == 0:
                    # Success
                    print("Partition [Boot] Mounted.")
                else:
                    # Error
                    print("Error mounting Partition [Boot]")
        else:
            # Any other filesystems
            cmd_str = "mount -t {} {} {}".format(curr_filesystem, target_disk_boot_Part, boot_Dir)

            print("Executing: {}".format(cmd_str))
            if self.env.MODE != "DEBUG":
                ## Check Other partition scheme for Boot partition
                stdout, stderr, returncode = process.subprocess_Sync(cmd_str)
                print("Standard Output: {}".format(stdout))

                if returncode == 0:
                    # Success
                    print("Partition [Boot] Mounted.")
                else:
                    # Error
                    print("Error mounting Partition [Boot]")

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
                AHCI/SATA
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

            ## Create directories if does not exists
            if not (os.path.isdir(part_mount_dir)):
                ### Directory does not exist
                cmd_str = "mkdir -p {}".format(part_mount_dir)
                
                print("Directory {} does not exist, creating directory...".format(part_mount_dir))
                print("Executing: {}".format(cmd_str))
                if self.env.MODE != "DEBUG":
                    ## Create the other partition mount points
                    stdout, stderr, returncode = process.subprocess_Sync(cmd_str)
                    print("Standard Output: {}".format(stdout))
            else:
                print("Directory {} exists.".format(part_mount_dir))

            ## --- Processing
            ### Mount the volume to the path
            #### Prepare and Format Partition according to Device Storage Controller Type for the current partition
            target_disk_curr_Part = device_management.format_partition_str(disk_Label, part_ID, storage_controller)

            #### Check filesystem
            print("Current Filesystem [{}] => [{}]".format(part_Name, part_filesystem))
            if part_filesystem == "fat32":
                cmd_str = "mount -t vfat {} {}".format(target_disk_curr_Part, part_mount_dir)

                print("Executing: {}".format(cmd_str))
                if self.env.MODE != "DEBUG":
                    ## Mount the other partition mount points using FAT32
                    stdout, stderr, returncode = process.subprocess_Sync(cmd_str)
                    print("Standard Output: {}".format(stdout))

                    if returncode == 0:
                        # Success
                        print("Partition [{}] Mounted.".format(part_Name))
                    else:
                        # Error
                        print("Error mounting Partition [{}]".format(part_Name))
            else:
                cmd_str = "mount -t {} {} {}".format(part_filesystem, target_disk_curr_Part, part_mount_dir)
                    
                print("Executing: {}".format(cmd_str))
                if self.env.MODE != "DEBUG":
                    ## Mount the other partition mount points using other filesystem types
                    stdout, stderr, returncode = process.subprocess_Sync(cmd_str)
                    print("Standard Output: {}".format(stdout))

                    if returncode == 0:
                        # Success
                        print("Partition [{}] Mounted.".format(part_Name))
                    else:
                        # Error
                        print("Error mounting Partition [{}]".format(part_Name))
        
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
        print("{}".format(self.env.EDITOR))
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
            if self.env.MODE != "DEBUG":
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
        cmd_str = "pacstrap {} {}".format(mount_Point, ' '.join(base_packages))

        print("Executing: {}".format(cmd_str))
        if self.env.MODE != "DEBUG":
            ## Begin bootstrapping
            # stdout, stderr, resultcode = process.subprocess_Realtime(cmd_str)
            resultcode = os.system(cmd_str)

        print("")

        # Select Mirror List
        self.select_Mirrors(self.mirrorlist_file_Name)

        print("")

        # Check package manager configuration file
        self.check_package_manager_Configurations(mount_Point)

        # Check result code
        if resultcode == 0:
            success_Flag = True

        return stdout, stderr, resultcode

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

        # Generate an fstab file (use -U or -L to define by UUID or labels, respectively):
        # cmd_str = "genfstab -U {}".format(dir_Mount)

        # Execute and get fstab content from command and write into /etc/fstab
        if self.env.MODE != "DEBUG":
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
                print("Exception : {}".format(ex))

        return success_Flag

    """
    Chroot Actions
    """
    def format_chroot_Subprocess(self, \
            cmd_str, \
            mount_Dir="/mnt", \
            chroot_Command="arch-chroot", \
            shell="/bin/bash" \
        ):
        """
        Format and returns the command string into the subprocess command list
        """
        return [chroot_Command, mount_Dir, shell, "-c", cmd_str]

    def chroot_execute_command(self, cmd_str, mount_Dir="/mnt", chroot_Command="arch-chroot", shell="/bin/bash"):
        """
        Generalized chroot command execution
        """
        # Initialize Variables
        chroot_cmd_fmt = [chroot_Command, mount_Dir, shell, "-c", cmd_str]
        stdout = []
        stderr = []
        resultcode = 0
        result = {
            "stdout" : [],
            "stderr" : [],
            "resultcode" : [],
            "command-string" : ""
        }

        # Process
        if self.env.MODE != "DEBUG":
            stdout, stderr, resultcode = process.subprocess_Line(chroot_cmd_fmt, stdin=process.PIPE)
            if resultcode == 0:
                # Success
                print("Standard Output: {}".format(stdout))
            else:
                # Error
                print("Error: {}".format(stderr))

            # Map/Append result results
            result["stdout"] = stdout
            result["stderr"] = stderr
            result["resultcode"] = resultcode

        # Output
        return result

    def chroot_execute_command_List(self, cmd_List, mount_Dir="/mnt", chroot_Command="arch-chroot", shell="/bin/bash"):
        """
        Generalized chroot command list execution
        """
        # Initialize Variables
        result = {
            "stdout" : [],
            "stderr" : [],
            "resultcode" : [],
            "command-string" : ""
        }

        if len(cmd_List) > 0:
            for i in range(len(cmd_List)):
                # Get current cmd
                cmd_str = cmd_List[i]

                # Formulate chroot command
                chroot_cmd_fmt = [chroot_Command, mount_Dir, shell, "-c", cmd_str]

                print("Executing: {}".format(' '.join(chroot_cmd_fmt)))
                if self.env.MODE != "DEBUG":
                    stdout, stderr, resultcode = process.subprocess_Sync(chroot_cmd_fmt, stdin=process.PIPE)
                    if resultcode == 0:
                        # Success
                        print("Standard Output: {}".format(stdout))
                    else:
                        # Error
                        print("Error: {}".format(stderr))

                    # Map/Append result results
                    result["stdout"].append(stdout)
                    result["stderr"].append(stderr)
                    result["resultcode"].append(resultcode)

        return result

    def sync_Timezone(self, mount_Dir, region, city):
        """
        Synchronize Hardware Clock in chroot
        """
        chroot_commands = [
            # "echo ======= Time Zones ======"												            # Step 10: Time Zones
            "ln -sf /usr/share/zoneinfo/{}/{} /etc/localtime".format(region, city),						# Step 10: Time Zones; Set time zone
            "hwclock --systohc",																        # Step 10: Time Zones; Generate /etc/adjtime via hwclock
        ]
        self.chroot_execute_command_List(chroot_commands, mount_Dir)

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
        self.chroot_execute_command_List(chroot_commands, mount_Dir)

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
        self.chroot_execute_command_List(chroot_commands, mount_Dir)

    def initialize_Ramdisk(self, mount_Dir, default_Kernel="linux"):
        """
        Format initial ramdisk
        """
        # Initialize Variables
        chroot_commands = [
            # "echo ======= Make Initial Ramdisk ======="										        # Step 13: Initialize RAM file system;
            "mkinitcpio -P {}".format(default_Kernel),												    # Step 13: Initialize RAM file system; Create initramfs image (linux-lts kernel)
        ]
        result = {
            "stdout" : [],
            "stderr" : [],
            "resultcode" : [],
            "command-string" : ""
        }

        # Execute commands
        self.chroot_execute_command_List(chroot_commands, mount_Dir)

        return result

    def set_root_Password(self, mount_Dir):
        """
        Set Root Password
        """
        # Initialize Variables
        str_root_passwd_change = "passwd || passwd;"
        cmd_root_passwd_change = self.format_chroot_Subprocess(str_root_passwd_change, mount_Dir)
        stdout = []
        stderr = []
        resultcode = 0
        result = {
            "stdout" : [],
            "stderr" : [],
            "resultcode" : [],
            "command-string" : ""
        }

        print("Executing: {}".format(' '.join(cmd_root_passwd_change)))
        if self.env.MODE != "DEBUG":
            proc = process.subprocess_Open(cmd_root_passwd_change, stdout=process.PIPE)

            # While the process is still working
            line = ""
            is_alive = proc.poll()
            while is_alive is None:
                # Still working

                # Check if standard output stream is empty
                if proc.stdout != None:
                    line = proc.stdout.readline()

                    # Append line to standard output
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

            # Map/Append result results
            result["stdout"] = stdout
            result["stderr"].append(stderr)
            result["resultcode"].append(resultcode)

        return result

    def install_bootloader_Packages(self, dir_Mount="/mnt", bootloader="grub", partition_Table="msdos"):
        """
        Install bootloader packages
        """
        # Initialize Variables
        chroot_commands = []
        result = {
            "stdout" : [],
            "stderr" : [],
            "resultcode" : [],
            "command-string" : ""
        }

        # Switch Case bootloader between grub and syslinux
        chroot_commands.append("echo \"(+) Installing Bootloader : {}\"".format(bootloader))
        if (bootloader == "grub"):
            # Setup bootloader
            chroot_commands.append("sudo pacman -S grub") # Install Grub Package

            # Check if partition table is GPT
            if partition_Table == "gpt":
                # Install GPT/(U)EFI dependencies
                chroot_commands.append("sudo pacman -S efibootmgr")
        elif bootloader == "syslinux":
            ### Syslinux bootloader support is currently still a WIP and Testing
            chroot_commands.append("sudo pacman -S syslinux")

        # --- Processing

        # Combine into a string
        cmd_str = ";\n".join(chroot_commands)

        # Map/Append Command String
        result["command-string"] = cmd_str

        for i in range(len(chroot_commands)):
            # Get current command
            curr_cmd = chroot_commands[i]

            # Begin
            print("Executing: {}".format(curr_cmd))
            if self.env.MODE != "DEBUG":
                stdout, stderr, resultcode = process.chroot_exec(curr_cmd, dir_Mount=dir_Mount)

                # Map/Append result results
                result["stdout"].append(stdout)
                result["stderr"].append(stderr)
                result["resultcode"].append(resultcode)

        return result

    def prepare_Bootloader(self, dir_Mount="/mnt", bootloader="grub", bootloader_directory="/boot/grub"):
        """
        Prepare Bootloader directories and Pre-Requisites
        """
        # Initialize Variables
        chroot_commands = []
        result = {
            "stdout" : [],
            "stderr" : [],
            "resultcode" : [],
            "command-string" : ""
        }
        # Switch Case bootloader between grub and syslinux
        if (bootloader == "grub"):
            chroot_commands.append("mkdir -p {}".format(bootloader_directory))                  # Create grub folder
        elif bootloader == "syslinux":
            ### Syslinux bootloader support is currently still a WIP and Testing
            chroot_commands.append("mkdir -p /boot/syslinux")
            chroot_commands.append("cp -r /usr/lib/syslinux/bios/*.c32 /boot/syslinux")

        # --- Processing

        # Combine into a string
        cmd_str = ";\n".join(chroot_commands)

        # Map/Append Command String
        result["command-string"] = cmd_str

        for i in range(len(chroot_commands)):
            # Get current command
            curr_cmd = chroot_commands[i]

            # Begin
            print("Executing: {}".format(curr_cmd))
            if self.env.MODE != "DEBUG":
                stdout, stderr, resultcode = process.chroot_exec(curr_cmd, dir_Mount=dir_Mount)

                # Map/Append result results
                result["stdout"].append(stdout)
                result["stderr"].append(stderr)
                result["resultcode"].append(resultcode)

        return result

    def install_Bootloader(self, disk_Label, dir_Mount="/mnt", bootloader="grub", bootloader_directory="/boot/grub", partition_Table="msdos", bootloader_optional_Params="", bootloader_target_Architecture="i386-pc"):
        """
        Install Bootloader to the Partition Table
        """
        # Initialize Variables
        chroot_commands = []
        result = {
            "stdout" : [],
            "stderr" : [],
            "resultcode" : [],
            "command-string" : ""
        }
        # Switch Case bootloader between grub and syslinux
        if (bootloader == "grub"):
            # Install Bootloader
            chroot_commands.append("grub-install --target={} {} {}".format(bootloader_target_Architecture, bootloader_optional_Params, disk_Label))	# Install Grub Bootloader
        elif bootloader == "syslinux":
            ### Syslinux bootloader support is currently still a WIP and Testing
            chroot_commands.append("extlinux --install /boot/syslinux")

        # --- Processing

        # Combine into a string
        cmd_str = ";\n".join(chroot_commands)

        # Map/Append Command String
        result["command-string"] = cmd_str

        for i in range(len(chroot_commands)):
            # Get current command
            curr_cmd = chroot_commands[i]

            # Begin
            print("Executing: {}".format(curr_cmd))
            if self.env.MODE != "DEBUG":
                stdout, stderr, resultcode = process.chroot_exec(curr_cmd, dir_Mount=dir_Mount)

                # Map/Append result results
                result["stdout"].append(stdout)
                result["stderr"].append(stderr)
                result["resultcode"].append(resultcode)

        return result

    def generate_bootloader_Configs(self, disk_Label, dir_Mount="/mnt", bootloader="grub", bootloader_directory="/boot/grub", partition_Table="msdos", bootloader_optional_Params="", bootloader_target_Architecture="i386-pc"):
        # Initialize Variables
        chroot_commands = []
        result = {
            "stdout" : [],
            "stderr" : [],
            "resultcode" : [],
            "command-string" : ""
        }

        # Switch Case bootloader between grub and syslinux
        if (bootloader == "grub"):
            # Generate bootloader configuration file
            chroot_commands.append("grub-mkconfig -o {}/grub.cfg".format(bootloader_directory)) # Create grub config
        elif bootloader == "syslinux":
            ### Syslinux bootloader support is currently still a WIP and Testing
            # Check partition table
            if (partition_Table == "msdos") or (partition_Table == "mbr"):
                chroot_commands.append("dd bs=440 count=1 conv=notrunc if=/usr/lib/syslinux/bios/mbr.bin of={}".format(disk_Label))
            elif (partition_Table == "gpt"):
                chroot_commands.append("sgdisk {} --attributes=1:set:2".format(disk_Label))
                chroot_commands.append("dd bs=440 conv=notrunc count=1 if=/usr/lib/syslinux/bios/gptmbr.bin of={}".format(disk_Label))

        # --- Processing

        # Combine into a string
        cmd_str = ";\n".join(chroot_commands)

        # Map/Append Command String
        result["command-string"] = cmd_str

        for i in range(len(chroot_commands)):
            # Get current command
            curr_cmd = chroot_commands[i]

            # Begin
            print("Executing: {}".format(curr_cmd))
            if self.env.MODE != "DEBUG":
                stdout, stderr, resultcode = process.chroot_exec(curr_cmd, dir_Mount=dir_Mount)

                # Map/Append result results
                result["stdout"].append(stdout)
                result["stderr"].append(stderr)
                result["resultcode"].append(resultcode)

        return result

    def bootloader_Management(self, disk_Label, dir_Mount="/mnt", bootloader="grub", bootloader_directory="/boot/grub", partition_Table="msdos", bootloader_optional_Params="", bootloader_target_Architecture="i386-pc"):
        """
        NOTE:
        1. Please Edit [osdef] on top with the bootloader information before proceeding
        """
        # Initialize Variables
        combined_res = []

        # Install bootloader packages
        res = self.install_bootloader_Packages(dir_Mount, bootloader, partition_Table)
        combined_res.append(res)

        # Prepare Bootloader dependencies
        res = self.prepare_Bootloader(dir_Mount, bootloader, bootloader_directory)
        combined_res.append(res)

        # Install Bootloader to partition table
        res = self.install_Bootloader(disk_Label, dir_Mount, bootloader, bootloader_directory, partition_Table, bootloader_optional_Params, bootloader_target_Architecture)
        combined_res.append(res)

        # Generate Bootloader configurations
        res = self.generate_bootloader_Configs(disk_Label, dir_Mount, bootloader, bootloader_directory, partition_Table, bootloader_optional_Params, bootloader_target_Architecture)
        combined_res.append(res)

        # Return output
        return combined_res

    def archive_command_Str(self, cmd_str, dir_Mount="/mnt"):
        """
        Output command string into a file for archiving
        """
        # Initialize Variables
        mount_Root="{}/root".format(dir_Mount)
        script_to_exe="chroot-comms.sh"
        target_directory = "{}/{}".format(mount_Root, script_to_exe)

        # Write commands into file for reusing
        print("Writing [\n{}\n] => {}".format(cmd_str, target_directory))
        if self.env.MODE != "DEBUG":
            with open(target_directory, "a+") as write_chroot_Commands:
                # Write to file
                write_chroot_Commands.write(cmd_str)

                # Close file after usage
                write_chroot_Commands.close()

        # Execute in arch-chroot
        # Future Codes deemed stable *enough*, thanks Past self for retaining legacy codes
        # for debugging
        self.default_Var["external_scripts"].append(
            ### Append all external scripts used ###
            "{}/{}".format(mount_Root, script_to_exe)
        )

    def arch_chroot_Exec(self):
        """
        Execute commands using arch-chroot due to limitations with shellscripting
        """

        # --- Input
        # Local Variables
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

        # Chroot Execute
        ## Synchronize Hardware Clock
        print("(+) Time Zones : Synchronize Hardware Clock")
        self.sync_Timezone(dir_Mount, region, city)

        print("")

        ## Enable locale/region
        print("(+) Enable Location/Region")
        self.enable_Locale(dir_Mount, language)

        print("")

        ## Append Network Host file
        print("(+) Network Configuration")
        self.network_Management(dir_Mount, hostname)

        print("")

        ## Format initial ramdisk
        print("(+) Making Initial Ramdisk")
        self.initialize_Ramdisk(dir_Mount, default_Kernel)

        print("")

        # Step 14: User Information - Set Root password
        print("======= Change Root Password =======")
        res = self.set_root_Password(dir_Mount)
        stdout = res["stdout"]
        stderr = res["stderr"]
        resultcode = res["resultcode"] 
        cmd_str = res["command-string"]

        print("")
        
        # Step 15: Install Bootloader
        combined_res = self.bootloader_Management(disk_Label, dir_Mount, bootloader, bootloader_directory, partition_Table, bootloader_optional_Params, bootloader_target_device_Type)
        
        print("")

        # Archive the command string into a file
        self.archive_command_Str(cmd_str, dir_Mount)

        print("")

    def installer(self):
        """
        Main setup installer
        """
        print("(S) Starting Base Installation...")

        print("========================")
        print("Stage 1: Prepare Network")
        print("========================")

        print("(S) 1. Testing Network...")
        network_Enabled = self.verify_network()
        if network_Enabled == False:
            cmd_str = "dhcpcd"
            print("")
            print("Executing: {}".format(cmd_str))
            if self.env.MODE != "DEBUG":
                ## Begin executing commands
                stdout, stderr, returncode = process.subprocess_Sync(cmd_str)
                print("Standard Output: {}".format(stdout))
                print("Standard Error: {}".format(stderr))

                if returncode == 0:
                    # Success
                    print("(+) Network is activated")
                else:
                    # Error
                    print("(-) Error starting Network")
        else:
            print("(+) Network is active")

        print("(D) Network testing completed.")

        if self.env.MODE == "DEBUG":
            tmp = input("Press anything to continue...")

        print("")

        print("==========================================")
        print("Stage 2: Verify Boot Mode (i.e. UEFI/BIOS)")
        print("==========================================")
        
        print("(S) Verifying Boot Mode...")
        boot_Mode = self.verify_boot_Mode()
        print("(+) Motherboard bootloader firmware boot mode (bios/uefi): {}".format(boot_Mode))

        print("(D) Boot Mode verification completed.")

        if self.env.MODE == "DEBUG":
            tmp = input("Press anything to continue...")

        print("")

        print("============================")
        print("Stage 3: Update System Clock")
        print("============================")
        
        print("(S) Updating System Clock...")
        stdout, stderr, resultcode, success_Flag = self.update_system_Clock()
        if success_Flag == False:
            print("(X) Error updating system clock via Network Time Protocol (NTP)")
        else:
            print("(D) System clock updated.")

        if self.env.MODE == "DEBUG":
            tmp = input("Press anything to continue...")

        print("")

        print("============================")
        print("Stage 4: Partition the Disks")
        print("============================")
        
        print("(S) Starting Disk Management...")
        success_Flag = self.device_partition_Manager()
        if success_Flag == False:
            print("(X) Error formatting disk and partitions")
        print("(D) Disk Management completed.")

        if self.env.MODE == "DEBUG":
            tmp = input("Press anything to continue...")

        print("")

        print("====================")
        print("Stage 5: Mount Disks")
        print("====================")
        
        print("(S) Mounting disks...")
        success_Flag = self.mount_Disks()
        if success_Flag == False:
            print("(X) Error mounting disks")
        print("(D) Disks mounted.")

        if self.env.MODE == "DEBUG":
            tmp = input("Press anything to continue...")

        print("")

        print("===================================")
        print("Stage 6: Install essential packages")
        print("===================================")
        print("(S) Strapping packages to mount point...")
        success_Flag = self.bootstrap_Install()
        if success_Flag == False:
            print("(X) Errors bootstrapping packages")
        print("(D) Packages strapped.")

        if self.env.MODE == "DEBUG":
            tmp = input("Press anything to continue...")

        print("")

        print("===========================================")
        print("Stage 7: Generate fstab (File System Table)")
        print("===========================================")
        print("(S) Generating Filesystems Table in /etc/fstab")
        success_Flag = self.fstab_Generate()
        if success_Flag == False:
            print("(X) Error generating filesystems table")
        print("(D) Filesystems Table generated.")

        if self.env.MODE == "DEBUG":
            tmp = input("Press anything to continue...")

        print("")

        print("===========================")
        print("Stage 8: Chroot and execute")
        print("===========================")

        print("(S) Executing chroot commands")
        success_Flag = self.arch_chroot_Exec() # Execute commands in arch-chroot
        if success_Flag == False:
            print("(X) Error executing commands in chroot")
        print("(D) Commands executed")

        if self.env.MODE == "DEBUG":
            tmp = input("Press anything to continue...")

        print("")

        print("=======================")
        print("Installation Completed.")
        print("=======================")


# =========================== #
# Post-Installation Functions #
# =========================== #
class PostInstallation():
    """
    Class for the Post-Installation functions in the installation library/framework
    """
    def __init__(self, setup, base_mechanism_Obj=None):
        # Local Variables
        self.setup = setup
        self.cfg = self.setup.cfg
        dir_Mount = self.cfg["mount_Paths"]["Root"]
        number_of_external_scripts = len(base_mechanism_Obj.default_Var["external_scripts"])

        if base_mechanism_Obj == None:
            # Initialize defaults from configuration file if no base installation object is specified
            self.init_Config()

    def init_Config(self):
        """
        Initialize defaults from configuration file if base installation is not used
        """
        # Update setup to the latest
        self.update_setup(self.setup)

    # Callback/Event Utility functions
    def update_setup(self, setup):
        self.setup = setup
        self.env = setup.env
        self.cfg = setup.cfg
        self.default_Var = setup.default_Var

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
                        if self.env.MODE != "DEBUG":
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
                            if self.env.MODE != "DEBUG":
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
                    if self.env.MODE == "DEBUG":
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
                        if self.env.MODE == "DEBUG":
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
            if self.env.MODE != "DEBUG":
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
            if self.env.MODE == "DEBUG":
                u_Exists = ""
            else:
                # Check if user exists | Empty if Not Found
                cmd_get_Entry = "getent passwd {}".format(u_Name)
                u_Exists, stderr, returncode = process.chroot_exec(cmd_get_Entry, dir_Mount=dir_Mount)

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
                    if self.env.MODE != "DEBUG":
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
                            if self.env.MODE != "DEBUG":
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
        if self.env.MODE != "DEBUG":
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

        if self.env.MODE == "DEBUG":
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

        if self.env.MODE == "DEBUG":
            tmp = input("Press anything to continue...")

        print("")

        print("(D) Basic Post-Installation processes completed.")

        finish = input("(D) Finished, press anything to quit.")


