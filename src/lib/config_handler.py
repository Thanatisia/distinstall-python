"""
Configurations file handler
"""
import os
import sys
import yaml

class YAMLConfig():
    """
    YAML Configurations file handler
    """
    def __init__(self, file_name, mode="r"):
        """
        Class constructor
        """
        self.file_name = file_name
        self.mode = mode
        self.file = None

    def open_file(self):
        """
        Open file and import file
        """
        # Open file for use
        self.file = open(self.file_name, self.mode)

    def close_file(self):
        """
        Close file after usage and set empty file object
        """
        # Check if file is opened
        if self.file != None:
            # Close file after use
            self.file.close()
            self.file = None

    def write_config(self, data):
        """
        Dump and write dictionary object to YAML configuration file
        """
        # Check if data is not empty and file is opened
        if (data != None) and (self.file != None):
            # Dump the data
            yaml.dump(data, file)

    def read_config(self):
        """
        Load and read YAML configuration file contents to dictionary
        """
        file = self.file

        # Check if file is opened
        if (file == None):
            # Open file if not opened
            file = open(self.file_name)

        return yaml.safe_load(file)

    def parse_yaml_str_to_dict(self, yaml_str):
        """
        Parse YAML strings into dictionary object
        """
        if yaml_str != "":
            return yaml.safe_load(yaml_str)


