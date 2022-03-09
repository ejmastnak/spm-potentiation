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
    print("Hi!")


if __name__ == "__main__":
    compute_tmg_params_for_all_subjects()
    # practice()
