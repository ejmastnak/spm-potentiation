import os
import numpy as np
import pandas as pd
import constants, frontiers_utils
import tmg_biomechanics.tmg_params as tmg_params_pypi
import tmg_biomechanics.constants as tmg_constants

""" 
This script is used to compute TMG parameters for each subject's measurements

IMPORTANT: this script relies on processed data files created by
`data_preprocessing.py`. You should run `data_preprocessing.py` before running
this script.

"""

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
    pre_input_dir = constants.RAW_CSV_1MPS_DATA_DIR + "pre-conditioning/"
    post_input_dir = constants.RAW_CSV_1MPS_DATA_DIR + "post-conditioning/"
    pre_output_dir = constants.TMG_PARAMS_BY_SUBJ_1MPS_DIR + "pre-conditioning/"
    post_output_dir = constants.TMG_PARAMS_BY_SUBJ_1MPS_DIR + "post-conditioning/"

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
    pre_base_input_dir = constants.RAW_CSV_8MPS_DATA_DIR + "pre-conditioning/"
    post_base_input_dir = constants.RAW_CSV_8MPS_DATA_DIR + "post-conditioning/"
    pre_base_output_dir = constants.TMG_PARAMS_BY_SUBJ_8MPS_DIR + "pre-conditioning/"
    post_base_output_dir = constants.TMG_PARAMS_BY_SUBJ_8MPS_DIR + "post-conditioning/"

    # Loop through each pre-conditioning athlete directory
    for athlete_subdir in frontiers_utils.natural_sort(os.listdir(pre_base_input_dir)):
        pre_input_dir = pre_base_input_dir + athlete_subdir + "/"
        pre_output_dir = frontiers_utils.make_output_dir(pre_base_output_dir + athlete_subdir,
                use_existing=True) + "/"
        _compute_tmg_params_for_files_in_dir(pre_input_dir, pre_output_dir)

    # Loop through each post-conditioning athlete directory
    for athlete_subdir in frontiers_utils.natural_sort(os.listdir(post_base_input_dir)):
        post_input_dir = post_base_input_dir + athlete_subdir + "/"
        post_output_dir = frontiers_utils.make_output_dir(post_base_output_dir + athlete_subdir,
                use_existing=True) + "/"
        _compute_tmg_params_for_files_in_dir(post_input_dir, post_output_dir)


def _compute_tmg_params_for_files_in_dir(input_dir, output_dir, max_sets=8):
    """
    Computes TMG parameters for all TMG measurement files in `input_dir` and
    writes the parameters to files in `output_dir`, mapping each measurement
    file in `input_dir` to a corresponding parameter file in `output_dir`.
    """
    for filename in frontiers_utils.natural_sort(os.listdir(input_dir)):

        print("Current file: {}".format(filename))

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
            param_array[:, m] = tmg_params_pypi.get_params_of_tmg_signal(tmg_signal)

        param_df = pd.DataFrame(param_array,
                columns=column_headers,
                index=tmg_constants.TMG_PARAM_NAMES)
        output_filename = filename.replace(".csv", "-tmg-params.csv")
        param_df.to_csv(output_dir + output_filename)


if __name__ == "__main__":
    compute_tmg_params_for_1mps_files()
    compute_tmg_params_for_8mps_files()
