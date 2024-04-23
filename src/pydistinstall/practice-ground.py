"""
Practice Ground/TestBench source code for practicing ideas
"""
import os
import sys
from subprocess import Popen, PIPE

def test_processes():
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

    # Begin test
    cmd_strings = [
        "ipconfig /all",
        "ping 8.8.8.8"
    ]

    print("Test Subprocess sequential communication:")

    print("")

    for cmd_str in cmd_strings:
        print("Testing: {}".format(cmd_str))
        stdout, stderr = subprocess_Sync(cmd_str)
        print("Standard Output: {}".format(stdout))
        print("Standard Error: {}".format(stderr))

        print("")

    print("")

    input("Press anything to continue with the next test: {}".format("Test Subprocess line-by-line read"))

    print("Test Subprocess line-by-line read:")

    print("")

    for cmd_str in cmd_strings:
        print("Testing: {}".format(cmd_str))
        stdout = subprocess_Line(cmd_str)
        print("Standard Output: {}".format(stdout))

        print("")

def test_reference():
    def increment(pos):
        # pos += 1
        print(pos, "+ 1 = ", pos+1)
        return pos+1

    pos = 1
    print(increment(pos))
    print(increment(pos))
    print(increment(pos))
    print(increment(pos))
    print(increment(pos))

def main():
    test_reference()

    print("")

    test_processes()

if __name__ == "__main__":
    main()
