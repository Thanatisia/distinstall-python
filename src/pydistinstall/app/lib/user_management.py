"""
User Management handler
"""

import os
import sys
from subprocess import Popen, PIPE
from pydistinstall.utils import process

def get_all_users():
    """
    Check if user exists
    
    exist_Token="0"
    delimiter=":"
    res_Existence="$(getent passwd)"
    all_users=($(cut -d ':' -f1 /etc/group | tr '\n' ' '))
    """
    exist_Token = 0
    delimiter = ":"
    passwd_Entry = ""

    # Get passwd entry and check if it exists
    cmd_get_passwd_Entry = "getent passwd"
    proc = Popen(cmd_get_passwd_Entry.split())
    stdout, stderr = proc.communicate()

    # Cut and get all users from the group
    cmd_cut_all_Users = "cut -d ':' -f1 /etc/group | tr '\n' ' '"
    proc = Popen(cmd_cut_all_Users.split())
    stdout, stderr = proc.communicate()

    # Split result to all users
    all_Users = stdout.split()
    return all_Users

def get_user_primary_group(user_Name):
    """
    Just retrieves the user's primary group (-g)

    :: Params
    - user_Name : Specify the target user's name
        Type: String
    """
    cmd_get_user_primary_Group = "$(id -gn {})".format(user_Name)
    primary_group, stderr = process.subprocess_Sync(cmd_get_user_primary_Group)
    return primary_group

def create_user(u_Name, u_primary_Group, u_secondary_Groups, u_home_Dir, u_other_Params):
    """
    =========================================
    :: Function to create user lol
      1. Append all arguments into the command
      2. Execute command and create
    =========================================

    :: Parameters
    - u_name        : Specify the target User Name
        + Type: String
    - User definition
        - u_primary_Group       : Primary Group
            Type: String
        - u_secondary_Groups    : Secondary Groups
            Type: String
        - u_home_Dir            : Home Directory
            Type: String
        - u_other_Params        : Any other parameters after the first 3
            Type: String
    """

    # --- Head

    # Local variables
    u_create_Command="useradd"
    create_Token="0"            # 0 : not Created; 1 : Created

    # --- Processing
    # Get Parameters
    if u_home_Dir != "NIL":
        # If Home Directory is not Empty
        u_create_Command+=" -m "
        u_create_Command+=" -d {} ".format(u_home_Dir)

    if u_primary_Group != "NIL":
        # If Primary Group is Not Empty
        u_create_Command+=" -g {} ".format(u_primary_Group)

    if u_secondary_Groups != "NIL":
        # If Primary Group is Not Empty
        u_create_Command+=" -G {} ".format(u_secondary_Groups)

    if u_other_Params != "NIL":
        # If there are any miscellenous parameters
        u_create_Command+=" {} ".format(u_other_Params)

    u_create_Command += u_Name

    # --- Output
    # Return Create Command
    return u_create_Command


