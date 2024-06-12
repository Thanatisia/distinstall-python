"""
Unit Test: Framework core - Base Installation: ArchLinux
"""
import os
import sys
from ruamel.yaml import YAML
from pydistinstall.core.distributions.archlinux import mechanism

def test_import_cfg(cfg_fname="config.yaml"):
    """
    Load and Import the specified YAML configuration file

    :: Params
    - cfg_fname : The configuration filename; Leave it empty to use the default configuration filename
        Type: String
        Defaults: config.yaml
    """
    # Initialize Variabes
    configs = {}
    yaml = YAML()
    yaml.indent(sequence=4, offset=2)
    yaml.default_flow_style = False

    # Open the YAML file
    with open(cfg_fname, "r+") as read_config:
        """
        Read configuration file
        """
        # Read configuration string
        contents = read_config.read()

        # Load configuration into Dictionary object
        configs = yaml.load(contents)

        # Close after usage
        read_config.close()
    return configs

def test_get_mount_point(cfg):
    """
    Get the rootfs mount point from the configurations dictionary
    """
    # Initialize Variables
    mount_paths = cfg["mount_Paths"] # Get mount paths

    # Get Root partition mount point
    mount_point = mount_paths["Root"]

    # Return/Output
    return mount_point

def test_import_baseinstall(cfg, MODE="DEBUG"):
    # Initialize Variables
    token = False
    err = ""
    base = None

    # Try to import base installation
    try:
        base = mechanism.BaseInstallation(cfg=cfg, MODE=MODE)

        # Success
        # Set token as true
        token = True
    except Exception as ex:
        # Error detected
        # Set error message
        err = ex

    # Output
    return [base, token, err]

def test_import_postinstall(cs_base_install=None, MODE="DEBUG", cfg=None):
    # Initialize Variables
    token = False
    err = ""
    cs_obj = None

    # Try to import base installation
    try:
        cs_obj = mechanism.PostInstallation(cs_base_install=cs_base_install, MODE=MODE, cfg=cfg)

        # Success
        # Set token as true
        token = True
    except Exception as ex:
        # Error detected
        # Set error message
        err = ex

    # Output
    return [cs_obj, token, err]

def test_complete_install(base):
    """
    Unit Test: ArchLinux base installation - complete install
    """
    # Initialize Variables
    token = False
    cfg = {}
    err = ""

    # Try to perform full installation
    try:
        base.installer()

        # Success
        # Set token as true
        token = True
    except Exception as ex:
        # Error detected
        # Set error message
        err = ex

    # Output
    return [token, err]

def test_stage_execute(base, post):
    # Initialize Variables
    stages = {
        1 : {"title" : "Verify Network", "function" : base.verify_network},
        2 : {"title" : "Verify Bootloader Firmware", "function" : base.verify_boot_Mode},
        3 : {"title" : "Update Host System Clock (NTP)", "function" : base.update_system_Clock},
        4 : {"title" : "Full Disk Partition Management", "function" : base.device_partition_Manager},
        5 : {"title" : "Mount Disks", "function" : base.mount_Disks},
        6 : {"title" : "Start Bootstrap base installation", "function" : base.bootstrap_Install},
        7 : {"title" : "Generate Filesystems Table in Chroot Environment", "function" : base.fstab_Generate},
        8 : {"title" : "Begin System Command Execution in Chroot Environment", "function" : base.begin_chroot_execution},
        9 : {"title" : "Perform Post-Installation Setup", "function" : post.postinstallation},
        10 : {"title" : "Perform Post-Installation Sanitization and Cleanup", "function" : post.postinstall_sanitize},
    }
    token = False
    err = ""

    # Try to execute each stage in the mapping
    try:
        for stage_number, stage_values in stages.items():
            # Get stage title and functions
            stage_title = stage_values["title"]
            stage_fn = stage_values["function"]

            # Debug messages
            print("[INFO] Executing Stage {}: {}".format(stage_number, stage_title))

            # Execute current stage
            stage_fn()

            # Add a break line
            print("")

        # Success
        # Set token as true
        token = True
    except Exception as ex:
        # Error detected
        # Set error message
        err = ex

    # Output
    return [token, err]

def test_unmount_drive(root_mount_dir):
    # Initialize Variables
    token = False
    err = ""

    # Try to execute each stage in the mapping
    try:
        os.system("umount -l {}".format(root_mount_dir))

        # Success
        # Set token as true
        token = True
    except Exception as ex:
        # Error detected
        # Set error message
        err = ex

    # Output
    return [token, err]

def unittest():
    cfg = test_import_cfg() # Test import configuration file
    if len(cfg) == 0:
        print("[X] Error importing YAML configuration file")
        exit(1)
    print("[+] YAML configuration file imported successfully: {}".format(cfg))

    root_mount_dir = test_get_mount_point(cfg) # Test get mount point
    if root_mount_dir == "":
        print("[X] Error obtaining the root partition's mount point")
        exit(1)
    print("[+] Root partition mount point obtained successfully: {}".format(root_mount_dir))

    base, token, err = test_import_baseinstall(cfg=cfg, MODE="RELEASE") # Initialize the BaseInstallation() class object and the configurations for usage
    if token == False:
        print("[X] Error initializing BaseInstallation() class: {}".format(err))
        exit(1)
    print("[+] BaseInstallation() class object initialized successfully: {}".format(base))

    post, token, err = test_import_postinstall(cs_base_install=base, MODE="RELEASE", cfg=cfg) # Initialize the PostInstallation() class object and the configurations for usage
    if token == False:
        print("[X] Error initializing PostInstallation() class: {}".format(err))
        exit(1)
    print("[+] PostInstallation() class object initialized successfully: {}".format(base))

    token, err = test_unmount_drive(root_mount_dir) # Begin Unit Test 1 : Execute the complete installation
    if token == False:
        print("[X] Error unmounting drive: {}".format(err))
        exit(1)
    print("[+] Unmounting of drive completed successfully.")

    token, err = test_complete_install(base) # Begin Unit Test 1 : Execute the complete installation
    if token == False:
        print("[X] Error during complete installation: {}".format(err))
        exit(1)
    print("[+] Distribution Complete Base Installation completed successfully.")

    token, err = test_unmount_drive(root_mount_dir) # Begin Unit Test 1 : Execute the complete installation
    if token == False:
        print("[X] Error unmounting drive: {}".format(err))
        exit(1)
    print("[+] Unmounting of drive completed successfully.")

    token, err = test_stage_execute(base, post) # Begin Unit Test 2 : Execute staged installation
    if token == False:
        print("[X] Error during staged installation: {}".format(err))
        exit(1)
    print("[+] Distribution Staged Base Installation completed successfully.")

if __name__ == "__main__":
    unittest()

