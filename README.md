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

### Quickstart Flow
#### Users
1. Perform setup
    - Create Virtual Environment
        ```console
        python3 -m venv env
        ```
    - Source and chroot into Virtual Environment
        - Linux
            ```console
            . env/bin/activate
            ```
        - Windows
            ```console
            .\env\Scripts\activate
            ```
    - Install dependencies
        ```console
        pip install -Ur requirements.txt
        ```
2. Change directory into application folder
    ```console
    cd src
    ```
3. Generate configuration file
    ```console
    python3 main.py --generate-config
    ```
4. Edit configuration file
    + Please refer to [USAGE.md](USAGE.md) for more information on customization
    + Under the 'customization' section
5. Perform a test run
    - Explanation
        + The Default mode is 'Debug', this will print the commands only
    - Perform full start
        ```console
        sudo python3 main.py start
        ```
    - Execute specific stages
        ```console
        sudo python3 main.py --execute-stage [stage-number]
        ```
6. Once you have confirmed
    - Explanation
        + To run the changes proper, you need to set the mode to RELEASE
    - Perform full start
        ```console
        sudo python3 main.py --mode RELEASE start
        ```
    - Execute specific stages
        ```console
        sudo python3 main.py --mode RELEASE --execute-stage [stage-number]
        ```

#### Developers
- To implement a new distribution installation step
    - Copy the template 'mechanism.py' from any of the 'src/app/distributions/[base-distribution-name]' to a test draft location
    - Edit accordingly
        - Please ensure that to maintain consistency, function names is adviced to be the same if the function already exists.
        - If the function didnt exist, then you may create a new function to be called as necessary

## Documentation
### Synopsis/Syntax
- Basic Run
    ```console
    {sudo} python main.py {options} <arguments> [positionals]
    ```

### Parameters
- Positionals
    + start : Confirm and Begin the installation
- Optionals
    - With Arguments
        + `--execute-stage [stage-number]` : Specify a target installation stage number to execute and executes it; You can append this option to execute all the steps in chronological order
        + `-m | --mode [DEBUG|RELEASE]` : Explicitly specify the program run mode; Default: DEBUG; Set this to 'RELEASE' to allow changes to be made; You can also set the Environment Variable 'MODE' to 'RELEASE'.
    - Flags

### Usage

### Notes
+ For more information on usage and customization, please refer to [USAGE.md](USAGE.md)

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

