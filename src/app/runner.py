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
        # Obtain parameters
        self.dist = distribution_Name # Distribution of choice
        # Initialize Variables
        self.supported_distributions = {
            "arch" : ["arch", "ArchLinux"],
        }
        self.setup = setup # Initialized Setup configurations
        self.env = env # Initialized Environment Variables
        self.installer = None # Variable to be substituted as the main installer mechanism depending on the distribution specified

        # Initialize Class
        self.platform_Select()
        self.installer_switch()

    def update_setup(self):
        """
        Update the setup variables according to that of the target platform's installer mechanism class
        """
        if self.installer_class != None:
            self.installer_class.update_setup(self.setup)
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
            self.installer_class = mechanism.ArchLinux(self.setup) # Import the distribution of choice's installation mechanism
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

            self.installer = self.install_Arch
        else:
            print("Invalid distribution specified.")
            print("")
            print("Please specify a valid distribution:")
            for k,v in self.supported_distributions.items():
                print("\t{} = {}\n".format(k,v))

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
                7 : self.installer_class.bootstrap_Install,
                8 : self.installer_class.fstab_Generate,
                9 : self.installer_class.arch_chroot_Exec,
            }

            # Obtain step to execute
            stage_to_Execute = steps[step_Number]

            # Execute stage
            result = stage_to_Execute()
            print(result)
        else:
            print("Installation mechanics class is not initialized, possible issues could be")
            print("\t1. Distribution name is invalid: please refer to the list of valid naming conventions")
            exit(1)

    def install_Arch(self):
        """
        Main setup installer
        """
        # Check if installer class is None
        if self.installer_class != None:
            # Initialize Variables
            print("(S) Starting Base Installation...")

            print("========================")
            print("Stage 1: Prepare Network")
            print("========================")

            print("(S) 1. Testing Network...")
            network_Enabled = self.installer_class.verify_network()
            if network_Enabled == False:
                cmd_str = "dhcpcd"
                print("")
                print("Executing: {}".format(cmd_str))
                if self.env.MODE != "DEBUG":
                    ## Begin executing commands
                    stdout, stderr, returncode = process.subprocess_Sync(cmd_str)
                    print("Standard Output: {}".format(stdout))
                    print("Standard Error: {}".format(stderr))

                    if returncode == 0:
                        # Success
                        print("(+) Network is activated")
                    else:
                        # Error
                        print("(-) Error starting Network")
            else:
                print("(+) Network is active")

            print("(D) Network testing completed.")

            if self.env.MODE == "DEBUG":
                tmp = input("Press anything to continue...")

            print("")

            print("==========================================")
            print("Stage 2: Verify Boot Mode (i.e. UEFI/BIOS)")
            print("==========================================")
            
            print("(S) Verifying Boot Mode...")
            boot_Mode = self.installer_class.verify_boot_Mode()
            print("(+) Motherboard bootloader firmware boot mode (bios/uefi): {}".format(boot_Mode))

            print("(D) Boot Mode verification completed.")

            if self.env.MODE == "DEBUG":
                tmp = input("Press anything to continue...")

            print("")

            print("============================")
            print("Stage 3: Update System Clock")
            print("============================")
            
            print("(S) Updating System Clock...")
            success_Flag = self.installer_class.update_system_Clock()
            if success_Flag == False:
                print("(X) Error updating system clock via Network Time Protocol (NTP)")
                exit(1)
            
            print("(D) System clock updated.")

            if self.env.MODE == "DEBUG":
                tmp = input("Press anything to continue...")

            print("")

            print("============================")
            print("Stage 4: Partition the Disks")
            print("============================")
            
            print("(S) Starting Disk Management...")
            success_Flag = self.installer_class.device_partition_Manager()
            if success_Flag == False:
                print("(X) Error formatting disk and partitions")
                exit(1)
            print("(D) Disk Management completed.")

            if self.env.MODE == "DEBUG":
                tmp = input("Press anything to continue...")

            print("")

            print("====================")
            print("Stage 5: Mount Disks")
            print("====================")
            
            print("(S) Mounting disks...")
            success_Flag = self.installer_class.mount_Disks()
            if success_Flag == False:
                print("(X) Error mounting disks")
                exit(1)
            print("(D) Disks mounted.")

            if self.env.MODE == "DEBUG":
                tmp = input("Press anything to continue...")

            print("")

            print("=======================")
            print("Stage 6: Select Mirrors")
            print("=======================")
            
            print("(S) Selecting mirrors...")
            print("{} /etc/pacman.d/mirrorlist".format(self.env.EDITOR))
            print("(D) Mirror selected.")

            if self.env.MODE == "DEBUG":
                tmp = input("Press anything to continue...")

            print("")

            print("===================================")
            print("Stage 7: Install essential packages")
            print("===================================")
            print("(S) Strapping packages to mount point...")
            success_Flag = self.installer_class.bootstrap_Install()
            if success_Flag == False:
                print("(X) Errors bootstrapping packages")
                exit(1)
            print("(D) Packages strapped.")

            if self.env.MODE == "DEBUG":
                tmp = input("Press anything to continue...")

            print("")

            print("===========================================")
            print("Stage 8: Generate fstab (File System Table)")
            print("===========================================")
            print("(S) Generating Filesystems Table in /etc/fstab")
            success_Flag = self.installer_class.fstab_Generate()
            if success_Flag == False:
                print("(X) Error generating filesystems table")
                exit(1)
            print("(D) Filesystems Table generated.")

            if self.env.MODE == "DEBUG":
                tmp = input("Press anything to continue...")

            print("")

            print("===========================")
            print("Stage 9: Chroot and execute")
            print("===========================")

            print("(S) Executing chroot commands")
            success_Flag = self.installer_class.arch_chroot_Exec() # Execute commands in arch-chroot
            if success_Flag == False:
                print("(X) Error executing commands in chroot")
                exit(1)
            print("(D) Commands executed")

            if self.env.MODE == "DEBUG":
                tmp = input("Press anything to continue...")

            print("")

            print("=======================")
            print("Installation Completed.")
            print("=======================")

            print("")

            print("=================")
            print("Post-Installation")
            print("=================")

            print("(S) Starting Basic Post-Installation")

            print("(+) Running post-installation...")
            success_Flag = self.installer_class.postinstallation()
            if success_Flag == False:
                print("(-) Error detected in post-installation process")
                exit(1)
            print("(+) Post-Installation execution completed")

            if self.env.MODE == "DEBUG":
                tmp = input("Press anything to continue...")

            print("")

            print("========================")
            print("Sanitization and Cleanup")
            print("========================")
            print("(+) Running finalization and sanitization...")
            success_Flag = self.installer_class.postinstall_sanitize()
            if success_Flag == False:
                print("(-) Error detected in post-installation sanitization and cleanup")
                exit(1)
            print("(+) Sanitization completed")

            if self.env.MODE == "DEBUG":
                tmp = input("Press anything to continue...")

            print("")

            print("(D) Basic Post-Installation processes completed.")

            finish = input("(D) Finished, press anything to quit.")

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
        else:
            print("Installation mechanics class is not initialized, possible issues could be")
            print("\t1. Distribution name is invalid: please refer to the list of valid naming conventions")
            exit(1)

