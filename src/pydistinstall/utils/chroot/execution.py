"""
Library containing functions related to (sub)process command execution in another shell/rootfs/chroot virtual environment
"""
import os
import sys
from pydistinstall.utils.process import subprocess_Line, subprocess_Sync, PIPE

def format_chroot_Subprocess(cmd_str, mount_Dir="/mnt", chroot_Command="arch-chroot", shell="/bin/bash"):
    """
    Format and returns the command string into the subprocess command list
    """
    return [chroot_Command, mount_Dir, shell, "-c", cmd_str]

def chroot_execute_command(cmd_str, mount_Dir="/mnt", chroot_Command="arch-chroot", shell="/bin/bash"):
    """
    Generalized chroot command execution
    """
    # Initialize Variables
    chroot_cmd_fmt = [chroot_Command, mount_Dir, shell, "-c", cmd_str]
    stdout = []
    stderr = []
    resultcode = 0
    result = {
        "stdout" : [],
        "stderr" : [],
        "resultcode" : [],
        "command-string" : ""
    }

    # Process
    stdout, stderr, resultcode = subprocess_Line(chroot_cmd_fmt, stdin=PIPE)

    # Map/Append result results
    result["stdout"] = stdout
    result["stderr"] = stderr
    result["resultcode"] = resultcode

    # Output
    return result

def chroot_execute_command_List(cmd_List, mount_Dir="/mnt", chroot_Command="arch-chroot", shell="/bin/bash") -> list:
    """
    Generalized chroot command list execution
    """
    # Initialize Variables
    result = []

    if len(cmd_List) > 0:
        for i in range(len(cmd_List)):
            # Get current cmd
            cmd_str = cmd_List[i]

            # Initialize result for current command
            curr_cmd_res = {
                "stdout" : [],
                "stderr" : [],
                "resultcode" : [],
                "command-string" : []
            }

            # Formulate chroot command
            chroot_cmd_fmt = [chroot_Command, mount_Dir, shell, "-c", cmd_str]

            stdout, stderr, resultcode = subprocess_Sync(chroot_cmd_fmt, stdin=PIPE)

            # Map the results for the current command
            curr_cmd_res["stdout"].append(stdout)
            curr_cmd_res["stderr"].append(stderr)
            curr_cmd_res["resultcode"].append(resultcode)
            curr_cmd_res["command-string"] = chroot_cmd_fmt

            # Append current command to the results list
            result.append(curr_cmd_res)

    return result


