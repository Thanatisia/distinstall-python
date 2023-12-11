# Demo

## Setup
### Running from a non-target distro-based Environment
#### Information
- Pre-Requisites
   + Chroot environment

- Demo Contents
   + Startup Docker container for non-ArchLinux chroot environment
   + Jumping into the chroot environment

#### Setup chroot environment
##### Using Docker
- Startup Docker container
    - ArchLinux chroot environment
        + ![chroot environment startup Demo](resources/demo/demo-archlinux-docker-startup.gif)

- Chroot/Exec into Docker container
    - ArchLinux chroot environment
        + ![chroot exec Demo](resources/demo/demo-archlinux-docker-chroot.gif)
        + ![workspace Demo](resources/demo/demo-archlinux-docker-chroot-workspace.gif)

### Running from a target distro-based Environment
- Setup working environment
    + ![Development environment startup Demo](resources/demo/demo-dev-environment-startup.gif)

## Main Process
### Notes
- The following steps have been recorded while running from an arch-linux based chroot environment as part of the development test and demonstration recording
    + However, the steps past this point are entirely repeatable/recreatable according to the demo provided below

- In the case of installation of a target distribution from a system that is not running the same distribution as the target distribution
    + Please remember to follow the [Setup](#Setup) steps above before proceeding

### Running from an ArchLinux-based Environment
- Generate configuration file
    + ![Configuration file generation Demo](resources/demo/demo-generate-config.gif)

- Edit configuration file
    + ![Configuration file editing Demo](resources/demo/demo-edit-config.gif)

- Run
    - Using run.sh
        + ![run.sh Demo](resources/demo/demo-using-run-script.gif)
    - Using 'start'
        + !['python main.py start' Demo](resources/demo/demo-start.gif)
    - Executing specific stages
        + ![execute specific stage Demo](resources/demo/demo-execute-specific-stage.gif)


## Resources

## References

## Remarks

