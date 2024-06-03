"""
General utilities and functions
"""
import os
import sys

def seperate_by_Delim(msg, delim=";"):
    """
	Seperate a string into an array by the delimiter

	str="$1"			# String to be seperated
	delim="${2:-';'}"	# Delimiter to split
	"""
    output = msg.split(delim)
    return output


