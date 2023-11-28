# Distribution installer - Python reimplementation/re-write

## Information
```
This is a planned full rewrite of the distribution install script from the (previously) Bash shellscript implementation to using a proper programming/scripting language such as Python, Golang and potentially C (or Rust)

Currently, this rewrite is in python as it is a good language for prototyping and future planning. From here, I might be able to have an easier time rewriting from python to other programming languages like the aforementioned - golang and/or C
```

## Setup
### Dependencies
+ arch-install-scripts
+ dd
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

- Install dependencies
    - From requirements.txt
        ```console
        python -m pip install -Ur requirements.txt
        ```

- (Optional) If you are installing into a Virtual Disk Image on Host
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

## Documentation
### Synopsis/Syntax
- Basic Run
    ```console
    python main.py {options} <arguments> [positionals]
    ```

### Parameters
- Positionals
    + start : Confirm and Begin the installation
- Optionals
    - With Arguments
    - Flags

### Usage

### Developers
#### Dependencies and Importing
- Linux Distributions Module
    ```python
    import app.distributions as dist
    ```
- ArchLinux base installation mechanism
    ```python
    from app.distributions.archlinux import mechanism
    ```
- Setup file
    ```python
    from setup import Setup
    ```

## Wiki
### Project Structure
```
project-root/
    |
    |-- src/ : For all project-related files
        |
        |-- main.py  : The main runner/launcher project code
        |-- setup.py : Root setup file for the main runner/launcher
        |-- unittest.py : WIP Unit Testing source file
        |-- app/ : For all application-specific functionalities; Such as source files related to the installation mechanism of the various Distributions
            |
            |-- distributions/ : For all distribution classes
                |
                |-- archlinux/ : Contains ArchLinux installation functionality and archlinux-specific libraries
        |-- lib/ : For all external/general libraries that are not application-specific
```

## TODO
### Pipeline
+ [ ] Migration from Linux Bash Shellscript to Python
- [ ] Configuration File Handling and Support
    - [ ] Key-Values
        - [ ] user_ProfileInfo
            - [ ] Change ['secondary_Groups'] into a list instead of a standalone
        - [ ] Plan to rename "device_Type" into "storage_Controller" for a better, more accurate name, OR to add a separate group called "storage_Controller"
        - [ ] Change configuration naming scheme
    - [ ] Support for JSON
    - [ ] Support for segmented running - Running only specific steps at any one time
    - [ ] Support for different disk medium typings
        - [O] NVME : /dev/nvme[disk-number]p[partition-number]
        - [O] Loopback device : /dev/loop[loopback-number]p[partition-number]
- [ ] Planned Quality-of-Life changes
    - [ ] Improved Readability
        + [ ] Usage of proper data structure objects such as Dictionary for Key-value mappings and Lists for Arrays and iterative data objects
        + [ ] Rename YAML configuration file keyword naming convention
    - [ ] Improved portability, customizability and modularity
        + [ ] Configuration File I/O: Using YAML serialized data object for configuration file handling instead of shellscript sourcing (and potentially classic JSON support, as well as other configuration file types if enough support and works)
        + [ ] Convenience: Easier to perform rewrites (if necessary)
- [ ] Bug Fixes
    + [ ] Fixed technical terminologies and makes it easier to understand

