""" 
This script is used to:
- Compute TMG parameters for each subject's measurements
- Perform basic statistical analysis of TMG parameters across subjects
"""
import numpy as np
import pandas as pd
import os
import constants, frontiers_utils

import tmg.tmg_params as tmg_params
import tmg.constants as tmg_constants

def compute_tmg_params_for_all_subjects():
    """
    Computes the TMG parameters for each subject's 
    pre- and post-ISQ TMG measurements.

    Input data: the per-subject TMG measurement files in `/data/csv-for-initial-analysis/`
    Output: Per-subject parameter files in `/output/tmg-params-by-subject/`,
        with a separate file for pre-ISQ and post-ISQ parameters.
        Output file structure:
        - Rows correspond to TMG/RDD parameters (e.g. Dm, Tc, etc...)
        - Columns correspond to measurements
        - Column headers specify:
          - Subject ID 
          - Measurement's set number
          - The measurement's number in the TMG Excel from the
            original measurement session (see `raw-data.md`)

    """
    input_dirs = [constants.INITIAL_DATA_DIR + "pre-exercise/", 
            constants.INITIAL_DATA_DIR + "post-exercise/"]
    output_dirs = [constants.TMG_PARAMS_BY_SUBJECT_DIR + "pre-exercise/", 
            constants.TMG_PARAMS_BY_SUBJECT_DIR + "post-exercise/"]

    # Process both pre- and post-exercise data using the same code
    for i in range(2):
        for filename in frontiers_utils.natural_sort(os.listdir(input_dirs[i])):
            # Measurement CSV files are first read into Pandas DataFrames
            # instead of directly into Numpy arrays for easier access to 
            # the header row than Numpy's `loadtxt` would allow.

            df = pd.read_csv(input_dirs[i] + filename, sep=',', header=0)
            column_headers = df.columns.values.tolist()
            data = df.to_numpy()

            # 2D Numpy array to hold TMG params across all four sets
            param_array = np.zeros([len(tmg_constants.TMG_PARAM_NAMES), 4])
            for m in range(4):
                tmg_signal = data[:, m]
                param_array[:, m] = tmg_params.get_params_of_tmg_signal(tmg_signal)

            param_df = pd.DataFrame(param_array,
                    columns=column_headers,
                    index=tmg_constants.TMG_PARAM_NAMES)
            output_filename = filename.replace(".csv", "-tmg-params.csv")
            param_df.to_csv(output_dirs[i] + output_filename)


def get_params_of_tmg_file(input_dir, xlsx_filename, output_dir,
        column_mode, base_msmts=1, pot_msmts=1, max_set=8):
    """
    Computes the TMG and RDD parameters of for the raw TMG measurements
    stored in a standard TMG Excel measurement file.
    See documentation of conversion constants in `constants.py`.

    Parameters
    ----------
    input_dir : str
        Parent directory holding the TMG Excel file
    xlsx_filename : str
        File name of the Excel file, excluding full path but including extension
    output_dir : str
        Output directory in which to write parameter files CSV files
    column_mode : int
        One of the conversion mode constants documented in `constants.py`
    base_msmts : int
        The number of baseline measurements per set in the Excel file
    pot_msmts : int
        The number of potentiated measurements per set in the Excel file
    max_set : int
        Ignore sets in Excel file above this set number.

    """
    xlsx_file = input_dir + xlsx_filename
    subject_id = io_utils.get_subject_ID_from_filename(xlsx_filename)

    # Read measurements from Excel file into a pandas dataframe
    df = io_utils.xlsx_to_pandas_df(xlsx_file)

    n_cols = df.shape[1]
    msmts_per_set = base_msmts + pot_msmts
    sets = n_cols/msmts_per_set

    if not sets.is_integer():
        print("Error: Non-integer number of measurements per sets.")
        print("Aborting")
        return
    else:
        sets = int(sets)

    col_names = []
    row_names = constants.TMG_PARAM_NAMES

    # First add parameters to a list, then create a DataFrame from the list
    param_list = []

    if column_mode == constants.VERBATIM:
        # Loop through each measurement number and TMG signal in Excel file
        for (m, tmg) in df.iteritems():

            # Determine if measurement is baseline or potentiated
            if 1 <= m % (msmts_per_set) <= base_msmts:  # baseline
                base_pot = "B"
            else:  # potentiated
                base_pot = "P"

            # Set and measurement number of each measurement
            col_names.append("ID{}-S{}-M{}-{}".format(subject_id, 
                int((m - 1)/msmts_per_set) + 1, m, base_pot))

            params = get_params_of_tmg_signal(tmg.to_numpy())
            param_list.append(params)

        param_df = pd.DataFrame(param_list).transpose()
        param_df.columns=col_names
        param_df.index=row_names
        param_df.to_csv(output_dir + xlsx_filename.replace(".xlsx", "-rdd-params.csv"))

    elif column_mode == constants.PRE_POST_BY_SET_FIRST_REP:
        for set in range(1, sets + 1):
            if set > max_set:
                break

            base_col = df.iloc[:, (set - 1) * msmts_per_set]
            col_names.append("ID{}-S{}-M{}-B".format(subject_id, set, base_col.name))
            params = get_params_of_tmg_signal(base_col.to_numpy())
            param_list.append(params)

            pot_col = df.iloc[:, (set - 1) * msmts_per_set + base_msmts]
            col_names.append("ID{}-S{}-M{}-P".format(subject_id, set, pot_col.name))
            params = get_params_of_tmg_signal(pot_col.to_numpy())
            param_list.append(params)

        param_df = pd.DataFrame(param_list).transpose()
        param_df.columns=col_names
        param_df.index=row_names
        param_df.to_csv(output_dir + xlsx_filename.replace(".xlsx", "-rdd-params.csv"))


# Set-by-set TMG parameters averaged over subjects
"""
For a given measurement set:
- Computes mean pre-ISQ and post-ISQ value of each TMG parameter,
  averaged across all subjects.
- Computes sample standard deviation of pre-ISQ and post-ISQ 
  value of each TMG parameter across all subjects.
- Performs a dependent, paired-sampled Student's t-test comparing
  the pre-ISQ and post-ISQ values of each TMG parameter across
  all subjects, and saves the t-statistic and corresponding p-value.

Input data: the per-subject parameter files in
    `/output/tmg-params-by-subject/`..
Output data: per-set CSV files in `/output/tmg-param-stats-by-set/`
    summarizing the results of the above-described statisical analysis.

"""

# Staggered TMG parameters averaged over subjects
"""
For a given measurement set:
- Performs the same mean and sample standard calculation for each TMG parameter
  as described above in the function TODO.

- Performs a dependent, paired-sampled Student's t-test comparing
  the pre-ISQ values of each TMG parameter from the FIRST measurement set
  to the post-ISQ values of each TMG parameter from sets 1, 2, 3, 4
  all subjects, and saves the t-statistic and corresponding p-value.

Input data: the per-subject parameter files in
    `/output/tmg-params-by-subject/`..
Output data: per-set CSV files in `/output/tmg-param-stats-staggered/`
    summarizing the results of the above-described statisical analysis.

"""

def practice():
    filename = "/home/ej/Media/tmg-bmc-media/frontiers-2022/data/csv-for-initial-analysis/post-exercise/1-BR20200910125909-post.csv"
    df = pd.read_csv(filename, sep=',', header=0)
    column_headers = df.columns.values.tolist()
    data = df.to_numpy()

    # 2D Numpy array to hold TMG params across all four sets
    param_array = np.zeros([len(tmg_constants.TMG_PARAM_NAMES), 4])
    for m in range(4):
        tmg_signal = data[:, m]
        param_array[:, m] = tmg_params.get_params_of_tmg_signal(tmg_signal)

    df = pd.DataFrame(param_array,
            columns=column_headers,
            index=tmg_constants.TMG_PARAM_NAMES)
    df.to_csv("~/test.csv")


if __name__ == "__main__":
    compute_tmg_params_for_all_subjects()
    # practice()
