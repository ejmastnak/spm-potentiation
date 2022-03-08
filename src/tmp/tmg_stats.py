import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import ttest_rel
from scipy.interpolate import lagrange
import os
import io_utils
import constants

"""
A collection of functions used to perform statistical analysis on of TMG 
parameters in an 8 (or variable)-set, 8-rep measurement protocol intended 
for SPM analysis.
"""

def analyze_tmg_params(data_dir, param_table_output_dir, 
        param_stats_output_dir, max_sets=8):
    """
    Functionality:
        - For a given set, creates tables of TMG and RDD 
          parameter values for all subjects.
          See "media/potentiation-2021/output/rdd-param-tables/" for examples
        - For a given set, performs statistical analysis of TMG and RDD
          parameter values across all subjects.
          See "media/potentiation-2021/output/rdd-param-stats/" for examples

    Parameters
    ----------
    data_dir : str
        Path to directory containing TMG and RDD parameter tables for each subject.
        See example input files in "tmg-bmc-media/potentiation-2021/output/raw-rdd-params"
        Important: data_dir must not contain any "dropped" files with problematic measurements.
    
        Assumed file naming convention: "{subject-ID}-{TMG-format-name}-rdd-params"
        Example: "1-BR20200910125909-rdd-params.csv"

        Assumed file format: CSV file with one row for each parameter,
                              one column per analyzed measurement,
                              and one header row with the set number and
                              measurement number of each analyzed measurement.
                              Headers should be in the form:
                              ID{id-number}-S{set-num}-M{measurement-num}-{B|P}
        Example:
                ,Header1,Header2,Header3,...,Header16
            Dm: ,8.152,9.269,8.231,...,9.105
            Td: ,8.152,9.269,8.231,...,9.105
            # and so on for all parameters
    max_sets : int
        Number of sets to analyze per subject.
        The function assumes the existence of exactly one baseline 
        and one potentiated measurement per set in each parameter file.

    Outputs
    -------
    The following output files for all 8 sets
        - set{set-num}-rdd-stats.csv for {set-num} = 1, 2, ..., max_sets
        - set{set-num}B-rdd-params.csv for {set-num} = 1, 2, ..., max_sets
        - set{set-num}P-rdd-params.csv for {set-num} = 1, 2, ..., max_sets

    setX-rdd-stats.csv: statistical analysis of TMG and RDD parameters in set X
                        averaged across all subjects. 
                        See README.md in `output/rdd-param-stats/README.md`
    
    setXB-rdd-params.csv: Table of baseline TMG and RDD parameters 
                          in set X for all subjects.
                          See README.md in `output/rdd-param-tables/README.md`
    
    setXP-rdd-params.csv: Table of potentiated TMG and RDD parameters 
                          in set X for all subjects.
                          See README.md in `output/rdd-param-tables/README.md`
    
    """
    param_names = constants.TMG_PARAM_NAMES
    stats_names = constants.TMG_STAT_NAMES
    num_params = len(param_names)

    param_files = []
    for file in io_utils.natural_sort(os.listdir(data_dir)):
        if "-rdd-params.csv" in file:
            param_files.append(file)
    subject_ids = []
    for file in param_files:
        subject_ids.append(io_utils.get_subject_ID_from_filename(file))
    num_subjects = len(param_files)

    # 3D Numpy arrays holding baseline and potentiated parameter values for
    # all parameters, subjects, and measurement sets.
    base_tensor = np.zeros((num_params, num_subjects, max_sets))
    pot_tensor = np.zeros((num_params, num_subjects, max_sets))

    # 2D Python lists holding column names for each subject
    base_headers, pot_headers = [], []

    for (subject_index, file) in enumerate(param_files):
        print(file)
        # Read parameter CSV file in pandas DataFrame, using first row 
        # as column names and first column as row names
        df = pd.read_csv(data_dir + file, header=0, index_col=0)
        params_in_file = df.values

        # 2D array: 14 rows for each param and max_set columns for each baseline measurements
        base_params_in_file = params_in_file[:, ::2]  
        base_headers.append(df.columns[::2])

        # 2D array: 14 rows for each param and max_set columns for each potentiated measurements
        pot_params_in_file = params_in_file[:, 1::2]  
        pot_headers.append(df.columns[1::2])

        # Accumulate baseline and potentiated parameters in 3D tensors for all files.
        # Example slicing: base_params[:, s] holds all baseline parameters
        # in the s-th (assuming 0-index) set of base_params.
        for set in range(max_sets):
            base_tensor[:, subject_index, set] = base_params_in_file[:, set]
            pot_tensor[:, subject_index, set] = pot_params_in_file[:, set]

    # Transpose headers so as to have each row (or the first index) correspond to a set
    # and each column (or the second index) correspond to a subject.
    base_headers = list(map(list, zip(*base_headers)))
    pot_headers = list(map(list, zip(*pot_headers)))

    for set in range(max_sets):
        base_header = base_headers[set]
        pot_header = pot_headers[set]

        base_avg = np.average(base_tensor[:, :, set], axis=1)
        pot_avg = np.average(pot_tensor[:, :, set], axis=1)

        # Uses ddof=1 for sample standard deviation
        base_sd = np.std(base_tensor[:, :, set], axis=1, ddof=1)
        pot_sd = np.std(pot_tensor[:, :, set], axis=1, ddof=1)

      # Takes a paired (related) ttest
        t_statistic, p_value = ttest_rel(base_tensor[:, :, set],
                pot_tensor[:, :, set], axis=1)

        # Convert Numpy arrays to Pandas dataframes, which is computationally bloated
        # but convenient for writing rows names to CSV files.
        df_base = pd.DataFrame(base_tensor[:, :, set], index=param_names,
                columns=base_header)
        df_pot = pd.DataFrame(pot_tensor[:, :, set], index=param_names,
                columns=pot_header)
        df_stats = pd.DataFrame(np.column_stack([base_avg, pot_avg, base_sd,
            pot_sd, t_statistic, p_value]), index=param_names, columns=stats_names)

        base_output_file = param_table_output_dir + "set{}-base-rdd-params.csv".format(set + 1)
        pot_output_file = param_table_output_dir + "set{}-pot-rdd-params.csv".format(set + 1)
        stats_output_file = param_stats_output_dir + "set{}-rdd-stats.csv".format(set + 1)

        df_base.to_csv(base_output_file)
        df_pot.to_csv(pot_output_file)
        df_stats.to_csv(stats_output_file)


def analyze_tmg_stats_staggered(data_dir, output_dir, sets_to_analyze):
    """
    For a given set, performs statistical analysis of TMG and RDD
    parameter values across all subjects like for analyze_tmg_rdd_params,
    but with the following difference: Baseline state is always taken to be set 1
    Comparisons are e.g. (B1, P1), (B1, P2), (B1, P3), (B1, P4), etc...

    See "media/potentiation-2021/output/rdd-param-stats/" for examples

    Parameters
    ----------
    data_dir : str
        Path to directory containing TMG and RDD parameter tables for each subject.
        See example input files in "tmg-bmc-media/potentiation-2021/output/raw-rdd-params"
        Important: data_dir must not contain any "dropped" files with problematic measurements.
    
        Assumed file naming convention: "{subject-ID}-{TMG-format-name}-rdd-params"
        Example: "1-BR20200910125909-rdd-params.csv"

        Assumed file format: CSV file with one row for each parameter,
                              one column per analyzed measurement,
                              and one header row with the set number and
                              measurement number of each analyzed measurement.
                              Headers should be in the form:
                              ID{id-number}-S{set-num}-M{measurement-num}-{B|P}
        Example:
                ,Header1,Header2,Header3,...,Header16
            Dm: ,8.152,9.269,8.231,...,9.105
            Td: ,8.152,9.269,8.231,...,9.105
            # and so on for all parameters

        The function assumes the existence of exactly one baseline 
        and one potentiated measurement per set in each parameter file.

    output_dir : str
        Path to directory in which to write outputted CSV files
    
    sets_to_analyze : tuple
        A tuple of integers containing the set numbers to analyze (using 1-based
        indexing for sets).
        The first set in `sets_to_analyze` is used as the baseline for all sets.
        Example: (1, 2, 3) will produce a statistical analysis of the form
                 (B1, P1), (B1, P2), (B1, P3)
        The maximum set number in `sets_to_analyze` 
        should be less than `sets_per_subject`.

    Outputs
    -------
    The following output files: files of the form 
    `setB{1}-P{set-num}-rdd-stats.csv` for all {set-num} in `sets_to_analyze`
    See README.md in `output/rdd-param-stats/README.md`
    
    """
    param_names = constants.TMG_PARAM_NAMES
    stats_names = constants.TMG_STAT_NAMES
    num_params = len(param_names)

    param_files = []
    for file in io_utils.natural_sort(os.listdir(data_dir)):
        if "-rdd-params.csv" in file:
            param_files.append(file)
    num_subjects = len(param_files)

    # 3D Numpy arrays holding baseline and potentiated parameter values for
    # all parameters, subjects, and measurement sets to analyze.
    base_tensor = np.zeros((num_params, num_subjects, len(sets_to_analyze)))
    pot_tensor = np.zeros((num_params, num_subjects, len(sets_to_analyze)))

    # Loop through parameter files for each subject
    for (subject_index, file) in enumerate(param_files):
        # Read parameter CSV file in pandas DataFrame, using first row 
        # as column names and first column as row names
        df = pd.read_csv(data_dir + file, header=0, index_col=0)
        params_in_file = df.values

        # 2D array: 14 rows for each param and 8 columns for each baseline measurements
        base_params_in_file = params_in_file[:, ::2]  

        # 2D array: 14 rows for each param and 8 columns for each potentiated measurements
        pot_params_in_file = params_in_file[:, 1::2]  

        # Accumulate baseline and potentiated parameters in 3D tensors for all files.
        # `set_index` takes on the values 0, 1, ..., len(sets_to_analyze)
        # `set` takes on the values `sets_to_analyze` and uses 1-based indexing
        for set_index, set in enumerate(sets_to_analyze):
            base_tensor[:, subject_index, set_index] = base_params_in_file[:, set-1]
            pot_tensor[:, subject_index, set_index] = pot_params_in_file[:, set-1]

    for set_index, set in enumerate(sets_to_analyze):
        # Note use of 0 as base_tensor set index to 
        # always use first set in `sets_to_analyze`
        base_avg = np.average(base_tensor[:, :, 0], axis=1)
        pot_avg = np.average(pot_tensor[:, :, set_index], axis=1)

        # Uses ddof=1 for sample standard deviation
        base_sd = np.std(base_tensor[:, :, 0], axis=1, ddof=1)
        pot_sd = np.std(pot_tensor[:, :, set_index], axis=1, ddof=1)

        # Takes a paired (related) ttest
        t_statistic, p_value = ttest_rel(base_tensor[:, :, 0],
                pot_tensor[:, :, 0], axis=1)

        # Convert Numpy arrays to Pandas dataframe for convenient writing 
        # of CSV files with row and header names included.
        stats_df = pd.DataFrame(np.column_stack([base_avg, pot_avg, base_sd,
            pot_sd, t_statistic, p_value]), index=param_names, columns=stats_names)

        stats_output_file = output_dir + "setB{}-P{}-rdd-stats.csv".format(sets_to_analyze[0], set)

        stats_df.to_csv(stats_output_file)


def practice():
    file = "/home/ej/Media/tmg-bmc-media/potentiation-2021/output/raw-rdd-params/1-BR20200910125909-rdd-params.csv"
    df = pd.read_csv(file, header=0, index_col=0)
    print(df.columns)
    print(df.columns[::2])
    print(df.columns[1::2])
    # print(df.index)
    # print(df.head())
    # print(df.values)
    # print(df.transpose().values)


def stats_wrapper():
    data_dir = "/home/ej/Media/tmg-bmc-media/potentiation-2021/output/rdd-params-by-subject/"
    max_sets = 4
    param_table_output_dir = "/home/ej/Media/tmg-bmc-media/potentiation-2021/output/rdd-param-tables-by-set/"
    param_stats_output_dir = "/home/ej/Media/tmg-bmc-media/potentiation-2021/output/rdd-param-stats-by-set/"

    analyze_tmg_params(data_dir, param_table_output_dir, param_stats_output_dir,
            max_sets=max_sets)


def stats_staggered_wrapper():
    data_dir = "/home/ej/Media/tmg-bmc-media/potentiation-2021/output/rdd-params-by-subject/"
    output_dir = "/home/ej/Media/tmg-bmc-media/potentiation-2021/output/rdd-param-stats-staggered/"
    sets_to_analyze = (1, 2, 3, 4)
    analyze_tmg_stats_staggered(data_dir, output_dir, sets_to_analyze)


if __name__ == "__main__":
    stats_wrapper()
    stats_staggered_wrapper()
    # practice()
