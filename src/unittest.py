import os
import sys
from subprocess import Popen, PIPE

def test_processes(cmd_str):
    def subprocess_Sync(cmd_str):
        """
        Open a subprocess and execute in sync
        - Check if the previous command is completed before proceeding

        :: Params
        - cmd_str : The command string to execute
            Type: String
        """
        ## Open process and Perform action
        proc = Popen(cmd_str.split())
        # Execute process in sync - check if the previous command is completed before proceeding
        stdout, stderr = proc.communicate()[0]
        return stdout, stderr

    # Begin test
    subprocess_Sync(cmd_str)

def test_reference(pos):
    def increment(pos):
        # pos += 1
        print(pos, "+ 1 = ", pos+1)
        return pos+1

    pos = increment(pos)
    increment(pos)
    increment(pos)
    increment(pos)
    increment(pos)

def main():
    pos:int = 0
    test_reference(pos)
    print(pos)

if __name__ == "__main__":
    main()
