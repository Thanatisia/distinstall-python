# CHANGELOGS

## Table of Contents
- [2023-09-26](#2023-09-26)
    + 1604H : v0.1.0
    + 2223H : v0.1.1
- [2023-09-27](#2023-09-27)
    + 2106H : v0.2.0
- [2023-09-30](#2023-09-30)
    + 1650H : v0.2.1
- [2023-11-28](#2023-11-28)
    + 1708H : v0.2.2
    + 1945H : v0.2.3
    + 2018H : v0.2.4
    + 2112H : v0.2.5
    + 2200H : v0.2.6
- [2023-11-29](#2023-11-29)
    + 2012H : v0.2.10
- [2023-12-02](#2023-12-02)
    + 0905H : v0.2.11
    + 0949H : v0.2.12
    + 1020H : v0.2.13
    + 1024H : v0.3.0
- [2023-12-03](#2023-12-03)
    + 2251H : v0.3.1
    + 2344H : v0.3.2
    + 2354H : v0.3.3
- [2023-12-04](#2023-12-04)
    + 1246H : v0.3.4
    + 1253H : v0.3.5
    + 1331H : v0.3.6
    + 2141H : v0.3.7
    + 2200H : v0.3.8
    + 2243H : v0.3.9
    + 2333H : v0.3.10
- [2023-12-05](#2023-12-05)
    + 1946H : v0.3.11
    + 2006H : v0.3.12
- [2023-12-11](#2023-12-11)
    + 1227H : v0.4.0
- [2024-01-29](#2024-01-29)
    + 1026H : v0.4.1
    + 1758H : v0.4.2
- [2024-01-29](#2024-01-29)
    + 1758H : v0.4.3
    + 2227H : v0.4.4
- [2024-01-30](#2024-01-30)
    + 1358H : v0.4.5
- [2024-04-19](#2024-04-19)
    + 1137H

## Entries

### 2023-09-26
#### 1604H
+ Version: v0.1.0

- Version Changes:
    + Initial commit of the rewrite of [Thanatisia/distro-installscript-arch](https://github.com/Thanatisia/distro-installscript-arch) in Python

#### 2223H : v0.1.1
+ Version: v0.1.1

- Version Changes:
    + Added support for CLI optional argument ['-c', '--config-file'] to specify the name of the configuration file
    + Added support for CLI optional argument ['-g', '--generate-config'] to generate the configuration file
    + Added support for CLI optional argument ['--print-config'] to import, load the configuration file and print the contents; Use this to specifically view the configuration file contents in the application
    + Changed requirements for YAML from 'pyyaml' => 'ruamel.yaml'
    + Changed default configuration variable 'CUSTOM_CONFIGURATION_FILENAME' value from "" => "config.yaml"
    + Added display_help support to 'main.py' (runner/launcher file
    + Updated YAML support in setup.py from pyyaml => ruamel.yaml
    + Fixed bug in setup.py: cfg - Added commas to the list

### 2023-09-27
#### 2106H
+ Version: v0.2.0

- Version Changes
    - Major fixes
        - General flow for ArchLinux's base installation mechanism is working
            + Requires some cleanup before it is production ready
    - began standardization of 
        + environment variables retrieval to be set in 'lib/env.py'
        + global constants to be set in 'lib/const.py'

- New
    + Created new file 'const.py' to place all immutable/constant variables

- Updates
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

### 2023-09-30
#### 1650H
+ Version: v0.2.1

- Version Changes:
    + Added new document 'USAGE.md' for a Quickstart Reference Guide for using
    + Improved developer's documentations

- New
    + Added new 'USAGE.md' for a Quickstart Reference Guide for using

- Updates
    - README.md
        + Added header 'Developers' for Developer Documentations
        + Added new TODO

### 2023-11-28
#### 1708H
+ Version: v0.2.2

- Version Changes:
    + Added new document 'Makefile' for automation/improved Quality-of-Life

- New
    - Added document 'Makefile' for automation

- Updates
    - Updated document 'README.md' with
        - New TODO 
    - Updated document 'requirements.txt'
        - Added dependency for pyinstaller : Attempting to implement pyinstaller compilation support for easier distribution
    - Updated installation mechanism 'archlinux'
        - Removed import 'yaml'

#### 1945H
+ Version: v0.2.3

- Version Changes:
    - Feature Changes
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

#### 2018H
+ Version: v0.2.4

- Version Changes:
    - src/setup.py
        + Added new function 'generate_config_Raw' to output a raw string of the configuration file directly
        + Renamed function 'generate_config' => 'generated_config_YAML' for a dedicated YAML configuration output

- Updates
    - Updated document 'README.md' 
        - Added a 'Quickflow guide' section for reference
    - Updated document 'main.py' in 'src'
        - Changed functions 'generate_config' => 'generate_config_Raw' because raw string is easier to handle
    - Updated document 'setup.py' in 'src'
        - Added new function 'generate_config_Raw' to output a raw string of the configuration file directly
        - Renamed function 'generate_config' => 'generated_config_YAML' for a dedicated YAML configuration output

#### 2112H
+ Version: v0.2.5

- Version Changes:
    - Files changes
        + Added new document 'device_management.py' in 'src/lib' for functions related to Device/Disk Management
    - Updated document 'mechanism.py' in 'src/app/distributions/archlinux'
        - Refactored and rewrote the Storage Controller validator into a single function in 'src/lib/device_management.py' titled 'format_partition_str' and
        - Replaced the validators with the function call to streamline and make things neater

- New
    - Added new document 'device_management.py' in 'src/lib' for functions related to Device/Disk Management

- Updates
    - Updated document 'mechanism.py' in 'src/app/distributions/archlinux'
        - Refactored and rewrote the Storage Controller validator into a single function in 'src/lib/device_management.py' titled 'format_partition_str' and
        - Replaced the validators with the function call to streamline and make things neater

#### 2200H
+ Version: v0.2.6

- Version Changes:
    - Updated document 'mechanism.py' in 'src/app/distributions/archlinux'
        - Refactored and removed unnecessary legacy code-comments and debug messages

- Updates
    - Updated document 'mechanism.py' in 'src/app/distributions/archlinux'
        - Refactored and removed unnecessary legacy code-comments and debug messages

### 2023-11-29
#### 2012H
+ Version: v0.2.10

- Version Changes:
    - Updated document 'process.py' in 'src/lib'
        + Added new function 'subprocess_Realtime()' to display standard output in real time, line by line (Testing)
    - Updated document 'mechanism.py' in 'src/app/distributions/archlinux'
        + Removed several standard output prints and 
        + Replaced 'subprocess_Line' with 'subprocess_Realtime' 
        + Fixed chroot_exec by parsing in the 'dir_Mount' parameter leading to the root partition (mount) directory
        + Added User Validator to check if user exists when copying files/scripts to user
        + Bug Fix: Moved action 'Select' by 1 indent inwards to be under the primary action 'Delete'
        + Added user and directory validator when copying files to user home directory in the post-installation
        - Replaced usage of configuration key 'device_Type' with new key 'storage-controller' for accuracy
        - Tested new feature support 
            - 'Multi-Storage Controller support for various Storage Controllers'
            - Installation support for 
                - Disk Image files (i.e. .img files from dd) and loopback devices
                - SATA/AHCI devices (/dev/sdX)
        - WIP
            - Perform refactorization and cleaning up
    - src/setup.py
        + Added new key 'storage-controller' into template skeleton
    - Planned Feature Change
        - New Support
            - Multi-Storage Controller support for various Storage Controllers
                - Storage Controller Types
                    - SATA/AHCI => '/dev/sdX'
                    - NVME      => '/dev/nvme[device-number]p[partition-number]'
                    - Loopback  => '/dev/loop[device-number]p[partition-number]'

- v0.2.7
    - Updates
        - Updated document 'process.py' in 'src/lib'
            - Added new function 'subprocess_Realtime()' to display standard output in real time, line by line (Testing)

        - Updated document 'mechanism.py' in 'src/app/distributions/archlinux'
            - Removed several standard output prints and 
            - Replaced 'subprocess_Line' with 'subprocess_Realtime' 

- v0.2.8
    - Updates
        - Updated document 'mechanism.py' in 'src/app/distributions/archlinux'
            - Fixed chroot_exec by parsing in the 'dir_Mount' parameter leading to the root partition (mount) directory
            - Added User Validator to check if user exists when copying files/scripts to user
            - Bug Fix: Moved action 'Select' by 1 indent inwards to be under the primary action 'Delete'
        - Updated document 'process.py' in 'src/lib'
            - Fixing 'subprocess_Realtime()' : WIP

- v0.2.9
    - Updates
        - Updated document 'mechanism.py' in 'src/app/distributions/archlinux'
            - Added user and directory validator when copying files to user home directory in the post-installation

- v0.2.10
    - Planned Feature Change
        - New Support
            - Multi-Storage Controller support for various Storage Controllers
                - Storage Controller Types
                    - SATA/AHCI => '/dev/sdX'
                    - NVME      => '/dev/nvme[device-number]p[partition-number]'
                    - Loopback  => '/dev/loop[device-number]p[partition-number]'

    - Updates
        - Updated document 'mechanism.py' in 'src/app/distributions/archlinux'
            - Replaced usage of configuration key 'device_Type' with new key 'storage-controller' for accuracy
            - Tested new feature support 
                - 'Multi-Storage Controller support for various Storage Controllers'
                - Installation support for 
                    - Disk Image files (i.e. .img files from dd) and loopback devices
                    - SATA/AHCI devices (/dev/sdX)
            - WIP
                - Perform refactorization and cleaning up
        - Updated document 'USAGE.md' 
            - with new configuration setting key 'storage-controller'
        - Updated document 'setup.py' in 'src'
            - Added new key 'storage-controller' into template skeleton

### 2023-12-02
#### 0905H
+ Version: v0.2.11

- Version Changes:
    - 'src/app/distributions/archlinux/mechanism.py'
        - Renamed Base Installation class 'ArchLinux' into 'BaseInstallation'
    - 'src/app/runner.py'
        - Changed base installation class from 'ArchLinux' into 'BaseInstallation'

- Updates
    - Updated document 'mechanism.py' in 'src/app/distributions/archlinux'
        - Renamed Base Installation class 'ArchLinux' into 'BaseInstallation'
    - Updated document 'runner.py' in 'src/app'
        - Changed base installation class from 'ArchLinux' into 'BaseInstallation'

#### 0949H
+ Version: v0.2.12

- Version Changes:
    - src/main.py
        + Added documentation and usage examples for '--list-stages' and '--execute-stage'

- Updates
    - Updated document 'README.md' 
        - Added primary documentations - synopsis/syntax, parameters and usage
    - Updated document 'main.py' in 'src/'
        - Added documentation and usage examples for '--list-stages' and '--execute-stage'

#### 1020H
+ Version: v0.2.13

- Version Changes:
    - Updated documentation 'USAGE.md'
        + Reordered headers 'Class Initialization' to be a subheader under 'Using the distribution installer template as a standalone framework'
        + Added new categories 'Calling Functions' and 'Attributes and Variables'

- Updates
    - Updated document 'USAGE.md' 
        - Reordered headers 'Class Initialization' to be a subheader under 'Using the distribution installer template as a standalone framework'
        - Added new categories 'Calling Functions' and 'Attributes and Variables'

#### 1024H
+ Version: v0.3.0

- Version Changes:
    - Feature Change
        - New Support
            - Multi-Storage Controller support for various Storage Controllers
                - Storage Controller Types
                    - SATA/AHCI => '/dev/sdX'
                    - NVME      => '/dev/nvme[device-number]p[partition-number]'
                    - Loopback  => '/dev/loop[device-number]p[partition-number]'

        - New CLI options
            - `--list-stages` : List all installation stages in the specified distribution
            - `--execute-stage [stage-number]` : Explicit stage selection; You can specify an installation step/stage to execute. 
                + You can append this to execute multiple steps at a single operation
                + Ensure that you place all your steps in consecutive order

        - UX/DX Improvements
            - Created a 'load balancer', or more appropriately, a Distribution switcher that will act as a middleman proxy to process what Distribution you wish to install
                - Afterwhich, import and call the functions from the framework/library appropriately.
                - This should help to improve the User Experience (UX), Developer's Experience (DX), such that it is not only easier to modify, but should also improve expandibility.
            - Several functions in the mechanism framework has been separated into individual files
            - Post-Installation functions have been separated into its own standalone PostInstallation class for usage
                - It supports taking in the Base Installation class object to continue from the state of the Base Installation
            - Renamed Base Installation class 'ArchLinux' into 'BaseInstallation'

        - Documentations
            - Updated Documentations to match the latest version and options
            - Added Usage examples


### 2023-12-03
#### 2251H
+ Version: v0.3.1

- Version Changes:
    - Documentations
        - README.md
             - Converted 'Information' from a block into sentences
             - Added additional dependencies
             - Added new pre-requisite: If you are using a non-ArchLinux distribution

- Updates
    - README.md
         - Converted 'Information' from a block into sentences
         - Added additional dependencies
         - Added new pre-requisite: If you are using a non-ArchLinux distribution

- Testing
    - Installing using a non-ArchLinux system
         - Debian

#### 2344H
+ Version: v0.3.2

- Version Changes:
    - Documentations
        - README.md
            - Reorganized and placed pre-rquisite 'If you are using a non-ArchLinux distribution' above 'Install Dependencies'
            - Added additional packages to the mkarchroot corresponding to the depedencies when bootstrapping the root filesystem

- Updates
    - README.md
        - Reorganized and placed pre-rquisite 'If you are using a non-ArchLinux distribution' above 'Install Dependencies'
        - Added additional packages to the mkarchroot corresponding to the depedencies when bootstrapping the root filesystem

#### 2354H
+ Version: v0.3.3

- Version Changes:
    - Documentations
        - README.md
            - Added 'git' and 'arch-install-scripts' into the bootstrap package list

- Upates
    - README.md
        - Added 'git' and 'arch-install-scripts' into the bootstrap package list

### 2023-12-04
#### 1246H
+ Version: v0.3.4

- Version Changes:
    - Documentations
        - README.md
            - Added 'parted' into the bootstrap package list

- Upates
    - README.md
        - Added 'parted' into the bootstrap package list

#### 1253H
+ Version: v0.3.5

- Version Changes:
    - Files
        - Added new document 'pkglist.txt' containing all system-related dependencies/packages
    - Documentations
        - README.md
            - Added instructions to install system dependencies from file 'pkglist.txt
            - Added 'python' to the existing python-related dependency installation instructions

- New
    - Added new document 'pkglist.txt' containing all system-related dependencies/packages

- Updates
    - README.md
        - Added instructions to install system dependencies from file 'pkglist.txt
        - Added 'python' to the existing python-related dependency installation instructions

#### 1331H
+ Version: v0.3.6

- Version Changes:
    - Feature Changes
        - main.py
            - Added calling and runner support for new parameter '-u | --unmount' for Unmounting the drive from the mount points specified in the config file
        - cli.py
            - Added CLI support for new parameter '-u | --unmount'
    - Documentations
        - README.md
            - Added documentation for new parameter '-u | --unmount' 

- Updates
    - main.py
        - Added calling and runner support for new parameter '-u | --unmount' for Unmounting the drive from the mount points specified in the config file
    - cli.py
        - Added CLI support for new parameter '-u | --unmount'
    - README.md
        - Added documentation for new parameter '-u | --unmount' 

#### 2141H
+ Version: v0.3.7

- Version Changes:
    - Documentations
        - Updated document 'README.md'
            - Added instructions on how to create a root filesystem chroot environment using docker
            - Indenting
        - Updated document 'REFERENCES.md' in folder 'docs'
            - Added links
        - Updated document 'pkglist.txt'
            - Added 'vim'
    - Project Layout/Structure
        - Added folder 'docker' for storing docker-support files
            - Added document 'archlinux.Dockerfile' in 'docker' for creating a pre-defined ArchLinux chroot environment for installation by creating a docker container for each distribution (In case is necessary) with useful and essential packages
            - Added document 'debian.Dockerfile' in 'docker' for creating a pre-defined Debian chroot environment for installation by creating a docker container for each distribution (In case is necessary) with useful and essential packages

- New
    - Added folder 'docker' for storing docker-support files
        - Added document 'archlinux.Dockerfile' in 'docker' for creating a pre-defined ArchLinux chroot environment for installation by creating a docker container for each distribution (In case is necessary) with useful and essential packages
        - Added document 'debian.Dockerfile' in 'docker' for creating a pre-defined Debian chroot environment for installation by creating a docker container for each distribution (In case is necessary) with useful and essential packages
- Updates
    - Updated document 'README.md'
        - Added instructions on how to create a root filesystem chroot environment using docker
        - Indenting
    - Updated document 'REFERENCES.md' in folder 'docs'
        - Added links
    - Updated document 'pkglist.txt'
        - Added 'vim'

#### 2200H
+ Version: v0.3.8

- Version Changes:
    - 'src/app/distributions/archlinux/mechanism.py'
        - Added function 'check_package_manager_Configurations(self, mount_Dir)' to check for the package manager's configuration files (i.e. pacman.conf) because certain scenarios 
            - may cause pacstrap to generate a rootfs without pacman.conf
        - Added class variable 'package_manager_Configurations' to hold the package manager's configuration file default template

- Updates
    - Updated document 'mechanism.py' in 'src/app/distributions/archlinux'
        - Added function 'check_package_manager_Configurations(self, mount_Dir)' to check for the package manager's configuration files (i.e. pacman.conf) because certain scenarios 
            - may cause pacstrap to generate a rootfs without pacman.conf
        - Added class variable 'package_manager_Configurations' to hold the package manager's configuration file default template

#### 2243H
+ Version: v0.3.9

- Version Changes:
    - Documentations
        - README.md
            + Added optional step for setting up the docker chroot environment if using the official images
    - Source Code
        - 'src/app/distributions/archlinux/mechanism.py'
            - Added and tested package manager configuration file checking and validation for ArchLinux - in this case, /etc/pacman.conf - within the generated rootfs using pacstrap
                - If the bootstrapped root filesystem contents do not contain '/etc/pacman.conf', it will copy from the host
                - If the copy fails, it will generate from the package manager configuration file template string class variable in the Class
                    - Each distribution installer template will contain a different configuration file template

- Updates
    - Updated document 'README.md'
         - Added optional step for setting up the docker chroot environment if using the official images
    - Updated document 'mechanism.py' in 'src/app/distributions/archlinux'
        - Added and tested package manager configuration file checking and validation for ArchLinux - in this case, /etc/pacman.conf - within the generated rootfs using pacstrap
            - If the bootstrapped root filesystem contents do not contain '/etc/pacman.conf', it will copy from the host
            - If the copy fails, it will generate from the package manager configuration file template string class variable in the Class
                - Each distribution installer template will contain a different configuration file template

#### 2333H
+ Version: v0.3.10

- Version Changes:
    - New Files
        - Added new document 'setup-debian.sh' and 'setup-archlinux.sh' in 'docker'
            - Shellscript to automatically startup the docker image of the respective chroot environments you wish to startup, and install the dependencies to prepare for use
            - Use this if you wish to use the official images and not the prebuilt Dockerfiles
    - Documentation
        - Updated document 'README.md'
            - Added basic docker setup instructions
    - Docker image and containerization
        - Updated document 'debian.Dockerfile' in 'docker'
            - Changed packages and dependencies

- New
    - Added new document 'setup-debian.sh' and 'setup-archlinux.sh' in 'docker'
        - Shellscript to automatically startup the docker image of the respective chroot environments you wish to startup, and install the dependencies to prepare for use
        - Use this if you wish to use the official images and not the prebuilt Dockerfiles
- Updates
    - Updated document 'README.md'
        - Added basic docker setup instructions
    - Updated document 'debian.Dockerfile' in 'docker'
        - Changed packages and dependencies


### 2023-12-05
#### 1946H
+ Version: v0.3.11

- Version Changes:
    - Documentations
        - Updated document 'README.md'
            - Added steps for after initial startup of docker chroot environment
    - Source Code
        - 'src/lib/device_management.py'
            + Added a simple implementation of a blkid UUID reference function
        - 'src/lib/process.py'
            + Changed result 'stdout' in function 'subprocess_Line()' to not take in from the process pipe instead

- Updates
    - Updated document 'README.md'
        - Added steps for after initial startup of docker chroot environment
    - Updated document 'device_management.py' in 'src/lib'
        - Added a simple implementation of a blkid UUID reference function
    - Updated document 'process.py' in 'src/lib'
        - Changed result 'stdout' in function 'subprocess_Line()' to not take in from the process pipe instead

#### 2006H
+ Version: v0.3.12

- Version Changes:
    - Source Code
        - 'src/lib/device_management.py'
            - Fixed import mistake

- Updates
    - Updated document 'device_management.py' in 'src/lib'
        - Fixed import mistake

### 2023-12-11
#### 1227H
+ Version: v0.4.0 

- Version Changes:
    + Mass Update
    - Feature Release
        + Standalone install stage execution : You can specify which stage you wanna execute using option '--execute-stage [stage-number]'
        + Standalone unmount option : Unmount partitions using the inline unmount option '-u | --unmount [mount-point]'
        + separation of certain functions so they can be executed on its own, also for modularity
        + you can import the distribution framework on its own as though you are writing your own main function
        - Separation of Duty 
            - Ability to use the installation templates as a standalone framework
                + You can treat the main.py and runner.py launcher files as a separate component of the stack, with the distribution installers being the main framework/template containing the (post)installation functionalities
                - As such, you can also create your own main.py and runner.py components
                    - Important Setup Components
                        + setup.py : This generates the Setup class required to be parsed into the installer framework so that the installers know what to do, more information in [USAGE](USAGE.md) and [wiki](wiki.md)
                    - Engines
                        + main.py is the main launcher application that takes in the Setup class, as well as any other program features such as CLI
                        - app/runner.py is the 'Load Balancer' of the application, the distribution switcher that processes the target distribution you specified in the configuration file and 
                            + Imports the target distribution's installation classes appropriately
                            + You can make your own with this in mind

- New
    - Added folder 'docker' for storing docker-support files
        - Added document 'archlinux.Dockerfile' in 'docker' for creating a pre-defined ArchLinux chroot environment for installation by creating a docker container for each distribution (In case is necessary) with useful and essential packages
        - Added document 'debian.Dockerfile' in 'docker' for creating a pre-defined Debian chroot environment for installation by creating a docker container for each distribution (In case is necessary) with useful and essential packages
    - Added folder 'resources' to store all git documentation resources and files
        - Added folder 'demo' for storage of the Demo GIFs
    - Added new documents 
        - 'pkglist.txt' containing all system-related dependencies/packages
        - 'setup-debian.sh' and 'setup-archlinux.sh' in 'docker'
            - Shellscript to automatically startup the docker image of the respective chroot environments you wish to startup, and install the dependencies to prepare for use
            - Use this if you wish to use the official images and not the prebuilt Dockerfiles
        - Added a simple run.sh script to automate the process
        - Added document 'demo.md' showing Demo GIFs 

- Updates
    - Updated documents 
        - 'README.md'
            - Converted 'Information' from a block into sentences
            - Added additional dependencies
            - Added new pre-requisite: If you are using a non-ArchLinux distribution
            - Reorganized and placed pre-rquisite 'If you are using a non-ArchLinux distribution' above 'Install Dependencies'
            - Added additional packages to the mkarchroot corresponding to the depedencies when bootstrapping the root filesystem
            - Added 'git', 'arch-install-scripts', 'parted' into the bootstrap package list
            - Added instructions to install system dependencies from file 'pkglist.txt
            - Added 'python' to the existing python-related dependency installation instructions
            - Added documentation for new parameter '-u | --unmount' 
            - Added instructions on how to create a root filesystem chroot environment using docker
            - Added optional step for setting up the docker chroot environment if using the official images
            - Added basic docker setup instructions
            - Added steps for after initial startup of docker chroot environment
        - wiki.md
            - Added new section block 'Troubleshooting' in 'wiki.md' for all FAQ Errors and Troubleshooting issues
        - 'REFERENCES.md' in folder 'docs'
            - Added links
        - 'debian.Dockerfile' in 'docker'
            - Changed packages and dependencies
        - 'main.py' in 'src'
            - Added calling and runner support for new parameter '-u | --unmount' for Unmounting the drive from the mount points specified in the config file
        - 'runner.py' in 'src/app'
            - Removed select_Mirrors from the installation stages
        - 'cli.py' in 'src/lib'
            - Added CLI support for new parameter '-u | --unmount'
        - 'device_management.py' in 'src/lib'
            - Added a simple implementation of a blkid UUID reference function
            - Fixed import mistake
            - fixes to function 'get_block_Information()
        - 'process.py' in 'src/lib'
            - Changed result 'stdout' in function 'subprocess_Line()' to not take in from the process pipe instead
        - 'mechanism.py' in 'src/app/distributions/archlinux'
            - Added function 'check_package_manager_Configurations(self, mount_Dir)' to check for the package manager's configuration files (i.e. pacman.conf) because certain scenarios 
                - may cause pacstrap to generate a rootfs without pacman.conf
            - Added class variable 'package_manager_Configurations' to hold the package manager's configuration file default template
            - Added and tested package manager configuration file checking and validation for ArchLinux - in this case, /etc/pacman.conf - within the generated rootfs using pacstrap
                - If the bootstrapped root filesystem contents do not contain '/etc/pacman.conf', it will copy from the host
                - If the copy fails, it will generate from the package manager configuration file template string class variable in the Class
                    - Each distribution installer template will contain a different configuration file template
            - Filesystems table (fstab) file generator: replaced the usage of 'genfstab' with a implemented block function
            - Separated mounting functions into individual functions for better visibility
            - Rewrote UEFI checker to use python logic instead of ls
            - Created function for select_Mirrors
            - Removed select_Mirrors as a standalone stage, and instead, merged it with the package manager validation step before the bootstrapping stage
            - Converted genfstab subprocess operation from subprocess_Line => subprocess_Sync

- Plans
    - Removal of command string consolidation and return at the end of the system commands
        - The purpose was
            + After executing system shellscript commands, return the commands to the main presentation/business logic layer functions for archiving/writing to file
        + Attempting to remove writing function
        + to be redesigned and reimplemented later
    - Add mirrorlist selection function

- Testing
    - Installing using a non-ArchLinux system
         - Debian
    + Tested the (currently only) ArchLinux installation on both a native archlinux virtual machine on a virtual disk image : it installs and runs properly
    - Tested that on a debian virtual machine running an archlinux docker container as an ArchLinux chroot environment, that also has the disk to install on passthrough'd into the container. 
        + This one also works and installs similarly to a native system, except afew differences
    - Due to the nature of dependency on some bootstrappers 
        - i.e. archlinux's pacstrap requiring pacman to exist 
            + installing natively on a non-ArchLinux system is borderline impossible or unnecessarily hard

### 2024-01-29
#### 1026H
+ Version: v0.4.1

- Version Changes:
    + Preparation of project structure for packaging and deployment

- New
    + Created new package folder 'distinstall-python' in 'src/' for holding the program as a package
    + Created setup.py for setuptools
    + Added pyproject.toml for packaging
    - Added '__init__.py' and '__main__.py' to 'src/'
        - '__init__.py' will initialize the project folder as a importable package/module, like a constructor initializer
        - '__main__.py' is a special macro function that will act as an alias to main.py in python
            + Python will find '__main__.py' as the launcher/entry point, and if it is found, python will execute a special runtime instruction set for these magic functions
            + TODO: Find out how to set main.py as the entry point instead
    - Added '__init__.py' and '__main__.py' to 'src/app'
        - '__init__.py' will initialize the project folder as a importable package/module, like a constructor initializer

- Updates
    - 'mechanism.py' in 'src/app/distributions/archlinux'
        - Modified package/module importing in mechanism.py
            + Used '.' as a relative path backwards up the parent directory tree, with each '.' being 1 directory upwards
            + TODO: Figure out how to add the module directories into the packaging so that '.' isnt needed
        - Added variables 'stdout, stderr and returncode' to timedatectl function
        - Removed 'loading' message and the standard output print as these are too verbose
    - 'runner.py' in 'src/app'
        - Modified package/module importing
            + Used '.' as a relative path backwards up the parent directory tree, with each '.' being 1 directory upwards
            + TODO: Figure out how to add the module directories into the packaging so that '.' isnt needed
    - 'device_management.py' in 'src/lib'
        - Modified package/module importing
            + Used '.' as a relative path backwards up the parent directory tree, with each '.' being 1 directory upwards
            + TODO: Figure out how to add the module directories into the packaging so that '.' isnt needed
    - 'user_management.py' in 'src/lib'
        - Modified package/module importing
            + Used '.' as a relative path backwards up the parent directory tree, with each '.' being 1 directory upwards
            + TODO: Figure out how to add the module directories into the packaging so that '.' isnt needed
    - 'setup.py' in 'src/'
        - Modified package/module importing
            + Used '.' as a relative path backwards up the parent directory tree, with each '.' being 1 directory upwards
            + TODO: Figure out how to add the module directories into the packaging so that '.' isnt needed

#### 1758H
+ Version: v0.4.2

- Version Changes:
    - Migration
        + Moved project structure from 'src/' to folder 'src/distinstall-python' as a package

- Updates
    + Moved project structure from 'src/' to folder 'src/distinstall-python' as a package

### 2024-01-29
#### 1758H
+ Version: v0.4.3

- Version Changes:
    - Deleted
        + Deleted remnants after moving to package folder 'distinstall-python'

- Updates
    + Deleted remnants after moving to package folder 'distinstall-python'

#### 2227H
+ Version: v0.4.4

- Version Changes:
    - Documentations
        - README.md
            + Added instructions to install python using setuptools packaging and deployment (via pip)

- Updates
    - README.md
        + Added instructions to install python using setuptools packaging and deployment (via pip)

### 2024-01-30
#### 1358H
+ Version: v0.4.5

- Version Changes:
    - New Files
        + Added new document 'CONTRIBUTING.md' for information relating to contribution rulesets
    - Source Code
        + Updated 'setup.py' and 'pyproject.toml' with latest version and setup entry point
        + Updated 'main.py' to be in sync with '__main__.py'

- New
    - Added new document 'CONTRIBUTING.md' for information relating to contribution rulesets

- Updates
    - Updated 'setup.py' and 'pyproject.toml' with latest version and setup entry point
    - Updated 'main.py' to be in sync with '__main__.py'

### 2024-04-19
#### 1137H
- Updates
    - Updated document 'README.md'
        + Added steps to generate a virtual hard disk image using dd
    - Updated document 'CHANGELOGS.md'
        + Complete rewrite of the CHANGELOGS entry system to be more robust for documentation changes + non-bug fixes, feature changes or breaking changes
        + Modifying/refactoring changelogs to follow a date-time system over a version update

