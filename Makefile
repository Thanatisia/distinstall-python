# Makefile for Linux Distro Install Script Execution

# [Variables]

# Settings and Configurations
TARGET_DISK = /dev/sdX
MOUNT_ROOT = "/mnt"
MOUNT_PATHS = "/mnt/boot" "/mnt" "/mnt/home"

# Program Variables
ENV = TARGET_DISK_NAME="$(TARGET_DISK)"	# Environment Variables
SCRIPT = py-distinstall					# Script Filename
CFG_FILE = config.yaml					# Script Default Configuration File
CFLAGS =                                # Compilation Flags

# [Commands]
CMD = $(ENV) $(SCRIPT)

# [Recipe]
.DEFAULT_GOAL := help
.PHONY: help init testinstall install clean run list-stage

### Program Recipes ###

help: 
    ## Displays this help menu
    @declare -A opts=(\
        [help]="Displays this help menu" \
        [display_snippets]="Display Sample Usages with both Makefile and bare metal" \
        [init]="Initialize Environment Variables and System/Program Information" \
        [download]="Download all files required: installer, config file" \
        [testinstall]="Run the install script's test suite and see the commands it will run before committing" \
        [install]="Run the install script. WARNING: This will overwrite the target disk/filesystem, please becareful. You will need to run 'sudo make install' to execute this" \
        [run]="Run a specific installation stage" \
        [list-stage]="List all stages" \
        [genscript]="Run install-gen and generate the commands to output as a script" \
        [clean]="Clean all temporary files and unmount drives" \
    ); \
    for opt in "$${!opts[@]}"; do \
        echo -e "$${opt} : $${opts[$${opt}]}"; \
    done

display_snippets:
    ## Display Sample Usages with both Makefile and bare metal
    @echo -e "Sample Usages with:"
    @echo -e ""
    @echo -e "[Makefile]"
    @echo -e "\t 1. make testinstall  : To display the commands in its entirety; Used to verify that the flow is what you want"
    @echo -e "\t 2. sudo make install : Requires sudo; To begin the partition management and installation process"
    @echo -e ""
    @echo -e "[Bare Metal]"
    @echo -e "\t 1. TARGET_DISK_NAME='target-disk-label (i.e. /dev/sdX)' ./distinstall            : To display the commands in its entirety; Used to verify that the flow is what you want"
    @echo -e "\t 2. sudo TARGET_DISK_NAME='target-disk-label (i.e. /dev/sdX)' ./distinstall start : Requires sudo; To begin the partition management and installation process"
    @echo -e ""

init:
    ## Initialize Environment Variables and System/Program Information

download:
    ## Download all files required
    ### 1. Installer
    ### 2. Configuration File

    # Download installer if not found
    @test -f "$(SCRIPT)" || curl -L -O "https://raw.githubusercontent.com/Thanatisia/distinstall-python/main/src/${SCRIPT}"

    # Generate config file if not found
    @test -f "$(CFG_FILE)" || ./$(SCRIPT) -g

testinstall: init
    ## Run the install script testsuite
    # - Run this with sudo for username verification
    $(CMD) $(CFLAGS) start

install: clean
    ## Run the install script and install
    # WARNING: This will overwrite the target disk/filesystem, please be careful
    # - Run this with sudo
    $(eval CFLAGS=-m "RELEASE")
    $(CMD) $(CFLAGS) start

list-stage:
    ## List all stages
    @$(CMD) $(CFLAGS) --list-stages

run: clean
    ## Run specific stage
    @cd src && \
        ${CMD} \
        -m RELEASE \
        -u /dev/sdb \
        --execute-stage 1

genscript:
    ## Run install-gen and generate the commands to install and
    # Output as a script file for backup
    $(CMD) $(CFLAGS) -g

clean: 
    ## Clean all temporary files and unmount drives 
    # Check if directory is a mount point
    ! mountpoint -q "$(MOUNT_ROOT)" || sudo umount -l $(MOUNT_ROOT) # If error, assume no errors

### Test Suites / Unit Tests


