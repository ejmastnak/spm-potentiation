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

import tmg_biomechanics.tmg_params as tmg_params
import tmg_biomechanics.constants as tmg_constants

def compute_tmg_params_for_1mps_files():
    """
    Input: the per-subject TMG measurement files in `RAW_CSV_1MPS_DATA_DIR`

    Processing: compute TMG parameters for each TMG measurement

    Output: in `TMG_BY_SUBJECT_1MPS_DIR`, one pre/post-ISQ file per
    subject holding the TMG params from the first pre/post-ISQ measurement
    in each of the subjects measurement sets

    Output file structure:
    - Rows correspond to TMG/RDD parameters (e.g. Dm, Tc, etc...)
    - Columns correspond to measurements
    - Column headers specify:
      - Subject ID 
      - Measurement's set number
      - The measurement's number in the TMG Excel from the
        original measurement session (see `raw-data.md`)

    """
    pre_input_dir = constants.RAW_CSV_1MPS_DATA_DIR + "pre-exercise/"
    post_input_dir = constants.RAW_CSV_1MPS_DATA_DIR + "post-exercise/"
    pre_output_dir = constants.TMG_PARAMS_BY_SUBJECT_1MPS_DIR + "pre-exercise/"
    post_output_dir = constants.TMG_PARAMS_BY_SUBJECT_1MPS_DIR + "post-exercise/"

    _compute_tmg_params_for_files_in_dir(pre_input_dir, pre_output_dir)
    _compute_tmg_params_for_files_in_dir(post_input_dir, post_output_dir)


def compute_tmg_params_for_8mps_files():
    """
    Input: the per-subject subdirectories in `RAW_CSV_8MPS_DATA_DIR` and the
    per-measurement-set TMG measurement files within.

    Processing: compute TMG parameters for each TMG measurement.

    Output: in `TMG_PARAMS_BY_SUBJECT_1MPS_DIR`, one pre/post-ISQ
    subdirectory per subject. Inside this directory, create 1 file per
    measurement set containing TMG parameters for all measurements in that set.

    Output file structure: as in `compute_tmg_params_for_1mps_files`

    """
    pre_base_input_dir = constants.RAW_CSV_8MPS_DATA_DIR + "pre-exercise/"
    post_base_input_dir = constants.RAW_CSV_8MPS_DATA_DIR + "post-exercise/"
    pre_base_output_dir = constants.TMG_PARAMS_BY_SUBJECT_8MPS_DIR + "pre-exercise/"
    post_base_output_dir = constants.TMG_PARAMS_BY_SUBJECT_8MPS_DIR + "post-exercise/"

    # Loop through each pre-conditioning athlete directory
    for athlete_subdir in frontiers_utils.natural_sort(os.listdir(pre_base_input_dir)):
        pre_input_dir = pre_base_input_dir + athlete_subdir + "/"
        pre_output_dir = frontiers_utils.make_output_dir(pre_base_output_dir + athlete_subdir)
        _compute_tmg_params_for_files_in_dir(pre_input_dir, pre_output_dir)

    # Loop through each post-conditioning athlete directory
    for athlete_subdir in frontiers_utils.natural_sort(os.listdir(post_base_input_dir)):
        post_input_dir = post_base_input_dir + athlete_subdir + "/"
        post_output_dir = frontiers_utils.make_output_dir(post_base_output_dir + athlete_subdir)
        _compute_tmg_params_for_files_in_dir(post_input_dir, post_output_dir)


def _compute_tmg_params_for_files_in_dir(input_dir, output_dir, max_sets=8):
    """
    Computes TMG parameters for all TMG measurement files in `input_dir` and
    writes the parameters to files in `output_dir`, mapping each measurement
    file in `input_dir` to a corresponding parameter file in `output_dir`.
    """
    for filename in frontiers_utils.natural_sort(os.listdir(input_dir)):

        # Measurement CSV files are first read into Pandas DataFrames
        # instead of directly into Numpy arrays for easier access to 
        # the header row than Numpy's `loadtxt` would allow.
        df = pd.read_csv(input_dir + filename, sep=',', header=0)
        column_headers = df.columns.values.tolist()
        data = df.to_numpy()

        # 2D Numpy array to hold TMG params across all four sets
        param_array = np.zeros([len(tmg_constants.TMG_PARAM_NAMES), max_sets])
        for m in range(max_sets):
            tmg_signal = data[:, m]
            param_array[:, m] = tmg_params.get_params_of_tmg_signal(tmg_signal)

        param_df = pd.DataFrame(param_array,
                columns=column_headers,
                index=tmg_constants.TMG_PARAM_NAMES)
        output_filename = filename.replace(".csv", "-tmg-params.csv")
        param_df.to_csv(output_dir + output_filename)


# Set-by-set TMG parameters averaged over subjects
def analyze_tmg_params_across_subjects(use_first_set_as_baseline=False):
    """
    Input data: the per-subject parameter files in
        constants.TMG_PARAMS_BY_SUBJECT_1MPS_DIR

    For a given measurement set:
    - Computes mean pre-ISQ and post-ISQ value of each TMG parameter,
      averaged across all subjects.
    - Computes sample standard deviation of pre-ISQ and post-ISQ 
      value of each TMG parameter across all subjects.
    - Performs a dependent, paired-sample Student's t-test comparing
      the pre-ISQ and post-ISQ values of each TMG parameter across
      all subjects, and saves the t-statistic and corresponding p-value.

    Output data: per-set CSV files in
    constants.TMG_STATS_ACROSS_SUBJECTS_DIR summarizing the results of the
    above-described statisical analysis.

    Parameters
    ----------
    use_first_set_as_baseline : bool
        If True, the post-exercise measurement in each set is compared
        to the pre-exercise measurement in the FIRST set.

    """
    pre_input_dir = constants.TMG_PARAMS_BY_SUBJECT_1MPS_DIR + "pre-exercise/"
    post_input_dir = constants.TMG_PARAMS_BY_SUBJECT_1MPS_DIR + "post-exercise/"

    if use_first_set_as_baseline:
        output_dir = constants.TMG_STATS_ACROSS_SUBJECTS_RELTO_BASELINE_DIR
    else:
        output_dir = constants.TMG_STATS_ACROSS_SUBJECTS_DIR

    param_names = constants.TMG_PARAM_NAMES
    stats_names = constants.TMG_STAT_NAMES

    max_sets = 8
    num_params = len(param_names)
    num_subjects = 54

    # Columns in param files to analyze; skip first column which contains
    # only parameter names.
    usecols = tuple(range(1, 1 + max_sets))

    # 3D Numpy arrays holding pre- and post-exercise parameter values
    # for all subjects, parameters, and measurement sets.
    pre_param_tensor = np.zeros((num_subjects, num_params, max_sets))
    post_param_tensor = np.zeros((num_subjects, num_params, max_sets))

    # Read pre-exercise params into 3D Numpy array
    for subj, filename in enumerate(frontiers_utils.natural_sort(os.listdir(pre_input_dir))):
        params = np.loadtxt(pre_input_dir + filename, skiprows=1, delimiter=',', usecols=usecols)
        pre_param_tensor[subj, :, :] = params

    # Read post-exercise params into 3D Numpy array
    for subj, filename in enumerate(frontiers_utils.natural_sort(os.listdir(post_input_dir))):
        params = np.loadtxt(post_input_dir + filename, skiprows=1, delimiter=',', usecols=usecols)
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
            pre_sd = np.std(pre_param_tensor[:, :, 0], axis=0, ddof=1)
        else:
            pre_sd = np.std(pre_param_tensor[:, :, s], axis=0, ddof=1)
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
            pre_sd, pot_sd,
            t_statistic, p_value]),
            index=param_names, columns=stats_names)

        if use_first_set_as_baseline:
            stats_output_file = output_dir + "setB1-P{}-tmg-stats.csv".format(s + 1)
        else:
            stats_output_file = output_dir + "set{}-tmg-stats.csv".format(s + 1)

        df_stats.to_csv(stats_output_file)


def analyze_tmg_params_by_athlete_8mps():
    """
    Input data: the per-subject subdirectories in
    constants.TMG_PARAMS_BY_SUBJECT_8MPS_DIR and the parameter files within.

    For a given subject and measurement set:
    - Computes mean pre-ISQ and post-ISQ value of each TMG parameter
      in the measurement set
    - Computes sample standard deviation of pre-ISQ and post-ISQ 
      value of each TMG parameter in the measurement set
    - Performs a dependent, paired-sample Student's t-test comparing 
      the pre-ISQ and post-ISQ values of each TMG parameter and saves
      the t-statistic and corresponding p-value.

    Output data: per-subject subdirectories in
    constants.TMG_STATS_BY_ATHLETE_8MPS_DIR holding per-measurement set
    files summarizing the results of the above-described statisical
    analysis.

    """
    pre_base_input_dir = constants.TMG_PARAMS_BY_SUBJECT_8MPS_DIR + "pre-exercise/"
    post_base_input_dir = constants.TMG_PARAMS_BY_SUBJECT_8MPS_DIR + "post-exercise/"
    output_base_dir = constants.TMG_STATS_BY_ATHLETE_8MPS_DIR

    param_names = constants.TMG_PARAM_NAMES
    stats_names = constants.TMG_STAT_NAMES

    max_sets = 8
    num_params = len(param_names)
    num_subjects = 54

    # Columns in param files to analyze; skip first column which contains
    # only parameter names.
    usecols = tuple(range(1, 1 + max_sets))

    pre_subject_subdirs = frontiers_utils.natural_sort(os.listdir(pre_base_input_dir))
    post_subject_subdirs = frontiers_utils.natural_sort(os.listdir(post_base_input_dir))

    # Loop through all subjects
    for subj in range(len(pre_subject_subdirs)):
        pre_input_dir = pre_base_input_dir + pre_subject_subdirs[subj] + "/"
        post_input_dir = post_base_input_dir + post_subject_subdirs[subj] + "/"
        output_dir = frontiers_utils.make_output_dir(output_base_dir + pre_subject_subdirs[subj])

        pre_filenames = frontiers_utils.natural_sort(os.listdir(pre_input_dir))
        post_filenames = frontiers_utils.natural_sort(os.listdir(post_input_dir))

        # For a given subject, loop through all measurement sets
        for s in range(max_sets):
            pre_filename = pre_filenames[s]
            post_filename = post_filenames[s]
            output_file = output_dir + "set-{}.csv".format(s + 1)

            pre_params = np.loadtxt(pre_input_dir + pre_filename, skiprows=1, delimiter=',', usecols=usecols)
            post_params = np.loadtxt(post_input_dir + post_filename, skiprows=1, delimiter=',', usecols=usecols)

    # || ValueError: Shape of passed values is (8, 6), indices imply (14, 6)

            # Compare pre-ISQ and post-ISQ parameters
            pre_avg = np.average(pre_params, axis=1)
            post_avg = np.average(post_params, axis=1)
            pre_sd = np.std(pre_params, axis=1, ddof=1)
            pot_sd = np.std(post_params, axis=1, ddof=1)
            t_statistic, p_value = ttest_rel(pre_params, post_params, axis=1)

            # Convert Numpy arrays of stat results to a Pandas DataFrame, 
            # which is inefficient in principle but convenient 
            # when writing rows names to CSV files.
            df_stats = pd.DataFrame(np.column_stack([pre_avg, post_avg,
                pre_sd, pot_sd,
                t_statistic, p_value]),
                index=param_names, columns=stats_names)
            df_stats.to_csv(output_file)


if __name__ == "__main__":
    compute_tmg_params_for_1mps_files()
    compute_tmg_params_for_8mps_files()
    analyze_tmg_params_across_subjects()
    analyze_tmg_params_across_subjects(use_first_set_as_baseline=True)
    analyze_tmg_params_by_athlete_8mps()
