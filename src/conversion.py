import pandas as pd
import os
import utilities
import constants

"""
A set of functions for converting Excel TMG measurement files
into plain-text CSV files.
"""

def excel_to_csv(xlsx_file, output_dir):
    """
    Converts a single TMG excel file to an equivalent csv file containing measurements in each column
    Parameters
    ----------
    xlsx_filename : str
        Full path to the to-be-converted xlsx file, including extension
    output_dir : str
        Output directory for the converted CSV file
    """
    # Read excel and drop first column, which is empty in TMG format
    df = pd.read_excel(xlsx_file, engine='openpyxl', header=None, skiprows=DATA_START_ROW).drop(columns=[0])
    df.to_csv(output_dir + xlsx_filename.replace(".xlsx", ".csv"), header=False, index=False)


def xlsx_to_pre_post_csv(input_dir, xlsx_filename, 
        pre_output_dir, post_output_dir, conversion_mode,
        pre_reps=1, post_reps=1, max_set=8):
    """
    Used to convert a raw TMG Excel file from a session of SPM-protocol 
    measurements into separate pre-exercise and post-exercise files.
    See documentation of conversion constants in `constants.py`.

    Parameters
    ----------
    input_dir : str
        Parent directory holding the TMG Excel file
    xlsx_filename : str
        File name of the Excel file, excluding full path but including extension
    pre_output_dir : str
        Output directory for converted pre-exercise CSV files
    conversion_mode : int
        One of the conversion mode constants documented in `constants.py`
    pre_reps : int
        The number of pre-exercise measurements per set in the Excel file
    post_reps : int
        The number of post-exercise measurements per set in the Excel file
    max_set : int
        Ignore sets in Excel file above this set number.

    """
    xlsx_file = input_dir + xlsx_filename

    # Read measurements from Excel file into a pandas dataframe
    df = utilities.xlsx_to_pandas_df(xlsx_file)

    n_cols = df.shape[1]
    reps_per_set = pre_reps + post_reps
    sets = n_cols/reps_per_set

    if not sets.is_integer():
        print("Error: Non-integer number of measurements per sets.")
        print("Aborting")
        return
    else:
        sets = int(sets)

    if conversion_mode == constants.VERBATIM:
        df.to_csv(xlsx_file.replace(".xlsx", ".csv"), header=False, index=False)

    elif conversion_mode == constants.PRE_POST_BY_SESSION:
        # Separate the column numbers of pre-exercise and post-exercise measurements.
        # Note use of 1-based indexing to align with physical sets and measurements.
        pre_cols, post_cols = [], []
        for set in range(1, sets + 1):
            if set > max_set:
                break
            for rep in range(1, pre_reps + 1):
                pre_cols.append((set - 1) * reps_per_set + rep)
            for rep in range(1, post_reps + 1):
                post_cols.append((set - 1) * reps_per_set + rep + pre_reps)

        print("Pre-exercise column numbers: ", end="")
        print(pre_cols)
        print("Post-exercise column numbers: ", end="")
        print(post_cols)

        pre_headers, post_headers = get_column_headers(pre_cols, post_cols)

        # Write CSV files
        df.to_csv(pre_output_dir + xlsx_filename.replace(".xlsx", "-pre.csv"),
                header=pre_headers, index=False, columns=pre_cols)
        df.to_csv(post_output_dir + xlsx_filename.replace(".xlsx", "-post.csv"),
                header=post_headers, index=False, columns=post_cols)

    elif conversion_mode == constants.PRE_POST_BY_SET_ALL_REPS:
        # Create an output directory for CSV files
        output_dir = utilities.make_output_dir(output_dir + xlsx_filename.replace(".xlsx", ""))
        for set in range(1, sets + 1):
            if set > max_set:
                break
            print("Set Number: {}".format(set))

            # Separate column numbers of all pre-exercise and post-exercise 
            # measurements in the current set.  Note use of 1-based 
            # indexing to align with physical sets and measurements.
            pre_cols, post_cols = [], []
            for rep in range(1, pre_reps + 1):
                pre_cols.append((set - 1) * reps_per_set + rep)
            for rep in range(1, post_reps + 1):
                post_cols.append((set - 1) * reps_per_set + rep + pre_reps)

            print("Pre-exercise column numbers: ", end="")
            print(pre_cols)
            print("Post-exercise column numbers: ", end="")
            print(post_cols)
            print()

            pre_headers, post_headers = get_column_headers(pre_cols, post_cols)

            # Write CSV files for the current set
            df.to_csv(pre_output_dir + xlsx_filename.replace(".xlsx",
                "-pre-set-{}.csv".format(set)), header=pre_headers,
                index=False, columns=pre_cols)
            df.to_csv(post_output_dir + xlsx_filename.replace(".xlsx",
                "-post-set-{}.csv".format(set)), header=post_headers,
                index=False, columns=post_cols)

    elif conversion_mode == constants.PRE_POST_BY_SET_FIRST_REP:
        # Separate the column numbers of pre-exercise and post-exercise 
        # measurements for each set and use only first measurement of each set.
        # Note use of 1-based indexing to align with physical sets and measurements.
        pre_cols, post_cols = [], []
        for set in range(1, sets + 1):
            if set > max_set:
                break
            pre_cols.append((set - 1) * reps_per_set + 1)
            post_cols.append((set - 1) * reps_per_set + pre_reps + 1)

        print("Pre-exercise column numbers: ", end="")
        print(pre_cols)
        print("Post-exercise column numbers: ", end="")
        print(post_cols)

        pre_headers, post_headers = get_column_headers(pre_cols, post_cols)

        # Write CSV files
        df.to_csv(pre_output_dir + xlsx_filename.replace(".xlsx", "-pre.csv"),
                header=pre_headers, index=False, columns=pre_cols)
        df.to_csv(post_output_dir + xlsx_filename.replace(".xlsx", "-post.csv"),
                header=post_headers, index=False, columns=post_cols)

def get_column_headers(pre_cols, post_cols):
    """
    Boilerplate code for converting a Numpy array of column numbers
    corresponding to measurement numbers into a Python list of the
    measurement numbers in human-friendlier form.

    Example input: [1, 9, 17, 25]
    Example output: ["Meas. 1", 9, 17, 25]
    """
    pre_headers, post_headers = [], []
    for col in pre_cols:
        pre_headers.append("Measurement {}".format(col))
    for col in post_cols:
        post_headers.append("Measurement {}".format(col))
    return pre_headers, post_headers
    

def frontiers_conversion_wrapper():
    """
    Wrapper method for converting all TMG-formatted Excel files
    in the inputted directory into CSV files. 
    Intended for use with the measurement files used in the Frontiers
    potentiation project.
    See documentation of conversion modes at the start of the script.

    """
    pre_output_dir = "/home/ej/Media/tmg-bmc-media/potentiation-2021/data/csv_for_spm/pre-exercise/"
    post_output_dir = "/home/ej/Media/tmg-bmc-media/potentiation-2021/data/csv_for_spm/post-exercise/"


    # Convert files with 1 pre and post measurement per measurement set
    input_dir = "/home/ej/Media/tmg-bmc-media/potentiation-2021/data/excel-raw/1/"
    pre_reps = 1    # number of pre-exercise measurements per set
    post_reps = 1   # number of pre-exercise measurements per set
    max_sets = 4    # ignore sets in Excel file larger than max_sets
    conversion_mode = constants.PRE_POST_BY_SESSION
    for xlsx_filename in utilities.natural_sort(os.listdir(input_dir)):
        if ".xlsx" in xlsx_filename and "$" not in xlsx_filename:
            print(xlsx_filename)
            xlsx_to_pre_post_csv(input_dir, xlsx_filename, 
                    pre_output_dir, post_output_dir,
                    conversion_mode, pre_reps=pre_reps,
                    post_reps=post_reps, max_set=max_sets)

    # Convert files with 8 pre and post measurements per measurement set,
    # but keep only first measurement in each set.
    input_dir = "/home/ej/Media/tmg-bmc-media/potentiation-2021/data/excel-raw/8/"
    pre_reps = 8
    post_reps = 8
    max_sets = 4
    conversion_mode = constants.PRE_POST_BY_SET_FIRST_REP
    for xlsx_filename in utilities.natural_sort(os.listdir(input_dir)):
        if ".xlsx" in xlsx_filename and "$" not in xlsx_filename:
            print(xlsx_filename)
            xlsx_to_pre_post_csv(input_dir, xlsx_filename, 
                    pre_output_dir, post_output_dir,
                    conversion_mode, pre_reps=pre_reps,
                    post_reps=post_reps, max_set=max_sets)


if __name__ == "__main__":
    frontiers_conversion_wrapper()
