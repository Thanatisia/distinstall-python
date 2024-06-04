"""
Library containing functions related to (sub)process command execution in another shell/rootfs/chroot virtual environment
"""
import os
import sys
from pydistinstall.utils.process import subprocess_Line, subprocess_Sync, PIPE

def format_chroot_Subprocess(self, \
        cmd_str, \
        mount_Dir="/mnt", \
        chroot_Command="arch-chroot", \
        shell="/bin/bash" \
    ):
    """
    Format and returns the command string into the subprocess command list
    """
    return [chroot_Command, mount_Dir, shell, "-c", cmd_str]

def chroot_execute_command(self, cmd_str, mount_Dir="/mnt", chroot_Command="arch-chroot", shell="/bin/bash"):
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
    if self.env.MODE != "DEBUG":
        stdout, stderr, resultcode = subprocess_Line(chroot_cmd_fmt, stdin=PIPE)
        if resultcode == 0:
            # Success
            print("Standard Output: {}".format(stdout))
        else:
            # Error
            print("Error: {}".format(stderr))

        # Map/Append result results
        result["stdout"] = stdout
        result["stderr"] = stderr
        result["resultcode"] = resultcode

    # Output
    return result

def chroot_execute_command_List(self, cmd_List, mount_Dir="/mnt", chroot_Command="arch-chroot", shell="/bin/bash"):
    """
    Generalized chroot command list execution
    """
    # Initialize Variables
    result = {
        "stdout" : [],
        "stderr" : [],
        "resultcode" : [],
        "command-string" : ""
    }

    if len(cmd_List) > 0:
        for i in range(len(cmd_List)):
            # Get current cmd
            cmd_str = cmd_List[i]

            # Formulate chroot command
            chroot_cmd_fmt = [chroot_Command, mount_Dir, shell, "-c", cmd_str]

            print("Executing: {}".format(' '.join(chroot_cmd_fmt)))
            if self.env.MODE != "DEBUG":
                stdout, stderr, resultcode = subprocess_Sync(chroot_cmd_fmt, stdin=PIPE)
                if resultcode == 0:
                    # Success
                    print("Standard Output: {}".format(stdout))
                else:
                    # Error
                    print("Error: {}".format(stderr))

                # Map/Append result results
                result["stdout"].append(stdout)
                result["stderr"].append(stderr)
                result["resultcode"].append(resultcode)

    return result

