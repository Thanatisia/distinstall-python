# Framework/Library Documentation

## Documentation
### Modules
- distribution-name
    - mechanism

### Classes
- mechanism
    - Distribution_Name : Contains Base-Installation functionalities; Represented by the distribution's name itself (i.e. ArchLinux); This is planned to be rewritten as 'BaseInstallation' instead
        - Parameters
            + Setup() : The Setup class object initialized by the main function during the initial setup, as well as the distribution switch/runner file
    - PostInstallation  : Contains Post-Installation functionalities
        - Parameters
            + Setup() : The Setup class object initialized by the main function during the initial setup, as well as the distribution switch/runner file
            + Distribution_Name() : The Base Installation class object initialized during startup; Optional - To be replaced with 'BaseInstallation()'

### Functions
- mechanism
    - Distribution_Name
        - Callback/Event Utility functions
            - update_setup(self, setup)  : Update the current attributes in the class with the parsed setup object
                - Parameters
                    + setup : The Setup class object initialized by the main function during the initial setup, as well as the distribution switch/runner file
            + print_configurations(self) : Print all current configurations

        - Installation Stages
            - verify_network(self, ping_Count=5, ipv4_address="8.8.8.8") : Step 1 - Verify that the host network is working
                - Parameters
                    - ping_Count : Number of times the ping test is ran
                        + Type: Integer
                        + Default: 5
                    - ipv4_address : The IPv4 Address to test ping with
                        + Type: String
                        + Default: "8.8.8.8"
            - verify_boot_Mode(self) : Step 2 - Verify motherboard bootloader firmware
                - Information
                    + BIOS : Legacy
                    + UEFI : Modern Universal EFI mode
            - update_system_Clock(self) : Sync the host system's NTP
            - device_partition_Manager(self) : Device & Partition Manager
            - mount_Disks(self) : Mount Disks and Partitions
            - bootstrap_Install(self) : Bootstrap all essential and must have packaes to mount (/mnt) before the chroot process
            - fstab_Generate(self) : Generate File System Table (fstab)
        - Chroot Actions
            - format_chroot_Subprocess(self, cmd_str, mount_Dir="/mnt", chroot_Command="arch-chroot", shell="/bin/bash") : Format and returns the command string into the subprocess command list
                - Parameters
                    + cmd_str : The command string to execute
                    - mount_Dir : The mount directory containing the mounted root partition
                        + Type: String
                        + Default: "/mnt"
                    - chroot_Command : The chroot executable used to enter the new root filesystem
                        + Type: String
                        + Default: "arch-chroot"
                    - shell : The shell
                        + Type: String
                        + Default: "/bin/bash"
                - Output
                    - Chroot-formatted List
                        + Type: List
            - chroot_execute_command(self, cmd_str, mount_Dir="/mnt", chroot_Command="arch-chroot", shell="/bin/bash") : Generalized chroot command execution
                - Parameters
                    + cmd_str : The command string to execute
                    - mount_Dir : The mount directory containing the mounted root partition
                        + Type: String
                        + Default: "/mnt"
                    - chroot_Command : The chroot executable used to enter the new root filesystem
                        + Type: String
                        + Default: "arch-chroot"
                    - shell : The shell
                        + Type: String
                        + Default: "/bin/bash"
            - chroot_execute_command_List(self, cmd_List, mount_Dir="/mnt", chroot_Command="arch-chroot", shell="/bin/bash") : Generalized chroot command list execution
                - Parameters
                    + cmd_list : The list of commands to execute
                    - mount_Dir : The mount directory containing the mounted root partition
                        + Type: String
                        + Default: "/mnt"
                    - chroot_Command : The chroot executable used to enter the new root filesystem
                        + Type: String
                        + Default: "arch-chroot"
                    - shell : The shell
                        + Type: String
                        + Default: "/bin/bash"
            - sync_Timezone(self, mount_Dir, region, city) : Synchronize Hardware Clock in chroot
                - Parameters
                    - mount_Dir : The mount directory containing the mounted root partition
                        + Type: String
                    - region : The target region (Country)
                        + Type: String
                    - city : The target city within your region
                        + Type: String
            - enable_Locale(self, mount_Dir, language) : Uncomment and Enable locale/region
                - Parameters
                    - mount_Dir : The mount directory containing the mounted root partition
                        + Type: String
                    - language : The target locale/language for your system
                        + Type: String
            - network_Management(self, mount_Dir, hostname) : Append Network Host file
                - Parameters
                    - mount_Dir : The mount directory containing the mounted root partition
                        + Type: String
                    - hostname : Specify the network host name you wish to map to your system; Found in '/etc/hostname'
                        + Type: String
            - initialize_Ramdisk(self, mount_Dir, default_Kernel="linux") : Format initial ramdisk
                - Parameters
                    - mount_Dir : The mount directory containing the mounted root partition
                        + Type: String
                    - default_Kernel : Specify the default kernel to format and initialize with
                        + Type: String
                        + Default: "linux"
            - set_root_Password(self, mount_Dir) : Set Root Password
                - Parameters
                    - mount_Dir : The mount directory containing the mounted root partition
                        + Type: String
            - install_bootloader_Packages(self, dir_Mount="/mnt", bootloader="grub", partition_Table="msdos") : Bootloader Step 1 - Install bootloader packages
                - Parameters
                    - dir_Mount : The mount directory containing the mounted root partition
                        + Type: String
                        + Default: "/mnt"
                    - bootloader : The target bootloader of your choice; i.e. 'grub', 'syslinux'
                        + Type: String
                        + Default: "grub"
                        - Possible Values
                            + grub
                            + syslinux
                    - partition_Table : Your disk's partition table; i.e. 'msdos', 'gpt'
                        + Type: String
                        + Default: "msdos"
                        - Possible Values
                            + msdos
                            + gpt
            - prepare_Bootloader(self, dir_Mount="/mnt", bootloader="grub", bootloader_directory="/boot/grub") : Bootloader Step 2 - Prepare Bootloader directories and Pre-Requisites
                - Parameters
                    - dir_Mount : The mount directory containing the mounted root partition
                        + Type: String
                        + Default: "/mnt"
                    - bootloader : The target bootloader of your choice; i.e. 'grub', 'syslinux'
                        + Type: String
                        + Default: "grub"
                        - Possible Values
                            + grub
                            + syslinux
                    - bootloader_directory : The directory where the bootloader will be installed to
                        + Type: String
                        + Default: "/boot/grub"
            - install_Bootloader(self, disk_Label, dir_Mount="/mnt", bootloader="grub", bootloader_directory="/boot/grub", partition_Table="msdos", bootloader_optional_Params="", bootloader_target_Architecture="i386-pc") : Bootloader Step 3 - Install Bootloader to the Partition Table
                - Parameters
                    - disk_Label : Your Device/Disk's Label/Name based on your storage controller; i.e. SATA|AHCI => /dev/sdX, NVME => /dev/nvmeNpX, Loopback => /dev/loopNpX
                        + Type: String
                        - Possible Values
                            + SATA/AHCI : /dev/sdX
                            + NVME : /dev/nvme[device-number]p[partition-number]
                            + Loopback : /dev/loop[device-number]p[partition-number]
                    - dir_Mount : The mount directory containing the mounted root partition
                        + Type: String
                        + Default: "/mnt"
                    - bootloader : The target bootloader of your choice; i.e. 'grub', 'syslinux'
                        + Type: String
                        + Default: "grub"
                        - Possible Values
                            + grub
                            + syslinux
                    - bootloader_directory : The directory where the bootloader will be installed to
                        + Type: String
                        + Default: "/boot/grub"
                    - partition_Table : Your disk's partition table; i.e. 'msdos', 'gpt'
                        + Type: String
                        + Default: "msdos"
                        - Possible Values
                            + msdos
                            + gpt
                    - bootloader_optional_Params : Any additional option parameters to parse into the bootloader
                        + Type: String
                        + Default: ""
                    - bootloader_target_Architecture : The target system architecture to install the bootloader on
                        + Type: String
                        + Default: "i386-pc"
            - generate_bootloader_Configs(self, disk_Label, dir_Mount="/mnt", bootloader="grub", bootloader_directory="/boot/grub", partition_Table="msdos", bootloader_optional_Params="", bootloader_target_Architecture="i386-pc") : Bootloader Step 4 - Generate Bootloader configuration files
                - Parameters
                    - disk_Label : Your Device/Disk's Label/Name based on your storage controller; i.e. SATA|AHCI => /dev/sdX, NVME => /dev/nvmeNpX, Loopback => /dev/loopNpX
                        + Type: String
                        - Possible Values
                            + SATA/AHCI : /dev/sdX
                            + NVME : /dev/nvme[device-number]p[partition-number]
                            + Loopback : /dev/loop[device-number]p[partition-number]
                    - dir_Mount : The mount directory containing the mounted root partition
                        + Type: String
                        + Default: "/mnt"
                    - bootloader : The target bootloader of your choice; i.e. 'grub', 'syslinux'
                        + Type: String
                        + Default: "grub"
                        - Possible Values
                            + grub
                            + syslinux
                    - bootloader_directory : The directory where the bootloader will be installed to
                        + Type: String
                        + Default: "/boot/grub"
                    - partition_Table : Your disk's partition table; i.e. 'msdos', 'gpt'
                        + Type: String
                        + Default: "msdos"
                        - Possible Values
                            + msdos
                            + gpt
                    - bootloader_optional_Params : Any additional option parameters to parse into the bootloader
                        + Type: String
                        + Default: ""
                    - bootloader_target_Architecture : The target system architecture to install the bootloader on
                        + Type: String
                        + Default: "i386-pc"
            - bootloader_Management(self, disk_Label, dir_Mount="/mnt", bootloader="grub", bootloader_directory="/boot/grub", partition_Table="msdos", bootloader_optional_Params="", bootloader_target_Architecture="i386-pc") : Executes Bootloader Steps 1 to 4
                - Parameters
                    - disk_Label : Your Device/Disk's Label/Name based on your storage controller; i.e. SATA|AHCI => /dev/sdX, NVME => /dev/nvmeNpX, Loopback => /dev/loopNpX
                        + Type: String
                        - Possible Values
                            + SATA/AHCI : /dev/sdX
                            + NVME : /dev/nvme[device-number]p[partition-number]
                            + Loopback : /dev/loop[device-number]p[partition-number]
                    - dir_Mount : The mount directory containing the mounted root partition
                        + Type: String
                        + Default: "/mnt"
                    - bootloader : The target bootloader of your choice; i.e. 'grub', 'syslinux'
                        + Type: String
                        + Default: "grub"
                        - Possible Values
                            + grub
                            + syslinux
                    - bootloader_directory : The directory where the bootloader will be installed to
                        + Type: String
                        + Default: "/boot/grub"
                    - partition_Table : Your disk's partition table; i.e. 'msdos', 'gpt'
                        + Type: String
                        + Default: "msdos"
                        - Possible Values
                            + msdos
                            + gpt
                    - bootloader_optional_Params : Any additional option parameters to parse into the bootloader
                        + Type: String
                        + Default: ""
                    - bootloader_target_Architecture : The target system architecture to install the bootloader on
                        + Type: String
                        + Default: "i386-pc"
            - archive_command_Str(self, cmd_str, dir_Mount="/mnt") : Output command string into a file for archiving
                - Parameters
                    - cmd_str : The command string to execute
                        + Type: String
                    - dir_Mount : The mount directory containing the mounted root partition
                        + Type: String
                        + Default: "/mnt"
        - Body
            - arch_chroot_Exec(self) : Execute commands using arch-chroot due to limitations with shellscripting
            - installer(self) : Main setup installer; Runs Step 1 to 9 - Chroot command execution
    - PostInstallation : Class for the Post-Installation functions in the installation library/framework
        - Initialization
            - init_Config(self) : Initialize defaults from configuration file if base installation is not used
        - Callback/Event Utility functions
            - update_setup(self, setup)
                - Parameters
                    - setup : The Setup class object initialized by the main function during the initial setup, as well as the distribution switch/runner file
                        + Type: Setup()
            - print_configurations(self)
            - postinstall_todo(self)
            - postinstall_sanitize(self) : To sanitize the account from any unnecessary files
        - User Management
            - get_users_Home(self, user_name) : Get the home directory of a user
                - Parameters
                    - user_name : The name of the target user
                        + Type: String
            - check_user_Exists(self, user_name) : Check if user exists
                - Parameters
                    - user_name : Specify the target user to check if exists
                        Type: String
            - useradd_get_default_Params(self) : Get default user parameters
        - Post-Installation Stages
            - enable_sudo(self, dir_Mount="/mnt") : Enabling sudo in /etc/sudoers via command line
                - Parameters
                    - dir_Mount : The mount directory containing the mounted root partition
                        + Type: String
                        + Default: "/mnt"
            - postinstallation(self) : Post-Installation Recommendations and TODOs 
        - Body
            - postinstaller(self) : Main post-installation installer

### Attributes/Variables
- mechanism
    - Distribution_Name
        + setup : The Setup class object
        + env : Environment class object
        + cfg : Contains the setup configuration key-value mappings in the class
        + default_Var : Contains the setup default variable key-value/dictionary mappings

    - PostInstallation
        + setup : The Setup class object
        + cfg : Contains the setup configuration key-value mappings in the class

## Wiki

## Resources

## References

## Remarks


