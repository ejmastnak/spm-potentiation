""" 
This script is used to:
- Compute TMG parameters for each subject's measurements
- Perform basic statistical analysis of TMG parameters across subjects
"""
import os
import numpy as np
import pandas as pd
from scipy.stats import ttest_rel
import constants, frontiers_utils

import tmg.tmg_params as tmg_params
import tmg.constants as tmg_constants

def compute_tmg_params_for_all_subjects():
    """
    Computes the TMG parameters for each subject's 
    pre- and post-ISQ TMG measurements.

    Input data: the per-subject TMG measurement files in constants.INITIAL_DATA_DIR
    Output: Per-subject parameter files in constants.TMG_PARAMS_BY_SUBJECT_DIR,
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


# Set-by-set TMG parameters averaged over subjects
def analyze_tmg_params_by_set(use_first_set_as_baseline=False):
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
        constants.TMG_PARAMS_BY_SUBJECT_DIR
    Output data: per-set CSV files in constants.TMG_PARAM_STATS_BY_SET_DIR
        summarizing the results of the above-described statisical analysis.

    Parameters
    ----------
    use_first_set_as_baseline : bool
        If True, the post-exercise measurement in each set is compared
        to the pre-exercise measurement in the FIRST set.

    """
    pre_input_dir = constants.TMG_PARAMS_BY_SUBJECT_DIR + "pre-exercise/"
    post_input_dir = constants.TMG_PARAMS_BY_SUBJECT_DIR + "post-exercise/"

    if use_first_set_as_baseline:
        output_dir = constants.TMG_PARAM_STATS_RELTO_SET1_DIR
    else:
        output_dir = constants.TMG_PARAM_STATS_BY_SET_DIR

    param_names = constants.TMG_PARAM_NAMES
    stats_names = constants.TMG_STAT_NAMES

    max_sets = 4
    num_params = len(param_names)
    num_subjects = 55

    # 3D Numpy arrays holding pre- and post-exercise parameter values
    # for all subjects, parameters, and measurement sets.
    pre_param_tensor = np.zeros((num_subjects, num_params, max_sets))
    post_param_tensor = np.zeros((num_subjects, num_params, max_sets))

    # Read pre-exercise params into 3D Numpy array
    for subj, filename in enumerate(frontiers_utils.natural_sort(os.listdir(pre_input_dir))):
        params = np.loadtxt(pre_input_dir + filename, skiprows=1, delimiter=',', usecols=(1, 2, 3, 4))
        pre_param_tensor[subj, :, :] = params

    # Read post-exercise params into 3D Numpy array
    for subj, filename in enumerate(frontiers_utils.natural_sort(os.listdir(post_input_dir))):
        params = np.loadtxt(post_input_dir + filename, skiprows=1, delimiter=',', usecols=(1, 2, 3, 4))
        post_param_tensor[subj, :, :] = params

    # Compute statistics across all subjects for each set
    for s in range(max_sets):
        if use_first_set_as_baseline:
            pre_avg = np.average(pre_param_tensor[:, :, 0], axis=0)
        else:
            pre_avg = np.average(pre_param_tensor[:, :, s], axis=0)
        post_avg = np.average(post_param_tensor[:, :, s], axis=0)

        # Uses ddof=1 for sample standard deviation
        if use_first_set_as_baseline:
            base_sd = np.std(pre_param_tensor[:, :, 0], axis=0, ddof=1)
        else:
            base_sd = np.std(pre_param_tensor[:, :, s], axis=0, ddof=1)
        pot_sd = np.std(post_param_tensor[:, :, s], axis=0, ddof=1)

      # Takes a paired (related) ttest
        if use_first_set_as_baseline:
            t_statistic, p_value = ttest_rel(pre_param_tensor[:, :, 0],
                    post_param_tensor[:, :, s], axis=0)
        else:
            t_statistic, p_value = ttest_rel(pre_param_tensor[:, :, s],
                    post_param_tensor[:, :, s], axis=0)

        # Convert Numpy arrays of stat results to a Pandas DataFrame, 
        # which is inefficient in principle but convenient 
        # when writing rows names to CSV files.
        df_stats = pd.DataFrame(np.column_stack([pre_avg, post_avg,
            base_sd, pot_sd,
            t_statistic, p_value]),
            index=param_names, columns=stats_names)

        if use_first_set_as_baseline:
            stats_output_file = output_dir + "setB1-P{}-tmg-stats.csv".format(s + 1)
        else:
            stats_output_file = output_dir + "set{}-tmg-stats.csv".format(s + 1)

        df_stats.to_csv(stats_output_file)


if __name__ == "__main__":
    compute_tmg_params_for_all_subjects()
    analyze_tmg_params_by_set()
    analyze_tmg_params_by_set(use_first_set_as_baseline=True)
