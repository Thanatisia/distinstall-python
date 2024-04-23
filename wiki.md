# Framework/Library Documentation

## Documentation

### Packages
- pydistinstall : The main/core distribution installer package

### Modules/Libraries
- pydistinstall
    + main : The main entry point source file for the 'py-distinstall' CLI utility executable; This is the current main project. This may be reworked and refactored
    + setup : The setup library for the 'py-distinstall' CLI utility executable
    - app/ : Submodule containing all the application logic and the core base/post-installation library/framework modules
        + `.runner` : The main runner for the distribution installation functionality; This is called by 'main.py' which will then be used as a load balancer for pulling the functions from the respective distribution's core module
        - distributions/ : Contains all submodules relating to each distributions (i.e archlinux : for ArchLinux)
            - archlinux/ : Contains all modules relating to ArchLinux
                + `.mechanism` : The core installation module/library containing functions and classes relating to installing and configuring a working, chrootable ArchLinux root filesystem
    - lib/ : Submodule containing all general helper libraries/modules used by the distribution installer CLI utility
        + `.cli`               : Contains functions relating to this application's CLI argument parsing
        + `.config_handler`    : Contains configuration file handling and processing functions
        + `.const`             : Contains all constant variables
        + `.device_management` : Device Management module containing device/disk handling functions
        + `.env `              : Contains Environment Variables used by the CLI application
        + `.format`            : Contains functions about formatting objects
        + `.process`           : Contains functions about system processes/subprocess handling
        + `.user_management`   : User Management module containing User authentication and authorization functions
        + `.utils`             : General utilities module containing various non-categorised helper functions

### Classes
- pydistinstall
    - .setup
        + `.Setup()` : Initializes the main CLI utility's setup functions

- pydistinstall.app
    - .runner
        - `.App(distribution_Name, setup, env)` : Initializes the main CLI utility's target distribution base installation load balancer
            - Parameter Signature/Header
                - distribution_Name : Pass the user's target distribution here
                    + Type: String
                - setup : Pass the caller's setup class instance here
                    + Type: pydistinstall.setup.Setup()
                - env : Pass the caller's environment class instance here
                    + Type: pydistinstall.lib.env.Environment()
            - Class constructor/initialization Flow
                1. Set the target distribution to install
                2. Initialize the supported distributions list
                3. Set the caller's setup class object to this application instance
                4. Set the caller's env class object to this application instance
                5. Initialize variables
                6. Set the class's distribution name according to the specified distribution in the configuration file
                7. Set the current distribution to the setup class instance's distribution name (to be refactored)
                8. Select and set/'switch' the platform acccording to the user's configuration settings
                9. Select and set/'switch' the installation function according to the user's configuration settings

- pydistinstall.app.distributions.archlinux
    - .mechanism
        - `.BaseInstallation(setup)` : Initializes the class object for the Base Installation of the target distribution containing various Base installation-related functions and attribues/variables
            - Parameter Signature/Header
                - setup : Specify and store the caller's initialized setup class object
                    + Type: pydistinstall.setup.Setup()
        - `.PostInstallation(setup, base_mechanism_Obj)` : Initializes the class object for the Post Installation of the target distribution containing various Post installation-related functions and attribues/variables
            - Parameter Signature/Header
                - setup : Specify and store the caller's initialized setup class object
                    + Type: pydistinstall.setup.Setup()
                - base_mechanism_Obj : Specify the caller's initialized BaseInstallation() class object
                    + Type: pydistinstall.app.distributions.archlinux.mechanism.BaseInstallation(setup)
                    + Default Value: None

- pydistinstall.lib
    - .cli
        + `.CLIParser()` : Initializes the class object for the CLI argument parser class and retrieve the CLI argument list specifeid by the user, calculate the count and start processing the CLI arguments
    - .config_handler
        - `.YAMLConfig(file_name, mode="r")` : Initializes the YAML Configuration File handler class object
            - Parameter Signature/Header
                - file_name : Specify the name of the configuration file you wish to import
                    + Type: String
                - mode : Specify the default mode you wish to open the file with
                    + Type: String
                    +  Default: "r"
                    - Accepted Values
                        + a : Append file
                        + r : Read-only
                        + w : Write-only (Overwrite/Truncate)
                        + w+ : Write + Read
                        + r+ : Reaad + Write
                        + rb : Read Bytes
                        + wb : Write Bytes
    - .const
        + `.Constants()` : Initializes the Constants class object (Currently Unused)
    - .env
        + `.Environment()` : Initializes the Environment Variable class object and obtaining all Environment Variables found on boot-time
    - .format
        + `.Text()` : Initializes Text Formatting class object containing text-related support and functions

### Data Classes/Types
### Functions
- pydistinstall.main
    - `.init()` : Application Initialization
        - Functional Flow
            1. Initialize the setup class
            2. Initialize Program Information
            3. Process CLI arguments
    + `.init_Application()` : Initialize the 'App' class
    + `.display_info()` : Print and display system information
    + `.display_help()` : Display help message
    + `.display_Options()` : Display all optionals and positionals arguments parsed
    + `.verify_Init()` : Perform distribution installer pre-processing and pre-startup check
    + `.verify_Env()` : Verify Environment Variables
    + `.begin_installer()` : Begin installation process
    + `.body()` : Begin the CLI argument processing
    + `.main()` : The CLI utility application's main entry point function

- pydistinstall.setup.Setup
    + `.init_defaults()` : Initialize system default on startup
    - `.init_prog_Info(program_scriptname, program_appName, program_Type, program_Version, program_Mode, distribution, config_Name="config.yaml")` : Initialize the program information
        - Parameter Signature/Header
            - program_scriptname : Specify the program's executable file name
                + Type: String
            - program_appName    : Specify the application's title/name
                + Type: String
            - program_Type       : Specify the type of application (i.e. CLI, GUI, TUI)
                + Type: String
            - program_Version : Specify the current program version
                + Type: String
            - program_Mode : Specify the boot mode (DEBUG|RELEASE)
                + Type: String
            - distribution : Specify the target base distribution you wish to install
                + Type: String
            - config_Name : Specify the target configuration file to import into the system
                + Type: String
                + Default: "config.yaml"
    - `.update_prog_variable(program_scriptname, program_appName, program_Type, program_Version, program_Mode, distribution, config_Name)` :  Update and replace the current program information with the new values
        - Parameter Signature/Header
            - program_scriptname : Specify the program's executable file name
                + Type: String
                + Default: ""
            - program_appName    : Specify the application's title/name
                + Type: String
                + Default: ""
            - program_Type       : Specify the type of application (i.e. CLI, GUI, TUI)
                + Type: String
                + Default: ""
            - program_Version : Specify the current program version
                + Type: String
                + Default: ""
            - program_Mode : Specify the boot mode (DEBUG|RELEASE)
                + Type: String
                + Default: ""
            - distribution : Specify the target base distribution you wish to install
                + Type: String
                + Default: ""
            - config_Name : Specify the target configuration file to import into the system
                + Type: String
                + Default: "config.yaml"
    + `.init_Variables()` : Initialize default variables
    - `.generate_config_YAML(cfg_fname)` : Generates a template env config file that will contain the variables to be used in the install script
        - Parameter Signature/Header
            - cfg_fname : Specify the file name of the configuration file to be generated
                + Type: String
                + Default: "config.yaml"
    - `.generate_config_Raw(cfg_fname)` : Generates a template configuration file that will contain the variables to be used in the install script as a raw string
        - Parameter Signature/Header
            - cfg_fname : Specify the file name of the configuration file to be generated
                + Type: String
                + Default: "config.yaml"
    - `.load_config(cfg_fname)` : Load the specified configuration file
        - Parameter Signature/Header
            - cfg_fname : Specify the file name of the configuration file to be loaded
                + Type: String
                + Default: "config.yaml"
        - Return
            - configs : A Dictionary (key-value) containing the imported configuration file contents
                + Type: Dictionary
    + `.start()` : Begin setup (Unused)

- pydistinstall.app.runner.App
    - `.set_distribution_Name()`: Get specified distribution from the configuration file and set it to `self.dist`
        - Return
            + Type: Void
    - `.update_setup()`: Update the setup variables according to that of the target platform's installer mechanism class
        - Return
            + Type: Void
    - `.platform_Select()`: Switch and initialize the distribution installation mechanic class according to the distribution name
        - Return
            + Type: Void
    - `.installer_switch()`: Search for the installation functions based on specified distribution and set `self.installer` and `self.postinstaller` to the `BaseInstallation()` class and the `PostInstallation()` respectively
        - Return
            + Type: Void
    - `.list_steps()`: List/Print all installation stages/steps
        - Return
            + Type: Void
    - `.execute_Step(step_Number)`: Execute only a specific step
        - Parameter Signature/Header
            - step_Number : Specify the installer stage to execute
                + Type: Integer
        - Operational Flow
            1. Check if the target distribution's BaseInstallation() class is initialized
            2. If it is, initialize a local dictionary variable containing a key-value mapping of the stage number to the corresponding base instalaltion stage function in the `BaseInstallation` class
                ```python
                steps = {
                    1 : self.installer_class.verify_network,
                    2 : self.installer_class.verify_boot_Mode,
                    3 : self.installer_class.update_system_Clock,
                    4 : self.installer_class.device_partition_Manager,
                    5 : self.installer_class.mount_Disks,
                    6 : self.installer_class.bootstrap_Install,
                    7 : self.installer_class.fstab_Generate,
                    8 : self.installer_class.arch_chroot_Exec,
                    9 : self.installer_class_PostInstall.postinstallation,
                    10 : self.installer_class_PostInstall.postinstall_sanitize,
                }
                ```
            3. Try and convert the stage number into integer
            4. Obtain the function to execute
            5. Execute the stage function and return the result
    - `.pre_start_Setup()`: Check if installer mechanism class is initialized
        - Return
            + Type: Void
    - `.begin()`: Begin the base and post installation
        - Return
            + Type: Void

- pydistinstall.app.distributions.archlinux.mechanism.BaseInstallation
    - Callback/Event Utility functions
        - `.update_setup(setup)` : Update the setup object to the latest data
            - Parameter Signature/Header
                - setup : Store the caller's initialized setup class object
                    + Type: pydistinstall.setup.Setup()
        - `.print_configurations()`: Print the currently stored configuration settings to standard output
            - Return
                + Type: Void

    - Installation stages
        - `.verify_network(ping_Count=5, ipv4_address="8.8.8.8")`: Installation Stage 1 - Verify that the host network is working
            - Parameter Signature/Header
                - ping_Count : The number of times (counts) the system will ping the target address
                    + Type: Integer
                    + Default Value: 5

                - ipv4_address : The IPv4 network address you wish to ping
                    + Type: String
                    + Default Value: 8.8.8.8
            - Return
                - res : Return the result of the verification (True = Network is available, False = Not available)
                    + Type: Boolean

        - `.verify_boot_Mode()`: Installation Stage 2 - Verifies and returns the motherboard bootloader firmware
            - Information
                - Motherboard Bootloader Firmware
                    - BIOS : Legacy
                    - UEFI : Modern Universal EFI mode

            - Return 
                - boot_Mode : Returns the boot mode/bootloader firmware of the system
                    + Type: String
                    + Default: bios
                    - Values
                        + uefi : If the '/sys/firmware/efi/efivars' directory is found

        - `.update_system_Clock(): Installation Stage 3 - Syncs the system clock using NTP (Network-Time Protocol) by syncing with a central server
            - Return 
                + Type: Tuple
                - Values
                    - [0] stdout : The Standard Output stream from the command execution
                        + Type: String
                    - [1] stderr :  The Standard Error stream from the command excution
                        + Type: String
                    - [2] returncode : Result/Return Status Code from the command execution
                        + Type: Integer
                        - Values
                            + 0 = Success
                            + > 0 = Failed
                    - [3] success_flag : A boolean flag showing if the command was a success or failed
                        + Type: Boolean
                        - Values
                            + True: Success
                            + False: Error

        - `.device_partition_Manager()`: Installation Stage 4 - Device & Partition Management
            - Operational Flow
                1. Get filesystem information
                2. Format disk label partition table
                3. Create disk partitions
                4. Set partition settings
                5. Format partition filesystem
            - Return
                + Type: Void

        - `.mount_partition_Root(disk_Label, root_Dir, partition_Scheme, storage_controller, partition_Name, partition_Number)`: Mount Root Partition
            - Parameter Signature/Header
                - disk_Label : Specify the target disk/device containing the root partition
                    + Type: String | pydistinstall.setup.Setup().cfg["disk_Label"]
                    - Disk Label Formats
                        - sata : For SATA/AHCI devices
                            + Format: /dev/sdX
                        - nvme : For NVME devices
                            + Format: /dev/nvme[device-number]np[partition-number]
                        - loop : For Loopback devices
                            + Format: /dev/loop[device-number]p[partition-number]

                - root_Dir : The root partition mount path
                    + Type: String | `pydistinstall.setup.Setup().cfg["mount_Paths"]["Root"]`

                - partition_Scheme : Key-Value Mapping of the partition scheme design
                    + Type: Dictionary | pydistinstall.setup.Setup().cfg["partition_Scheme"]

                - storage_controller : The type of storage controller your device/disk uses
                    + Type: String | pydistinstall.setup.Setup().cfg["storage-controller"]
                    - Storage Controllers:
                        + sata : AHCI/SATA
                        + nvme : NVME
                        + loop : Loopback

                - partition_Name : Name of the current partition
                    + Type: String
                    + Default: Root

                - partition_Number : The partition number
                    + Type: Integer
                    + Default: 1
            - Return
                + Type: Void

        - `.mount_partition_Boot(disk_Label, boot_Dir, partition_Scheme, storage_controller, partition_Name, partition_Number)`: Mount Boot Partition
            - Parameter Signature/Header
                - disk_Label : Specify the target disk/device containing the boot partition
                    + Type: String | pydistinstall.setup.Setup().cfg["disk_Label"]
                    - Disk Label Formats
                        - sata : For SATA/AHCI devices
                            + Format: /dev/sdX
                        - nvme : For NVME devices
                            + Format: /dev/nvme[device-number]np[partition-number]
                        - loop : For Loopback devices
                            + Format: /dev/loop[device-number]p[partition-number]

                - boot_Dir : The boot partition mount path
                    + Type: String | `pydistinstall.setup.Setup().cfg["mount_Paths"]["Boot"]`

                - partition_Scheme : Key-Value Mapping of the partition scheme design
                    + Type: Dictionary | pydistinstall.setup.Setup().cfg["partition_Scheme"]

                - storage_controller : The type of storage controller your device/disk uses
                    + Type: String | pydistinstall.setup.Setup().cfg["storage-controller"]
                    - Storage Controllers:
                        + sata : AHCI/SATA
                        + nvme : NVME
                        + loop : Loopback

                - partition_Name : Name of the current partition
                    + Type: String
                    + Default: Boot

                - partition_Number : The partition number
                    + Type: Integer
                    + Default: 2
            - Return
                + Type: Void

        - `.mount_partition_Remaining(disk_Label, mount_Paths, partition_Scheme, storage_controller)`: Mount all other partitions
            - Parameter Signature/Header
                - disk_Label : The target disk you wish to write into
                    + Type: String | pydistinstall.setup.Setup().cfg["disk_Label"]
                    - Disk Label Formats
                        - sata : For SATA/AHCI devices
                            + Format: /dev/sdX
                        - nvme : For NVME devices
                            + Format: /dev/nvme[device-number]np[partition-number]
                        - loop : For Loopback devices
                            + Format: /dev/loop[device-number]p[partition-number]

                - mount_Paths : A Dictionary (key-value) mapping of a mount directory name to its mount path
                    + Type: Dictionary | pydistinstall.setup.Setup().cfg["mount_Paths"]

                - partition_Scheme : Key-Value Mapping of the partition scheme design
                    + Type: Dictionary | pydistinstall.setup.Setup().cfg["partition_Scheme"]

                - storage_controller : The type of storage controller your device/disk uses
                    + Type: String | pydistinstall.setup.Setup().cfg["storage-controller"]
                    - Storage Controllers:
                        + sata : AHCI/SATA
                        + nvme : NVME
                        + loop : Loopback

        - `.mount_Disks()`: Installation Stage 5 - Mount Disks, the Root, Boot and other Partitions
            - Return
                + Type: Void

        - `.select_Mirrors(mirrorlist_Path)`: Select a mirror for the package manager (TODO: Currently unused; unimplemented)
            - Parameter Signature/Header
                - mirrorlist_Path : Specify the path to the mirrorlist
                    + Type: String
            - Return
                + Type: Void

        - `.check_package_manager_Configurations(mount_Dir)`: Check Package Manager configuration support
            - Parameter Signature/Header
                - mount_Dir : Specify the root/base filesystem mount path/directory containing the chroot environment
                    + Type: String
            - Return
                + Type: Void

        - `.bootstrap_Install()`: Installation Stage 6 - Bootstrap all essential and must have packages to the mounted root filesystem before the chroot process
            - Return 
                + Type: Tuple
                - Values
                    - [0] stdout : The Standard Output stream from the command execution
                        + Type: String
                    - [1] stderr :  The Standard Error stream from the command excution
                        + Type: String
                    - [2] returncode : Result/Return Status Code from the command execution
                        + Type: Integer
                        - Values
                            + 0 = Success
                            + > 0 = Failed

        - `.fstab_Generate()`: Installation Stage 7 - Generate the chroot root filesystem's File System Table (fstab)
            - Return
                - success_flag : A boolean flag showing if the command was a success or failed
                    + Type: Boolean
                    - Values
                        + True: Success
                        + False: Error

    - Chroot Actions
        - `.format_chroot_Subprocess(cmd_str, mount_Dir, chroot_Command, shell)`: Format and returns the command string into the subprocess command list
            - Parameter Signature/Header
                - cmd_str : Specify the system command string you want to execute in a subprocess pipe
                    + Type: String
                - mount_Dir : Specify the root/base filesystem mount path/directory containing the chroot environment
                    + Type: String
                    + Default: "/mnt"
                - chroot_Command : Specify the system command you wish to use to chroot into the root filesystem environment
                    + Type: String
                    + Default: "arch-chroot"
                - shell : Specify the shell used to execute the chroot systems command
                    + Type: String
                    + Default: "/bin/bash"
            - Return
                - subprocess_cmd_fmt : A list containing the commands to be executed in the chroot environment as well as the other flags and options
                    + Type List

        - `.chroot_execute_command(cmd_str, mount_Dir, chroot_Command, shell)`: Execute the system command string into the target mount point chroot root filesystem environment
            - Parameter Signature/Header
                - cmd_str : Specify the system command string you want to execute in a subprocess pipe
                    + Type: String
                - mount_Dir : Specify the root/base filesystem mount path/directory containing the chroot environment
                    + Type: String
                    + Default: "/mnt"
                - chroot_Command : Specify the system command you wish to use to chroot into the root filesystem environment
                    + Type: String
                    + Default: "arch-chroot"
                - shell : Specify the shell used to execute the chroot systems command
                    + Type: String
                    + Default: "/bin/bash"
            - Return
                - result : A Dictionary (key-value) mapping containing the standard output (stdout), standard error (stderr), the return status code (resultcode) and the command string (command-string)
                    + Type: Dictionary
                    - Key-Value Mappings
                        - stdout : The Standard Output stream from the command execution
                            + Type: String
                        - stderr :  The Standard Error stream from the command excution
                            + Type: String
                        - returncode : Result/Return Status Code from the command execution
                            + Type: Integer
                            - Values
                                + 0 = Success
                                + > 0 = Failed
                        - command-string : The command string formed from the chroot command list
                            + Type: String

        - `.chroot_execute_command_List(cmd_List, mount_Dir, chroot_Command, shell)`: Execute a system command in list form into the target mount point chroot root filesystem environment
            - Parameter Signature/Header
                - cmd_List : Specify the system command list you want to execute in a subprocess pipe
                    + Type: List
                - mount_Dir : Specify the root/base filesystem mount path/directory containing the chroot environment
                    + Type: String
                    + Default: "/mnt"
                - chroot_Command : Specify the system command you wish to use to chroot into the root filesystem environment
                    + Type: String
                    + Default: "arch-chroot"
                - shell : Specify the shell used to execute the chroot systems command
                    + Type: String
                    + Default: "/bin/bash"
            - Return
                - result : A Dictionary (key-value) mapping containing the standard output (stdout), standard error (stderr), the return status code (resultcode) and the command string (command-string)
                    + Type: Dictionary
                    - Key-Value Mappings
                        - stdout : The Standard Output stream from the command execution
                            + Type: String
                        - stderr :  The Standard Error stream from the command excution
                            + Type: String
                        - returncode : Result/Return Status Code from the command execution
                            + Type: Integer
                            - Values
                                + 0 = Success
                                + > 0 = Failed
                        - command-string : The command string formed from the chroot command list
                            + Type: String

        - `.sync_Timezone(mount_Dir, region, city)`: Synchronize Hardware Clock in the chroot root filesystem
            - Parameter Signature/Header
                - mount_Dir : Specify the root/base filesystem mount path/directory containing the chroot environment
                    + Type: String
                - region : Specify your system region (You can find it using 'ls /usr/share/zoneinfo' and choosing your region)
                    + Type: String
                - city : Specify your system city/country (You can find it using 'ls /usr/share/zoneinfo/<your-region>' and choosing your city)
                    + Type: String
            - Return
                + Type: Void

        - `.enable_Locale(mount_Dir, language)`: Uncomment and Enable locale/region
            - Parameter Signature/Header
                - mount_Dir : Specify the root/base filesystem mount path/directory containing the chroot environment
                    + Type: String
                - language : Specify the locale/language ISO code to set for your system (i.e. en_SG, en_US)
                    + Type: String
                    - NOTE: 
                        + You can find your language by searching in '/etc/locale.gen'
            - Return
                + Type: Void

        - `.network_Management(mount_Dir, hostname)`: Append Network Host file
            - Parameter Signature/Header
                - mount_Dir : Specify the root/base filesystem mount path/directory containing the chroot environment
                    + Type: String
                - hostname : Specify the chroot environment's network hostname to write into '/etc/hostname' and the '/etc/hosts' file; The hostname is used as an identifier for your system on the network
                    + Type: String
            - Return
                + Type: Void

        - `.initialize_Ramdisk(mount_Dir, default_Kernel="linux")`: Format initial ramdisk
            - Parameter Signature/Header
                - mount_Dir : Specify the root/base filesystem mount path/directory containing the chroot environment
                    + Type: String
                - default_Kernel : Specify the default linux kernel you wish to install with
                    + Type: String
                    + Default: linux
                    - Tested kernels
                        + linux : Linux base
            - Return
                - result : A Dictionary (key-value) mapping containing the standard output (stdout), standard error (stderr), the return status code (resultcode) and the command string (command-string)
                    + Type: Dictionary
                    - Key-Value Mappings
                        - stdout : The Standard Output stream from the command execution
                            + Type: String
                        - stderr :  The Standard Error stream from the command excution
                            + Type: String
                        - returncode : Result/Return Status Code from the command execution
                            + Type: Integer
                            - Values
                                + 0 = Success
                                + > 0 = Failed
                        - command-string : The command string formed from the chroot command list
                            + Type: String

        - `.set_root_Password(mount_Dir)`: Set the Root Password in the chroot root filesystem
            - Parameter Signature/Header
                - mount_Dir : Specify the root/base filesystem mount path/directory containing the chroot environment
                    + Type: String
            - Return
                - result : A Dictionary (key-value) mapping containing the standard output (stdout), standard error (stderr), the return status code (resultcode) and the command string (command-string)
                    + Type: Dictionary
                    - Key-Value Mappings
                        - stdout : The Standard Output stream from the command execution
                            + Type: String
                        - stderr :  The Standard Error stream from the command excution
                            + Type: String
                        - returncode : Result/Return Status Code from the command execution
                            + Type: Integer
                            - Values
                                + 0 = Success
                                + > 0 = Failed
                        - command-string : The command string formed from the chroot command list
                            + Type: String

        - `.install_bootloader_Packages(dir_Mount, bootloader, partition_Table)`: Install bootloader packages in the chroot root filesystem
            - Parameter Signature/Header
                - dir_Mount : Specify the root/base filesystem mount path/directory containing the chroot environment
                    + Type: String
                    + Default: "/mnt"
                - bootloader: Specify the target bootloader to install to your chroot environment
                    + Type: String
                    - Accepted Values
                        + grub : GRUB2
                - partition_Table: Specify the storage device/disk's partition table
                    + Type: String
                    + Default: msdos
                    - Accepted Values
                        + msdos : aka MBR (Master Boot Record); Used by BIOS Legacy Motherboard Bootloader Firmware
                        + gpt : aka GUID partition Table; Used by modern (U)EFI Motherboard Bootloader Firmware
            - Return
                - result : A Dictionary (key-value) mapping containing the standard output (stdout), standard error (stderr), the return status code (resultcode) and the command string (command-string)
                    + Type: Dictionary
                    - Key-Value Mappings
                        - stdout : The Standard Output stream from the command execution
                            + Type: String
                        - stderr :  The Standard Error stream from the command excution
                            + Type: String
                        - returncode : Result/Return Status Code from the command execution
                            + Type: Integer
                            - Values
                                + 0 = Success
                                + > 0 = Failed
                        - command-string : The command string formed from the chroot command list
                            + Type: String

        - `.prepare_Bootloader(dir_Mount, bootloader, bootloader_directory)`: Prepare Bootloader directories and Pre-Requisites
            - Parameter Signature/Header
                - dir_Mount : Specify the root/base filesystem mount path/directory containing the chroot environment
                    + Type: String
                    + Default: "/mnt"
                - bootloader: Specify the target bootloader to install to your chroot environment
                    + Type: String
                    - Accepted Values
                        + grub : GRUB2
                - bootloader_directory : Specify the boot directory containing your bootloader configuration files
                    + Type: String
                    + Default: "/boot/grub"
                    - Notes
                        + Certain bootloaders (i.e. Grub) have different boot directories based on partition table (i.e. MBR/GPT); 
                    + Value Format String: "/boot/<your-bootloader>"
                    - Recommended Bootloader directories
                        + grub: /boot/grub
            - Return
                - result : A Dictionary (key-value) mapping containing the standard output (stdout), standard error (stderr), the return status code (resultcode) and the command string (command-string)
                    + Type: Dictionary
                    - Key-Value Mappings
                        - stdout : The Standard Output stream from the command execution
                            + Type: String
                        - stderr :  The Standard Error stream from the command excution
                            + Type: String
                        - returncode : Result/Return Status Code from the command execution
                            + Type: Integer
                            - Values
                                + 0 = Success
                                + > 0 = Failed
                        - command-string : The command string formed from the chroot command list
                            + Type: String

        - `.install_Bootloader(disk_Label, dir_Mount="/mnt", bootloader="grub", bootloader_directory="/boot/grub", partition_Table="msdos", bootloader_optional_Params="", bootloader_target_Architecture="i386-pc")`: Install Bootloader to the chroot root filesyste's Partition Table
            - Parameter Signature/Header
                - disk_Label : Specify the target disk/device label you wish to install the bootloader into
                    + Type: String
                    - Disk Label Formats
                        - sata : For SATA/AHCI devices
                            + Format: /dev/sdX
                        - nvme : For NVME devices
                            + Format: /dev/nvme[device-number]
                        - loop : For Loopback devices
                            + Format: /dev/loop[device-number]
                - dir_Mount : Specify the root/base filesystem mount path/directory containing the chroot environment
                    + Type: String
                    + Default: "/mnt"
                - bootloader: Specify the target bootloader to install to your chroot environment
                    + Type: String
                    - Accepted Values
                        + grub : GRUB2
                - bootloader_directory : Specify the boot directory containing your bootloader configuration files
                    + Type: String
                    + Default: "/boot/grub"
                    - Notes
                        + Certain bootloaders (i.e. Grub) have different boot directories based on partition table (i.e. MBR/GPT); 
                    + Value Format String: "/boot/<your-bootloader>"
                    - Recommended Bootloader directories
                        + grub: /boot/grub
                - partition_Table: Specify the storage device/disk's partition table
                    + Type: String
                    + Default: msdos
                    - Accepted Values
                        + msdos : aka MBR (Master Boot Record); Used by BIOS Legacy Motherboard Bootloader Firmware
                        + gpt : aka GUID partition Table; Used by modern (U)EFI Motherboard Bootloader Firmware
                - bootloader_optional_Params : Specify the optional parameters you wish to pass into your bootloader's installation command; Leave empty to pass nothing
                    + Type: String
                    + Default: ""
                - bootloader_target_Architecture : Specify your bootloader's target platform/architecture to install for
                    + Type: String
                    + Default: "i386-pc"
                    - Supported/Tested Values
                        + i386-pc : Generic x86-64 CPU architectures
            - Return
                - result : A Dictionary (key-value) mapping containing the standard output (stdout), standard error (stderr), the return status code (resultcode) and the command string (command-string)
                    + Type: Dictionary
                    - Key-Value Mappings
                        - stdout : The Standard Output stream from the command execution
                            + Type: String
                        - stderr :  The Standard Error stream from the command excution
                            + Type: String
                        - returncode : Result/Return Status Code from the command execution
                            + Type: Integer
                            - Values
                                + 0 = Success
                                + > 0 = Failed
                        - command-string : The command string formed from the chroot command list
                            + Type: String

        - `.generate_bootloader_Configs(disk_Label, dir_Mount, bootloader, bootloader_directory, partition_Table, bootloader_optional_Params, bootloader_target_Architecture)`: Generate bootloader's configuration files in the chroot root filesystem
            - Parameter Signature/Header
                - disk_Label : Specify the target disk/device label containing the target root filesystem chroot environment you wish to generate the bootloader's configuration files into
                    + Type: String
                    - Disk Label Formats
                        - sata : For SATA/AHCI devices
                            + Format: /dev/sdX
                        - nvme : For NVME devices
                            + Format: /dev/nvme[device-number]
                        - loop : For Loopback devices
                            + Format: /dev/loop[device-number]
                - dir_Mount : Specify the root/base filesystem mount path/directory containing the chroot environment
                    + Type: String
                    + Default: "/mnt"
                - bootloader: Specify the target bootloader to install to your chroot environment
                    + Type: String
                    + Default: "grub"
                    - Accepted Values
                        + grub : GRUB2
                - bootloader_directory : Specify the boot directory containing your bootloader configuration files
                    + Type: String
                    + Default: "/boot/grub"
                    - Notes
                        + Certain bootloaders (i.e. Grub) have different boot directories based on partition table (i.e. MBR/GPT); 
                    + Value Format String: "/boot/<your-bootloader>"
                    - Recommended Bootloader directories
                        + grub: /boot/grub
                - partition_Table: Specify the storage device/disk's partition table
                    + Type: String
                    + Default: "msdos"
                    - Accepted Values
                        + msdos : aka MBR (Master Boot Record); Used by BIOS Legacy Motherboard Bootloader Firmware
                        + gpt : aka GUID partition Table; Used by modern (U)EFI Motherboard Bootloader Firmware
                - bootloader_optional_Params : Specify the optional parameters you wish to pass into your bootloader's installation command; Leave empty to pass nothing
                    + Type: String
                    + Default: ""
                - bootloader_target_Architecture : Specify your bootloader's target platform/architecture to install for
                    + Type: String
                    + Default: "i386-pc"
                    - Supported/Tested Values
                        + i386-pc : Generic x86-64 CPU architectures
            - Return
                - result : A Dictionary (key-value) mapping containing the standard output (stdout), standard error (stderr), the return status code (resultcode) and the command string (command-string)
                    + Type: Dictionary
                    - Key-Value Mappings
                        - stdout : The Standard Output stream from the command execution
                            + Type: String
                        - stderr :  The Standard Error stream from the command excution
                            + Type: String
                        - returncode : Result/Return Status Code from the command execution
                            + Type: Integer
                            - Values
                                + 0 = Success
                                + > 0 = Failed
                        - command-string : The command string formed from the chroot command list
                            + Type: String

        - `.bootloader_Management(disk_Label, dir_Mount, bootloader, bootloader_directory, partition_Table, bootloader_optional_Params, bootloader_target_Architecture)`: Consolidation function
            - Parameter Signature/Header
                - disk_Label : Specify the target disk/device label containing the target root filesystem chroot environment you wish to generate the bootloader's configuration files into
                    + Type: String
                    - Disk Label Formats
                        - sata : For SATA/AHCI devices
                            + Format: /dev/sdX
                        - nvme : For NVME devices
                            + Format: /dev/nvme[device-number]
                        - loop : For Loopback devices
                            + Format: /dev/loop[device-number]
                - dir_Mount : Specify the root/base filesystem mount path/directory containing the chroot environment
                    + Type: String
                    + Default: "/mnt"
                - bootloader: Specify the target bootloader to install to your chroot environment
                    + Type: String
                    + Default: "grub"
                    - Accepted Values
                        + grub : GRUB2
                - bootloader_directory : Specify the boot directory containing your bootloader configuration files
                    + Type: String
                    + Default: "/boot/grub"
                    - Notes
                        + Certain bootloaders (i.e. Grub) have different boot directories based on partition table (i.e. MBR/GPT); 
                    + Value Format String: "/boot/<your-bootloader>"
                    - Recommended Bootloader directories
                        + grub: /boot/grub
                - partition_Table: Specify the storage device/disk's partition table
                    + Type: String
                    + Default: "msdos"
                    - Accepted Values
                        + msdos : aka MBR (Master Boot Record); Used by BIOS Legacy Motherboard Bootloader Firmware
                        + gpt : aka GUID partition Table; Used by modern (U)EFI Motherboard Bootloader Firmware
                - bootloader_optional_Params : Specify the optional parameters you wish to pass into your bootloader's installation command; Leave empty to pass nothing
                    + Type: String
                    + Default: ""
                - bootloader_target_Architecture : Specify your bootloader's target platform/architecture to install for
                    + Type: String
                    + Default: "i386-pc"
                    - Supported/Tested Values
                        + i386-pc : Generic x86-64 CPU architectures
            - Operational flow
                1. Install the bootloader packages in the chroot root filesystem
                2. Prepare the bootloader dependencies in the chroot root filesystem
                3. Install the bootloader to the target disk/device's partition table
                4. Generate the bootloader configuration files in the chroot root filesystem
            - Return
                - combined_res : A list of all the results from all the bootloader-related commands
                    + Type: List
                    - Elements
                        + [0] : res from install_bootloader_Packages()
                        + [1] : res from prepare_Bootloader()
                        + [2] : res from install_Bootloader()
                        + [3] : res from generate_bootloader_Configs()

        - `.archive_command_Str(cmd_str, dir_Mount="/mnt")`: Output command string into a file for archiving
            - Parameter Signature/Header
                - cmd_str : Specify the string of commands to output to the chroot mount directory
                    + Type: String
                - dir_Mount : Specify the root/base filesystem mount path/directory containing the chroot environment
                    + Type: String
                    + Default: "/mnt"
            - Return
                + Type: Void

        - `.arch_chroot_Exec()` : Installation Stage 8 - Execute commands using arch-chroot due to limitations with shellscripting
            - Operational flow
                1. Retrieve all required key-value mappings from the imported configuration settings
                2. Synchronize Hard Clock in chroot root filesystem
                3. Enable locale/region in chroot root filesystem
                4. Append Network Host File (/etc/hosts) in chroot root filesystem
                5. Format initial ramdisk in chroot root filesystem
                6. Set root password to chroot root filesystem
                7. Install bootloader in chroot root filesystem
                8. Archive the command strings into a file
            - Return
                + Type: Void

        - `.installer()`: Main base installation installer function
            - Operational flow
                1. Verify that network exists and works
                2. Obtain the motherboard firmware (boot mode)
                3. Update the system clock
                4. Format/Partition the disks
                5. Mount the disks
                6. Bootstrap install the essential packages into the mount point (root/base filesystem)
                7. Generate the filesystems table file in the root filesystem
                8. Chroot and execute the commands in `.arch_chroot_Exec()` in the chroot root filesystem
            - Return
                + Type: Void

- pydistinstall.app.distributions.archlinux.mechanism.PostInstallation
    - General
        + `.init_Config()`: Initialize defaults from configuration file if base installation is not used

    - Callback/Event Utility functions
        - `.update_setup(setup)`: Update the setup variables according to that of the target platform's installer mechanism class
            - Parameter Signature/Header
                - setup : Store the caller's initialized setup class object
                    + Type: pydistinstall.setup.Setup()
            - Return
                + Type: Void

        - `.print_configurations()`: Print the currently stored configuration settings to standard output
            - Return
                + Type: Void

        - `.postinstall_todo()`: Prints out to standard output a list of tasks todo after base installation (Unused)
            - Return
                + Type: Void

        - `.postinstall_sanitize()`: Post-Installation Sanitization and cleanup the user accounts from any unnecessary files, as well as to save the commands
            - Return
                + Type: Void

    - User Management
        - `.get_users_Home(user_name)`: Get the home directory of a user
            - Parameter Signature/Header
                - user_name : The name of the target user
                    + Type: String
            - Return
                - home_dir : Return the home directory mapped to the user

        - `.check_user_Exists(user_name)`: Check if user exists
            - Parameter Signature/Header
                - user_name : Specify the target user to check if exists
                    + Type: String
            - Return 
                - exist_Token : Return a token indicating if the user exists (True = Exists, False = Does not exists)
                    + Type: Boolean

        - `.useradd_get_default_Params()`: Get default parameters for 'useradd'
            - Return
                - user_params : A dictionary (key-value) mapping of the default user parameters used by 'useradd'
                    + Type: Dictionary
                    - Key-Value Mappings
                        + GROUP : Obtain the groups
                        + HOME  : Obtain the home directory
                        + INACTIVE : Inactivity rule
                        + EXPIRE : User expiry period
                        + SHELL  : User's default shell
                        + SKEL   : User's skeleton directory
                        + CREATE_MAIL_SPOOL : Mail spool

    - Post-Installation Stages
        - `.enable_sudo(dir_Mount="/mnt")`: Enabling sudo in /etc/sudoers via command line
            - Parameter Signature/Header
                - dir_Mount : Specify the root/base filesystem mount path/directory containing the chroot environment
                    + Type: String
                    + Default: "/mnt"
            - Return
                - return_val : List containing the list [stdout, stderr, resultcode] for each command output
                    + Type: List of Lists
                    - Elements
                        - [0] [stdout, stderr, resultcode]
                            + Type: List
                            - Sub-elements
                                - [0] stdout : The Standard Output Stream returned from the command
                                    + Type: String
                                - [1] stderr : The Standard Errr Stream returned from the command
                                    + Type: String
                                - [2] ret_Code : The return code/result status from the execution of the command (0 = Success, > 0 = Failed)
                                    + Type: Integer

        - `.postinstallation()`: Main Post-Installation Recommendations and TODOs command execution
            - Operational Flow
                1. Obtain the root partition mount point
                2. Enable sudo in the chroot root filesystem
                3. Create users specified in the configuration file in the chroot root filesystem
                4. Write command string to external script for usage
            - Return
                + Type: Void

    - Main Post-Installer
        - `.postinstaller()`: Start the post-installer in its entirety
            - Return
                + Type: Void

- pydistinstall.lib.cli.CLIParser
    - `.get_cli_arguments()` : Iterates and processes through all the elements in the argument list and stores them according to the user's application requirements, then stores the final configurations back into the `self.configurations` class variable
        - Return
            + Type: Void/None
    - `.get_cli_subarguments(argv, pos)` : Iterates through the provided list and search for the element found in the index 'pos+1', and return the objects `position, next_element`
        - Parameter Signature/Header
            - argv : Specify the list, in which you wish to obtain the element found in the 'position+1'th index of the list
                + Type: List
            - pos : Specify the position you wish to search where the result is the element found in the 'position+1'th index of the list
                + Type: Integer
        - Return
            + Type: Tuple
            - Values
                - pos : Return the position index 'pos+1'
                    + Type: Integer
                - next_element : Return the element found in the 'pos+1'th index position
                    + Type: String
    - `.process_cli_arguments()` : Process the main configurations dictionary and split into optional and positional arguments
        - Return
            + Type: List
            - Values
                - optionals :  Dictionary containing all optional CLI arguments and its mappings
                    + Type: Dictionary
                - positionals : List containing all the positional arguments (arranged according to the position) specified by the user
                    + Type: List
    - `.start()` : Start the CLI argument parsing process. This will 1. get the CLI arguments list, process them and return into the `self.optionals` and `self.positionals` arguments
        - Return
            + Type: Void/None

- pydistinstall.lib.config_handler.YAMLConfig
    - `.open_file()`  : Open the specified file (`self.file_name`) using the specified mode (`self.mode`) and return/store the file IO object in `self.file`
        - Return
            + Type: Void/None
    - `.close_file()` : Close the currently-opened file (`self.file`) after usage and set unset the file object
        - Return
            + Type: Void/None
    - `.write_config(data)` : Dump and write the specified dictionary object to YAML configuration file
        - Parameter Signature/Header
            - data : Specify the dictionary object you wish to dump and write into the YAML configuration file
                + Type: Dictionary
    - `.read_config()` : Load and read YAML configuration file contents to dictionary
        - Return
            - yaml_contents: The imported YAML configuration file dictionary object
                + Type: Dictionary
    - `.parse_yaml_str_to_dict(yaml_str)` : Parse YAML strings and convert into dictionary object
        - Parameter Signature/Header
            - yaml_str : Specify the YAML string you wish to import and return as dictionary object
                + Type: Dictionary
        - Return
            - yaml_contents: The imported YAML configuration file dictionary object
                + Type: Dictionary

- pydistinstall.lib.device_management
    - `.format_partition_str(disk_Label, partition_Number=0, storage_Controller="sata")`: Prepare and Format Partition according to the Storage Controller
        - Parameter Signature/Header
            - disk_Label : Specify the target disk/device label you wish to format/manage
                + Type: String
                - Disk Label Formats
                    - sata : For SATA/AHCI devices
                        + Format: /dev/sdX
                    - nvme : For NVME devices
                        + Format: /dev/nvme[device-number]np[partition-number]
                    - loop : For Loopback devices
                        + Format: /dev/loop[device-number]p[partition-number]
            - partition_Number : Specify the disk/device's target partition number
                + Type: Integer
                + Default: 0
            - storage_Controller
                + Type: String
                + Default: sata
                + Value: "sata|nvme|loop"
                - Storage Controller Types
                    + sata : For SATA/AHCI devices
                    + nvme : For NVME devices
                    + loop : For Loopback devices
        - Return
            - target_partition_Label : Return the full partition label path as formatted according to the specifications provided
                + Type: String

    - `.get_block_Information(disk_Label)`: Obtain block information regarding the disk using 'blkid' and return the information formatted as a dictionary
        - Parameter Signature/Header
            - disk_Label : Your target disk label; i.e. SATA|AHCI = /dev/sdX, NVME = /dev/nvme[disk-number], Loopback = /dev/loop[disk-number]
                + Type: String
                - Disk storage controller formats
                    - sata : For SATA/AHCI devices
                        + Format: /dev/sdX
                    - nvme : For NVME devices
                        + Format: /dev/nvme[device-number]
                    - loop : For Loopback devices
                        + Format: /dev/loop[device-number]
        - Return
            - block_Information : Contains a dictionary containing various block information key-value mappings
                + Type: Dictionary
                - Key-Value Mappings
                    - disk_Label : This 'disk_Label' refers to the disk label specified in the parameter; Contains a list of properties/information returned from 'blkid' relating to that disk label
                        + type: Dictionary
                        + Mapped Values : List of information/attributes relating to the disk/device block

    - `.design_filesystems_Table(disk_Label, dir_Mount, disk_block_Information, partition_Scheme, mount_Points)` : Design Filesystem Table (fstab) and return the fstab contents
        - Parameter Signature/Header
            - disk_Label : The target disk/device path; i.e. SATA|AHCI = /dev/sdX, nvme = /dev/nvmeX, loop = /dev/loopX
                + Type: String
            - dir_Mount : The root mount directory
                + Type: String
            - disk_block_Information : Dictionary (key-value) mapping) of the disk label information
                + Type: Dictionary
                - Structure:
                    ```python
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
                    ```
            - partition_Scheme : Dictionary containing the mappings of the partition number to the partition information
                + Type: Dictionary
            - mount_Points : Dictionary containing the partition names mapped to the mount points
                + Type: Dictionary

        - Return
            - fstab_Contents : List containing the filesystems table (fstab) contents
                + Type: List

- pydistinstall.lib.format.Text
    - `.END(msg="Pause")` : Print out a pause/end message
        - Parameter Signature/Header
            - msg : Specify the message you wish to print
                + Type: String
                + Default: Pause

    - `.processing(msg="Processing...", format="", delimiter="- ")` : Format a processing/loading message
        - Parameter Signature/Header
            - msg : Specify the message you wish to print
                + Type: String
                + Default: Processing...
            - format: Specify the format of the string you want to print
                + Type: String
                + Default: ""
            - delimiter: Specify the separator/delimiter you wish to use to identify that this line is a processing/loading message
                + Type: String
                + Default: "- "
        - Return
            - fmt_str : The formatted string
                + Type: String

- pydistinstall.lib.process
    - Process/Subprocess object functions
        - `.subprocess_Open(cmd_str, **opts)` : Open a subprocess pipe and return it
            - Parameter Signature/Header
                - cmd_str : The command string to execute
                    + Type: String
                - opts : All Key=Value parameters you wish to parse into Popen
                    + Type: kwargs (Keyword Arguments) aka Dictionary
            - Return
                - proc : The opened subprocess process pipe
                    + Type: subprocess.Popen
    - Process/Subprocess Execution functions
        - `.subprocess_Realtime(cmd_str, **opts)` : Open a subprocess and read the stdout line by line in real time
            - Parameter Signature/Header
                - cmd_str : The command string to execute
                    + Type: String

                - opts : All Key=Value parameters you wish to parse into Popen
                    + Type: kwargs (Keyword Arguments) aka Dictionary
            - Return
                + Type: Tuple
                - Values
                    1. stdout : The Standard Output Stream returned from the command
                        + Type: String
                    2. stderr : The Standard Errr Stream returned from the command
                        + Type: String
                    3. ret_Code : The return code/result status from the execution of the command (0 = Success, > 0 = Failed)
                        + Type: Integer
        - `.subprocess_Line(cmd_str, **opts)` : Open a subprocess and read the stdout line by line
            - Parameter Signature/Header
                - cmd_str : The command string to execute
                    Type: String
                - opts : All Key=Value parameters you wish to parse into Popen
                    Type: kwargs (Keyword Arguments) aka Dictionary
            - Return
                + Type: Tuple
                - Values
                    1. stdout : The Standard Output Stream returned from the command
                        + Type: String
                    2. stderr : The Standard Errr Stream returned from the command
                        + Type: String
                    3. ret_Code : The return code/result status from the execution of the command (0 = Success, > 0 = Failed)
                        + Type: Integer
        - `.subprocess_Sync(cmd_str, **opts)` : Open a subprocess and execute in sync (Check if the previous command is completed before proceeding)
            - Parameter Signature/Header
                - cmd_str : The command string to execute
                    Type: String
                - opts : All Key=Value parameters you wish to parse into Popen
                    Type: kwargs (Keyword Arguments) aka Dictionary
            - Return
                + Type: Tuple
                - Values
                    1. stdout : The Standard Output Stream returned from the command
                        + Type: String
                    2. stderr : The Standard Errr Stream returned from the command
                        + Type: String
                    3. ret_Code : The return code/result status from the execution of the command (0 = Success, > 0 = Failed)
                        + Type: Integer
        - `.chroot_exec(cmd_str, chroot_exec="arch-chroot", dir_Mount="/mnt", shell="/bin/bash", communicate_opts=None, **opts)` : Open Subprocess and execute commands in chroot
            - Parameter Signature/Header
                - cmd_str : The command string to execute
                    + Type: String
                - chroot_exec : The binary to chroot with
                    + Type: String
                    + Default Value: arch-chroot
                - dir_Mount : The mount point
                    + Type: String
                    + Default Value: /mnt
                - shell : The target shell to work with
                    + Type: String
                    + Default Value: /bin/bash
                - communicate_opts : Options to parse into the .communicate() command
                    + Type: Dictionary
                    + Default Value: None
                - opts : All Key=Value parameters you wish to parse into Popen
                    + Type: kwargs (Keyword Arguments) aka Dictionary
            - Return
                + Type: Tuple
                - Values
                    1. stdout : The Standard Output Stream returned from the command
                        + Type: String
                    2. stderr : The Standard Errr Stream returned from the command
                        + Type: String
                    3. ret_Code : The return code/result status from the execution of the command (0 = Success, > 0 = Failed)
                        + Type: Integer
    - Subprocess stdin (Standard Input) handlers
        - `.subprocess_Input(proc, texts=None)` : Enter multiple input buffer strings into stdin buffer reader
            - Parameter Signature/Header
                - proc : The target subprocess object (Popen)
                    + Type: subprocess.Popen()

                - texts : List of all texts you wish to input into the stdin for that process instance; Please append all the texts in linear sequential order
                    - Explanation
                        - For example
                            - If you wish to enter a password for 'passwd' or something: ['your-password', 'your-password']
                    + Type: List
        - `.subprocess_stdin_Clear(proc)` : Wrapper function to flush and clear the subprocess stdin buffer stream using 'proc.stdin.flush'
            - Parameter Signature/Header
                - proc : The target subprocess object (Popen)
                    + Type: subprocess.Popen()

- pydistinstall.lib.user_management
    - `.get_all_users()` : Check if the user exists
        - Return
            - all_Users : List of all users in the system
                + Type: List
    - `.get_user_primary_group(user_Name)` : Retrieve the specified user's primary group
        - Parameter Signature/Header
            - user_Name : Specify the target user's username
                + Type: String
        - Return
            - primary_group : The primary group mapped to the user
                + Type: String
    - `.create_user(u_Name, u_primary_Group, u_secondary_Groups, u_home_Dir, u_other_Params)` : Function to format a command string used to create a user in the chroot filesystem
        - Parameter Signature/Header
            - u_Name             : Specify the target User Name
                + Type: String
            - u_primary_Group    : Primary Group
                + Type: String
            - u_secondary_Groups : Secondary Groups
                + Type: String
            - u_home_Dir         : Home Directory
                + Type: String
            - u_other_Params     : Any other parameters after the first 3
                + Type: String
        - Return
            - u_create_Command : The formatted command string to execute to create a user in the chroot root filesystem
                + Type: String

- pydistinstall.lib.utils
    - `.seperate_by_Delim(msg, delim=";")` : Seperate a string into an array by the delimiter
        - Parameter Signature/Header
            - msg : Specify the message to be separated by its delimiter/separator into a list
                + Type: String
            - delim : Specify the delimiter/separator to separate the message with
                + Type: String
                + Default: ";"
        - Return
            - output : List of all elements after separating by the specified delimiter
                + Type: List

### Attributes/Variables
- pydistinstall.setup.Setup()
    - `.yaml` : Contains the ruamel.yaml.YAML() class object
        + Type: ruamel.yaml.YAML()
    - `.cliparser` : Contains the CLIParser() class object
        + Type: pydistinstall.lib.cli.CLIParser()
    - `.fmt_Text` : Contains the Text() class object
        + Type:  pydistinstall.lib.format.Text()
    - `.env` : Contains the Environment() class object
        + Type:  pydistinstall.lib.env.Environment()
    - `.cfg` : Dictionary (Key-Value) container containing the installation configuration settings starting from boot-time
        + Type: Dictionary
        + Default Value:
            ```python
            {
                "distribution-name" : "[arch]",
                "device_Type" : "<hdd|ssd|flashdrive|microSD>", # Your disk/device/file type; i.e. VHD|HDD|SSD|Flashdrive|Microsd etc
                "storage-controller": "[your-storage-controller (ahci|nvme|loop)]",
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
            ```
        - Keys
            - distribution-name : Contains the target distribution you (the user) wants to install the base/root filesystem of
                + Type: String
                + Value Format: "[arch]"
                - Supported Values
                    + arch : ArchLinux
            - device_Type : Your disk/device/file type; i.e. VHD|HDD|SSD|Flashdrive|Microsd etc
                + Type: String
                + Value format: "<vhd|hdd|ssd|flashdrive|microSD>"
            - storage-controller : Your disk/device's storage controller
                + Type: String
                + Value Format: "[your-storage-controller (sata|nvme|loop)]",
                - Accepted Values
                    + sata : For SATA/AHCI storage controller devices
                    + nvme : For NVME storage controller devices
                    + loop : For Loopback devices
            - device_Size : The total disk size
                + Type: String
                + Value Format: "<x {GB | GiB | MB | MiB}>"
            - disk_Label : The disk's name/label (i.e. /dev/sdX for SATA, /dev/nvme0np1 for NVME); Default: uses the environment variable '$TARGET_DISK_NAME'
                + Type: String
                - Disk Label Formats
                    - sata : For SATA/AHCI devices
                        + Format: /dev/sdX
                    - nvme : For NVME devices
                        + Format: /dev/nvme[device-number]np[partition-number]
                    - loop : For Loopback devices
                        + Format: /dev/loop[device-number]p[partition-number]
                + Default Value: The Environment Variable "TARGET_DISK_NAME"
            - disk_partition_Table : Specify the partition table of the target storage disk/device (i.e. msdos for MBR/BIOS/Legacy, gpt for (U)EFI Modern motherboard bios)
                + Type: String
                - Accepted Values
                    + msdos : For mbr/msdos (BIOS), Legacy bootloader firmware; Supports drives up to 2TB maximum storage
                    + gpt : For (UEFI) Modern bootloader firmware; Required for all drives > 2TB storage
            - bootloader_firmware : Specify the motherboard bootloader ('BIOS') firmware
                + Type: String
                - Accepted Values
                    + BIOS : The BIOS Legacy motherboard BIOS firmware
                    + UEFI : The (U)EFI modern motherboard BIOS firmware
            - bootloader : Specify the target bootloader you want to install to the filesystem
                + Type: String
                - Accepted Values
                    + grub : The GRUB(2) Bootloader
            - partition_Scheme : This contains your partition scheme, a dictionary (key-value) mapping of the partition number and that partition's specifications and design (i.e. partition label (for GPT/UEFI), partition type (primary, extended, logical for MBR/MSDOS/BIOS) etc etc)
                + Type: Dictionary
                - Information
                    - Configuration Synopsis/Syntax
                        - MBR Partition Table/MSDOS Bootloader Firmware
                            ```
                            <partition_Number> : [<partition_Name>, <partition_Type>, <partition_filesystem_Type>, <partition_start_Size>, <partition_end_Size>, <partition_Bootable>, <partition_Others>]
                            ```
                        - GPT Partition Table/UEFI Bootloader Firmware
                            ```
                            <partition_Number> : [<partition_Label>, <partition_Type>, <partition_filesystem_Type>, <partition_start_Size>, <partition_end_Size>, <partition_Bootable>, <partition_Others>]
                            ```
                    - Notes
                        + The Boot partition for a GPT partition layout/configuration needs to be an EFI System Partition type
                        - Some Manadatory partition names:
                            + For Boot Partition : 'Boot'
                            + For Root Partition : 'Root'
                - Key-Value Mappings
                    - partition_Number : Map this partition number (key) to the partition specifications, definitions and other optional configurations
                        + Type: Integer
                        - Value Mappings
                            + Type: List
                            - Entries
                                - [0] = Partition Label/Alias/Name for identification purposes
                                    + Type: String
                                    - Notes
                                        + Unlike index [1], this is just for documentation and description of the partition in the partition scheme
                                - [1] = Partition Type (For MSDOS/MBR/BIOS), Partition Label (For GPT/(U)EFI)
                                    - Partition Type: For MSDOS/MBR disk filesystem labels
                                        + Type: String
                                        - Accepted Values
                                            + primary
                                            + logical
                                            + extended
                                    - Partition Label: For GPT disk filesystem labels; This is effectively a 'name' (aka Label) you can assign to the partition as GPT doesnt use primary, extended, nor logical for separation
                                        + Type: String
                                - [2] = Partition Filesystem; This is the filesystem of the partition
                                    - Filesystem Types
                                        + ext4 : Used if booting with BIOS legacy motherboard firmware
                                        + fat32 : Required to be used for the boot partition when booting with UEFI
                                - [3] = Partition Starting Size; Specify the starting position of the partition to write from. 
                                    + Type: String
                                    + Value Format: <xMB|MiB|GB|GiB>
                                    - Special Values/Syntx
                                        + 0% : Start from the beginning of the storage device
                                        + 25% : Start from 1/4 of the storage device
                                        + 50% : Start from half of the storage device
                                        + 75% : Start from 3/4 of the storage device
                                    - Notes
                                        - If the partition is after a previous partition, 
                                            + the partition start size is the end size of the previous partition (side by side)
                                - [4] = Partition Ending Size; Specify the ending position of the partition to write to.
                                    + Type: String
                                    + Value Format: <xMB|MiB|GB|GiB>
                                    - Special Values/Syntx
                                        + 25% : Write 1/4 of the storage device
                                        + 50% : Write half of the storage device
                                        + 75% : Write 3/4 of the storage device
                                        + 100% : Fill up the entire/remaining storage device space
                                    - Notes
                                        - If the partition's start size is 0% and the partition's end size is 100%
                                            + This will fill up the entire storage
                                        - If the partition is after a previous partition, 
                                            + the partition end size is the start size of the next partition (side by side)
                                        - If the partition is after a previous partition, and the partition's start size is 50% and the partition's end size is 100%
                                            + This will fill up the remaining 50% storage
                                - [5] = Enable/Disable 'Bootable' flag in this partition; Set 'True' to Enable and 'False' to Disable
                                    + Type: Boolean
                                    - Recommended
                                        + Set 'True' only to your Boot partition
                                - [6] = Set/Specify other options to pass to parted; Set 'NIL' to ignore this element. Currently unused
                                    + Type: String
                                    + Default Value: NIL
                - Default Value
                    ```python
                    {
                        1 : ["Boot", "primary", "ext4", "0%", "1024MiB", True, "NIL"],
                        2 : ["Root", "primary", "ext4", "1024MiB", "<x1MiB>", False, "NIL"],
                        3 : ["Home", "primary", "ext4", "<x1MiB>", "100%", False, "NIL"],
                    }
                    ```
            - mount_Paths : This contains the mount paths mapped to the partition name
                + Type: Dictionary
                - Information
                    - Notes
                        + Please seperate all parameters with delimiter ','
                        + Please seperate all subvalues with delimiter ';'
                        - Some Manadatory partition names:
                            + For Boot Partition : 'Boot'
                            + For Root Partition : 'Root'
                - Synopsis/Syntax: 
                    ```python
                    {
                        "[Partition Name]" : "[mount path]", # Your Partition
                    }
                    ```
                - Default Value:
                    ```python
                    {
                        "Boot" : "/mnt/boot",	# Boot
                        "Root" : "/mnt",		# Root
                        "Home" : "/mnt/home",	# Home
                    }
                    ```
            - base_pkgs : Specify all the packages you want to include into the bootstrap installation process
                + Type: List
                - Default Values
                    ```python
                    [
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
                    ]
                    ```
            - location : This contains a dictionary (key-value) mapping of Timezone, Region and Locale information of the system
                + Type: Dictionary
                - Key-Value Mappings
                    - Region : Specify your locale's region (i.e. Region); Refer to /usr/share/zoneinfo for your region
                        + Type: String
                        + Value Format: `"<your-region (Asia|US etc)>"`
                    - City : Specify your locale's city (i.e. Country); Refer to /usr/share/zoneinfo/<your-region> for your City
                        + Type: String
                        + Value Format: `"<your-city (Singapore|US etc)>"`
                    - Language : Specify your Language code - refer to /etc/locale.gen for a list of all language codes
                        + Type: String
                        + Value Format: `"<language-code (en_US.UTF-8|en_SG.TF-8 etc)>"`
                    - KeyboardMapping : Specify your Keyboard Mapping (TODO: 2022-06-17 2314H : At the moment this is not used)
                        + Type: String
                        + Value Format: `"en_UTF-8"`
                - Default Values
                    ```python
                    {
                        "Region" : "<your-region (Asia|US etc)>", # Refer to /usr/share/zoneinfo for your region
                        "City" : "<your-city (Singapore etc)>", # Refer to /usr/share/zoneinfo/<your-region> for your City
                        "Language" : "<language-code (en_US.UTF-8|en_SG.TF-8 etc)>", # Your Language code - refer to /etc/locale.gen for a list of all language codes
                        "KeyboardMapping" : "en_UTF-8", # Your Keyboard Mapping - change this if you use this (TODO: 2022-06-17 2314H : At the moment this is not used)
                    }
                    ```
            - user_ProfileInfo"  : This contains a dictionary (key-value) mapping of the Users and its mapped Profile Informations
                + Type: Dictionary
                - Synopsis/Syntax
                    ```python
                    {
                        <username> : [
                           <primary_group>,
                           <secondary_group (put NIL if none),
                           <custom_directory_path (put NIL if none)>,
                           <any_other_Parameters>
                       ]
                    }
                    ```
                - Key-Value Mappings
                    - username : 
                        + Type: List
                        - Elements
                            - [0] : Set the user's primary group (only 1)
                                + Type: String
                            - [1] : Set the user's secondary group(s); Put NIL if none
                                + Type: String
                                - Format
                                    ```python
                                    "grp1;grp2;grp3;...;grpN"
                                    ```
                                - Notes
                                    + Please seperate all parameters with delimiter ','
                                    + Please seperate all subvalues with delimiter ';'
                            - [2] : Set the user's custom home directory path; Put NIL if none
                                + Type: String
                            - [3] : Set any other parameters you want to pass into 'useradd'; Put NIL if none
                                + Type: String
                        - Format
                            ```python
                            [
                                <primary_group>,
                                <secondary_group (put NIL if none),
                                <custom_directory_path (put NIL if none)>,
                                <any_other_Parameters>
                            ]
                            ```
                - Default Values
                    ```python
                    {
                        "username" : ["wheel", "NIL", "/home/profiles/username", "NIL"]
                    }
                    ```
            - networkConfig_hostname : Specify the hostname for the system to be used as an identifier in the network (used in /etc/hostname); Similar to workspace group name
                + Type: String
                + Value Format: "<your-network-hostname>"
            - bootloader : Specify the bootloader you want to use and install in your filesystem
                + Type: String
                + Value Format: "<your-bootloader>"
                - Tested and working bootloader
                    + grub: GRUB(2) bootloader
                - Implemented and testing
                    + syslinux
            - bootloader_directory : Specify your Bootloader's boot mount point (i.e /boot/grub)
                + Type: String
                - Notes
                    + Certain bootloaders (i.e. Grub) have different boot directories based on partition table (i.e. MBR/GPT); 
                + Value Format String: "/boot/<your-bootloader>"
                - Recommended Bootloader directories
                    + grub: /boot/grub
            - bootloader_Params : Specify additional parameters to parse into your Bootloader options/parameters; Type "" if none/NIL.
                + Type: String
                - Notes
                    - If you are installing on a GPT/UEFI motherboard bootloader firmware
                        + --efi-directory=/boot
            - default_kernel : Set your Default Linux Kernel
                + Type: String
                + Value Format String: "<linux-kernel>"
                - Supported Kernels and value
                    + linux : The default linux kernel
            - platform_Arch : Specify your Platform Architecture
                + Type: String
                + Value Format String: "<platform-architecture>", # 
                - System Architectures
                    + i386-pc : For Generic x86-64 CPU platform/systems
                    + x86_64-efi : For UEFI|GPT x86-64 platform/systems
    - `.PROGRAM_SCRIPTNAME` : Store the program's executable file name here
        + Type: String
    - `.PROGRAM_NAME` : Store the application's title/name here
        + Type: String
    - `.PROGRAM_TYPE` : Store the type of the program here
        + Type: String
    - `.PROGRAM_VERSION` : Store the current version of the program here
        + Type: String
    - `.MODE` : Store the boot-time program mode here (DEBUG|RELEASE)
        + Type: String
    - `.DISTRO` : Store the target base distribution to install here
        + Type: String
    - `.cfg_name` : Store the imported configuration file here
        + Type: String

- pydistinstall.app.runner.App
    - `.dist` : Store the passed target distribution here
        + Type: String
        - Supported Keywords
            + arch : ArchLinux
    - `.supported_distributions` : Contains a dictionary (Key-value) mapping of a distribution and its 'accepted equivalent/similar keywords'
        + Type: Dictionary
        - Example Format
            ```python
            {
                "distribution-name" : ["alternative", "method", "of", "writing"],
            }
            ```
        - Default
            ```python
            {
                "arch" : ["arch", "ArchLinux"],
            }
            ```
    - `.setup` : Store the caller's initialized setup class object
        + Type: pydistinstall.setup.Setup()
    - `.env` : Store the caller's initialized environment variables class object
        + Type: pydistinstall.lib.env.Environment()
    - `.installer` : Variable to be substituted as the main installer mechanism depending on the distribution specified
        + Type: function<pydistinstall.app.disributions.[distribution-name].mechanism.BaseInstallation()>
        + Default Value: None
    - `.postinstaller` : Variable to be substituted as the post installation mechanism depending on the distribution specified
        + Type: function<pydistinstall.app.disributions.[distribution-name].mechanism.PostInstallation()>
        + Default Value: None
    - `.installation_stages` : Dictionary (Key-value) mapping of installation stage numbers to their stage installation description/title
        + Type: Dictionary
        - Format
            ```python
            {
                # stage-number : "description/title",
            }
            ```
        - Default Value
            ```python
            {
                1 : "Verify Network",
                2 : "Verify Boot Mode",
                3 : "Update System Clock",
                4 : "Disk Partition Management",
                5 : "Disk Mounting",
                6 : "Root filesystem Bootstrap Packaging",
                7 : "Filesystems Table (/etc/fstab) generating",
                8 : "System chroot execution",
                9 : "Post-Installation",
                10 : "Post-Installation Cleanup and Sanitization",
            }
            ```

- pydistinstall.app.distributions.archlinux.mechanism.BaseInstallation
    - `.setup` : Store the caller's initialized setup class object
        + Type: pydistinstall.setup.Setup()
    - `.env` : Store the Environment Variables found in the caller's initialized setp class object
        + Type: pydistinstall.setup.Setup().env
    - `.cfg` : Store a memory copy of the caller's configurations stored in the setup class object
        + Type: pydistinstall.setup.Setup().cfg
    - `.default_Var` : Store a memory copy of the caller's default variables dictionary stored in the setup class object
        + Type: pydistinstall.setup.Setup().default_Var
    - `.package_manager_config_Path` : Explicitly specify the package manager custom configuration path
        + Type: String
        + Default: "/etc/pacman.d"
    - `.mirrorlist_file_Name` : Specify the target mirrorlist file directory
        + Type: String
        + Default: "{}/mirrorlist".format(self.package_manager_config_Path)
    - `.package_manager_Configurations` : Specify the contents of the package manager's configuration file
        + Type: String
        - Default:
```
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
```

- pydistinstall.app.distributions.archlinux.mechanism.PostInstallation
    - `.setup` : Store the caller's initialized setup class object
        + Type: pydistinstall.setup.Setup()
    - `.base_mechanism_Obj` : Store the caller's initialized BaseInstallation() class object
        + Type: pydistinstall.app.distributions.archlinux.mechanism.BaseInstallation(setup)
        + Default Value: None

- pydistinstall.lib.cli.CLIParser
    - `.configurations = { "optionals" : {}, "positionals" : [] }` : Dictionary (Key-Value) container containing the CLI configuration arguments parsed
        + Type: Dictionary
        - Keys
            - optionals : Contains all optionals (flags and with arguments) specified by the user
                + Type: Dictionary
                - Values
                    - Flags
                        - help : Display help menu
                            + Type: Boolean
                            + Default: False
                        - version : Display system version information
                            + Type: Boolean
                            + Default: False
                        - display-options
                            + Type: Boolean
                            + Default: False
                        - generate-config
                            + Type: Boolean
                            + Default: False
                        - print-config
                            + Type: Boolean
                            + Default: False
                        - list-stages
                            + Type: Boolean
                            + Default: False
                        - unmount
                            + Type: Boolean
                            + Default: False
                    - With arguments
                        - CUSTOM_CONFIGURATION_FILENAME : Stores the name of the custom configuration file specified by the user to import
                            + Type: String
                            + Default: config.yaml
                        - TARGET_DISK_NAME : Stores the target disk/device medium to install into
                            + Type: String
                            + Default: None
                        - EDITOR : Stores the specified editor to open
                            + Type: String
                            + Default: None
                        - MODE : Stores the specified run mode to start with
                            + Type: String
                            + Default: DEBUG
                        - CFDISK_TARGET : Specify the target device/disk to edit with cfdisk
                            + Type: String
                            + Default: None
                        - FDISK_TARGET : Specify the target device/disk to edit with fdisk
                            + Type: String
                            + Default: None
                        - ROOTFS_MOUNT_PATH : Stores the mount path of the root filesystem specified by the user
                            + Type: String
                            + Default: None
                        - STAGES : Stores all stages to be executed as specified by the user using '--stage'
                            + Type: Array (List)
                            + Default: []
            - positionals : Contains all positional arguments specified by the user
                + Type: List
    - `.optionals` : Contains a dictionary of all optional CLI arguments (With Arguments and flags) found in `configurations["optionals"]`
        + Type: Dictionary
    - `.positionals` : Contains a list of all positional arguments found in `configurations["positionals"]`
        + Type: List
    - `.exec` : Contains the executable's full file name (file path and file name)
        + Type: String
        - Tips
            - Can be split into the file path and file name using 'os.path.basename(exec)'
                + [0] = File Path
                + [1] = File Name
    - `.argv` : Contains the system CLI arguments list parsed by the user
        + Type: Array/List
    - `.argc` : Contains the Argument Lists count (Number of arguments parsed)
        + Type: Integer

- pydistinstall.lib.config_handler.YAMLConfig
    - `.file_name` : Contains the name of the opened configuration file
        + Type: String
    - `.mode` : Contains the open mode of the opened configuration file
        + Type: String
    - `.file` : Contains the file object of the opened configuration file
        + Type: IO (File)

- pydistinstall.lib.env.Environment
    - `.EDITOR` : The system's default text editor
        + Environment Variable: "EDITOR"
    - `.TARGET_DISK_NAME` : The target disk's label (i.e. /dev/sdX for SATA|AHCI, or /dev/nvme0np1 for NVME)
        + Environment Variable: "TARGET_DISK_NAME"
    - `.MODE` : The Runtime boot mode - DEBUG|RELEASE
        + Environment Variable: "MODE"
        - Supported Values
            + DEBUG
            + RELEASE
    - `.USER` : Name of regular user
        + Environment Variable: "USER"
    - `.SUDO_USER` : Name of superuser
        + Environment Variable: "SUDO_USER"

- pydistinstall.lib.format.Text
    - `.msg` : Contains the text message you wish to format
        + Type: String

## Troubleshooting
### Post-Installation
#### Package Manager
- Running 'pacman -Syu' after a successful build results in 'archlinux-key' out of date
    - Potential Issues: 
        - Host system's pacman is not updated
    - Solutions
        - Update your host system to the latest version
        - Re-Install again

## Wiki

## Resources

## References

## Remarks


