# py-unidist

## Information
### Description
+ A Universal Distribution Install library/framework written in Python
- This package contains
    - working pre-made script for installing distributions
        - Currently supported systems
            + ArchLinux
    + modules for installing/setting up the base/root filesystem of various distributions/systems using bootstrap installation

+ ![py-distinstall full demo](resources/demo/demo-archlinux-full.gif)

### Project
+ Package Name: py-unidist
+ Current Version: v0.4.5

### Timeline
+ The project has went through various major checkpoints and changes including rewriting from the original [Bash shellscript implementation - distro-installscript-arch](https://github.com/Thanatisia/distro-installscript-arch) as a standalone ArchLinux base filesystem installer via bootstrap installation
+ In the midst of improving the project, I realised that the installation flow at times can be quite similar, it might work as a library/framework.
- Additionally, at about that period, I felt that this deserves to be written in a proper programming language (such as Python, Golang, Rust etc) if it helps with scalability
    + Because I was using Python more often during that period, I went with Python

## Setup
### Dependencies
- pacman
- parted
- arch-install-scripts
    + pacstrap
+ dd
+ dhcpcd
+ python
- python pypi packages
    + ruamel.yaml : For YAML configuration file handling

### Pre-Requisites
- (Optional; Recommended) Setup python Virtual Environment
    - Install dependencies
        + venv/virtualenv
    - Generate virtual environment
        ```console
        python -m venv [virtual-environment]
        ```
    - Chroot/Source the virtual environment
        - *NIX
            ```console
            . [virtual-environment]/bin/activate
            ```
        - Windows
            ```console
            [virtual-environment]\Scripts\activate
            ```

- (Optional) Performing within a non-ArchLinux system
    - Create a chroot environment with pacman/for ArchLinux
        - Using 'archlinux/devtools'
            - Dependencies
                - [archlinux/devtools](https://gitlab.archlinux.org/archlinux/devtools) : Tools for Archlinux package maintainers
                
            - Make your chroot folder to store the chroot root environment
                ```console
                mkdir chroots
                ```

            - Create the actual chroot directory within it
                - Using mkarchroot
                    - Explanation
                        - mkarchroot will 
                            + create the actual chroot environment - named 'root' - within the folder 'chroots'
                            - Afterwhich, the packages and package groups specified - in this case, 'base' - will be bootstrapped and installed into the chroot environment's filesystem
                                + 'base' is the package group that contains the root filesystem, this is necessary to make a working environment
                    ```console
                    mkarchroot chroots/root base base-devel git arch-install-scripts parted vim dhcpcd python3 python-pip python-ruamel-yaml
                    ```

            - Edit the mirrorlist within the chroot environment to facilitate the downgrade
                - Explanation
                    - Write the line 'Server = https://archive.archlinux.org/repos/[year]/[month]/[date]/$repo/os/$arch' into the mirrorlist of the chroot environment
                        - where
                            + year = the year of the repository; i.e. 2016
                            + month = the month of the repository; i.e. 02 = February
                            + date = the date of the repository; i.e. 19
                ```console
                echo 'Server = https://archive.archlinux.org/repos/[year]/[month]/[date]/$repo/os/$arch' > [chroot-environment-path]/root/etc/pacman.d/mirrorlist
                ```

            - Enter the chroot environment
                - Explanation
                    + This is just basically chroot (Change root)-ing into the newly create ArchLinux filesystem chroot environment as per normal
                    - However, in this example
                        - We will be using 'arch-chroot' which can be found in the ArchLinux package 'arch-install-scripts' which is effectively a wrapper that 
                            + performs several mounts before chroot is ran
                ```console
                sudo arch-chroot [chroot-environment-path]/root [shell]
                ```

        - Using docker
            - Setup
                - Dependencies
                    + docker
                    + (Optional) docker-compose
                - Add your user into the 'docker' group to be able to use docker-compose and docker functionalities
                    ```console
                    sudo usermod -aG docker [username]
                    ```
                - Restart your system to refresh the permission
                    ```console
                    sudo reboot now
                    ```
            - Pull latest archlinux image
                ```console
                docker pull archlinux:latest
                ```
            - (Optional) Use the Dockerfile created with the proper packages pre-defined
                - Information
                    + Located in the folder [docker](docker)
                - Build the Dockerfile of your choice
                    ```console
                    docker build -t [tag] -f docker/[dockerfile-of-choice] [context-directory]
                    ```
            - Startup a container
                - Using docker run
                    - Explanation
                        - Startup an ArchLinux docker container with the name 'arch-chroot'
                            - Enable privileged mode so that 
                                - the device can be passthrough from host into the container and
                                - the passthrough devices can be modified, and used
                            - Adding/Passthrough the disk/devices to container
                                - Examples
                                    - SATA/AHCI
                                        ```console
                                        --device=/dev/sdX
                                        ```
                                    - NVME
                                        ```console
                                        --device=/dev/nvme[device-number]
                                        ```
                                    - Loopback Device
                                        ```console
                                        --device=/dev/loop[device-number]
                                        ```
                                ```console
                                --device=[disk-label]
                                ```
                            - Mount the following volumes from the host system to the container
                                - [host-system-source-volume] => [container-destination-volume]
                                    - Mounting disk/devices from host system into container
                                        - Use-Case:
                                            + Useful for using the container rootfs environment as a temporary chroot environment to install a distribution via command line using bootstrapping (ArchLinux style)
                                        + Structure: `[host-target-disk-label] => [container-disk-label]`
                                        - (Optional) Mount distinstall-python repository from the host system to the container (if it already exists and you want to use that)
                                            ```console
                                            -v "/path/to/distinstall-python:/tmp/distinstall-python"
                                            ```
                            - Set the network mode to "host"
                                - So that the container is using the host's network address for consistency whilst formatting and bootstrapping
                        - Parameters
                    ```console
                    docker run -itd --name=arch-chroot --privileged --device=[disk-label] "/path/to/distinstall-python:/tmp/distinstall-python" --network=host {other-options} archlinux:latest
                    ```
            - Chroot (Change root) into the container
                ```console
                docker exec -it [container-name] [shell]
                ```
            - (Optional) If you are using the default official image(s)
                - ArchLinux
                    ```console
                    docker exec -it [container-name] /bin/bash -c "pacman -Syu && pacman -S base-devel git arch-install-scripts parted vim dhcpcd python3 python-pip python-ruamel-yaml"
                    ```
                - Debian
                    ```console
                    docker exec -it [container-name] /bin/bash -c "apt update -y && apt upgrade -y && apt install -y base-devel git arch-install-scripts parted vim dhcpcd python3 python-pip python-ruamel-yaml"
                    ```
            - After initial startup 
                - Explanation
                    + If you did not remove the container, you can just start the container back up after every restart if you require the chroot environment
                - Start up the container
                    ```console
                    docker start [container-name]
                    ```

        - In the chroot environment
            - Update accordingly
                ```console
                pacman -Syu
                ```

- Install system dependencies
    - From pkglist
        - If using pacman
            ```console
            pacman -S - < pkglist.txt
            ```
        - If using apt
            ```console
            apt install < pkglist.txt
            ```

- (Optional) If you are installing into a Virtual Disk Image on Host
    - Create a Virtual Hard Disk image
        - Explanation
            - Parameters
                - Positionals
                    - path-to-virtual-hard-disk-img : This specifies the output file to create
                - Options
                    - bs : This contains the size (in bytes) of each block that dd will read each time
                    - count : This specifies the number of counts to write each block in the Virtual Disk
            - Therefore, to create a VHD of size 56gb
                - Options
                    - bs = 1G
                    - count = 56
                - 1G * 56 = 56Gb
        ```console
        dd if=/dev/zero of=[path-to-virtual-hard-disk-img] bs=[block-size (bytes-per-block)] count=[number-of-counts]
        ```
    - Mount Disk Image and Partitions as loopback devices
        - Using losetup
            - Pre-Requisites
                + losetup
            - Explanation
                - Parameters
                    + -P
                    + -f : Print the first available loop device
            ```console
            sudo losetup -Pf [path-to-virtual-hard-disk-img]
            ```

### Installation
- Using python pip
    - Install git package
        - From GitHub
            ```bash
            python3 -m pip install git+https://github.com/Thanatisia/py-unidist{@[branch-tag-name]}
            ```
        - From requirements.txt
            - Prepare requirements.txt file
                ```
                distinstall-python @ git+https://github.com/Thanatisia/py-unidist{@[branch-tag-name]}
                ```
            - (Optional) Install requirements.txt
                ```bash
                python3 -m pip install -Ur requirements.txt
                ```

    - Manually via cloning
        - Clone git repository
            ```bash
            git clone https://github.com/Thanatisia/py-unidist
            ```
        - Change directory into project root
            ```bash
            cd py-unidist
            ```
        - (Optional) Install python dependencies
            ```bash
            python3 -m pip install -Ur requirements.txt
            ```
        - Install package as development mode
            ```bash
            pip install .
            ```
        - (Optional) Uninstall package
            ```bash
            pip uninstall py-unidist
            ```

### Compiling into an executable
> Still undergoing tests
- Using PyInstaller
    - Pre-Requisites
        - Dependencies
            - Python package
                + pyinstaller
    - Compile/Build the executable
        - Parameters
            + --onefile : Generate a single executable file with everything bundled inside
        - Notes
            - Output: 
                + dist: The executable will be placed here
        - Syntax
            ```console
            {python -m} pyinstaller --onefile [main-driver-file]
            ```
        - Usage
            ```console
            {python -m} pyinstaller --onefile main.py
            ```

### Quickstart Flow
#### Users
1. Perform setup
    - Create Virtual Environment
        ```console
        python3 -m venv [virtual-environment-name]
        ```
    - Source and chroot into Virtual Environment
        - Linux
            ```bash
            . [virtual-environment-name]/bin/activate
            ```
        - Windows
            ```bash
            .\[virtual-environment-name]\Scripts\activate
            ```
    - Install dependencies
        ```console
        pip install -Ur requirements.txt
        ```
1. Installing package
    + Follow the steps in [Installation](#installation) to install the package

2. Generate configuration file
    ```console
    py-distinstall --generate-config
    ```
3. Edit configuration file
    + Please refer to [USAGE.md](USAGE.md) for more information on customization
    + Under the 'customization' section
4. Perform a test run
    - Explanation
        + The Default mode is 'Debug', this will print the commands only
    - Perform full start
        ```console
        sudo py-distinstall start
        ```
    - Execute specific stages
        ```console
        sudo py-distinstall --execute-stage [stage-number]
        ```
5. Once you have confirmed
    - Explanation
        + To run the changes proper, you need to set the mode to RELEASE
    - Perform full start
        ```console
        sudo py-distinstall --mode RELEASE start
        ```
    - Execute specific stages
        ```console
        sudo py-distinstall --mode RELEASE --execute-stage [stage-number]
        ```

#### Developers
- To implement a new distribution installation step
    - Make directory for the new base distribution
        ```bash
        mkdir -pv src/pydistinstall/app/distributions/[new-base-distribution-name]
        ```
    - Copy the template 'mechanism.py' from any of the 'src/pydistinstall/app/distributions/[base-distribution-name]' to a test draft location
        ```bash
        cp -r src/pydistinstall/app/distributions/[base-distribution-name] src/pydistinstall/app/distributions/[new-base-distribution-name]
        ```
    - Edit accordingly
        + Please ensure that to maintain consistency, function names is adviced to be the same if the function already exists.
        + If the function didnt exist, then you may create a new function to be called as necessary

## Documentation
### Synopsis/Syntax
- Basic Run
    ```console
    {sudo} py-distinstall {options} <arguments> [positionals]
    ```

### Parameters
- Positionals
- Optionals
    - With Arguments
        + `-c [config-file-name] | --config      [config-file-name]` : Set custom configuration file name
        + `-d [target-disk-name] | --target-disk [target-disk-name]` : Set target disk name
        + `-e [default-editor]   | --editor      [default-editor]`   : Set default text editor
        + `-m [DEBUG|RELEASE]    | --mode        [DEBUG|RELEASE]`    : Set mode (DEBUG|RELEASE)
        + `-u [mount-point]      | --unmount     [mount-point]`      : Unmount the drive from the mount points specified in the configuration file
        + `--execute-stage [stage-number]`                           : Specify an installation stage number to execute
    - Flags
        + --display-options         : Display all options
        + -g | --generate-config    : Generate configuration file
        + --print-config            : Import configuration file, load it and print contents
        + -h | --help               : Display this help menu and all commands/command line arguments
        + --fdisk                   : Open up fdisk for manual partition configuration
        + --cfdisk                  : Open up cfdisk for manual partition configuration
        + --list-stages             : List all installation steps/stages of the target platform to install
        + -v | --version            : Display system version information
        + start                     : Start the full base installer + post-installer process

### Modes
+ DEBUG (Default) : Test install; Allows you to see all the commands that will be executed if you set the MODE to 'RELEASE'; set by default to prevent accidental reinstallation/overwriting
+ RELEASE : Performs the real RELEASE; must use with sudo

### Environment Variables
+ TARGET_DISK_NAME : This is used in the environment variable to specify the target disk you want to install with
+ MODE : This indicates the execution permission of the application; Default: DEBUG; Set this to 'RELEASE' to begin and commit execution and changes to be made

### Usage
- Generate configuration file
    ```console
    py-distinstall --generate-config
    ```

- Default (Test Install; Did not specify target disk name explicitly)
    ```console
    sudo py-distinstall start
    ```

- Unmount the drive from the mount points specified in the configuration file
    ```console
    sudo py-distinstall -u [root-mount-point]
    ```

- Test Install; with target disk name specified as flag
    ```console
    sudo py-distinstall -d "/dev/sdX" start
    ```

- Test Install; with target disk name specified with environment variable TARGET_DISK_NAME
    ```console
    sudo TARGET_DISK_NAME="/dev/sdX" py-distinstall start
    ```

- Test Install; with custom configuration file
    ```console
    sudo py-distinstall -c "new config file" -d "/dev/sdX" start
    ```

- Start installation (Did not specify target disk name explicitly)
    ```console
    sudo py-distinstall -m RELEASE start
    ```

- Start installation with the start mode specified with environment variable 'MODE'
    ```console
    sudo MODE=RELEASE py-distinstall start
    ```

- Start installation (with target disk name specified as flag)
    ```console
    sudo py-distinstall -d "/dev/sdX" -m RELEASE start
    ```

- Start installation (with target disk name specified with environment variable TARGET_DISK_NAME)
    ```console
    sudo TARGET_DISK_NAME="/dev/sdX" py-distinstall -m RELEASE start
    ```

- Start installation (with custom configuration file)
    ```console
    sudo py-distinstall -c "new config file" -d "/dev/sdX" -m RELEASE start
    ```

- List all installation stages
    ```console
    sudo py-distinstall --list-stages
    ```

- Execute specific stages
    ```console
    sudo py-distinstall --execute-stage 1 --execute-stage 2 .... -m RELEASE
    ```

- Open up fdisk for manual partition configuration
    ```console
    sudo py-distinstall --fdisk
    ```

- Open up fdisk for manual partition configuration
    ```console
    sudo py-distinstall --cfdisk
    ```

### Notes
+ For more information on usage and customization, please refer to [USAGE.md](USAGE.md)

## Wiki

### Project Structure
```
project-root/
    |
    |-- src/ : For all project-related files
        |
        |-- pydistinstall/ : Main package
            |
            |-- main.py  : The main runner/launcher project code
            |-- setup.py : Root setup file for the main runner/launcher
            |-- unittest.py : WIP Unit Testing source file
            |-- app/ : For all application-specific functionalities; Such as source files related to the installation mechanism of the various Distributions
                |
                |-- runner.py : This is the Distribution Switcher ("Load Balancer") that will process your target distribution name and separate to the appropriate distributions
                |-- distributions/ : For all distribution classes
                    |
                    |-- archlinux/ : Contains ArchLinux installation functionality and archlinux-specific libraries
                        |
                        |-- mechanism.py : The primary library containing the Base Installation and Post-Installation mechanism classes for the distribution
            |-- lib/ : For all external/general libraries that are not application-specific
                |
                |-- cli.py : This contains functionality to Command Line Interface (CLI) Argument handling
                |-- config_handler.py : This contains functionality to handling Configuration Files
                |-- const.py : This contains constant variables and values
                |-- device_management.py : This contains Device and Disk Handling functions
                |-- env.py : This contains Environment Variables
                |-- format.py : This contains string formatting support
                |-- process.py : This contains Subprocess and systems command execution functions
                |-- user_management.py : This contains User management functionalities
                |-- utils.py : This contains general utilities
```

## TODO
### Pipeline
+ [ ] Migration from Linux Bash Shellscript to Python
- [ ] Configuration File Handling and Support
    - [ ] Key-Values
        - [X] user_ProfileInfo
            - [X] Change ['secondary_Groups'] into a list instead of a standalone
        - [X] Plan to rename "device_Type" into "storage_Controller" for a better, more accurate name, OR to add a separate group called "storage_Controller"
        - [ ] Change configuration naming scheme
    - [ ] Support for JSON
    - [X] Support for segmented running - Running only specific steps at any one time
    - Support for different disk medium typings
        - [X] NVME : /dev/nvme[disk-number]p[partition-number]
        - [X] Loopback device : /dev/loop[loopback-number]p[partition-number]
- [ ] Planned Quality-of-Life changes
    - [ ] Improved Readability
        + [ ] Usage of proper data structure objects such as Dictionary for Key-value mappings and Lists for Arrays and iterative data objects
        + [ ] Rename YAML configuration file keyword naming convention
    - [ ] Improved portability, customizability and modularity
        + [ ] Configuration File I/O: Using YAML serialized data object for configuration file handling instead of shellscript sourcing (and potentially classic JSON support, as well as other configuration file types if enough support and works)
        + [ ] Convenience: Easier to perform rewrites (if necessary)
        + [ ] Easier distribution methods - i.e. Compilation into binary using compilers for python like pyinstaller
- [ ] Bug Fixes
    + [ ] Fixed technical terminologies and makes it easier to understand
- [ ] Refactoring
    + Remake the main CLI utility entry point to be less messy

