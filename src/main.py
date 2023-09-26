"""
Distribution Installer ported to Python
"""
## Built-in
import os
import sys

## External Libraries
import app.distributions as dist
from app.distributions.archlinux import mechanism
from setup import Setup
from lib.env import Environment

def init():
    """
    Application Initialization
    """
    global setup, installer_archlinux, env, fmt_Text, optionals, positionals

    # Initialize and setup class
    setup = Setup()
    env = Environment()
    setup.init_prog_Info("installer", "ArchLinux Profile Setup Installer", "Main", "v1.4.0", "DEBUG", "ArchLinux") # Initialize Program Information
    installer_archlinux = mechanism.ArchLinux(setup) # Import the distribution of choice's installation mechanism

    # Process CLI arguments
    fmt_Text = setup.fmt_Text
    cliparser = setup.cliparser
    optionals = cliparser.optionals
    positionals = cliparser.positionals

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

def init_check():
    """
    Perform distribution installer pre-processing and pre-startup check
    """
    print(f"""
(S) Starting Initialization..."
    Program Name: {setup.PROGRAM_NAME}"
    Program Type: {setup.PROGRAM_TYPE}"
    Distro: {setup.DISTRO}"
          """)

    # Check if configuration file exists
    if os.path.isfile(setup.cfg_name):
        # File exists
        # Import Configuration File
        print("Import Configuration File")
    else:
        setup.generate_config()
        print("please modify the variables and rerun the program again, thank you!")
        exit(1)

    # Initialize Variables
    setup.init_Variables()

    print("")

    print("(+) Verifying Environment Variables...")

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

    print("")

    print("(D) Initialization completed")

def begin_installer():
    """
    Begin installation process
    """
    # installer_archlinux.installer()

def body():
    """
    Begin CLI argument processing
    """
    ## Switch-case CLI positionals
    for i in range(len(positionals)):
        curr_pos = positionals[i]
        if (curr_pos == "start"):
            """
            Start the Installer
            """
            print(fmt_Text.processing("Starting installation process", delimiter="- "))

            print("")

            # Initialize and perform pre-processing and pre-startup checks
            init_check()

            # Start the main Installer
            begin_installer()

def main():
    display_Options()

    print("")

    body()

if __name__ == "__main__":
    init()
    main()
