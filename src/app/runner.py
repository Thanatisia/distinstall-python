"""
Main runner for the distribution installation functionality
"""
## Built-in
import os
import sys

## External Libraries
from app.distributions.archlinux import mechanism
from lib import process

class App():
    def __init__(self, distribution_Name, setup, env):
        # Initialize Variables
        self.dist = distribution_Name
        self.supported_distributions = {
            "arch" : ["arch", "ArchLinux"],
        }
        self.setup = setup # Initialized Setup configurations
        self.env = env # Initialized Environment Variables
        self.installer = None # Variable to be substituted as the main installer mechanism depending on the distribution specified
        self.postinstaller = None # Variable to be substituted as the post installation mechanism depending on the distribution specified
        self.installation_stages = {
            1 : "Verify Network",
            2 : "Verify Boot Mode",
            3 : "Update System Clock",
            4 : "Disk Partition Management",
            5 : "Disk Mounting",
            6 : "Root filesystem Bootstrap Packaging",
            7 : "Filesystems Table (/etc/fstab) generating",
            8 : "System chroot execution",
            9 : "Post-Installation",
            10 : "Post-Installation Cleanup and Sanitization",
        }

        # Obtain parameters
        self.set_distribution_Name()
        setup.DISTRO = self.dist

        # Initialize Class
        self.platform_Select()
        self.installer_switch()

    def set_distribution_Name(self):
        """
        Get specified distribution from the configuration file
        """
        # Check if 'distribution-name' is in configuration file
        if ("distribution-name" in self.setup.cfg):
            # Check if 'distribution-name' is empty and value is in the dictionary of supported distributions
            if (self.setup.cfg["distribution-name"] != "") and (self.setup.cfg["distribution-name"] in list(self.supported_distributions.keys())):
                # Distribution is accepted
                self.dist = self.setup.cfg["distribution-name"]
            else:
                # Invalid Distribution
                print("Invalid distribution: {}".format(self.setup.cfg["distribution-name"]))
                print("Please specify a valid distribution:")
                for k,v in self.supported_distributions.items():
                    print("\t{} = {}\n".format(k,v))
                exit(1)

    def update_setup(self):
        """
        Update the setup variables according to that of the target platform's installer mechanism class
        """
        if self.installer_class != None:
            self.installer_class.update_setup(self.setup)
            self.installer_class_PostInstall.update_setup(self.setup)
        else:
            print("Installation mechanics class is not initialized, possible issues could be")
            print("\t1. Distribution name is invalid: please refer to the list of valid naming conventions")
            exit(1)

    def platform_Select(self):
        """
        Switch and initialize the distribution installation mechanic class according to the
        distribution name
        """
        # Initialize Variables
        dist_Name = self.dist

        # Process
        if dist_Name == "arch":
            self.installer_class = mechanism.BaseInstallation(self.setup) # Import the distribution of choice's installation mechanism
            print("Base Installation class initialized.")
            self.installer_class_PostInstall = mechanism.PostInstallation(self.setup, self.installer_class) # Import the distribution of choice's postinstallation class
            print("Post Installation class initialized.")
        else:
            self.installer_class = None

    def installer_switch(self):
        """
        Switch installer based on specified distribution

        :: Objects
        - dist : Specify the distribution of your choice
            - Valid Values
                - arch : For ArchLinux
        """
        if self.dist == "arch":
            # Update installer one more time
            self.pre_start_Setup()

            # Check if installer mechanism class is initialized
            if self.installer_class != None:
                self.installer = self.installer_class.installer
                self.postinstaller = self.installer_class_PostInstall.postinstaller
            else:
                print("Installation mechanics class is not initialized, possible issues could be")
                print("\t1. Distribution name is invalid: please refer to the list of valid naming conventions")
                exit(1)
        else:
            print("Invalid distribution specified.")
            print("")
            print("Please specify a valid distribution:")
            for k,v in self.supported_distributions.items():
                print("\t{} = {}\n".format(k,v))

    def list_steps(self):
        """
        List all installation stages/steps
        """
        for k,v in self.installation_stages.items():
            # k = Stage Number
            # v = Stage Description
            print("{} : {}".format(k,v))

    def execute_Step(self, step_Number):
        """
        Execute only a specific step
        """
        if self.installer_class != None:
            # Initialize Variables
            steps = {
                1 : self.installer_class.verify_network,
                2 : self.installer_class.verify_boot_Mode,
                3 : self.installer_class.update_system_Clock,
                4 : self.installer_class.device_partition_Manager,
                5 : self.installer_class.mount_Disks,
                6 : self.installer_class.bootstrap_Install,
                7 : self.installer_class.fstab_Generate,
                8 : self.installer_class.arch_chroot_Exec,
                9 : self.installer_class_PostInstall.postinstallation,
                10 : self.installer_class_PostInstall.postinstall_sanitize,
            }

            # Try and convert stage to integer
            try:
                # Convert string to integer
                step_Number = int(step_Number)

                # Obtain step to execute
                stage_to_Execute = steps[step_Number]

                # Execute stage
                result = stage_to_Execute()
            except Exception as ex:
                # Not an integer
                print("Exception detected: [{}]".format(ex))
        else:
            print("Installation mechanics class is not initialized, possible issues could be")
            print("\t1. Distribution name is invalid: please refer to the list of valid naming conventions")
            exit(1)

    def pre_start_Setup(self):
        # Check if installer mechanism class is initialized
        self.update_setup()

    def begin(self):
        """
        Begin installation
        """
        # Check if installer mechanism class is initialized
        if self.installer_class != None:
            # Check if installer function is set
            if self.installer != None:
                self.installer()
            else:
                print("Installer function is not set.")
                exit(1)

            if self.postinstaller != None:
                self.postinstaller()
            else:
                print("Post Installer function is not set.")
                exit(1)
        else:
            print("Installation mechanics class is not initialized, possible issues could be")
            print("\t1. Distribution name is invalid: please refer to the list of valid naming conventions")
            exit(1)

