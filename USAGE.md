# Quickstart Usage Reference Guide

## Table of Contents
- [Users](#users)
    + [Steps](#steps)
- [Developers](#developers)
    - [Dependencies and Importing](#dependencies-and-importing)
        + [Modules](#importing-modules)
    - [Using the distribution installer template as a standalone framework](#using-distribution-installer-template-as-a-standalone-framework)
        - [Class Initialization](#class-initialization)
- [Project Structure](#project-structure)
    + [Format](#format)
    + [Components](#project-components)
- [Configuration](#configuration)
    + [Components](#configuration-components)
    - [Template](#configuration-template)
        + [Structure](#template-structure)
        + [Examples](#template-examples)

## Users
### Steps
- Research
    - Planning
        - You need to figure out afew things prior to installation
            - Use-Case/Purpose
                + determines the below
            - What device medium
                + storage speed
            - What packages will be required
                + base system packages
            - How much storage is required
                + storage medium device space
            - Where will it be installed into
                + hardware device
            - Who will be using it
                + users
- Design
    - Generate a configuration template from the CLI
        - Default
            + System will generate a default config file 'config.yaml'
            ```console
            sudo py-distinstall -g
            ```
        - Custom configuration file name
            ```console
            sudo py-distinstall -c [new-config-file-name] -g
            ```
    - Update the configuration file with your requirements
        + Please refer to [Configuration](#configuration) for more information on the configuration documentation and template structure
- Running
    - Debug
        + the installer has 2 modes - DEBUG and RELEASE
        - By default, 
            - the installer is in DEBUG mode where it will display all the steps and commands that will be executed during the installation process
                ```console
                sudo py-distinstall {options} start
                ```
        - To begin the installation proper 
            + You will need to explicitly modify it to 'RELEASE' mode
            + Run as sudo
    - Release
        - Notes
            + You can also set the mode to 'RELEASE' via the Environment Variables 'MODE=RELEASE'
            - On startup
                + Enter accordingly
        - Default
            ```console
            sudo py-distinstall {options} -m RELEASE start
            ```
        - Using a custom configuration file
            ```console
            sudo py-distinstall {options} -c [custom-configuration-file-name] -m RELEASE start
            ```

## Developers
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
        - `.PostInstallation(setup, base_mechanism_Obj)` : Initializes the class object for the Base Installation of the target distribution containing various Base installation-related functions and attribues/variables
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
        - `.verify_network(ping_Count=5, ipv4_address="8.8.8.8")`: Installation Stage 1: Verify that the host network is working
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

        - `.verify_boot_Mode()`: Verifies and returns the motherboard bootloader firmware
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

        - `.update_system_Clock(): Syncs the system clock using NTP (Network-Time Protocol) by syncing with a central server
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

        - `.device_partition_Manager()`: Device & Partition Management
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

        - `.mount_Disks()`: Mount Disks, the Root, Boot and other Partitions
            - Return
                + Type: Void

        - `.select_Mirrors(mirrorlist_Path)`: Select a mirror for the package manager (TODO: Currently unused; unimplemented)
            - Parameter Signature/Header
                - mirrorlist_Path : Specify the path to the mirrorlist
                    + Type: String
            - Return
                + Type: Void

        - `.check_package_manager_Configurations(mount_Dir)`: Check Package Manager configuration support
            - Return
                + Type: Void

        - `.bootstrap_Install()`: Bootstrap all essential and must have packages to the mounted root filesystem before the chroot process
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

        - `.fstab_Generate()`: Generate the chroot root filesystem's File System Table (fstab)
            - Return
                - success_flag : A boolean flag showing if the command was a success or failed
                    + Type: Boolean
                    - Values
                        + True: Success
                        + False: Error

    - Chroot Actions
        - `.format_chroot_Subprocess(cmd_str, mount_Dir="/mnt", chroot_Command="arch-chroot", shell="/bin/bash")`: Format and returns the command string into the subprocess command list
            - Parameter Signature/Header
            - Return
                - subprocess_cmd_fmt : A list containing the commands to be executed in the chroot environment as well as the other flags and options
                    + Type List

        - `.chroot_execute_command(cmd_str, mount_Dir="/mnt", chroot_Command="arch-chroot", shell="/bin/bash")`: Generalized chroot command execution
            - Return
                - result : A Dictionary (key-value) mapping containing the standard output (stdout), standard error (stderr), the return status code (resultcode) and the command string (command-string)
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

- pydistinstall.app.distributions.archlinux.mechanism.PostInstallation

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
            ```python
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

### Dependencies and Importing

#### Importing Modules
- Linux Distributions Module
    ```python
    import app.distributions as dist
    ```
- Import target distribution Base installation mechanism
    ```python
    from app.distributions.[distribution] import mechanism
    ```
- Setup file
    ```python
    from setup import Setup
    ```
- Import a library/module from the collection of libraries
    ```python
    from lib import process
    ```

### Using distribution installer template as a standalone framework

#### Class Initialization
- Initialize Setup class object
    ```python
    setup = Setup(...)
    ```

- Initialize distribution's Base Installation class object
    ```python
    installer_class = mechanism.BaseInstallation(setup) # Import the distribution of choice's installation mechanism
    ```

- Initialize distribution's Post Installation class object
    ```python
    installer_class_PostInstall = mechanism.PostInstallation(setup, installer_class) # Import the distribution of choice's postinstallation class
    ```

#### Calling functions
- Base Installation
    ```python
    self.installer_class.[functions-from-framework]()
    ```

- Post Installation
    ```python
    self.installer_class_PostInstall.[functions-from-framework]()
    ```

#### Attributes and Variables
- Base Installation
    ```python
    self.installer_class.[attributes]
    ```

- Post Installation
    ```python
    self.installer_class_PostInstall.[attributes]
    ```

## Project Structure
### Format
```
project-root/
    |
    |-- src/ 
        |
        |-- main.py  
        |-- setup.py 
        |-- unittest.py 
        |-- app/ 
            |
            |-- runner.py 
            |-- distributions/ 
                |
                |-- archlinux/ 
                    |
                    |-- mechanism.py 
        |-- lib/ 
            |
            |-- cli.py 
            |-- config_handler.py 
            |-- const.py 
            |-- device_management.py 
            |-- env.py 
            |-- format.py 
            |-- process.py 
            |-- user_management.py 
            |-- utils.py 
```

### Project Components
- project-root/
    - src/ : For all project-related files
        - main.py  : The main runner/launcher project code
        - setup.py : Root setup file for the main runner/launcher
        - unittest.py : WIP Unit Testing source file
        - app/ : For all application-specific functionalities; Such as source files related to the installation mechanism of the various Distributions
            - runner.py : This is the Distribution Switcher ("Load Balancer") that will process your target distribution name and separate to the appropriate distributions
            - distributions/ : For all distribution classes
                - archlinux/ : Contains ArchLinux installation functionality and archlinux-specific libraries
                    - mechanism.py : The primary library containing the Base Installation and Post-Installation mechanism classes for the distribution
        - lib/ : For all external/general libraries that are not application-specific
            - cli.py : This contains functionality to Command Line Interface (CLI) Argument handling
            - config_handler.py : This contains functionality to handling Configuration Files
            - const.py : This contains constant variables and values
            - device_management.py : This contains Device and Disk Handling functions
            - env.py : This contains Environment Variables
            - format.py : This contains string formatting support
            - process.py : This contains Subprocess and systems command execution functions
            - user_management.py : This contains User management functionalities
            - utils.py : This contains general utilities

## Configuration
### Configuration Components
- Key-Values
    - distribution-name: The target distribution/platform you wish to install
        - Valid Values
            + arch : ArchLinux
            + debian : (WIP) Debian
            + gentoo : (WIP) Debian
    - device_Type: (Currently not in use); This specifies the type of storage medium/device you are using; i.e. SSD, HDD, VHD, VDI, QCOW2
        - Format
            ```yaml
            device_Type: VHD
            ```
        - Storage Medium Types
            + HDD : Hard Disk Drive
            + SSH : Solid State Drive
            + VHD : Virtual Hard Drive
            + VDI : Virtual Disk Image
            + QCOW2 : QEMU Image format
    - storage-controller: Specify the storage controller used by the storage medium/device
        - Storage Controllers
            - Currently supported
                + sata : For SATA/AHCI Controllers; Format: /dev/sdX
                + nvme : For NVME Controllers; Format: /dev/nvmeXpN
                + loop : Loopback Devices; Format: /dev/loopXpN
    - device_Size: This specifies the total disk/drive storage space/size
        - Format
            ```yaml
            device_Size: 51200MiB
            ```
        - Space/Size Formats 
            + Megabytes : MB
            + Mibibytes : MiB
            + Gigabytes : GB
            + Gibibytes : GiB
    - disk_Label: This specifies the disk/drive label aka the device index; i.e. /dev/sdX or /dev/nvme0np1
        - Format
            ```yaml
            disk_Label: /dev/sdX
            ```
        - Disk Label naming formats:
            - Supported
                + SATA: /dev/sdb
            - WIP
                + NVME: /dev/nvme[drive-number]np[partition-number]
    - disk_partition_Table: This specifies the partition table the drive will be formatted with before disk management and partitioning will take place; At the moment there are 2 choices - MSDOS (for Master Boot Record/MBR) and GPT (GUID Partition Table)
        - Format
            ```yaml
            disk_partition_Table: msdos
            ```
        - Partition Table Formats 
            - Supported
                + msdos : Legacy partition table format; Used back in the day when the maximum HDD size was ~2TB; This partition table only supports a maximum of 2TB per partition scheme
                + gpt   : Modern partition table format; Developed as a modern replacement for MSDOS; This partition table is required for partition sizes > 2TB
    - bootloader_firmware: This specifies the Motherboard Bootloader Firmware that determines if it is Legacy, or if it supports modern features (i.e. UEFI)
        - Format
            ```yaml
            bootloader_firmware: bios
            ```
        - Motherboard Bootloader Firmware
            - Supported
                + bios : Legacy
                + efi : For Universal EFI support; typically used with GPT but not always
    - bootloader: This contains the bootloader to install to load the operating system from the Boot Manager
        - Format
            ```yaml
            bootloader: grub
            ```
        - Bootloaders
            - Supported
                + grub
    - partition_Scheme: Dictionary/Mapping of the partition's number/ID to that partition's definitions and specifications
        - Format
            ```yaml
            partition_Scheme:
                1:
                    - partition-label
                    - partition-type
                    - partition-filesystem
                    - partition-start-size
                    - partition-end-size
                    - partition-bootable
                    - partition-others
                2:
                    - ...
            ```
        - partition number/ID
            - partition label/name : This is the name that will be tagged to the partition if partition table is MBR/MSDOS; Used as the name and type of the partition if partition table is GPT
            - partition type : The type of partition it is; Used for MBR/MSDOS partitions
                - Possible Values
                    - if partition table is MBR/MSDOS 
                        + primary
                        + logical
                        + extended
                    - if partition table is GPT: This is the same as the partition label
            - partition filesystem : The filesystem type of the partition
                - Formats
                    - Currently Supported
                        + ext4
                    - WIP
                        + btrfs
            - partition start size : The starting index/position/size of the partition block to begin writing; Place it at the exact same size as the end of the previous partition to place the blocks side by side
                - Special Values
                    + 0% : From the start
                    + N% : N-th percent of the whole disk/partition space
                    + 50% : Half the whole disk/partition space
                    + 75% : 3/4 the whole disk/partition space
                    + 100% : The end of the disk/partition space
            - partition end size : The ending index/position/size of the partition block to begin writing; Place this at the exact same size as the start of the next partition to place the blocks side by side
                - Special Values
                    + N% : From the partition starting position to the N-th percent of the remaining space
                    + 50% : From the partition starting position to Half the remaining space
                    + 75% : From the partition starting position to 3/4 the remaining space
                    + 100% : From the partition starting position to the end of the disk/partition space; Use up the remaining space
            - partition bootable : Flag to enable/disable bootable partition; True = Bootable, False = Not Bootable
            - partition other options : Currently not in use; Specify other options that you might want to add into the partitions
                + WIP
    - mount_Paths: Key-Value/Dictionary Mapping of name of the partition and the mount point; Note: This might be removed in a future update as this could potentially be merged into the key 'partition_Scheme' for efficiency
        - Format
            ```yaml
            - mount_Paths:
                partition-label/name: mount-point
            ```
    - base_pkgs: List of all the packages you wish to be bootstrapped into the base/root filesystem at the start
        - Format
            ```yaml
            base_pkgs:
                - your
                - packages
                - here
            ```
        - Recommended Packages
            + base
            + linux
            + linux-firmware
            + linux-lts
            + linux-lts-headers
            + base-devel
            + nano
            + vim
            + networkmanager
            + os-prober
    - location: Key-Value/Dictionary mapping of locale/location-based information required to be entered into the Operating System
        - Format
            ```yaml
            location:
                Region: [your-region]
                City: [your-city]
                Language: en_[Country-Code].UTF-8
                KeyboardMapping: en_UTF-8
            ```
        - Region: This is mapped to your country/city's region in your timezone/locale (i.e. Asia, America)
        - City: This is mapped to your city in your timezone/locale (i.e. Singapore, Chicago)
        - Language: This is mapped to the language code found in '/etc/locale' and used by locale-gen; i.e. en_SG.UTF-8, en_US.UTF-8
        - KeyboardMapping: This is mapped to your keyboard's mapping; i.e. en_UTF-8 for English
    - user_ProfileInfo: Key-Value mapping of a user to its properties; Note: This key name may be changed to a better name in general
        - Format
            ```yaml
            user_ProfileInfo:
                [user-name]:
                    - primary-group
                    - secondary-groups
                    -
            ```
        - [user-name]: This is the entry user's username
            - primary-group : This contains the user's primary group
            - secondary-groups : This contains the user's secondary group(s); Multiple entries are currently a WIP but please separate each entry with a ',' delimiter
            - home-directory : This contains the user's target home directory
            - other-options : (Currently Not Implemented) this contains other options that may be used for User Management; You can just leave it as NIL
    - networkConfig_hostname: This specifies the Operating System's Hostname within the network; This hostname will be used to recognize the device from the default gateway router by mapping the hostname and the IP address
        - Format
            ```yaml
            networkConfig_hostname: your-hostname
            ```
    - bootloader_directory: This specifies the directory/folder where the bootloader will be generated and storing its configurations into; Use '/boot/grub' if in doubt
        - Format
            ```yaml
            bootloader_directory: /boot/grub
            ```
    - bootloader_Params: This specifies additional parameters/options you wish to parse into the bootloader configuration generating process; Default: '' (Empty)
        - Format
            ```yaml
            bootloader_Params: ''
            ```
    - default_kernel: This specifies the default linux kernel to be used
        - Format 
            ```yaml
            default_kernel: linux
            ```
        - Kernel Variants
            - Supported
                + linux
            - WIP
                + linux-lts
                + linux-zen
    - platform_Arch: This specifies the CPU platform/architecture you wish to install the distribution into
        - Format
            ```yaml
            platform_Arch: i386-pc
            ```
        - CPU Architectures/Platforms
            - Supported
                + i386-pc : Generic x86_64 CPU architecture
            - WIP
                + amd64
                + x86_64
                + ARM32
                + ARM64

### Configuration Template
#### Template Structure
- JSON
    + WIP
- YAML
    ```yaml
    ## Platform Management
    distribution_Name: [arch] # The target distribution/platform you wish to install

    # Storage Disk/Device Firmware and Controller Settings
    device_Type: [your-device-type (VHD|VDI|QCOW2)]
    storage-Controller: [your-storage-controller (ahci|nvme|loop)]
    device_Size: [total-storage-size (xMiB|xMB|xGiB|xGB)]
    disk_Label: [your-device-file (i.e. SATA|AHCI => /dev/sdX, NVME => /dev/nvme[device-number], Loopback device => /dev/loop[device-number])]
    disk_partition_Table: [partition-table (msdos|uefi)]
    bootloader_firmware: [motherboard-bootloader-firmware (mbr|gpt)]
    bootloader: [your-bootloader (grub)]

    # Partition Scheme/Layout
    partition_Scheme:
      # Format:
      # Partition-number:
      #     - Partition-Label | Partition-Name
      #     - Partition-Type
      #     - Partition-Filesystem
      #     - Partition-Starting position/size of partition (Integer|Percentage)
      #     - Partition-Ending position/size of partition (Integer|Percentage)
      1:
        - Boot
        - primary
        - ext4
        - 0%
        - 1024MiB
        - true
        - NIL
      2:
        - Root
        - primary
        - ext4
        - 1024MiB
        - 32768MiB
        - false
        - NIL
      3:
        - Home
        - primary
        - ext4
        - 32768MiB
        - 100%
        - false
        - NIL

    # Filesystem Mounting
    mount_Paths:
      # Key = Partition Name/ID
      # Value = Mount Path/directory
      Boot: /mnt/boot
      Root: /mnt
      Home: /mnt/home

    # System Management

    ## Package Management
    base_pkgs:
      # - Package Name
      - base
      - linux
      - linux-firmware
      - linux-lts
      - linux-lts-headers
      - base-devel
      - nano
      - vim
      - networkmanager
      - os-prober

    ## System Location (Locale)
    location:
      Region: your-region
      City: your-city
      Language: [locale].UTF-8
      KeyboardMapping: en_UTF-8

    ## User Profile
    user_ProfileInfo:
      username:
        - wheel
        - users
        - /home/profiles/username
        - NIL

    ## Network Management
    networkConfig_hostname: your-hostname

    ## System Management
    bootloader_directory: /boot/grub
    bootloader_Params: ''
    default_kernel: [kernel-name (i.e. linux | linux-lts | linux-zen)]
    platform_Arch: [system-platform-architecture (i386-pc)]
    ```

#### Template Examples
- JSON
    + WIP
- YAML
    - ArchLinux (arch), /dev/sdX (sata|ahci), 51200MIB Storage, MSDOS, BIOS, GRUB
        ```yaml
        distribution-name: arch
        device_Type: VHD
        storage-controller: sata
        device_Size: 51200MiB
        disk_Label: /dev/sdX
        disk_partition_Table: msdos
        bootloader_firmware: bios
        bootloader: grub
        partition_Scheme:
          1:
            - Boot
            - primary
            - ext4
            - 0%
            - 1024MiB
            - true
            - NIL
          2:
            - Root
            - primary
            - ext4
            - 1024MiB
            - 32768MiB
            - false
            - NIL
          3:
            - Home
            - primary
            - ext4
            - 32768MiB
            - 100%
            - false
            - NIL
        mount_Paths:
          Boot: /mnt/boot
          Root: /mnt
          Home: /mnt/home
        base_pkgs:
          - base
          - linux
          - linux-firmware
          - linux-lts
          - linux-lts-headers
          - base-devel
          - nano
          - vim
          - networkmanager
          - os-prober
        location:
          Region: your-region
          City: your-city
          Language: [locale].UTF-8
          KeyboardMapping: en_UTF-8
        user_ProfileInfo:
          username:
            - wheel
            - users
            - /home/profiles/username
            - NIL
        networkConfig_hostname: your-hostname
        bootloader_directory: /boot/grub
        bootloader_Params: ''
        default_kernel: linux
        platform_Arch: i386-pc
        ```

## Wiki
### Terminologies
- Partition Type (For MSDOS/MBR/BIOS), Partition Label (For GPT/(U)EFI)
    - Partition Type: For MSDOS/MBR disk filesystem labels
        + Type: String
        - Accepted Values
            + primary
            + logical
            + extended
- Partition Label: For GPT disk filesystem labels; This is effectively a 'name' (aka Label) you can assign to the partition as GPT doesnt use primary, extended, nor logical for separation
    + Type: String
- Filesystem : A filesystem is effectively a descriptor installed in a storage disk/device to specify what kind of storage this device is storing/able to store
    - Filesystem Types
        + ext4 : Used if booting with BIOS legacy motherboard firmware
        + fat32 : Required to be used for the boot partition when booting with UEFI

