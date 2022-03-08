import os
import re
import numpy as np
import pandas as pd

"""
A collection of functions related to directory creation and file system utilities.
"""

def make_output_dir(base_dir):
    """
    Attempts to make a directory with the inputted base directory name.
    If a directory with the inputted base name already exists, the function
    and appends natural numbers to the end of the base name until reaching
    an available directory name.

    Parameters
    ----------
    base_dir : str
        Desired base directory name
        Example: "~/test/tmg/converted"
    
    Returns
    -------
    created_dir : str
        Name of actually created directory, with numbers appended as needed
        to avoid conflict with existing directories.
        Example: "~/test/tmg/converted"
                 "~/test/tmg/converted_01"
                 "~/test/tmg/converted_02"
                 ... and so on
    
    """
    try:  # try created directory with base name only
        os.mkdir(base_dir + "/")
        return base_dir + "/"
    except OSError as error:  # if a directoy with the base name exists
        success = False
        counter = 0
        while not success:
            counter += 1
            if counter > 99:
                print("Aborting. Maximum output directory count exceeded.")
                return
            success = try_next_output_dir(base_dir + "_" + str(counter) + "/")

        return base_dir + "_" + str(counter) + "/"


def try_next_output_dir(base_dir_name):
    """ Helper method for the make_output_dir method; see above """
    try:
        os.mkdir(base_dir_name)
        return True
    except OSError as error:
        return False


def natural_sort(list_to_sort):
    """
    For sorting filenames in natural numerical order instead of alphabetical order.
    Example input: [2.txt, 11.txt, 1.txt]
    Example output: [1.txt, 2.txt, 11.txt] (and not [1.txt, 11.txt, 2.txt])

    """
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(list_to_sort, key=alphanum_key)

