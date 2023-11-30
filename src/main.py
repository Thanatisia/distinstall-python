"""
Distribution Installer ported to Python
"""
## Built-in
import os
import sys

## External Libraries
import app.runner as app_runner
from setup import Setup

def init():
    """
    Application Initialization
    """
    global setup, app, env, fmt_Text, cliparser, optionals, positionals

    # Initialize and setup class
    setup = Setup()
    setup.init_prog_Info("installer", "ArchLinux Profile Setup Installer", "Main", "v1.4.0", "DEBUG", "arch") # Initialize Program Information

    # Process CLI arguments
    fmt_Text = setup.fmt_Text
    cliparser = setup.cliparser
    env = setup.env
    optionals = cliparser.optionals
    positionals = cliparser.positionals
    
    # Application class
    app = app_runner.App(setup.DISTRO, setup, env)

def display_help():
    """
    Display help message

    - Message Contents
        + Syntax/Synopsis
        + CLI Arguments/Parameters
    """
    help_msg = f"""
Running as      : {env.USER}
Script Name     : {setup.PROGRAM_SCRIPTNAME}
Program Name    : {setup.PROGRAM_NAME}
Program Version : {setup.PROGRAM_VERSION}

Synopsis/Syntax:
    {cliparser.exec} <options> [positional] <arguments>

Command Line (CLI) Arguments:
    - Optional Parameters
        - With Arguments
            + -c [config-file-name] | --config      [config-file-name] : Set custom configuration file name
            + -d [target-disk-name] | --target-disk [target-disk-name] : Set target disk name
            + -e [default-editor]   | --editor      [default-editor]   : Set default text editor
            + -m [DEBUG|RELEASE]    | --mode        [DEBUG|RELEASE]    : Set mode (DEBUG|RELEASE)
            + --execute-stage [stage-number]                           : Specify an installation stage number to execute
        - Flags
            + -g | --generate-config    : Generate configuration file
            + --print-config            : Import configuration file, load it and print contents
            + -h | --help               : Display this help menu and all commands/command line arguments
            + --fdisk                   : Open up fdisk for manual partition configuration
            + --cfdisk                  : Open up cfdisk for manual partition configuration
            + --list-stages             : List all installation steps/stages of the target platform to install

    - Positional Parameters
        + start : Start the installer

Modes:
	+ DEBUG (Default) : Test install; Allows you to see all the commands that will be executed if you set the MODE to 'RELEASE'; set by default to prevent accidental reinstallation/overwriting
	+ RELEASE : Performs the real RELEASE; must use with sudo

Environment Variables:
	+ TARGET_DISK_NAME : This is used in the environment variable to specify the target disk you want to install with

Examples:
    1. Default (Test Install; Did not specify target disk name explicitly)
        {cliparser.exec} start

    2. Test Install; with target disk name specified as flag
        {cliparser.exec} -d "/dev/sdX" start

    3. Test Install; with target disk name specified with environment variable TARGET_DISK_NAME
        TARGET_DISK_NAME="/dev/sdX" {cliparser.exec} start

    4. Test Install; with custom configuration file
        {cliparser.exec} -c "new config file" -d "/dev/sdX" start

    5. Start installation (Did not specify target disk name explicitly)
        sudo {cliparser.exec} -m RELEASE start

    6. Start installation (with target disk name specified as flag)
        sudo {cliparser.exec} -d "/dev/sdX" -m RELEASE start

    7. Start installation (with target disk name specified with environment variable TARGET_DISK_NAME)
        sudo TARGET_DISK_NAME="/dev/sdX" {cliparser.exec} -m RELEASE start

    8. Start installation (with custom configuration file)
        sudo {cliparser.exec} -c "new config file" -d "/dev/sdX" -m RELEASE start

    9. Open up fdisk for manual partition configuration
        sudo {cliparser.exec} --fdisk

    10. Open up fdisk for manual partition configuration
        sudo {cliparser.exec} --cfdisk

    11. Test Install; using Makefile
        make testinstall

    12. Start installation; using Makefile
        sudo make install

    13. Dis/Unmount using Makefile
        sudo make clean

    14. Download the important files (i.e. installer and generate config files) using Makefile
        sudo make genscript
    """
    print(help_msg)

def display_Options():
    print("Optionals: ")
    for k,v in optionals.items():
        curr_opt = k
        curr_val = v
        print("\t{} = {}".format(curr_opt, curr_val))

    print("")

    print("Positionals: ")
    for i in range(len(positionals)):
        curr_pos = positionals[i]
        print("\t{}: {}".format(i, curr_pos))

def verify_Init():
    """
    Perform distribution installer pre-processing and pre-startup check
    """
    # Get custom configuration file name (if any)
    cfg_name = cliparser.configurations["optionals"]["CUSTOM_CONFIGURATION_FILENAME"]

    # Check if configuration file exists
    if os.path.isfile(cfg_name):
        # File exists

        # Import Configuration File
        print("(+) Import Configuration File")
        setup.cfg = setup.load_config(cfg_name)
    else:
        setup.generate_config_Raw(cfg_name)
        print("please modify the variables and rerun the program again, thank you!")
        exit(1)

    # Initialize Variables
    setup.init_Variables()

def verify_Env():
    """
    Verify Environment Variables
    """
    # Check if environment variables are empty
    disk_Label = env.TARGET_DISK_NAME
    if disk_Label == "":
        # If the target disk name/label (i.e. /dev/sdX) is empty
        while disk_Label == "":
            ## While the device is still empty
            print("(-) TARGET_DISK_NAME not set")

            ## Get user input
            disk_Label = input("Please indicate the target disk's name/label (i.e. /dev/sdX for SATA, /dev/nvme0np1 for NVME (still in trial)): ")

        print("(+) Target disk set to {}".format(disk_Label))

        # Set target disk name to configuration set
        setup.cfg["disk_Label"] = disk_Label

def begin_installer():
    """
    Begin installation process
    """
    app.update_setup()
    app.begin()

def body():
    """
    Begin CLI argument processing
    """
    # Initialize and perform pre-processing and pre-startup checks
    print(f"""
(S) Starting Initialization...
    Running as  : {env.USER}
    Program Name: {setup.PROGRAM_NAME}
    Program Type: {setup.PROGRAM_TYPE}
    Distro: {setup.DISTRO}
    MODE: {setup.env.MODE}
          """)
    verify_Init()

    print("")

    # Verify Environment Variables
    print("(+) Verifying Environment Variables...")
    verify_Env()

    # Initialization Completed
    print("(D) Initialization completed")
    print("")

    ## Switch-case CLI optionals
    for k,v in optionals.items():
        # Get keyword and value
        curr_opt = k
        curr_opt_val = v

        # Process and check
        if (curr_opt == "help"):
            if (curr_opt_val == True):
                display_help()
                display_Options()
                exit(1)
        elif (curr_opt == "display-options"):
            if (curr_opt_val == True):
                display_Options()
                exit(1)
        elif (curr_opt == "generate-config"):
            if (curr_opt_val == True):
                # Get the new custom configuration file name (if any)
                cfg_name = cliparser.configurations["optionals"]["CUSTOM_CONFIGURATION_FILENAME"]
                setup.generate_config_Raw(cfg_name)
                exit(1)
        elif (curr_opt == "print-config"):
            if (curr_opt_val == True):
                # Get the new custom configuration file name (if any)
                cfg_name = cliparser.configurations["optionals"]["CUSTOM_CONFIGURATION_FILENAME"]

                # Import configuration file, load it and print
                setup.cfg = setup.load_config(cfg_name)

                # Print out configuration dictionary object
                for k,v in setup.cfg.items():
                    print("{} : {}".format(k,v))
                exit(1)
        elif (curr_opt == "list-stages"):
            if (curr_opt_val == True):
                app.list_steps()
                exit(1)
        elif (curr_opt == "MODE"):
            if (curr_opt_val != None):
                # Get the new mode (if any)
                new_mode = cliparser.configurations["optionals"]["MODE"]

                # Set the new mode into the Environment Variable class variable
                setup.env.MODE = new_mode
        elif (curr_opt == "STAGES"):
            """
            Execute the specific stage
            """
            if (curr_opt_val != None):
                # Get the list of stages to execute
                target_stages = cliparser.configurations["optionals"]["STAGES"]

                # Loop through list of stages
                for curr_stage_Number in target_stages:
                    # Execute in the launcher
                    print("Executing stage number: {}".format(curr_stage_Number))
                    app.update_setup()
                    app.execute_Step(curr_stage_Number)
                    print("")

    ## Switch-case CLI positionals
    for i in range(len(positionals)):
        curr_pos = positionals[i]
        if (curr_pos == "start"):
            """
            Start the Installer
            """
            print("")
            print("(+) Beginning Installation...")
            print("")

            if env.USER == "root":
                ## Running as super user
                ### Start the main Installer
                begin_installer()
            else:
                ## Not running as super user
                print("")
                print("\t(X) Please run the application as super user via sudo")
                print("")

def main():
    body()

if __name__ == "__main__":
    init()
    main()
