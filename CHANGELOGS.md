# CHANGELOGS

## Table of Contents
- Entries
    > [version] | [date] [time] | [status]
    + v0.1.0 | 2023-09-26 1604H | Merged to main
    + v0.1.1 | 2023-09-26 2223H | Merged to main
    + v0.2.0 | 2023-09-27 2106H | Development

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
    - began standardization of 
        + environment variables retrieval to be set in 'lib/env.py'
        + global constants to be set in 'lib/const.py'
    - README.md
        - Updated TODO list with new tasks: 
            + configuration file handling and support
            + Rename YAML configuration file keyword naming convention
    - main.py
        + Changed initialization of class 'env.Environment()' => setup.env : Referencing of the environment class variable from 'setup.py' so that everything is in one location (unless otherwise required/specified)
        + Fixed header message: Removed quotation marks at the end
        + Utilised 'update_setup()' just before starting the installer function to update the class variables
        + Added testing user validation and cleanup
        + Added implementation of ['-m', '--mode'] CLI options in the processing of the parsed arguments in the body
    - setup.py
        + initialized class 'lib/env.Environment()' to be used as a global reference variable during runtime.
        + Updated init_prog_Info() to have a default value of retrieving from 'env.MODE' (which takes from the environment variable 'MODE') if parameter 'program_MODE' is not specified.
        + Removed program_Mode parameter checking and set it to as-is
    - archlinux
        + Performing initial workflow fix
        - mechanism.py
            + Added function 'print_configurations'
            + Wrapped the constructor lines into a standalone event update function 'update_setup'
            - Fixes
                + Added '.items()' behind partition_Scheme in line 247 and line 314
                - Replaced unsetting via '= None' (Wrong) => using .pop (Correct)
                    + Unsetting doesnt remove thee index, only remove the value and set it as None/Null
            + Added the return element 'resultcode' to every subprocess the process function requires
            + Removed any error messages via bash 'echo' command and through native python via print
    - lib
        - cli.py
            + Added support for CLI optional argument ['--display-options'] to display options only
            + Updated value of configurations keyword 'MODE' to a default value of 'DEBUG'
        - env.py
            + Added environment variables 'USER' and 'SUDO_USER' for user run validation
        - process.py
            + Updated functions subprocess_Line and subprocess_Sync to return the result/exit/status code

