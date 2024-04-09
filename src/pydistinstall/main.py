"""
Distribution Installer ported to Python
"""
## Built-in
import os
import sys

## External Libraries
from pydistinstall.app import runner as app_runner
from pydistinstall.setup import Setup

def init():
    """
    Application Initialization
    """
    global setup, env, fmt_Text, cliparser, optionals, positionals

    # Initialize and setup class
    setup = Setup()
    setup.init_prog_Info("installer", "ArchLinux Profile Setup Installer", "Main", "v0.3.0", "DEBUG", "arch") # Initialize Program Information

    # Process CLI arguments
    fmt_Text = setup.fmt_Text
    cliparser = setup.cliparser
    env = setup.env
    optionals = cliparser.optionals
    positionals = cliparser.positionals

def init_Application():
    """ 
    Initialize Application class
    """
    global app
    # Initialize Class
    app = app_runner.App(setup.DISTRO, setup, env)

def display_info():
    """
    Print and display system information
    """
    print(f"""
    Running as  : {env.USER}
    Program Name: {setup.PROGRAM_NAME}
    Program Type: {setup.PROGRAM_TYPE}
    Distro: {setup.DISTRO}
    MODE: {setup.env.MODE}
          """)

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
            + -u [mount-point]      | --unmount     [mount-point]      : Unmount the drive from the mount points specified in the configuration file
            + --execute-stage [stage-number]                           : Specify an installation stage number to execute
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

    - Positional Parameters

Modes:
	+ DEBUG (Default) : Test install; Allows you to see all the commands that will be executed if you set the MODE to 'RELEASE'; set by default to prevent accidental reinstallation/overwriting
	+ RELEASE : Performs the real RELEASE; must use with sudo

Environment Variables:
    + TARGET_DISK_NAME : This is used in the environment variable to specify the target disk you want to install with
    + MODE : This indicates the execution permission of the application; Default: DEBUG; Set this to 'RELEASE' to begin and commit execution and changes to be made

Examples:
    - Generate configuration file
        python {cliparser.exec} --generate-config

    - Default (Test Install; Did not specify target disk name explicitly)
        python {cliparser.exec} start

    - Unmount the drive from the mount points specified in the configuration file
        sudo python {cliparser.exec} -u [root-mount-point]

    - Test Install; with target disk name specified as flag
        python {cliparser.exec} -d "/dev/sdX" start

    - Test Install; with target disk name specified with environment variable TARGET_DISK_NAME
        TARGET_DISK_NAME="/dev/sdX" python {cliparser.exec} start

    - Test Install; with custom configuration file
        python {cliparser.exec} -c "new config file" -d "/dev/sdX" start

    - Start installation (Did not specify target disk name explicitly)
        sudo python {cliparser.exec} -m RELEASE start

    - Start installation with the start mode specified with environment variable 'MODE'
        sudo MODE=RELEASE python {cliparser.exec} start

    - Start installation (with target disk name specified as flag)
        sudo python {cliparser.exec} -d "/dev/sdX" -m RELEASE start

    - Start installation (with target disk name specified with environment variable TARGET_DISK_NAME)
        sudo TARGET_DISK_NAME="/dev/sdX" python {cliparser.exec} -m RELEASE start

    - Start installation (with custom configuration file)
        sudo python {cliparser.exec} -c "new config file" -d "/dev/sdX" -m RELEASE start

    - List all installation stages
        sudo python {cliparser.exec} --list-stages

    - Execute specific stages
        sudo python {cliparser.exec} --execute-stage 1 --execute-stage 2 .... -m RELEASE

    - Open up fdisk for manual partition configuration
        sudo python {cliparser.exec} --fdisk

    - Open up fdisk for manual partition configuration
        sudo python {cliparser.exec} --cfdisk

    - Test Install; using Makefile
        make testinstall

    - Start installation; using Makefile
        sudo make install

    - Dis/Unmount using Makefile
        sudo make clean

    - Download the important files (i.e. installer and generate config files) using Makefile
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
    print("(S) Starting Initialization...")
    verify_Init()

    # Verify Environment Variables
    print("(+) Verifying Environment Variables...")
    verify_Env()

    # Initialize Application class after importing configurations
    init_Application()

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
        elif (curr_opt == "unmount"):
            if (curr_opt_val == True):
                # Get the specified mount point (if any)
                ## Check if 'Root' is in mount paths
                if "Root" in list(setup.cfg["mount_Paths"].keys()):
                    ## Root is specified
                    dir_Mount = setup.cfg["mount_Paths"]["Root"]
                else:
                    ## Root is not specified
                    dir_Mount = cliparser.configurations["optionals"]["ROOTFS_MOUNT_PATH"]

                print("Unmounting mount point [{}]...".format(dir_Mount))

                # Unmount the drive from the mount points specified in the configuration file
                result_code:int = os.system("umount -l {}".format(dir_Mount))
                if result_code == 0:
                    # Success
                    print("Mount point [{}] Unmounted.".format(dir_Mount))
                else:
                    # Error
                    print("Error encountered: result code = {}".format(result_code))
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
                    try:
                        # Get executing state name
                        exec_stage_Name = app.installation_stages[int(curr_stage_Number)]

                        # Execute in the launcher
                        print("Executing stage number: {} => {}".format(curr_stage_Number, exec_stage_Name))
                        app.update_setup()
                        app.execute_Step(curr_stage_Number)
                        print("")
                    except Exception as ex:
                        print("Exception: Error running stage {}".format(ex))

    ## Switch-case CLI positionals
    for i in range(len(positionals)):
        curr_pos = positionals[i]
        if (curr_pos == "start"):
            """
            Start the Installer
            """
            display_info()

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
    init()
    body()

if __name__ == "__main__":
    init()
    main()

