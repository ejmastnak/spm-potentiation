import os
import re
import numpy as np
import pandas as pd
import constants

"""
A mostly miscellaneous set of utility functions related to file I/O for use
with the SPM potentiation project.
"""

def xlsx_to_pandas_df(xlsx_file, num_rows=constants.TMG_MAX_ROWS):
    """
    Reads the measurements in a TMG-formatted Excel file into a Pandas dataframe.
    Drops the following information from the Excel file:
    - The first column  (does not contain TMG signal data)
    - The first constants.DATA_START_ROW rows (contain metadata but no signal)

    Parameters
    ----------
    xlsx_file : str
        Full path to a TMG-formatted Excel measurement file
    num_rows : int
        Number of rows (i.e. data points, i.e. milliseconds assuming
        1 kHz sampling) of inputted TMG signal `x` to analyze, since most
        relevant information occurs in the first few hundred milliseconds only.

    Returns
    -------
    df : DataFrame
        Pandas dataframe equivalent of Excel file's measurement
    
    """
    return pd.read_excel(xlsx_file, engine='openpyxl', header=None, nrows=num_rows,
            skiprows=constants.TMG_DATA_START_ROW).drop(columns=[0])
    

def make_output_dir(dir_path, exist_ok=True):
    """
    Attempts to make a directory with the inputted base directory name.
    If `exist_ok=False` and a directory with the inputted base name already
    exists, the function and appends natural numbers to the end of the base
    name until reaching an available directory name.

    Parameters
    ----------
    dir_path : str
        Desired base directory name
        Example: "~/test/tmg/converted"
    exist_ok : bool
        Behavior if True: If a directory with name `dir_path` already exists,
        use the existing directory.
        Behavior if False: If a directory with name `base_dir` already exists,
        try creating new directories `dir_path_01`,  `dir_path_02`, etc.
    
    Returns
    -------
    created_dir : str
        Name of used or created directory, with numbers appended as needed to
        avoid conflict with existing directories.
        Example: "~/test/tmg/converted"
        Example: "~/test/tmg/converted_01"
        Example: "~/test/tmg/converted_04"
    
    """
    try:  # try creating directory with base name only
        os.makedirs(dir_path, exist_ok=exist_ok)
        return dir_path
    except FileExistsError as error:  # if a directoy with the base name exists
        success = False
        counter = 0
        while not success:
            counter += 1
            if counter > 99:
                print("Aborting. Maximum output directory count exceeded at {}_{}.".format(dir_path, counter))
                return
            success = try_next_output_dir(dir_path + "_" + str(counter))

        return dir_path + "_" + str(counter)


def try_next_output_dir(base_dir_name):
    """ Helper method for the make_output_dir method; see above """
    try:
        os.makedirs(base_dir_name)
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

