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
    # Initialize Variables
    cmd = None

    # Check if type is list or string
    if type(cmd_str) == str:
        # Input is string - split it into a list
        cmd = cmd_str.split()
    else:
        cmd = cmd_str

    proc = Popen(cmd, **opts)
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

    # Open process and Perform action
    # with Popen(cmd_str.split(), stdout=PIPE, **opts) as proc:
    proc = subprocess_Open(cmd_str, stdout=PIPE, **opts)
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

    proc.wait()

    stdout = proc.stdout
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
    cmd = [chroot_exec, dir_Mount, shell, "-c", cmd_str]

    ## Open process and Perform action
    proc = subprocess_Open(cmd, stdout=PIPE, **opts)

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

"""
subprocess stdin (Standard Input) handlers
"""
def subprocess_Input(proc, texts=None):
    """
    Enter multiple input buffer strings into stdin buffer reader

    :: Params
    - proc : The target subprocess object (Popen)
        Type: subprocess.Popen()

    - texts : List of all texts you wish to input into the stdin for that process instance; Please append all the texts in linear sequential order
        - Explanation
            - For example
                - If you wish to enter a password for 'passwd' or something: ['your-password', 'your-password']
        Type: List
    """
    # Check if process is empty
    if (proc != None) and (texts != None):
        # Not Empty
        # Loop through all the texts
        for text in texts:
            # Check if standard input stream is empty
            if proc.stdin != None:
                # Check if line is entered
                if text != "":
                    # Write this buffer string into the process' stdin
                    proc.stdin.write('{}\n'.format(text))

def subprocess_stdin_Clear(proc):
    """
    Wrapper function to flush and clear the subprocess stdin buffer stream using 'proc.stdin.flush'
    """
    # Check if process is empty
    if (proc != None):
        # Check if standard input stream is empty
        if proc.stdin != None:
            # Flush the standard input stream
            proc.stdin.flush()

