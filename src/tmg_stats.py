import os
import numpy as np
import pandas as pd
from scipy.stats import ttest_rel
import constants, frontiers_utils
import tmg_biomechanics.tmg_params as tmg_params_pypi
import tmg_biomechanics.constants as tmg_constants

""" 
This script is used to:
- Compute TMG parameters for each subject's measurements
- Perform basic statistical analysis of TMG parameters across subjects

IMPORTANT: this script relies on TMG parameters computed in `tmg_params.py`.
You should run `tmg_params.py` before running this script.

"""

# Set-by-set TMG parameters averaged over subjects
def tmg_stats_by_set_across_subj_1mps(first_set_as_baseline=False):
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
    first_set_as_baseline : bool
        If True, the post-conditioning measurement in each set is compared
        to the pre-conditioning measurement in the FIRST set.

    """
    pre_input_dir = constants.TMG_PARAMS_BY_SUBJ_1MPS_DIR + "pre-conditioning/"
    post_input_dir = constants.TMG_PARAMS_BY_SUBJ_1MPS_DIR + "post-conditioning/"

    if first_set_as_baseline:
        output_dir = constants.TMG_STATS_BY_SET_ACROSS_SUBJ_RELTO_BASELINE_DIR
    else:
        output_dir = constants.TMG_STATS_BY_SET_ACROSS_SUBJ_DIR

    param_names = constants.TMG_PARAM_NAMES
    stats_names = constants.TMG_STAT_NAMES

    max_sets = 8
    num_params = len(param_names)
    num_subjects = 54

    # Columns in param files to analyze; skip first column which contains
    # only parameter names.
    usecols = tuple(range(1, 1 + max_sets))

    # 3D Numpy arrays holding pre- and post-conditioning parameter values
    # for all subjects, parameters, and measurement sets.
    pre_param_tensor = np.zeros((num_subjects, num_params, max_sets))
    post_param_tensor = np.zeros((num_subjects, num_params, max_sets))

    # Read pre-conditioning params into 3D Numpy array
    for subj, filename in enumerate(frontiers_utils.natural_sort(os.listdir(pre_input_dir))):
        params = np.loadtxt(pre_input_dir + filename, skiprows=1, delimiter=',', usecols=usecols)
        pre_param_tensor[subj, :, :] = params

    # Read post-conditioning params into 3D Numpy array
    for subj, filename in enumerate(frontiers_utils.natural_sort(os.listdir(post_input_dir))):
        params = np.loadtxt(post_input_dir + filename, skiprows=1, delimiter=',', usecols=usecols)
        post_param_tensor[subj, :, :] = params

    # Compute statistics across all subjects for each set
    for s in range(max_sets):
        post_params = post_param_tensor[:, :, s].T
        if first_set_as_baseline:
            pre_params = pre_param_tensor[:, :, 0].T
            output_file = output_dir + "set-B1-P{}-tmg-stats.csv".format(s + 1)
        else:
            pre_params = pre_param_tensor[:, :, s].T
            output_file = output_dir + "set-{}-tmg-stats.csv".format(s + 1)
        print("Analyzing across subjects for set {}".format(s + 1))
        _compute_stats_for_tmg_params(pre_params, post_params, output_file)


def tmg_stats_by_subj_by_set_8mps():
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
    pre_base_input_dir = constants.TMG_PARAMS_BY_SUBJ_8MPS_DIR + "pre-conditioning/"
    post_base_input_dir = constants.TMG_PARAMS_BY_SUBJ_8MPS_DIR + "post-conditioning/"
    output_base_dir = constants.TMG_STATS_BY_SUBJ_BY_SET_8MPS_DIR

    param_names = constants.TMG_PARAM_NAMES
    stats_names = constants.TMG_STAT_NAMES
    max_sets = 8

    # Columns in param files to analyze; skip first column which contains
    # only parameter names.
    usecols = tuple(range(1, 1 + max_sets))

    pre_subject_subdirs = frontiers_utils.natural_sort(os.listdir(pre_base_input_dir))
    post_subject_subdirs = frontiers_utils.natural_sort(os.listdir(post_base_input_dir))

    # Loop through all subjects
    for subj in range(len(pre_subject_subdirs)):
        pre_input_dir = pre_base_input_dir + pre_subject_subdirs[subj] + "/"
        post_input_dir = post_base_input_dir + post_subject_subdirs[subj] + "/"
        output_dir = frontiers_utils.make_output_dir(output_base_dir + pre_subject_subdirs[subj],
                use_existing=True) + "/"

        pre_filenames = frontiers_utils.natural_sort(os.listdir(pre_input_dir))
        post_filenames = frontiers_utils.natural_sort(os.listdir(post_input_dir))

        # For a given subject, loop through all measurement sets
        for s in range(max_sets):
            pre_filename = pre_filenames[s]
            post_filename = post_filenames[s]
            output_file = output_dir + "set-{}-tmg-stats.csv".format(s + 1)

            pre_params = np.loadtxt(pre_input_dir + pre_filename, skiprows=1, delimiter=',', usecols=usecols)
            post_params = np.loadtxt(post_input_dir + post_filename, skiprows=1, delimiter=',', usecols=usecols)

            print("Analyzing set {} for {}".format(s + 1, pre_subject_subdirs[subj]))
            _compute_stats_for_tmg_params(pre_params, post_params, output_file)


def tmg_stats_by_subj_across_sets_1mps():
    """
    Input data: the per-subject parameter files in
        constants.TMG_PARAMS_BY_SUBJECT_1MPS_DIR

    For a given subject
    - Computes mean pre-ISQ and post-ISQ value of each TMG parameter
      across all measurement sets
    - Computes sample standard deviation of pre-ISQ and post-ISQ 
      value of each TMG parameter across all measurement sets
    - Performs a dependent, paired-sample Student's t-test comparing 
      the pre-ISQ and post-ISQ values of each TMG parameter and saves
      the t-statistic and corresponding p-value.

    Output data: per-subject files in TMG_STATS_BY_SUBJ_ACROSS_SETS_1MPS_DIR
    summarizing the results of the above-described statisical analysis.

    """
    pre_input_dir = constants.TMG_PARAMS_BY_SUBJ_1MPS_DIR + "pre-conditioning/"
    post_input_dir = constants.TMG_PARAMS_BY_SUBJ_1MPS_DIR + "post-conditioning/"
    output_dir = constants.TMG_STATS_BY_SUBJ_ACROSS_SETS_1MPS_DIR

    max_sets = 8

    # Columns in param files to analyze; skip first column which contains
    # only parameter names.
    usecols = tuple(range(1, 1 + max_sets))

    pre_filenames = frontiers_utils.natural_sort(os.listdir(pre_input_dir))
    post_filenames = frontiers_utils.natural_sort(os.listdir(post_input_dir))

    for subj in range(len(pre_filenames)):
        pre_params = np.loadtxt(pre_input_dir + pre_filenames[subj], skiprows=1, delimiter=',', usecols=usecols)
        post_params = np.loadtxt(post_input_dir + post_filenames[subj], skiprows=1, delimiter=',', usecols=usecols)
        output_file = output_dir + pre_filenames[subj].replace("pre-tmg-params.csv", "tmg-stats.csv")

        print("Analyzing across sets for {}".format(pre_filenames[subj]).replace("-pre-tmg-params.csv", ""))
        _compute_stats_for_tmg_params(pre_params, post_params, output_file)


def _compute_stats_for_tmg_params(pre_params, post_params, output_file):
    """
    Performs a simple statistical analysis comparing all TMG parameters in
    `pre_params` to the TMG parameters in `post_params` and writes the
    results to `output_file`.

    Shape: `pre_params` and `post_params` should have TMG parameters in rows
    and measurements in columns. The measurements should be in the same
    order as `constants.TMG_PARAM_NAMES`, i.e.
    ["Dm:", "Td:", "Tc:", "Ts:", "Tr:", "P1:", "P2:", "P3:",
        "RDD Max:", "RDD Min:", "RDD Peak to Peak:",
        "RDD Max Time:", "RDD Min Time:", "Max to Min Time:"]

    """
    param_names = constants.TMG_PARAM_NAMES
    stats_names = constants.TMG_STAT_NAMES

    # Compare pre-ISQ and post-ISQ parameters
    pre_avg = np.average(pre_params, axis=1)
    post_avg = np.average(post_params, axis=1)

    percent_change = 100 * (post_avg - pre_avg) / pre_avg

    pre_sd = np.std(pre_params, axis=1, ddof=1)
    post_sd = np.std(post_params, axis=1, ddof=1)

    t_statistic, p_value = ttest_rel(post_params, pre_params, axis=1)

    # Convert Numpy arrays of stat results to a Pandas DataFrame, 
    # which is inefficient in principle but convenient 
    # when writing rows names to CSV files.
    df_stats = pd.DataFrame(np.column_stack([pre_avg, post_avg,
        percent_change,
        pre_sd, post_sd,
        t_statistic, p_value]),
        index=param_names, columns=stats_names)
    df_stats.to_csv(output_file)
    

if __name__ == "__main__":
    tmg_stats_by_set_across_subj_1mps()
    tmg_stats_by_set_across_subj_1mps(first_set_as_baseline=True)
    tmg_stats_by_subj_by_set_8mps()
    tmg_stats_by_subj_across_sets_1mps()
