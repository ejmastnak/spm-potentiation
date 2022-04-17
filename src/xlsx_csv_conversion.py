import pandas as pd
import os
import constants, frontiers_utils

"""
A set of functions for converting raw, TMG-formatted 
Excel measurement files into plain-text CSV files.
The functions implement various ways of organizing the Excel file's
pre- and post-exercise measurements into formats more suitable to
later data processing.
"""

def convert_verbatim(xlsx_file, output_dir):
    """
    Converts a single TMG Excel file to an equivalent CSV file "verbatim".
    Every TMG measurement in the Excel file appears, in order, as a column in the CSV file.
    This function reserves only TMG measurements and 
    drops all other metadata in the Excel file.

    Parameters
    ----------
    xlsx_filename : str
        Full path to the to-be-converted xlsx file, including extension
    output_dir : str
        Output directory for the converted CSV file
    """
    # Read Excel and drop first column, which is empty in TMG format
    df = pd.read_excel(xlsx_file, engine='openpyxl', header=None, skiprows=DATA_START_ROW).drop(columns=[0])
    df.to_csv(output_dir + xlsx_filename.replace(".xlsx", ".csv"), header=False, index=False)


"""
PARAMTER DOCUMENTATION FOR CONVERSION FUNCTIONS
--------------------------------------------------------------------------
The same parameters are used in multiple functions below, 
and are documented in one place here to avoid repetition.

input_dir : str
    Parent directory of the to-be-converted TMG-formatted Excel file.
xlsx_file : str
    Name, excluding full path, of the TMG-formatted Excel file.
    The input file's parent directory and filename are separated
    to make naming processed output files easier.
pre_output_dir : str
    Output directory for converted pre-exercise CSV files.
post_output_dir : str
    Output directory for converted post-exercise CSV files.
conversion_mode : int
    One of the conversion mode constants documented in `constants.py`
msmnts_per_pre_set : int
    The number of pre-exercise measurements per set in the Excel file
msmnts_per_post_set : int
    The number of post-exercise measurements per set in the Excel file
max_set : int
    The maximum set in the Excel file to write to CSV files.
    Sets in Excel file above this set number are ignored.
--------------------------------------------------------------------------
"""

def split_by_pre_post(input_dir, xlsx_filename, 
        pre_output_dir, post_output_dir,
        msmnts_per_pre_set, msmnts_per_post_set, max_set=8):
    """
    SEPARATE_PRE_AND_POST = 2
    Input: One TMG-formatted Excel file
    Output: Two CSV files holding, respectively,
            - all baseline measurements in the inputted Excel file,
            - all potentiated measurements in the inputted Excel file.
    All baseline measurements are clumped into one CSV file and all
    potentiated measurements are clumped into a separate CSV file.

    """
    xlsx_file = input_dir + xlsx_filename
    df = frontiers_utils.xlsx_to_pandas_df(xlsx_file)

    try:
      sets = _check_sets_before_conversion(xlsx_filename, df,
              msmnts_per_pre_set, msmnts_per_post_set)
    except:
        return
    msmnts_per_full_set = msmnts_per_pre_set + msmnts_per_post_set

    pre_col_nums, post_col_nums = [], []
    pre_headers, post_headers = [], []
    # I have hesitantly opted for 1-based indexing 
    # to align with physical sets and measurements.
    for s in range(1, sets + 1):
        if s > max_set:
            break
        for m in range(1, msmnts_per_pre_set + 1):
            col = (s - 1) * msmnts_per_full_set + m
            pre_col_nums.append(col)
            pre_headers.append("S{}-M{}".format(s, col))
        for m in range(1, msmnts_per_post_set + 1):
            col = (s - 1) * msmnts_per_full_set + m + msmnts_per_pre_set
            post_col_nums.append(col)
            post_headers.append("S{}-M{}".format(s, col))

    print("Pre-exercise column numbers: {}".format(pre_col_nums))
    print("Post-exercise column numbers: {}".format(post_col_nums))
    print()

    # Write CSV files
    df.to_csv(pre_output_dir + xlsx_filename.replace(".xlsx", "-pre.csv"),
            header=pre_headers, index=False, columns=pre_col_nums)
    df.to_csv(post_output_dir + xlsx_filename.replace(".xlsx", "-post.csv"),
            header=post_headers, index=False, columns=post_col_nums)


def split_by_pre_post_and_set(input_dir, xlsx_filename, 
        pre_output_dir, post_output_dir,
        msmnts_per_pre_set, msmnts_per_post_set, max_set=8):
    """
    PRE_POST_BY_SET_ALL_REPS
    Input: One TMG-formatted Excel file
    Output: FOR EACH MEASUREMENT SET in Excel file:
            - a file holding all pre-exercise measurements in that set.
            - a file holding all post-exercise measurements in that set.
            Net output: 2 * (number of sets in Excel file) CSV files.

    """
    xlsx_file = input_dir + xlsx_filename
    df = frontiers_utils.xlsx_to_pandas_df(xlsx_file)

    try:
      sets = _check_sets_before_conversion(xlsx_filename, df,
              msmnts_per_pre_set, msmnts_per_post_set)
    except:
        return
    msmnts_per_full_set = msmnts_per_pre_set + msmnts_per_post_set

    # Create an additional directory layer for each Excel file
    pre_output_dir = frontiers_utils.make_output_dir(pre_output_dir + xlsx_filename.replace(".xlsx", "")) + "/"
    post_output_dir = frontiers_utils.make_output_dir(post_output_dir + xlsx_filename.replace(".xlsx", "")) + "/"

    for s in range(1, sets + 1):
        if s > max_set:
            break
        print("Set Number: {}".format(s))

        pre_col_nums, post_col_nums = [], []
        pre_headers, post_headers = [], []

        # I have hesitantly opted for 1-based indexing 
        # to align with physical sets and measurements.
        for m in range(1, msmnts_per_pre_set + 1):
            col = (s - 1) * msmnts_per_full_set + m
            pre_col_nums.append(col)
            pre_headers.append("S{}-M{}".format(s, col))
        for m in range(1, msmnts_per_post_set + 1):
            col = (s - 1) * msmnts_per_full_set + m + msmnts_per_pre_set
            post_col_nums.append(col)
            post_headers.append("S{}-M{}".format(s, col))

        print("Pre-exercise column numbers: {}".format(pre_col_nums))
        print("Post-exercise column numbers: {}".format(post_col_nums))
        print()

        # Write CSV files for the current set
        df.to_csv(pre_output_dir + xlsx_filename.replace(".xlsx",
            "-pre-set-{}.csv".format(s)), header=pre_headers,
            index=False, columns=pre_col_nums)
        df.to_csv(post_output_dir + xlsx_filename.replace(".xlsx",
            "-post-set-{}.csv".format(s)), header=post_headers,
            index=False, columns=post_col_nums)


def split_by_pre_post_and_set_using_first_msmt(input_dir, xlsx_filename, 
        pre_output_dir, post_output_dir,
        msmnts_per_pre_set, msmnts_per_post_set, max_set=8):
    """
    PRE_POST_BY_SET_FIRST_REP
    Input: One TMG-formatted Excel file
    Output: Two CSV files:
            One file holds the FIRST pre-exercise measurement of each set.
            One file holds the FIRST post-exercise measurement of each set.
    The Excel file is divided into sets, and each set is further
    divided into pre-exercise and post-exercise measurements, but only
    the first measurement in each set is saved to the outputted CSV file.

    """
    xlsx_file = input_dir + xlsx_filename
    df = frontiers_utils.xlsx_to_pandas_df(xlsx_file)

    try:
      sets = _check_sets_before_conversion(xlsx_filename, df,
              msmnts_per_pre_set, msmnts_per_post_set)
    except:
        return
    msmnts_per_full_set = msmnts_per_pre_set + msmnts_per_post_set

    pre_col_nums, post_col_nums = [], []
    pre_headers, post_headers = [], []

    # I have hesitantly opted for 1-based indexing 
    # to align with physical sets and measurements.
    for s in range(1, sets + 1):
        if s > max_set:
            break
        pre_col = (s - 1) * msmnts_per_full_set + 1
        pre_col_nums.append(pre_col)
        pre_headers.append("S{}-M{}".format(s, pre_col))

        post_col = (s - 1) * msmnts_per_full_set + msmnts_per_pre_set + 1
        post_col_nums.append(post_col)
        post_headers.append("S{}-M{}".format(s, post_col))

    print("Pre-exercise column numbers: {}".format(pre_col_nums))
    print("Post-exercise column numbers: {}".format(post_col_nums))
    print()

    # Write CSV files
    df.to_csv(pre_output_dir + xlsx_filename.replace(".xlsx", "-pre.csv"),
            header=pre_headers, index=False, columns=pre_col_nums)
    df.to_csv(post_output_dir + xlsx_filename.replace(".xlsx", "-post.csv"),
            header=post_headers, index=False, columns=post_col_nums)


def _check_sets_before_conversion(xlsx_filename, raw_df, msmnts_per_pre_set, msmnts_per_post_set):
    """
    Cross-checks consistency the measurement structure in a raw Excel file 
    (inputted as Pandas DataFrame, but no matter) with the user-specified
    number of pre- and post-exercise measurements per set for the data in
    the inputted Excel file.
    In practice, this function helps check the inputted Excel file 
    for dropped measurements or other minor irregularities.

    The Excel filename is included only for logging purposes.
    """
    n_cols = raw_df.shape[1]
    msmnts_per_full_set = msmnts_per_pre_set + msmnts_per_post_set
    sets = n_cols/msmnts_per_full_set

    if not sets.is_integer():
        raise ValueError
        print("Aborting Excel to CSV conversion:")
        print("The measurement structure of the inputted Excel file ({})\n does not appear to agree with the inputted number of measurements per pre-exercise measurement set ({})\n and number of measurements per post-exercise measurement set ({})".format(xlsx_filename, msmnts_per_pre_set, msmnts_per_post_set))
        return None
    else:
        return int(sets)
