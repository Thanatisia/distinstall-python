"""
Primary Installation Mechanism
"""
import os
import sys
import yaml
import shutil
from lib import utils, env, user_management, process
from lib.env import Environment

class ArchLinux():
    def __init__(self, setup):
        # Initialize Environment variable class 
        self.update_setup(setup)

    # Callback/Event Utility functions
    def update_setup(self, setup):
        self.setup = setup
        self.env = setup.env
        self.cfg = setup.cfg
        self.default_Var = setup.default_Var

    def print_configurations(self):
        print(self.cfg)

    # Installation stages
    def verify_network(self):
        """
        Step 1: Verify that the host network is working
        """
        ping_Count = 5
        ipv4_address = "8.8.8.8"
        ret_Code:int = os.system("ping -c {} {}".format(ping_Count, ipv4_address))
        res = False
        if ret_Code != 0:
            # Success
            res=True
        return res

    def verify_boot_Mode(self):
        """
        Verify motherboard bootloader firmware

        - BIOS : Legacy
        - UEFI : Modern Universal EFI mode
        """
        boot_Mode:str = "bios"

        # Check if sytem has EFI
        ret_Code:int = os.system("ls /sys/firmware/efi/efivars")
        if ret_Code == 0:
            # UEFI
            boot_Mode="uefi"
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
                print("Standard Output: {}".format(stdout))

                # To check system clock
                stdout, stderr, returncode = process.subprocess_Sync(cmd_check_NTP)

                if returncode == 0:
                    # Successfully set system clock
                    success_flag = True
                else:
                    # Error setting system clock
                    success_flag = False

        return success_flag

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
        partition_Scheme = cfg["partition_Scheme"]

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
                stdout, stderr, returncode = process.subprocess_Sync(cmd_str)
                print("Standard Output: {}".format(stdout))

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

                ## Format file system
                if part_filesystem == "fat32":
                    cmd_str = "mkfs.fat -F32 {}{}".format(disk_Label, part_ID)
                elif part_filesystem == "ext4":
                    cmd_str = "mkfs.ext4 {}{}".format(disk_Label, part_ID)
                elif part_filesystem == "swap":
                    cmd_str = "mkswap {}{}".format(disk_Label, part_ID)
                else:
                    print("(-) Unknown File System: [$part_file_Type]")

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

    def mount_Disks(self):
        """
        Mount Disks and Partitions
        """
        
        # --- Input
        # Local Variables
        cfg = self.cfg
        disk_Label = cfg["disk_Label"]
        partition_Table = cfg["disk_partition_Table"]

        """
        Mount root partition
        """
        mount_dir_Root = cfg["mount_Paths"]["Root"]

        ## Create directories if does not exists
        if not (os.path.isdir(mount_dir_Root)):
            ### Directory does not exist
            cmd_str = "mkdir -p {}".format(mount_dir_Root)

            print("Directory {} does not exist, creating directory...".format(mount_dir_Root))
            print("Executing: {}".format(cmd_str))
            if self.env.MODE != "DEBUG":
                ## Mount root partition
                # stdout, stderr = process.subprocess_Sync(cmd_str)
                stdout = process.subprocess_Line(cmd_str)
                print("Standard Output: {}".format(stdout))
        else:
            print("Directory {} exists.".format(mount_dir_Root))

        ## --- Processing
        ### Mount the volume to the path
        #### Get information of current partition
        partition_Scheme = cfg["partition_Scheme"]
        target_Partition = "Root"
        curr_part_Number = 1

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

        #### Check filesystem of current partition
        print("Current Filesystem [Root] => [{}]".format(curr_filesystem))
        if (curr_filesystem == "fat32"):
            # FAT32 formatting is in vfat
            cmd_str = "mount -t vfat {}{} {}".format(disk_Label, curr_part_Number, mount_dir_Root)
                
            print("Executing: {}".format(cmd_str))
            if self.env.MODE != "DEBUG":
                ## Check filesystem for FAT32
                # stdout, stderr = process.subprocess_Sync(cmd_str)
                stdout, returncode = process.subprocess_Line(cmd_str)
                print("Standard Output: {}".format(stdout))
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
            cmd_str = "mount -t {} {}{} {}".format(curr_filesystem, disk_Label, curr_part_Number, mount_dir_Root)
                
            print("Executing: {}".format(cmd_str))
            if self.env.MODE != "DEBUG":
                ## Check other filesystems
                # stdout, stderr = process.subprocess_Sync(cmd_str)
                stdout, returncode = process.subprocess_Line(cmd_str)
                print("Standard Output: {}".format(stdout))
                if returncode == 0:
                    # Success
                    print("Partition [Root] Mounted.")
                else:
                    # Error
                    print("Error mounting Partition [Root]")

        ### Unset/Remove Root partition from mount list
        partition_Scheme.pop(curr_part_Number)

        """
        Mount boot partition
        """
        mount_dir_Boot = cfg["mount_Paths"]["Boot"]

        ## Create directories if does not exists
        if not (os.path.isdir(mount_dir_Boot)):
            ### Directory does not exist
            cmd_str = "mkdir -p {}".format(mount_dir_Boot)

            print("Directory {} does not exist, creating directory...".format(mount_dir_Boot))
            print("Executing: {}".format(cmd_str))
            if self.env.MODE != "DEBUG":
                ## Mount boot partition
                # stdout, stderr = process.subprocess_Sync(cmd_str)
                stdout, returncode = process.subprocess_Line(cmd_str)
                print("Standard Output: {}".format(stdout))
        else:
            print("Directory {} exists.".format(mount_dir_Boot))

        ## --- Processing
        ### Mount the volume to the path
        #### Get information of current partition
        partition_Scheme = cfg["partition_Scheme"]
        target_Partition = "Boot"
        curr_part_Number = 1

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
        #### Check filesystem
        print("Current Filesystem [Boot] => [{}]".format(curr_filesystem))
        if curr_filesystem == "fat32":
            # FAT32 formatting is in vfat
            cmd_str = "mount -t vfat {}{} {}".format(disk_Label, curr_part_Number, mount_dir_Boot)

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
            cmd_str = "mount -t {} {}{} {}".format(curr_filesystem, disk_Label, curr_part_Number, mount_dir_Boot)

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

        """
        Mount all other partitions
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
            part_mount_dir = cfg["mount_Paths"][part_Name]

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
            #### Check filesystem
            print("Current Filesystem [{}] => [{}]".format(part_Name, part_filesystem))
            if part_filesystem == "fat32":
                cmd_str = "mount -t vfat {}{} {}".format(disk_Label, part_ID, part_mount_dir)

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
                cmd_str = "mount -t {} {}{} {}".format(curr_filesystem, disk_Label, part_ID, part_mount_dir)
                    
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

        # --- Processing
        cmd_str = "pacstrap {} {}".format(mount_Point, ' '.join(base_packages))

        print("Executing: {}".format(cmd_str))
        if self.env.MODE != "DEBUG":
            ## Begin bootstrapping
            stdout = process.subprocess_Line(cmd_str)
            print("Standard Output: {}".format(stdout))

    def fstab_Generate(self):
        """
        Generate File System Table (fstab)
        """
        # --- Input
        # Local Variables
        cfg = self.cfg
        dir_Mount = cfg["mount_Paths"]["Root"] # Look for root/mount partition

        # Generate an fstab file (use -U or -L to define by UUID or labels, respectively):
        cmd_str = "genfstab -U {} >> {}/etc/fstab".format(dir_Mount, dir_Mount)
            
        print("Executing: {}".format(cmd_str))
        if self.env.MODE != "DEBUG":
            ## Begin generating filesystems table
            stdout, stderr, returncode = process.subprocess_Sync(cmd_str)
            print("Standard Output: {}".format(stdout))

    def arch_chroot_Exec(self):
        """
        Execute commands using arch-chroot due to limitations with shellscripting
        """

        # --- Input
        # Local Variables
        cfg = self.cfg
        disk_Label = cfg["disk_Label"]
        partition_Table = cfg["disk_partition_Table"]
        bootloader_firmware = cfg["bootloader_firmware"]
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

        # Array

        # Associative Array
        chroot_commands = [
            # "echo ======= Time Zones ======"												            # Step 10: Time Zones
            "echo (+) Time Zones",
            "ln -sf /usr/share/zoneinfo/{}/{} /etc/localtime".format(region, city),						# Step 10: Time Zones; Set time zone
            "hwclock --systohc",																        # Step 10: Time Zones; Generate /etc/adjtime via hwclock
            # "echo ======= Location ======"													        # Step 11: Localization;
            "echo (+) Location",
            "sed -i '/{}/s/^#//g' /etc/locale.gen".format(language), 									# Step 11: Localization; Uncomment locale using sed
            "locale-gen",																	            # Step 11: Localization; Generate the locales by running
            "echo \"LANG=${}\" | tee -a /etc/locale.conf".format(language),								# Step 11: Localization; Set LANG variable according to your locale
            # "echo ======= Network Configuration ======"										        # step 12: Network Configuration;
            "echo (+) Network Configuration",
            "echo \"{}\" | tee -a /etc/hostname".format(hostname),										# Step 12: Network Configuration; Set Network Hostname Configuration; Create hostname file
            "echo \"127.0.0.1   localhost\" | tee -a /etc/hosts",							            # Step 12: Network Configuration; Add matching entries to hosts file
            "echo \"::1         localhost\" | tee -a /etc/hosts",							            # Step 12: Network Configuration; Add matching entries to hosts file
            "echo \"127.0.1.1   {}.localdomain	{}\" | tee -a /etc/hosts".format(hostname, hostname),	# Step 12: Network Configuration; Add matching entries to hosts file
            # "echo ======= Make Initial Ramdisk ======="										        # Step 13: Initialize RAM file system;
            "echo (+) Making Initial Ramdisk",
            "mkinitcpio -P {}".format(default_Kernel),												    # Step 13: Initialize RAM file system; Create initramfs image (linux-lts kernel)
            # "echo ======= Change Root Password ======="										        # Step 14: User Information; Set Root Password
            "echo (+) Change Root Password",
            "passwd || passwd",																	        # Step 14: User Information; Set Root Password
        ]

        # --- Extra Information

        #### Step 15: Install Bootloader
        ### NOTE:
        ### 1. Please Edit [osdef] on top with the bootloader information before proceeding
        ####
        # Default Bootloader
        if bootloader == "":
            # Empty : Reset to 'Grub'
            print("(-) Bootloader is not specified, we will default to Grub(2.0)")
            bootloader="grub"

        # Step 15: Bootloader
        # Switch Case bootloader between grub and syslinux
        if (bootloader == "grub"):
            # Default Bootloader Directory
            if bootloader_directory == "":
                # Empty : Reset to 'Grub'
                print("(-) Sorry, $bootloader_directory is not provided, defaulting to /boot/grub")
                bootloader_directory="/boot/grub"

            # Setup bootloader
            chroot_commands.append("echo (+) Installing Bootloader : Grub")
            chroot_commands.append("sudo pacman -S grub")						# Install Grub Package

            # Check if partition table is GPT
            if partition_Table == "gpt":
                # Install GPT/(U)EFI dependencies
                chroot_commands.append("sudo pacman -S efibootmgr")
    
            # Install Bootloader
            chroot_commands.append("grub-install --target={} {} {}".format(bootloader_target_device_Type, bootloader_optional_Params, disk_Label))	# Install Grub Bootloader

            # Generate bootloader configuration file
            chroot_commands.append("mkdir -p {}".format(bootloader_directory))                  # Create grub folder
            chroot_commands.append("grub-mkconfig -o {}/grub.cfg".format(bootloader_directory)) # Create grub config
        elif bootloader == "syslinux":
            ### Syslinux bootloader support is currently still a WIP and Testing
            chroot_commands.append("echo (+) Installing Bootloader : Syslinux")
            chroot_commands.append("sudo pacman -S syslinux")
            chroot_commands.append("mkdir -p /boot/syslinux")
            chroot_commands.append("cp -r /usr/lib/syslinux/bios/*.c32 /boot/syslinux")
            chroot_commands.append("extlinux --install /boot/syslinux")

            # Check partition table
            if (partition_Table == "msdos") or (partition_Table == "mbr"):
                chroot_commands.append("dd bs=440 count=1 conv=notrunc if=/usr/lib/syslinux/bios/mbr.bin of={}".format(disk_Label))
            elif (partition_Table == "gpt"):
                chroot_commands.append("sgdisk {} --attributes=1:set:2".format(disk_Label))
                chroot_commands.append("dd bs=440 conv=notrunc count=1 if=/usr/lib/syslinux/bios/gptmbr.bin of={}".format(disk_Label))

        # --- Processing

        # Combine into a string
        cmd_str = ";\n".join(chroot_commands)
        """
        for c in "${chroot_commands[@]}"; do
            cmd_str+="\n$c;"
        done
        """

        # Cat commands into script file in mount root
        mount_Root="{}/root".format(dir_Mount)
        script_to_exe="chroot-comms.sh"
        target_directory = "{}/{}".format(mount_Root, script_to_exe)
            
        print("Writing [\n{}\n] => {}".format(cmd_str, target_directory))
        if self.env.MODE != "DEBUG":
            with open(target_directory, "a+") as write_chroot_Commands:
                write_chroot_Commands.write(cmd_str)
                # Close file after usage
                write_chroot_Commands.close()

        print("")

        # Execute in arch-chroot
        # Future Codes deemed stable *enough*, thanks Past self for retaining legacy codes
        # for debugging
        self.default_Var["external_scripts"].append(
            ### Append all external scripts used ###
            "{}/{}".format(mount_Root, script_to_exe)
        )

        cmd_copy = [
            "chmod +x {}/{}".format(mount_Root, script_to_exe), 
            "arch-chroot {} /bin/bash -c \"/root/{}\"".format(dir_Mount, script_to_exe)
        ]
        if self.env.MODE != "DEBUG":
            # Loop through all actions
            for cmd in cmd_copy:
                ## Begin executing commands
                print("Executing: {}".format(cmd))
                stdout, stderr, returncode = process.subprocess_Sync(cmd)
                print("Standard Output: {}".format(stdout))

    # =========================== #
    # Post-Installation Functions #
    # =========================== #
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
    def postinstallation(self):
        """
        Post-Installation Recommendations and TODOs 
        - To be seperated into its own individual scripts for running
        """ 
        ### Header ###

        # Local Variable
        dir_Mount = self.cfg["mount_Paths"]["Root"] # Look for root/mount partition
        postinstall_commands = [
            ### Body ###
            # Enable Sudo
            "echo (+) Enable sudo",
            # PostInstall Must Do | Step 1: Enable sudo for group 'wheel'
            "sed -i 's/^#\s*\(%wheel\s\+ALL=(ALL:ALL)\s\+ALL\)/\1/' /etc/sudoers",
            # User Management
            "echo (+) User Management",
        ]

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
                cmd_check_if_user_Exists = "arch-chroot {} /bin/bash -c \"getent passwd {}\"".format(dir_Mount, u_Name) #  Check if user exists | Empty if Not Found
                u_Exists, stderr, returncode = process.subprocess_Sync(cmd_check_if_user_Exists)

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

                postinstall_commands.append("{}".format(u_create_Command))
                postinstall_commands.append("echo \"\t(+) Password change for {}\"".format(u_Name))
                postinstall_commands.append("if [[ \"$?\" == \"0\" ]]; then")
                postinstall_commands.append("	passwd $u_name")
                postinstall_commands.append("fi")

        ### Footer ###

        # =============== #
        # Execute Command #
        # =============== #

        # Combine into a string
        cmd_str = ";\n".join(postinstall_commands)
        """
        cmd_str=""
        for c in "${postinstall_commands[@]}"; do
            cmd_str+="\n$c"
        done
        """
        
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

        # Iterate and loop through elements of chroot_exec_Script
        for script in chroot_exec_Script:
            print("Executing: {}".format(script))
            if self.env.MODE != "DEBUG":
                # Change Permission and Execute command
                stdout, returncode = process.subprocess_Line(chroot_exec_Script)

                if returncode == 0:
                    # Success
                    print("Standard Output: {}".format(stdout))

        # Append external script path to the default variable key "external_scripts"
        self.default_Var["external_scripts"].append(
            ### Append all external scripts used ###
            "{}/{}".format(mount_Root, script_to_exe)
        )

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

                cmd_to_exec = [
                    "arch-chroot {} /bin/bash -c \"su - {} -c 'echo $(id -gn {})'\"".format(dir_Mount, sel_uhome, sel_uhome),
                    "arch-chroot {} /bin/bash -c \"su - {} -c 'echo $HOME'\"".format(dir_Mount, sel_uhome)
                ]

                if self.env.MODE == "DEBUG":
                    print("Executing: {}".format(cmd_to_exec[0]))
                    print("Executing: {}".format(cmd_to_exec[1]))
                else:
                    # Get the home directory of the user
                    sel_primary_group, stderr, returncode = process.subprocess_Sync(cmd_to_exec[0])
                    sel_uhome_dir, stderr, returncode = process.subprocess_Sync(cmd_to_exec[1])

                    # Start copy
                    for i in range(number_of_external_scripts):
                        curr_script = self.default_Var["external_scripts"][i]
                        print("Copying from [{}] : {} => {}/{}/".format(dir_Mount, curr_script, dir_Mount, sel_uhome_dir))
                        shutil.copy2(curr_script, "{}/{}".format(dir_Mount, sel_uhome_dir))

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

        print("")

        print("Sanitization Completed.")

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
        success_Flag = self.update_system_Clock()
        if success_Flag == False:
            print("(X) Error updating system clock via Network Time Protocol (NTP)")
            exit(1)
        
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
            exit(1)
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
            exit(1)
        print("(D) Disks mounted.")

        if self.env.MODE == "DEBUG":
            tmp = input("Press anything to continue...")

        print("")

        print("=======================")
        print("Stage 6: Select Mirrors")
        print("=======================")
        
        print("(S) Selecting mirrors...")
        print("{} /etc/pacman.d/mirrorlist".format(self.env.EDITOR))
        print("(D) Mirror selected.")

        if self.env.MODE == "DEBUG":
            tmp = input("Press anything to continue...")

        print("")

        print("===================================")
        print("Stage 7: Install essential packages")
        print("===================================")
        print("(S) Strapping packages to mount point...")
        success_Flag = self.bootstrap_Install()
        if success_Flag == False:
            print("(X) Errors bootstrapping packages")
            exit(1)
        print("(D) Packages strapped.")

        if self.env.MODE == "DEBUG":
            tmp = input("Press anything to continue...")

        print("")

        print("===========================================")
        print("Stage 8: Generate fstab (File System Table)")
        print("===========================================")
        print("(S) Generating Filesystems Table in /etc/fstab")
        success_Flag = self.fstab_Generate()
        if success_Flag == False:
            print("(X) Error generating filesystems table")
            exit(1)
        print("(D) Filesystems Table generated.")

        if self.env.MODE == "DEBUG":
            tmp = input("Press anything to continue...")

        print("")

        print("===========================")
        print("Stage 9: Chroot and execute")
        print("===========================")

        print("(S) Executing chroot commands")
        success_Flag = self.arch_chroot_Exec() # Execute commands in arch-chroot
        if success_Flag == False:
            print("(X) Error executing commands in chroot")
            exit(1)
        print("(D) Commands executed")

        if self.env.MODE == "DEBUG":
            tmp = input("Press anything to continue...")

        print("")

        print("=======================")
        print("Installation Completed.")
        print("=======================")

        print("")

        print("=================")
        print("Post-Installation")
        print("=================")

        print("(S) Starting Basic Post-Installation")

        print("(+) Running post-installation...")
        success_Flag = self.postinstallation()
        if success_Flag == False:
            print("(-) Error detected in post-installation process")
            exit(1)
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
            exit(1)
        print("(+) Sanitization completed")

        if self.env.MODE == "DEBUG":
            tmp = input("Press anything to continue...")

        print("")

        print("(D) Basic Post-Installation processes completed.")

        finish = input("(D) Finished, press anything to quit.")

