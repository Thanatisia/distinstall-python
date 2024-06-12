# Self-Hosting and using the framework API's libraries, functions and attributes/variables

## Documentations

### Classes

### Usages
- Import package libraries
    ```python
    from pydistinstall.core.distributions.archlinux import mechanism
    ```

- Load and Import the specified configuration file
    - Information
        - Parameter Signature/Headers
            - cfg_fname : The configuration filename; Leave it empty to use the default configuration filename
                + Type: String
                + Defaults: config.yaml
        - Return
            - cfg : Dictionary (Key-Value Mapping) generated from importing the YAML configuration file contents
                + Type: Dictionary (Key-Value Mapping)
    - Initialize Variables
        ```python
        # Initialize Variables
        configs = {}
        ```
    - YAML configuration file
        ```python
        # Initialize YAML configurations
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
        ```
    - Return/Output
        ```python
        return configs
        ```

- Get the rootfs mount point from the configurations dictionary
    ```python
    # Initialize Variables
    mount_paths = cfg["mount_Paths"] # Get mount paths

    # Get Root partition mount point
    mount_point = mount_paths["Root"]
    ```

- Try to import base-installation class
    ```python
    MODE = "<DEBUG|RELEASE>"
    try:
        base = mechanism.BaseInstallation(cfg=cfg, MODE=MODE)
    except Exception as ex:
        # Error detected
        print("Exception: {}".format(ex))
    ```

- Try to import the post-installation class
    ```python
    MODE = "<DEBUG|RELEASE>"
    try:
        cs_obj = mechanism.PostInstallation(cs_base_install=cs_base_install, MODE=MODE, cfg=cfg)
    except Exception as ex:
        # Error detected
        print("Exception: {}".format(ex))
    ```

- (Optional) If you are mounting the disk partitions: Unmount disk before proceeding with installation
    ```python
    try:
        os.system("umount -l {}".format(root_mount_dir))

        # Success
        # Set token as true
        token = True
    except Exception as ex:
        # Error detected
        print("Exception: {}".format(ex))
    ```

- Distribution Base Installaion: ArchLinux - complete install
    ```python
    try:
        base.installer()
    except Exception as ex:
        # Error detected
        print("Exception: {}".format(ex))
    ```

- Staged Execution
    - Define Stages
        ```python
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
        ```
    - Try to execute each stage in the mapping
        ```python
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
        except Exception as ex:
            # Error detected
            print("Exception: {}".format(ex))
        ```

## Resources

## References

## Remarks

