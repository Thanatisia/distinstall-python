# CHANGELOGS

## Table of Contents
- Entries
    > [version] | [date] [time] | [status]
    + v0.1.0 | 2023-09-26 1604H | Merged to main
    + v0.1.1 | 2023-09-26 2223H | Merged to main
    + v0.1.2 | 2023-09-27 1416H | Development

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

### v0.1.2
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
    - setup.py
        + initialized class 'lib/env.Environment()' to be used as a global reference variable during runtime.
        + Updated init_prog_Info() to have a default value of retrieving from 'env.MODE' (which takes from the environment variable 'MODE') if parameter 'program_MODE' is not specified.
    - archlinux
        - mechanism.py
            + Added function 'print_configurations'
            + Wrapped the constructor lines into a standalone event update function 'update_setup'
    - lib
        - cli.py
            + Added support for CLI optional argument ['--display-options'] to display options only

