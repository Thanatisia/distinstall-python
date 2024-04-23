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

