"""
Process/Subprocess handling
"""
import os
import sys
from subprocess import Popen, PIPE

def subprocess_Line(cmd_str):
    """
    Open a subprocess and read the stdout line by line

    :: Params
    - cmd_str : The command string to execute
        Type: String
    """
    # Initialize Variables
    stdout = []
    stderr = ""
    line = ""

    print(cmd_str.split())

    # Open process and Perform action
    with Popen(cmd_str.split(), stdout=PIPE) as proc:
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
            print("Current Line: {}".format(line))
            stdout.append(line)

    return stdout

def subprocess_Sync(cmd_str):
    """
    Open a subprocess and execute in sync
    - Check if the previous command is completed before proceeding

    :: Params
    - cmd_str : The command string to execute
        Type: String
    """
    # Initialize Variables
    stdout = ""
    stderr = ""

    ## Open process and Perform action
    proc = Popen(cmd_str.split(), shell=True, stdin=PIPE, stdout=PIPE)

    # Execute process in sync - check if the previous command is completed before proceeding
    stdout, stderr = proc.communicate()

    # Decode and clean-up output
    if stdout != None:
        stdout = stdout.decode("utf-8")

    if stderr != None:
        stderr = stderr.decode("utf-8")
    else:
        stderr = ""

    return stdout, stderr


