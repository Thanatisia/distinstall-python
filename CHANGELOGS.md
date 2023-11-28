# CHANGELOGS

## Table of Contents
- Entries
    > [version] | [date] [time] | [status]
    + v0.1.0 | 2023-09-26 1604H | Merged to main
    + v0.1.1 | 2023-09-26 2223H | Merged to main
    + v0.2.0 | 2023-09-27 2106H | Merged to main
    + v0.2.1 | 2023-09-30 1650H | Merged to main
    + v0.2.2 | 2023-11-28 1708H | Development
    + v0.2.3 | 2023-11-28 1945H | Development
    + v0.2.4 | 2023-11-28 2018H | Development
    + v0.2.5 | 2023-11-28 2112H | Development
    + v0.2.6 | 2023-11-28 2200H | Development

## Entries

### v0.1.0
- New
    + Initial commit of the rewrite of [Thanatisia/distro-installscript-arch](https://github.com/Thanatisia/distro-installscript-arch) in Python

### v0.1.1
- Updates
    + Added support for CLI optional argument ['-c', '--config-file'] to specify the name of the configuration file
    + Added support for CLI optional argument ['-g', '--generate-config'] to generate the configuration file
    + Added support for CLI optional argument ['--print-config'] to import, load the configuration file and print the contents; Use this to specifically view the configuration file contents in the application
    + Changed requirements for YAML from 'pyyaml' => 'ruamel.yaml'
    + Changed default configuration variable 'CUSTOM_CONFIGURATION_FILENAME' value from "" => "config.yaml"
    + Added display_help support to 'main.py' (runner/launcher file
    + Updated YAML support in setup.py from pyyaml => ruamel.yaml
    + Fixed bug in setup.py: cfg - Added commas to the list

## Development
### v0.1.1
- Updates
    + Added support for CLI optional argument ['-c', '--config-file'] to specify the name of the configuration file
    + Added support for CLI optional argument ['-g', '--generate-config'] to generate the configuration file
    + Added support for CLI optional argument ['--print-config'] to import, load the configuration file and print the contents; Use this to specifically view the configuration file contents in the application
    + Changed requirements for YAML from 'pyyaml' => 'ruamel.yaml'
    + Changed default configuration variable 'CUSTOM_CONFIGURATION_FILENAME' value from "" => "config.yaml"
    + Added display_help support to 'main.py' (runner/launcher file
    + Updated YAML support in setup.py from pyyaml => ruamel.yaml
    + Fixed bug in setup.py: cfg - Added commas to the list

### v0.2.0
- New
    + Created new file 'const.py' to place all immutable/constant variables
- Updates
    - Major fixes
        - General flow for ArchLinux's base installation mechanism is working
            + Requires some cleanup before it is production ready
    - began standardization of 
        + environment variables retrieval to be set in 'lib/env.py'
        + global constants to be set in 'lib/const.py'
    - README.md
        - Updated TODO list with new tasks: 
            + configuration file handling and support
            + Rename YAML configuration file keyword naming convention
        - Added Synopsis/Syntax, Parameters and Usage for basic documentation
        - Added implementation steps to use the project in your own personal project
    - main.py
        + Changed initialization of class 'env.Environment()' => setup.env : Referencing of the environment class variable from 'setup.py' so that everything is in one location (unless otherwise required/specified)
        + Fixed header message: Removed quotation marks at the end
        + Utilised 'update_setup()' just before starting the installer function to update the class variables
        + Added testing user validation and cleanup
        + Added implementation of ['-m', '--mode'] CLI options in the processing of the parsed arguments in the body
        + Updated 'begin_installer.py' with a distribution selector to iterate between the distributions and select which to install
    - setup.py
        + initialized class 'lib/env.Environment()' to be used as a global reference variable during runtime.
        + Updated init_prog_Info() to have a default value of retrieving from 'env.MODE' (which takes from the environment variable 'MODE') if parameter 'program_MODE' is not specified.
        + Removed program_Mode parameter checking and set it to as-is
    - archlinux
        + Performing initial workflow fix
        - mechanism.py
            + Added function 'print_configurations'
            + Wrapped the constructor lines into a standalone event update function 'update_setup'
            + Added the return element 'resultcode' to every subprocess the process function requires
            + Removed any error messages via bash 'echo' command and through native python via print
            + Replaced copy function via echo to writing
            + Added quotation wraps around echo commands
            + Added stderr return from 'subprocess_Line' calls
            + Removing the dependency on shellscript file 'chroot_cmds.sh' and 'postinstallation_cmds.sh' to execute and execute using python
            + Added '.items()' behind partition_Scheme in line 247 and line 314
            - Replaced unsetting via '= None' (Wrong) => using .pop (Correct)
                + Unsetting doesnt remove thee index, only remove the value and set it as None/Null
            + Removed quotation marks surrounding the folders to be mounted
            + Removed quotation marks surrounding the device to be mounted
            + Created standalone postinstallation function 'enable_sudo' for enabling sudoers
            + Changed the postinstallation cleanup process to become more efficient
            - Fixes
                + Fixed Genfstab
                + Fixed Localization
                + Fixed Network Configuration
                + Fixed Initial RAM filesystem formatting
                + Fixed setting root password + Creating working subprocess stdin buffer stream flow
                + Fixed Bootloader installation
                + Fixed User Management
                + Fixed User Creation process
                + Fixed User password setting
    - lib
        - cli.py
            + Added support for CLI optional argument ['--display-options'] to display options only
            + Updated value of configurations keyword 'MODE' to a default value of 'DEBUG'
        - env.py
            + Added environment variables 'USER' and 'SUDO_USER' for user run validation
        - process.py
            + Updated functions subprocess_Line and subprocess_Sync to return the result/exit/status code
            + Added Variable-Length Keyword Arguments '**opts' into commands 'subprocess_Sync' and 'subprocess_Line'
            + Added function 'subprocess_Open' to open a subprocess
            + Added function 'chroot_exec' to open a subprocess pipe and execute in chroot
            + Added stderr return to the function 'subprocess_Line'
            + Added function 'subprocess_Input' for any steps requiring subprocess stdin (standard input) buffer stream writing
            + Added function 'subprocess_stdin_Clear' to clear off the stdin stream after writing or usage
            + Separated 'with Popen()... as proc' to individual steps for modularity
            - Fixes
                + Fixed subprocess_Line() to return the returncode proper

### v0.2.1
- New
    + Added new 'USAGE.md' for a Quickstart Reference Guide for using
- Updates
    - README.md
        + Added header 'Developers' for Developer Documentations
        + Added new TODO

### v0.2.2
- New
    - Added document 'Makefile' for automation

- Updates
    - Updated document 'README.md' with
        - New TODO 
    - Updated document 'requirements.txt'
        - Added dependency for pyinstaller : Attempting to implement pyinstaller compilation support for easier distribution
    - Updated installation mechanism 'archlinux'
        - Removed import 'yaml'

### v0.2.3
- Updates
    - Updated document 'README.md'
        - Additional pre-requisite if you are installing in a loopback device (i.e. a Virtual Disk Image/Virtual Hard Drive)
        - Added new TODO regarding the configuration key-value "device_Type"
    - Updated document 'USAGE.md' 
        - Updated section 'configuration'
            - Added valid values to 'device_Type'
            - Plans to either
                1. Rename 'device_Type' to 'storage_Controller', or
                2. Add a new key named 'storage_Controller'
    - Updated installation mechanism 'archlinux'
        - Implemented feature: Multi-storage platform support 
            - i.e. 
                + SATA/AHCI => /dev/sdX, 
                + NVME => /dev/nvmeXpN, 
                + Loopback => /dev/loopXpN, 
                + ...
            - Users have to specify their device medium in the configuration file's keyword 'device_Type' 
                - Accepted Values
                    + sata : For SATA/AHCI Controllers; Format: /dev/sdX
                    + nvme : For NVME Controllers; Format: /dev/nvmeXpN
                    + loop : Loopback Devices; Format: /dev/loopXpN

### v0.2.4
- Updates
    - Updated document 'README.md' 
        - Added a 'Quickflow guide' section for reference
    - Updated document 'main.py' in 'src'
        - Changed functions 'generate_config' => 'generate_config_Raw' because raw string is easier to handle
    - Updated document 'setup.py' in 'src'
        - Added new function 'generate_config_Raw' to output a raw string of the configuration file directly
        - Renamed function 'generate_config' => 'generated_config_YAML' for a dedicated YAML configuration output

### v0.2.5
- New
    - Added new document 'device_management.py' in 'src/lib' for functions related to Device/Disk Management

- Updates
    - Updated document 'mechanism.py' in 'src/app/distributions/archlinux'
        - Refactored and rewrote the Storage Controller validator into a single function in 'src/lib/device_management.py' titled 'format_partition_str' and
        - Replaced the validators with the function call to streamline and make things neater

### v0.2.6
- Updates
    - Updated document 'mechanism.py' in 'src/app/distributions/archlinux'
        - Refactored and removed unnecessary legacy code-comments and debug messages

### v0.2.7
- Updates
    - Updated document 'process.py' in 'src/lib'
        - Added new function 'subprocess_Realtime()' to display standard output in real time, line by line (Testing)

    - Updated document 'mechanism.py' in 'src/app/distributions/archlinux'
        - Removed several standard output prints and 
        - Replaced 'subprocess_Line' with 'subprocess_Realtime' 

### v0.2.8
- Updates
    - Updated document 'mechanism.py' in 'src/app/distributions/archlinux'
        - Fixed chroot_exec by parsing in the 'dir_Mount' parameter leading to the root partition (mount) directory
        - Added User Validator to check if user exists when copying files/scripts to user
        - Bug Fix: Moved action 'Select' by 1 indent inwards to be under the primary action 'Delete'
    - Updated document 'process.py' in 'src/lib'
        - Fixing 'subprocess_Realtime()' : WIP
