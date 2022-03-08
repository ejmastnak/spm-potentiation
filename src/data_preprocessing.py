import os
import constants, frontiers_utils
from xlsx_csv_conversion import xlsx_to_pre_post_csv

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

def frontiers_conversion_wrapper():
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

    Input:  `/data/excel-raw/`
    Output: `/data/csv-processed/`

    """
    input_dir  = constants.ROOT_DATA_DIR + "/excel-raw/"
    output_dir = constants.ROOT_DATA_DIR + "/csv-processed/"

    pre_output_dir  = constants.ROOT_DATA_DIR + "/csv-processed/pre-exercise/"
    post_output_dir = constants.ROOT_DATA_DIR + "/csv-processed/post-exercise/"

    # Convert files with 1 pre and post measurement per measurement set
    # --------------------------------------------- #
    input_dir = constants.ROOT_DATA_DIR + "/excel-raw/1/"
    pre_reps  = 1   # number of pre-exercise measurements per set
    post_reps = 1   # number of post-exercise measurements per set
    max_sets  = 4   # ignore sets in Excel file larger than max_sets

    # Keep only first measurement in each set
    conversion_mode = constants.PRE_POST_BY_SET_FIRST_REP
    for xlsx_filename in frontiers_utils.natural_sort(os.listdir(input_dir)):
        if ".xlsx" in xlsx_filename and "$" not in xlsx_filename:
            print(xlsx_filename)
            xlsx_to_pre_post_csv(input_dir, xlsx_filename,
                    pre_output_dir, post_output_dir,
                    conversion_mode, pre_reps=pre_reps,
                    post_reps=post_reps, max_set=max_sets)

    # Convert files with 8 pre and post measurements per measurement set,
    # --------------------------------------------- #
    input_dir = constants.ROOT_DATA_DIR + "/excel-raw/8/"
    pre_reps  = 8
    post_reps = 8
    max_sets  = 4

    # Keep only first measurement in each set
    conversion_mode = constants.PRE_POST_BY_SET_FIRST_REP
    for xlsx_filename in frontiers_utils.natural_sort(os.listdir(input_dir)):
        if ".xlsx" in xlsx_filename and "$" not in xlsx_filename:
            print(xlsx_filename)
            xlsx_to_pre_post_csv(input_dir, xlsx_filename,
                    pre_output_dir, post_output_dir,
                    conversion_mode, pre_reps=pre_reps,
                    post_reps=post_reps, max_set=max_sets)

# SPM pre-processing
"""
Processes data
Input: `/data/csv-processed/`
Output: `/data/csv-for-spm-normed/`

File structure similar to `/data/csv-processed/`, i.e.
- One pre-ISQ and one post-ISQ CSV file per subject
- Each file contains four columns; these columns hold the first pre-ISQ or post-ISQ measurement from each of the subject's first four measurement sets.
Differences:
- Meaurements

"""


if __name__ == "__main__":
    frontiers_conversion_wrapper()

