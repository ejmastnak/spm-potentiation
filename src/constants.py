# Root directory with measurement data
ROOT_PROJECT_DIR = "/home/ej/Media/tmg-bmc-media/frontiers-2022/"
ROOT_DATA_DIR = ROOT_PROJECT_DIR + "data/"
ROOT_OUTPUT_DIR = ROOT_PROJECT_DIR + "output/"

# Intial step in pipeline of processing data
INITIAL_DATA_DIR = ROOT_DATA_DIR + "csv-for-initial-analysis/"
SPM_DATA_DIR = ROOT_DATA_DIR + "csv-for-spm/"
NORMED_SPM_DATA_DIR = ROOT_DATA_DIR + "csv-for-spm-normed/"

TMG_PARAMS_BY_SUBJECT_DIR = ROOT_OUTPUT_DIR + "tmg-params-by-subject/"
TMG_PARAM_STATS_BY_SET_DIR = ROOT_OUTPUT_DIR + "tmg-param-stats-by-set/"
TMG_PARAM_STATS_RELTO_SET1_DIR = ROOT_OUTPUT_DIR + "tmg-param-stats-relto-set1/"

# --------------------------------------------- #
# The number of rows to skip from the beginning of a raw TMG signal
# when performing SPM analysis.
# Motivation: the first row of a TMG signal is always zero,
# which causes zero-variance problems in SPM.
TMG_ROWS_TO_SKIP_FOR_SPM = 1

# Number of rows in a TMG signal to use for SPM analysis.
# Motivation: the full 1000 rows are not needed; most "interesting"
# information occurs in the first 100 ms or so.
TMG_ROWS_TO_USE_FOR_SPM = 150

# Used in `data_preprocessing.py` to prevent SPM from registering a false
# significance region as a result of signal artefacts from filtering TMG signals.
FILTER_ARTEFACT_ROWS_TO_AVERAGE = 3

SPM_PARAM_NAMES = ["alpha",
        "threshold",
        "p value",
        "Significance start time [ms]",
        "Significance end time [ms]",
        "Centroid time [ms]",
        "Centroid t-value",
        "Maximum",
        "Area above threshold",
        "Area above x axis"]


# Names of TMG parameters
TMG_PARAM_NAMES = ["Dm:", "Td:", "Tc:", "Ts:", "Tr:", "P1:", "P2:", "P3:",
        "RDD Max:", "RDD Min:", "RDD Peak to Peak:",
        "RDD Max Time:", "RDD Min Time:", "Max to Min Time:"]

# Names of statistical quantities used to analyze TMG parameters
TMG_STAT_NAMES = ['base-avg', 'pot-avg', 'base-sample-std', 'pot-sample-std', 't-statistic', 't-test-p-value']


# BEGIN DUMP FROM TMG PROJECT
# --------------------------------------------- #-

# The first row (assuming zero-based row indexing) containing 
# TMG signal data in a standard TMG format Excel file.
TMG_DATA_START_ROW = 24

# Time in milliseconds between successive points in a TMG signal (which is sampled at 1kHz)
TMG_DT = 1

# Maximum number of rows (datapoints) of the TMG signal to analyze.
# Also the number of milliseconds to analyze, assuming 1kHz sampling.
TMG_MAX_ROWS = 500  

# The number of points to use for interpolating polynomial when estimating 
# the times of the TMG parameters td, tc, ts and tr
TIME_INTERP_WINDOW_SIZE = 2  

# [ms] time granularity to use when interpolating td, tc, ts and tr times
TIME_INTERP_DT = 0.01  

# Occasionally TMG signal will have artificial, filter-induced local maxima in
# the first few data points that can be confusing when finding Dm. This 
# parameter is used to reject any local maxima that occur before 
REJECT_TMG_PEAK_INDEX_LESS_THAN = 8

# Number of points to use on either side of extrema when interpolating
EXTREMA_INTERP_WINDOW_SIZE = 2  

# [ms] time granularity to use when interpolating extrema (generally of rdd signal)
EXTREMA_INTERP_DT = 0.01  


# BEGIN CONVERSION MODE CONSTANTS
# --------------------------------------------- #
# Input: One TMG-formatted Excel file
# Output: One CSV file holding all measurements in the Excel file
#         in exactly the same order as they appear in the Excel file.
VERBATIM = 1

# Input: One TMG-formatted Excel file
# Output: Two CSV files:
#         One file holds all baseline measurements in the measurement session.
#         One file holds all potentiated measurements in the measurement session.
# All baseline measurements are clumped into one CSV file and all
# potentiated measurements are clumped into a separate CSV file.
SEPARATE_PRE_AND_POST = 2

# Input: One TMG-formatted Excel file
# Output: Two CSV files PER MEASUREMENT SET in Excel file:
#         One file holds baseline measurements in that set.
#         One file holds potentiated measurements in that set.
#         Creates (2 times the number of sets in Excel file) CSV files total.
# The Excel file is divided into sets, and each set is further
# divided into baseline and potentiated measurements.
PRE_POST_BY_SET_ALL_REPS = 3

# Input: One TMG-formatted Excel file
# Output: Two CSV files:
#         One file holds the FIRST baseline measurement of each set.
#         One file holds the FIRST potentiated measurement of each set.
# The Excel file is divided into sets, and each set is further
# divided into baseline and potentiated measurements, but only
# the first rep of each set is saved to the outputted CSV file.
PRE_POST_BY_SET_FIRST_REP = 4
# --------------------------------------------- #
