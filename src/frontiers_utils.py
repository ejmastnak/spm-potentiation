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
    

def make_output_dir(base_dir, use_existing=False):
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
    use_existing : bool
        Behavior if True: If a directory with name `base_dir` already
        exists, use the existing `base_dir` name (instead of creating new
        directories by appending a counter). This would be used to
        intentionally overwrite files inside the existing `base_dir`.
    
    Returns
    -------
    created_dir : str
        Name of actually created directory, with numbers appended as needed
        to avoid conflict with existing directories.
        Example: "~/test/tmg/converted"
        Example: "~/test/tmg/converted_01"
        Example: "~/test/tmg/converted_04"
    
    """
    try:  # try created directory with base name only
        os.mkdir(base_dir)
        return base_dir
    except OSError as error:  # if a directoy with the base name exists
        if use_existing:
            # Double-check directory with name `base_dir` indeed exists, (in
            # case OSError was raised for some other reason).
            if os.path.isdir(base_dir):
                return base_dir

        success = False
        counter = 0
        while not success:
            counter += 1
            if counter > 99:
                print("Aborting. Maximum output directory count exceeded.")
                return
            success = try_next_output_dir(base_dir + "_" + str(counter))

        return base_dir + "_" + str(counter)


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

