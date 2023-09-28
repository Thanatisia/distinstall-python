"""
Process/Subprocess handling
"""
import os
import sys
from subprocess import Popen, PIPE

"""
Process/Subprocess object functions
"""
def subprocess_Open(cmd_str, **opts):
    """
    Open a subprocess and return it

    - cmd_str : The command string to execute
        Type: String

    - opts : All Key=Value parameters you wish to parse into Popen
        Type: kwargs (Keyword Arguments) aka Dictionary
    """
    proc = Popen(cmd_str.split(), **opts)
    return proc

"""
Process/Subprocess Execution functions
"""
def subprocess_Line(cmd_str, **opts):
    """
    Open a subprocess and read the stdout line by line

    :: Params
    - cmd_str : The command string to execute
        Type: String

    - opts : All Key=Value parameters you wish to parse into Popen
        Type: kwargs (Keyword Arguments) aka Dictionary
    """
    # Initialize Variables
    stdout = []
    stderr = ""
    line = ""
    ret_Code = 0

    print(cmd_str.split())

    # Open process and Perform action
    with Popen(cmd_str.split(), stdout=PIPE, **opts) as proc:
        # Loop until there are no more lines
        while True:
            # While there are still lines

            # Check if process is still alive
            if proc.stdout != None:
                # Read first line
                line = proc.stdout.readline()

            if not line:
                break

            ## Operate data and store in list
            line = line.rstrip().lstrip().decode("utf-8")
            # print("Current Line: {}".format(line))
            print(line)
            stdout.append(line)

        stderr = proc.stderr
        ret_Code = proc.returncode

    return stdout, stderr, ret_Code

def subprocess_Sync(cmd_str, **opts):
    """
    Open a subprocess and execute in sync
    - Check if the previous command is completed before proceeding

    :: Params
    - cmd_str : The command string to execute
        Type: String
    - opts : All Key=Value parameters you wish to parse into Popen
        Type: kwargs (Keyword Arguments) aka Dictionary
    """
    # Initialize Variables
    stdout = ""
    stderr = ""

    ## Open process and Perform action
    proc = subprocess_Open(cmd_str, stdout=PIPE, **opts)

    # Execute process in sync - check if the previous command is completed before proceeding
    stdout, stderr = proc.communicate()

    # Decode and clean-up output
    if stdout != None:
        stdout = stdout.decode("utf-8")

    if stderr != None:
        stderr = stderr.decode("utf-8")
    else:
        stderr = ""

    # Get result code from process pipe
    resultcode = proc.returncode

    return stdout, stderr, resultcode

def chroot_exec(cmd_str, chroot_exec="arch-chroot", dir_Mount="/mnt", shell="/bin/bash", communicate_opts=None, **opts):
    """
    Open Subprocess and execute commands in chroot

    :: Params
    - cmd_str : The command string to execute
        Type: String

    - chroot_exec : The binary to chroot with
        Type: String
        Default Value: arch-chroot

    - dir_Mount : The mount point
        Type: String
        Default Value: /mnt

    - shell : The target shell to work with
        Type: String
        Default Value: /bin/bash

    - communicate_opts : Options to parse into the .communicate() command
        Type: Dictionary
        Default Value: None

    - opts : All Key=Value parameters you wish to parse into Popen
        Type: kwargs (Keyword Arguments) aka Dictionary
    """
    cmd = "{} {} {} -c \"{}\"".format(chroot_exec, dir_Mount, shell, cmd_str)

    ## Open process and Perform action
    proc = subprocess_Open(cmd_str, stdout=PIPE, **opts)

    # Execute process in sync - check if the previous command is completed before proceeding
    stdout, stderr = proc.communicate(communicate_opts)

    # Decode and clean-up output
    if stdout != None:
        stdout = stdout.decode("utf-8")

    if stderr != None:
        stderr = stderr.decode("utf-8")
    else:
        stderr = ""

    # Get result code from process pipe
    resultcode = proc.returncode

    return stdout, stderr, resultcode


