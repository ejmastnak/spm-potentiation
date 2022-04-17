import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import constants, frontiers_utils
import xlsx_csv_conversion

"""
This script is used to process the raw TMG-formatted Excel measurements,
which contain a variable number of measurement sets and measurements per
measurement set, into a uniform, text-based format more conducive to 
further data processing.

This script reads input from the directory `/data/excel-raw/`
and outputs processed data files into the directory `/data/csv-processed`

After the processing performed by this script, the project's dataset
has the following structure 
- 55 subjects
- 4 sets per subject
- 1 pre-exercise and 1 post-exercise measurement per set
- 1000 data points per measurement (1 second of data a 1 kHz sampling)

For a longer description of the processed dataset, see the file
`/doc/processed-data.md` in this project's documentation directory.

"""

def process_raw_excel_files():
    """
    The first step in the data processing pipeline;
    used to process raw Excel TMG measurements.

    Converts each subject's raw Excel TMG measurement file into...
    - One pre-ISQ and one post-ISQ CSV file per subject
    - Each file contains four columns; these columns hold the first pre-ISQ or post-ISQ measurement from each of the subject's first four measurement sets.
    - Column headers contain:
      - Subject ID
      - The measurement's set number
      - The measurement's number in the TMG Excel from original measurement session (see `raw-data.md`)
      Example: `ID42-S1-M2`

    """

    # Convert files with 1 pre and post measurement per measurement set
    # --------------------------------------------- #
    input_dir = constants.RAW_EXCEL_1MPS_DATA_DIR
    pre_output_dir  = constants.RAW_CSV_1MPS_DATA_DIR + "pre-exercise/"
    post_output_dir = constants.RAW_CSV_1MPS_DATA_DIR + "post-exercise/"

    # Number of pre/post exercise measurements per set
    msmnts_per_pre_set = 1   
    msmnt_per_post_set = 1

    # Maximum number of sets to take measurements from
    max_sets = 8

    for xlsx_filename in frontiers_utils.natural_sort(os.listdir(input_dir)):
        if ".xlsx" in xlsx_filename and "$" not in xlsx_filename:
            print(xlsx_filename)
            xlsx_csv_conversion.split_by_pre_post_and_set_using_first_msmt(
                    input_dir, xlsx_filename,
                    pre_output_dir, post_output_dir,
                    msmnts_per_pre_set, msmnt_per_post_set,
                    max_set=max_sets)

    # Convert files with 8 pre and post measurements per measurement set,
    # taking only first measurement from each set
    # --------------------------------------------- #
    input_dir = constants.RAW_EXCEL_8MPS_DATA_DIR
    pre_output_dir  = constants.RAW_CSV_1MPS_DATA_DIR + "pre-exercise/"
    post_output_dir = constants.RAW_CSV_1MPS_DATA_DIR + "post-exercise/"
    msmnts_per_pre_set = 8
    msmnt_per_post_set = 8

    # Maximum number of sets to take measurements from
    max_sets = 8

    for xlsx_filename in frontiers_utils.natural_sort(os.listdir(input_dir)):
        if ".xlsx" in xlsx_filename and "$" not in xlsx_filename:
            print(xlsx_filename)
            xlsx_csv_conversion.split_by_pre_post_and_set_using_first_msmt(
                    input_dir, xlsx_filename,
                    pre_output_dir, post_output_dir,
                    msmnts_per_pre_set, msmnt_per_post_set,
                    max_set=max_sets)

    # Convert files with 8 pre and post measurements per measurement set,
    # taking all measurements from each set
    # --------------------------------------------- #
    input_dir = constants.RAW_EXCEL_8MPS_DATA_DIR
    pre_output_dir  = constants.RAW_CSV_8MPS_DATA_DIR + "pre-exercise/"
    post_output_dir = constants.RAW_CSV_8MPS_DATA_DIR + "post-exercise/"

    msmnts_per_pre_set = 8
    msmnts_per_post_set = 8
    max_sets  = 8

    for xlsx_filename in frontiers_utils.natural_sort(os.listdir(input_dir)):
        if ".xlsx" in xlsx_filename and "$" not in xlsx_filename:
            print(xlsx_filename)
            xlsx_csv_conversion.split_by_pre_post_and_set(
                    input_dir, xlsx_filename,
                    pre_output_dir, post_output_dir,
                    msmnts_per_pre_set, msmnts_per_post_set,
                    max_set=max_sets)


def prepare_1mps_csv_files_for_spm():
    """
    Input: All raw CSV measurement files in RAW_CSV_1MPS_DATA_DIR

    Processing on all pre-ISQ/post-ISQ TMG measurement pairs:
        1. Trim to first 100 ms
        2. Mitigate false SPM significance from transient TMG filter artefact
        3. Normalize to the displacement maximum value in the pair 

    Output: Files in SPM_1MPS_DATA_DIR (steps 1 and 2) and
    NORMED_SPM_1MPS_DATA_DIR (steps 1, 2, and 3) with file structure mapping
    directly to that in RAW_CSV_1MPS_DATA_DIR, just with the aforementioned
    processing steps performed on them

    """
    pre_input_dir = constants.RAW_CSV_1MPS_DATA_DIR + "pre-exercise/"
    post_input_dir = constants.RAW_CSV_1MPS_DATA_DIR + "post-exercise/"
    pre_filenames = []
    post_filenames = []

    include_normalized = True

    # Build up file names (name only; without path) of CSV files to process
    for filename in frontiers_utils.natural_sort(os.listdir(pre_input_dir)):
        pre_filenames.append(filename)
    for filename in frontiers_utils.natural_sort(os.listdir(post_input_dir)):
        post_filenames.append(filename)

    pre_output_dir = constants.SPM_1MPS_DATA_DIR + "pre-exercise/"
    pre_normed_output_dir = constants.NORMED_SPM_1MPS_DATA_DIR + "pre-exercise/"
    post_output_dir = constants.SPM_1MPS_DATA_DIR + "post-exercise/"
    post_normed_output_dir = constants.NORMED_SPM_1MPS_DATA_DIR + "post-exercise/"

    _prepare_csv_files_for_spm(pre_input_dir, post_input_dir,
        pre_filenames, post_filenames,
        pre_output_dir, post_output_dir,
        pre_normed_output_dir, post_normed_output_dir,
        normalize=include_normalized)


def prepare_8mps_csv_files_for_spm():
    """
    Input: All raw CSV measurement files in RAW_CSV_8MPS_DATA_DIR
    Processing: analog of `prepare_8mps_csv_files_for_spm`
    Output: analog of `prepare_8mps_csv_files_for_spm`, just generalized 
    one directory level deeper to accomodate the extra directory level in
    `RAW_EXCEL_8MPS_DATA_DIR`.

    """
    pre_input_dir = constants.RAW_CSV_8MPS_DATA_DIR + "pre-exercise/"
    post_input_dir = constants.RAW_CSV_8MPS_DATA_DIR + "post-exercise/"
    include_normalized = True

    # Loop through each athlete directory
    for athlete_subdir in frontiers_utils.natural_sort(os.listdir(pre_input_dir)):

        pre_filenames = []
        post_filenames = []

        # Build up file names (name only; without path) of CSV files to process
        for filename in frontiers_utils.natural_sort(os.listdir(pre_input_dir + athlete_subdir)):
            pre_filenames.append(filename)
        for filename in frontiers_utils.natural_sort(os.listdir(post_input_dir + athlete_subdir)):
            post_filenames.append(filename)

        # Create output directories
        pre_output_dir = frontiers_utils.make_output_dir(constants.SPM_8MPS_DATA_DIR + "pre-exercise/" + athlete_subdir,
                use_existing=True) + "/"
        pre_normed_output_dir = frontiers_utils.make_output_dir(constants.NORMED_SPM_8MPS_DATA_DIR + "pre-exercise/" + athlete_subdir,
                use_existing=True) + "/"

        post_output_dir = frontiers_utils.make_output_dir(constants.SPM_8MPS_DATA_DIR + "post-exercise/" + athlete_subdir,
                use_existing=True) + "/"
        post_normed_output_dir = frontiers_utils.make_output_dir(constants.NORMED_SPM_8MPS_DATA_DIR + "post-exercise/" + athlete_subdir,
                use_existing=True) + "/"

        _prepare_csv_files_for_spm(pre_input_dir + athlete_subdir + "/",
                post_input_dir + athlete_subdir + "/",
                pre_filenames, post_filenames,
                pre_output_dir, post_output_dir,
                pre_normed_output_dir, post_normed_output_dir,
                normalize=include_normalized)


def _prepare_csv_files_for_spm(pre_input_dir, post_input_dir,
        pre_filenames, post_filenames,
        pre_output_dir, post_output_dir,
        pre_normed_output_dir, post_normed_output_dir,
        normalize=False):
    """
    Performs the following processing steps on all pre-ISQ/post-ISQ TMG measurement pairs in the inputted `pre_input_dir`/`post_input_dir`
        1. Trim to first 100 ms
        2. Mitigate false SPM significance from transient TMG filter artefact
        3. Normalize to the displacement maximum value in the pair 

    Writes the result of steps 1 and 2 to `*_output_dir` and the result 
    of steps 1, 2, and 3 to `*_normed_output_dir`.

    """
    max_rows_for_spm = constants.TMG_ROWS_TO_USE_FOR_SPM
    skiprows = constants.TMG_ROWS_TO_SKIP_FOR_SPM

    for i in range(len(pre_filenames)):
        pre_df = pd.read_csv(pre_input_dir + pre_filenames[i],
                sep=',', header=0, nrows=max_rows_for_spm)
        post_df = pd.read_csv(post_input_dir + post_filenames[i],
                sep=',', header=0, nrows=max_rows_for_spm)
        pre_column_headers = pre_df.columns.values.tolist()
        post_column_headers = post_df.columns.values.tolist()

        pre_df, post_df = _remove_spm_significance_from_filter_artefact(pre_df, post_df)

        # Drop first row and save files to CSV
        pre_df.iloc[skiprows:].to_csv(pre_output_dir + pre_filenames[i], index=False)
        post_df.iloc[skiprows:].to_csv(post_output_dir + post_filenames[i], index=False)

        if not normalize:
            continue

        # Normalize files and save again
        # --------------------------------------------- #
        # Convert to Numpy for easier processing
        pre_np = pre_df.to_numpy()
        post_np = post_df.to_numpy()

        pre_max = pre_np.max(axis=0)
        post_max = post_np.max(axis=0)
        # Example: If pre_max = [1 2 42] and post_max = [3, 4, 0]
        #          then  pre_post_max = [3, 4, 42]
        pre_post_max = np.maximum(pre_max, post_max)

        pre_df = pre_df/pre_post_max
        post_df = post_df/pre_post_max

        # Drop first row and save files to CSV
        pre_df.iloc[skiprows:].to_csv(pre_normed_output_dir + pre_filenames[i], header=pre_column_headers, index=False)
        post_df.iloc[skiprows:].to_csv(post_normed_output_dir + post_filenames[i], header=post_column_headers, index=False)


def _remove_spm_significance_from_filter_artefact(pre_df, post_df, 
        first_n_rows_to_average=constants.FILTER_ARTEFACT_ROWS_TO_AVERAGE):
    """
    Context: Initial IIR filtering applied to TMG signals creates a small
             filter artefact over the first few milliseconds of a TMG signal.
             This artefact can lead to non-physical regions of significance
             in the first few ms of an SPM t-test between TMG signals.
    This function removes this SPM significance very simply, namely by 
    subtracting from the post-exercise data the average of the difference 
    between pre- and post-exercise data over the first few ms of 
    the TMG curve; see implementation details in the code below.
    This is safe to do without appreciable affecting the later 
    (i.e. t > ~5 ms) portion of a TMG signal because signal values in the 
    first few ms are of the order 0.001 mm, while typical values later in
    the TMG curve are of the order 5 mm.

    Parameters
    ----------
    pre_df : DataFrame
        Pandas DataFrame containing raw pre-exericse data.
        Rows traverse time and columns traverse measurements
    post_df : DataFrame
        Pandas DataFrame containing raw pre-exericse data.
        Rows traverse time and columns traverse measurements

    Returns
    -------
    pre_df : DataFrame
        Same as pre_df; see processing description above.
    post_df : DataFrame
        Processed analog of post_df; see processing description above.
    
    """
    # Mean is taken over rows (time) and then over columns (measurements)
    # to produce a single scalar value for each 2D DataFrame.
    pre_mean = pre_df.head(first_n_rows_to_average).mean().mean()
    post_mean = post_df.head(first_n_rows_to_average).mean().mean()

    if post_mean > pre_mean:
        post_df = post_df - np.mean(post_mean - pre_mean)

    return pre_df, post_df


if __name__ == "__main__":
    process_raw_excel_files()
    prepare_1mps_csv_files_for_spm()
    prepare_8mps_csv_files_for_spm()
